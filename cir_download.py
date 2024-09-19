from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
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
                        href_value = link.get_attribute('href')
                        print(href_value)
                        link.click()
                        time.sleep(5)
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