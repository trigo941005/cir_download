from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

def download_pdf(pdf_link, folder_name, pdf_filename):
    response = requests.get(pdf_link)
    if response.status_code == 200:
        with open(os.path.join(folder_name, pdf_filename), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {pdf_filename}")
    else:
        print(f"Failed to download: {pdf_link}")

def folder(folder_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print(f"資料夾已創建於: {folder_path}")
    return folder_path

def search():
    driver = webdriver.Chrome()
    try:
        driver.get("https://cir-reports.cir-safety.org/")
        driver.maximize_window()

        # 等待頁面完全加載
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # 查找所有 href="#" 的 <a> 標籤
        elements = driver.find_elements(By.XPATH, "//a[@href='#']")
        print(f"Found {len(elements)} elements with href='#'.")

        for index, element in enumerate(elements):
            try:
                print(element.text)

                # 確保元素可點擊
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
                element.click()

                time.sleep(3)

                # 找出 target="_blank" 的 <a> 標籤
                links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//a[@target="_blank"]'))
                )
                
                for i in range(len(links)):
                    try:
                        link = links[i]
                        print(link.text)

                        # 確保連結可點擊
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link))
                        folder_name = link.text
                        link.click()

                        # 等待新標籤頁打開並切換
                        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                        windows = driver.window_handles
                        driver.switch_to.window(windows[-1])
                        print(f"Switched to new tab with title: {driver.title}")

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'body'))
                        )

                        # 查找 PDF 下載連結
                        link_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'view-attachment')]")
                        folder_path = folder(folder_name)

                        for pdf_element in link_elements:
                            pdf_link = pdf_element.get_attribute('href')
                            download_pdf(pdf_link, folder_path, pdf_element.text)

                        driver.close()
                        driver.switch_to.window(windows[0])
                        if i > 4:
                            break
                    except StaleElementReferenceException:
                        print("StaleElementReferenceException: 重新查找元素")
                        links = driver.find_elements(By.XPATH, '//a[@target="_blank"]')
                        continue
                    
            except (NoSuchElementException, TimeoutException) as e:
                print(f"處理元素 {index + 1} 時發生錯誤: {e}")
                continue

            time.sleep(2)

    except Exception as e:
        print(f"在加載網頁時發生錯誤: {e}")

    finally:
        driver.quit()

# 呼叫 search() 函數
search()
