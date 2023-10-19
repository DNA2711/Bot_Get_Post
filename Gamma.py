import time
from selenium import webdriver
from newspaper import Article
from bs4 import BeautifulSoup
import json
import urllib.parse
from datetime import datetime
from selenium.webdriver.common.by import By


def search_google_and_extract(keyword):
    try:
        # Khởi tạo trình duyệt mà không sử dụng proxy
        driver = webdriver.Chrome()

        # Tạo URL tìm kiếm tùy chỉnh với biểu thức tìm kiếm
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}"

        # Truy cập trang tìm kiếm Google
        driver.get(search_url)

        # Chờ cho trang kết quả tải hoàn tất
        time.sleep(5)

        # Lấy danh sách các liên kết đến bài viết trên hai trang đầu tiên
        search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
        search_results = search_results[:2]  # Lấy liên kết đầu tiên và thứ hai

        result_array = []

        # Lấy URL của liên kết đầu tiên và thứ hai
        first_link_url = (
            search_results[0].find_element(By.XPATH, "..").get_attribute("href")
        )
        second_link_url = (
            search_results[1].find_element(By.XPATH, "..").get_attribute("href")
        )

        # Mở liên kết đầu tiên trong tab mới
        driver.execute_script(f"window.open('{first_link_url}', '_blank');")

        # Chuyển sang tab mới
        driver.switch_to.window(driver.window_handles[1])

        # Sử dụng Newspaper để trích xuất nội dung bài viết đầu tiên
        article = Article(first_link_url)
        article.download()
        article.parse()

        # Lấy tiêu đề và nội dung bài viết
        title = article.title
        content = article.text.strip()

        content = content.replace("\n", " ")

        # Thêm thông tin bài viết vào danh sách
        result_array.append({"Title": title, "Content": content})

        # Mở liên kết thứ hai trong tab mới
        driver.execute_script(f"window.open('{second_link_url}', '_blank');")

        # Chuyển sang tab mới
        driver.switch_to.window(driver.window_handles[2])

        # Sử dụng Newspaper để trích xuất nội dung bài viết thứ hai
        article = Article(second_link_url)
        article.download()
        article.parse()

        # Lấy tiêu đề và nội dung bài viết
        title = article.title
        content = article.text.strip()
        authors = article.authors
        content = content.replace("\n", " ")
        publish_date = article.publish_date
        url = article.url

        # Thêm thông tin bài viết vào danh sách
        result_array.append(
            {
                "Title": title,
                "Content": content,
                "authors": authors,
                "publish_date": publish_date,
                "url": url,
            }
        )

        # Lấy alt của tất cả các hình ảnh và liên kết trên trang
        soup = BeautifulSoup(driver.page_source, "html.parser")
        images = soup.find_all("img")
        links = soup.find_all("a")

        alt_text = list({img.get("alt") for img in images})
        link_urls = list({link.get("href") for link in links if link.get("href")})

        # Thêm alt text và link URLs vào kết quả
        result_array.append({"Alt Text": alt_text, "Links": link_urls})

        driver.close()

        return result_array

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    finally:
        driver.quit()


def main():
    try:
        input_keywords = ["Chiến tranh nga và ukraine"]

        result_array = []  # Tạo danh sách tổng hợp kết quả từ tất cả các từ khoá

        # Thực hiện tìm kiếm và trích xuất nội dung cho từng từ khoá
        for keyword in input_keywords:
            result_array.extend(
                search_google_and_extract(keyword)
            )  # Sử dụng extend để thêm kết quả vào danh sách tổng hợp

        # Sử dụng cls=MyEncoder để serialize datetime thành chuỗi
        result_json = json.dumps(
            result_array, indent=4, ensure_ascii=False, cls=MyEncoder
        )
        print(result_json)

    except Exception as e:
        print(f"Error: {str(e)}")


# Lớp tùy chỉnh để serialize datetime thành chuỗi
class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return super(MyEncoder, self).default(o)


if __name__ == "__main__":
    main()
