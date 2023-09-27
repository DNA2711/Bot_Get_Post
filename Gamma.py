import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

        # Tìm thẻ h3 đầu tiên và click vào nó
        first_h3 = driver.find_element(By.CSS_SELECTOR, "h3")
        first_h3.click()

        # Chờ cho trang bài viết tải hoàn tất
        time.sleep(5)

        # Sử dụng Newspaper để trích xuất nội dung bài viết
        article = Article(driver.current_url)
        article.download()
        article.parse()

        # Lấy tiêu đề và nội dung bài viết
        title = article.title
        content = article.text.strip()

        # Loại bỏ ký tự '\n' và thay thế thành thẻ '<br>'
        content = content.replace('\n', ' ')

        # Thêm thông tin bài viết vào danh sách
        result_array = [{"Title": title, "Content": content}]

        driver.quit()  # Đóng trình duyệt

        return result_array

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def main():
    try:
        input_keywords = ['planets in the solar system wiki']
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
