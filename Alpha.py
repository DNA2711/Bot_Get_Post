import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from newspaper import Article
import json
import urllib.parse

def search_google_and_extract(keyword):
    try:
        # Khởi tạo trình duyệt (Chrome)
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
        first_link_url = search_results[0].find_element(By.XPATH, "..").get_attribute("href")
        second_link_url = search_results[1].find_element(By.XPATH, "..").get_attribute("href")

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
        input_keywords = ['10 ngày Thủ tướng công du Mỹ, Brazil', 'Ukraine khát tiền']

        # Thực hiện tìm kiếm và trích xuất nội dung cho từng từ khoá trong mảng
        for keyword in input_keywords:
            result_array = search_google_and_extract(keyword)
            result_json = json.dumps(result_array, indent=4, ensure_ascii=False)
            print(result_json)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
