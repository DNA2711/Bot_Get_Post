import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from newspaper import Article
import json
import urllib.parse

def search_google_and_extract(keyword, proxy):
    try:
        # Cấu hình proxy
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=http://' + proxy)

        # Khởi tạo trình duyệt với proxy
        driver = webdriver.Chrome(options=chrome_options)

        # Tạo URL tìm kiếm tùy chỉnh với biểu thức tìm kiếm
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}"

        # Truy cập trang tìm kiếm Google
        driver.get(search_url)

        # Chờ cho trang kết quả tải hoàn tất
        time.sleep(5)

        # Lấy danh sách các liên kết đến bài viết trên hai trang đầu tiên
        search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
        # search_results = search_results[:2]  # Lấy liên kết đầu tiên và thứ hai

        result_array = []

        # Lấy URL của liên kết đầu tiên và thứ hai
        first_link_url = search_results[0].find_element(By.XPATH, "..").get_attribute("href")
        second_link_url = search_results[1].find_element(By.XPATH, "..").get_attribute("href")

        # Mở liên kết đầu tiên trong tab mới
        # driver.execute_script(f"window.open('{first_link_url}', '_blank');")

        # Chuyển sang tab mới
        driver.switch_to.window(driver.window_handles[1])

        # Sử dụng Newspaper để trích xuất nội dung bài viết đầu tiên
        article = Article(first_link_url)
        article.download()
        article.parse()

        # Lấy tiêu đề và nội dung bài viết
        title = article.title
        content = article.text.strip()

        # Loại bỏ ký tự '\n' và thay thế thành thẻ '<br>'
        content = content.replace('\n', ' ')

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

        content = content.replace('\n', ' ')

        # Thêm thông tin bài viết vào danh sách
        result_array.append({"Title": title, "Content": content})

        driver.close()  # Đóng tab hiện tại

        return result_array

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    finally:
        # Đóng trình duyệt sau khi hoàn thành
        driver.quit()

def main():
    try:
        input_keywords = ['planets in the solar system']
        proxy = '38.153.192.39:8800'

        result_array = []  # Tạo danh sách tổng hợp kết quả từ tất cả các từ khoá

        # Thực hiện tìm kiếm và trích xuất nội dung cho từng từ khoá với proxy duy nhất
        for keyword in input_keywords:
            result_array.extend(search_google_and_extract(keyword, proxy))  # Sử dụng extend để thêm kết quả vào danh sách tổng hợp

        result_json = json.dumps(result_array, indent=4, ensure_ascii=False)
        print(result_json)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
