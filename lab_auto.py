from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from selenium.webdriver.chrome.options import Options
import time
import calendar
import math
import sys
import hashlib
import stdiomask  # 설치해야됨.
import tkinter
import os
from tkinter import filedialog

# --------------------------------------------------------------------------------------------------------------------


def check_all():

    for i in [1, 6, 11]:
        WebDriverWait(d, 1).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr['+str(i)+']/th[2]/input'))).click()
        time.sleep(0.5)

    WebDriverWait(d, 1).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="frmOn"]/div[2]/a[1]'))).click()


def find_path(i, USER_TYPE):

    try:
        d.find_element_by_xpath(
            '//*[@id="dtpicker"]/div/table/tbody/tr[' + str(1+i//7) + ']/td[' + str(1+(i % 7)) + ']/a').click()
        time.sleep(0.5)
    except:
        pass

    if 1+(i % 7) in [1, 7]:
        try:
            d.find_element_by_xpath(
                '//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[1]').click()
            time.sleep(0.5)
            
        except:
            pass
        
        if USER_TYPE == '1':
            try:
                WebDriverWait(d, 0.5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="divList"]/div[2]/div/a[2]'))).click()
                time.sleep(0.5)
            except:
                pass

    else:
        try:
            d.find_element_by_xpath(
                '//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[2]').click()
            time.sleep(0.5)
        except:
            pass

        try:
            check_all()
            time.sleep(0.5)
        except:
            pass

        if USER_TYPE == '1':
            try:
                WebDriverWait(d, 0.5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="divList"]/div[2]/div/a[3]'))).click()
                time.sleep(0.5)
            except:
                pass


# --------------------------------------------------------------------------------------------------------------------

USER_TYPE = input(
    ' 다음 중 하나를 선택해 주십시오.\n 1. 학내구성원 + 연구실책임자\n 2. 학내구성원 \n 3. 그외 연구활동종사자 (사용자 등록정보를 이용한 로그인) \n\n ')
USER = input('\n USER ID       : ')
PASSWORD = stdiomask.getpass(prompt=' USER PASSWORD : ', mask='*')

dur_month = int(input('\n 몇달간 작업하시겠습니까? 숫자로 입력 (1 이상의 자연수)\n\n '))

print('\n\n chromedriver.exe 파일을 선택해주십시오. \n\n')
root = tkinter.Tk()
root.withdraw()


if getattr(sys, 'frozen', False):
    APPLICATION_EXE_DIR = os.path.dirname(sys.executable)
else:
    APPLICATION_EXE_DIR = os.path.dirname(os.path.abspath(__file__))


chrome_dir = tkinter.filedialog.askopenfilename(
    initialdir=APPLICATION_EXE_DIR + '//chromedriver', title="Select chromedriver.exe file")


print('\n------------------ 작업을 시작합니다. --------------------\n')
day = date.today()
cur_month = day.strftime("%m")
cur_year = day.strftime("%Y")
cur_month = int(cur_month)
cur_year = int(cur_year)

options = Options()
# options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
d = webdriver.Chrome(chrome_dir, options=options)

url = 'https://safe.knu.ac.kr/Account/LogOn'
d.get(url)
if USER_TYPE == '1' or USER_TYPE == '2':
    WebDriverWait(d, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="btnStudent"]')))
    id_var = d.find_element_by_xpath('//*[@id="stdUniqueKey"]')
    id_var.send_keys(USER)
    id_var = d.find_element_by_xpath('//*[@id="stdPassword"]')
    id_var.send_keys(PASSWORD)
    d.find_element_by_xpath('//*[@id="btnStudent"]').click()
    WebDriverWait(d, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="contents"]/div/div[2]/a'))).click()

elif USER_TYPE == '3':
    WebDriverWait(d, 20).until(EC.element_to_be_clickable(
        (By.XPATH, 'btnUser')))
    id_var = d.find_element_by_id("userUniqueKey")
    id_var.send_keys(USER)
    id_var = d.find_element_by_id('userPassword')
    id_var.send_keys(PASSWORD)
    d.find_element_by_id('btnUser').click()

    WebDriverWait(d, 20).until(EC.element_to_be_clickable(
        (By.XPATH, 'TopMenu_3'))).click()

else:
    print('숫자만 입력해주십시오.')
    exit()

action = ActionChains(d)
WebDriverWait(d, 20).until(EC.element_to_be_clickable(
    (By.XPATH, '/html/body/div[6]/div[1]/button/span[1]'))).click()


lab_list = []
lab_list_name = []
for i in range(1, 10, 1):
    try:
        lab_list.append(d.find_element_by_xpath(
            '//*[@id="cboLabList"]/option[' + str(i) + ']').get_attribute("value"))
        lab_list_name.append(d.find_element_by_xpath(
            '//*[@id="cboLabList"]/option[' + str(i) + ']').get_attribute("innerHTML"))
    except:
        break

for k in range(len(lab_list)):
    url = 'https://safe.knu.ac.kr/Home?LabNo=' + lab_list[k]
    d.get(url)
    action = ActionChains(d)
    time.sleep(3)
    source = d.find_element_by_xpath('/html/body/div[6]/div[1]/button/span[1]')
    action.move_to_element(source).click().perform()
    d.find_element_by_xpath(
        '//*[@id="main_bg_area_wrap"]/div[1]/div[1]/div[2]/ul/li[1]/a').click()  # dailycheck click
    cur_url = d.current_url
    d.get(cur_url)

    for _ in range(dur_month-1):
        WebDriverWait(d, 4).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="dtpicker"]/div/div/a[1]/span'))).click()
        time.sleep(1)
        WebDriverWait(d, 4).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="dtpicker"]/div/div/a[1]/span')))
    # row and column setting which is dependant on month and year
    final_flag = 0
    while True:
        time.sleep(1)

        WebDriverWait(d, 4).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="dtpicker"]/div/div/div/span[2]')))
        year_str = d.find_element_by_xpath(
            '//*[@id="dtpicker"]/div/div/div/span[1]').get_attribute('innerHTML')
        month_str = d.find_element_by_xpath(
            '//*[@id="dtpicker"]/div/div/div/span[2]').get_attribute('innerHTML')[:-1]
        
        year = int(year_str)
        month = int(month_str)

        start_day, month_days = calendar.monthrange(year, month)   
        
        # for each month, we will check all
        if year == cur_year and month == cur_month:
            final_flag = 1

        if final_flag == 1:
            for i in range((start_day+1)%7, (start_day+1)%7 + int(day.strftime("%d"))):    
                find_path(i, USER_TYPE)
                print(year_str + ' 년 ' + month_str + ' 월 ' + str(i + 1 - (start_day+1)%7) +     ' 일 ... ' + lab_list_name[k])
            break
        else:
            for i in range((start_day+1)%7, (start_day+1)%7 + month_days):    
                find_path(i, USER_TYPE)
                print(year_str + ' 년 ' + month_str + ' 월 ' + str(i + 1 - (start_day+1)%7) +     ' 일 ... ' + lab_list_name[k])

          # 여기부터 작업

        try:
            d.find_element_by_xpath(
                '//*[@id="dtpicker"]/div/div/a[2]/span').click()
            time.sleep(0.5)
        except:
            pass

print('\n------------------ 작업을 완료합니다. --------------------\n')
time.sleep(3)
d.close()
sys.exit()