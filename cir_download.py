from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from urllib.parse import urlparse, parse_qs

def search_and_download():
    driver = webdriver.Chrome()

    try:
        # 開啟目標網站
        driver.get("https://cir-reports.cir-safety.org/")  # 替換成正確的網站
        driver.maximize_window()

        # 使用 WebDriverWait 等待頁面加載完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # 使用 XPath 查找包含 'view-attachment' 的 <a> 標籤
        link_element = driver.find_element(By.XPATH, "//a[contains(@href, 'view-attachment')]")

        # 獲取該連結的 href 屬性
        href_value = link_element.get_attribute('href')
        print(f"Found href: {href_value}")

        # 提取文件名
        # 假設文件名在 URL 的最後一部分（這是根據實際情況調整的）
        parsed_url = urlparse(href_value)
        query_params = parse_qs(parsed_url.query)
        file_id = query_params.get('id', [None])[0]
        file_name = f"File_{file_id}.pdf" if file_id else "downloaded_file.pdf"

        print(f"File name: {file_name}")

        # 下載該文件
        if href_value:
            # 確保目錄存在
            download_dir = os.path.join(os.getcwd(), 'downloads')
            os.makedirs(download_dir, exist_ok=True)

            # 下載文件的路徑
            file_path = os.path.join(download_dir, file_name)

            # 通過 requests 庫下載文件
            response = requests.get(href_value, stream=True)
            
            # 如果請求成功，將文件寫入本地
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"文件已成功下載，保存在 {file_path}")
            else:
                print(f"下載失敗，狀態碼: {response.status_code}")

    except Exception as e:
        print(f"在處理時發生錯誤: {e}")

    finally:
        # 關閉瀏覽器
        driver.quit()

# 呼叫函數
search_and_download()
