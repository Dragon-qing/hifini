import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#判断元素是否可以点击
def isclickable(xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        return True
    except :
        return False

url = "https://www.hifini.com/"
temp = "bbs_sid=71ftqg13r0sohr9fv5np2gqebp; bbs_token=ndlS5_2FcRTPDeck3X9n2n3s8Lni3nGYzQjgKsWXlGNvfb6UanY6jKY9mSD3dK7Pm9ViYlAlKYT2H7zXG774Tq9Y6_2F4eDgFg4z; cookie_test=6FfHkUz_2Bt_2B5YUPLTWr7zaI_2BryDg4S5nKf7fEGdY6KR3en225; Hm_lvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1652013429,1652265506,1652359257,1652406736; Hm_lpvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1652406736"
temp_cookies = {cookie.split("=")[0]: cookie.split("=")[-1] for cookie in temp.split("; ")};

options = Options()
options.add_argument('--headless')    # 设置无界面
options.add_argument('--no-sandbox')  # root用户下运行代码需添加这一行
driver = webdriver.Chrome(options=options)
driver.get(url)
for key, value in temp_cookies.items():
    cookies = {"value": value,
               "name": key}
    driver.add_cookie(cookies)
driver.get(url)
# 点击第一个按钮
el = driver.find_element(by=By.XPATH, value='//*[@id="header"]/div/button')
el.click()
# 等待一些时间来加载
time.sleep(2)
# 点击签到链接
el = driver.find_element(by=By.XPATH, value='//a[@id="sg_sign_mobile"]')
el.click()
time.sleep(2)

if driver.current_url == "https://www.hifini.com/sg_sign.htm":
    print("音乐磁场签到成功！！")
else:
    print("音乐磁场签到失败！！")
driver.quit()
