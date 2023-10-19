import time
from selenium import webdriver
from newspaper import Article
import json
import urllib.parse
from datetime import datetime
from selenium.webdriver.common.by import By


def search_google_and_extract(keyword):
    try:
        driver = webdriver.Chrome()

        # Tạo URL tìm kiếm tùy chỉnh với biểu thức tìm kiếm
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}"

        # Truy cập trang tìm kiếm Google
        driver.get(search_url)

        # Chờ cho trang kết quả tải hoàn tất
        time.sleep(5)

        # Lấy danh sách các liên kết đến bài viết trên trang đầu tiên
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf div span a")
        search_results = search_results[:2]  # Lấy liên kết đầu tiên và thứ hai

        result_array = []

        for result in search_results:
            link_url = result.get_attribute("href")
            # Tạo một tab mới cho mỗi liên kết và chuyển sang tab mới
            driver.execute_script("window.open();")
            driver.switch_to.window(driver.window_handles[-1])
            # Truy cập liên kết trong tab mới
            driver.get(link_url)

            # Kiểm tra nếu tab đã bị đóng, thì không thực hiện thêm thao tác
            if driver.current_window_handle not in driver.window_handles:
                continue

            # Sử dụng Newspaper để trích xuất nội dung bài viết
            article = Article(link_url)
            article.download()
            article.parse()

            # Lấy tiêu đề và nội dung bài viết
            title = article.title
            content = article.text.strip()

            content = content.replace("\n", " ")

            # Thêm thông tin bài viết vào danh sách
            result_array.append({"Title": title, "Content": content})

            # Đóng tab hiện tại
            driver.close()
            # Chuyển về tab trước đó (trong trường hợp còn tab khác)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])

        driver.quit()

        return result_array

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    finally:
        driver.quit()


def main():
    try:
        input_keywords = ["planet in our solar system"]

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
