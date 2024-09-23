from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

def download_pdf(pdf_link, folder_name,pdf_filename):
    # 下載 PDF 檔案
    #pdf_filename = pdf_link.split("/")[-1]
    response = requests.get(pdf_link)
    if response.status_code == 200:
        with open(os.path.join(folder_name, pdf_filename), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {pdf_filename}")
    else:
        print(f"Failed to download: {pdf_link}")
def folder(folder_name):
    # 獲取當前執行程式的路徑
    current_directory = os.getcwd()

    # 組合路徑 (當前路徑 + 資料夾名稱)
    folder_path = os.path.join(current_directory, folder_name)

    # 如果資料夾不存在，則創建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 打印資料夾的路徑 (檢查資料夾是否創建成功)
    print(f"資料夾已創建於: {folder_path}")
    return folder_path

def search():
    driver = webdriver.Chrome()
    try:
        # 開啟目標網站
        driver.get("https://cir-reports.cir-safety.org/")  # 替換成你的目標網站
        driver.maximize_window()

        # 使用 WebDriverWait 等待網頁加載完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))  # 等待頁面主體加載
        )

        # 查找所有 href="#" 的 <a> 標籤
        elements = driver.find_elements(By.XPATH, "//a[@href='#']")
        print(f"Found {len(elements)} elements with href='#'.")

        # 點擊每個 href="#" 的 <a> 標籤，並處理 target="_blank" 的連結
        for index, element in enumerate(elements):
            try:
                # 點擊當前元素
                element.click()
                # 等待頁面主體重新加載
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))  # 等待頁面主體加載
                )

                # 找出所有帶有 target="_blank" 的 <a> 標籤
                links = driver.find_elements(By.XPATH, '//a[@target="_blank"]')

                # 提取這些連結的 href 值
                for link in links:
                    try:
                        # 點擊該連結並等待新標籤頁打開
                        print(link.text)
                        folder_name = link.text
                        link.click()
                        # 動態等待新標籤頁打開後進行切換
                        WebDriverWait(driver, 10).until(
                            EC.number_of_windows_to_be(2)  # 等待新標籤頁打開（總標籤頁數應為2）
                        )
                        
                        # 切換到新打開的標籤頁
                        windows = driver.window_handles  # 獲取所有標籤頁
                        driver.switch_to.window(windows[-1])  # 切換到最新的標籤頁
                        print(f"Switched to new tab with title: {driver.title}")

                        # 等待新標籤頁完全加載
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'body'))  # 確保新標籤頁主體加載
                        )

                        # 查找所有 href 包含 'view-attachment' 的 <a> 標籤
                        link_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'view-attachment')]")
                        folder_path = folder(folder_name)
                        #download
                        for pdf_element in link_elements:
                            pdf_link = pdf_element.get_attribute('href')  # 提取 href 屬性（連結的 URL 字串）
                            print(pdf_element.text)
                            download_pdf(pdf_link, folder_path,pdf_element.text)  # 傳遞 URL 字串給 download_pdf 函數

                        # 操作新標籤頁後關閉它，並返回原始標籤頁
                        driver.close()
                        driver.switch_to.window(windows[0])  # 切回到原標籤頁
                        
                    except StaleElementReferenceException:
                        print("StaleElementReferenceException: 重新查找超連結元素")
                        continue  # 如果元素已經無效，則跳過繼續下個元素

            except (NoSuchElementException, TimeoutException) as e:
                print(f"處理元素 {index + 1} 時發生錯誤: {e}")
                continue  # 繼續處理下一個元素

            # 等待幾秒以便查看結果
            time.sleep(2)

    except Exception as e:
        print(f"在加載網頁時發生錯誤: {e}")

    finally:
        # 關閉瀏覽器
        driver.quit()

# 呼叫 search() 函數
search()