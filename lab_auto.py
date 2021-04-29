from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
import calendar
import math

#--------------------------------------------------------------------------------------------------------------------

USER_TYPE='student' # 'student' or 'others'
USER='USER ID'
PASSWORD='PASSWORD'
chrome_dir=r'C:\Users\DELL\Desktop\chromedriver.exe'

#--------------------------------------------------------------------------------------------------------------------

def check_all():
    
    for i in [1, 6, 11]:
        d.find_element_by_xpath('//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr['+str(i)+']/th[2]/input').click()
        time.sleep(1)
    
    d.find_element_by_xpath('//*[@id="frmOn"]/div[2]/a[1]').click()
    time.sleep(1)
    
def find_path(i, j):
    
    if j in [1, 7]:
        try:
            d.find_element_by_xpath('//*[@id="dtpicker"]/div/table/tbody/tr['+str(i)+']/td['+str(j)+']/a').click()
            time.sleep(1)
        except:
            pass
    
        try:
            d.find_element_by_xpath('//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[1]').click()
            time.sleep(1)
        except:
            pass
            
    else:
        try:
            d.find_element_by_xpath('//*[@id="dtpicker"]/div/table/tbody/tr['+str(i)+']/td['+str(j)+']/a').click()
            time.sleep(1)
        except:
            pass

        try:
            d.find_element_by_xpath('//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[2]').click()
            time.sleep(1)
        except:
            pass

        try:
            check_all()
        except:
            pass

    try:
        d.find_element_by_xpath('//*[@id="divList"]/div[2]/div/a[3]').click()
        time.sleep(1)
    except:
        pass

#--------------------------------------------------------------------------------------------------------------------

day=date.today()
cur_month=day.strftime("%m")
year=day.strftime("%y")
cur_month=int(cur_month)
year=int(year)

d=webdriver.Chrome(chrome_dir)
url='https://safe.knu.ac.kr/Account/LogOn'
d.get(url)
if USER_TYPE=='student':
    id_var=d.find_element_by_xpath('//*[@id="stdUniqueKey"]')
    id_var.send_keys(USER)
    id_var=d.find_element_by_xpath('//*[@id="stdPassword"]')
    id_var.send_keys(PASSWORD)
    d.find_element_by_xpath('//*[@id="btnStudent"]').click()
    d.find_element_by_xpath('//*[@id="contents"]/div/div[2]/a').click()

else:
    id_var=d.find_element_by_id("userUniqueKey")
    id_var.send_keys(USER)
    id_var=d.find_element_by_id('userPassword')
    id_var.send_keys(PASSWORD)
    d.find_element_by_id('btnUser').click()
    d.find_element_by_id('TopMenu_3').click()

action=ActionChains(d)
time.sleep(10)
source=d.find_element_by_xpath('/html/body/div[6]/div[1]/button/span[1]')
action.move_to_element(source).click().perform()



lab_list = []
for i in range(1, 10, 1):
    try:
        lab_list.append(d.find_element_by_xpath('//*[@id="cboLabList"]/option[' + str(i) + ']').get_attribute("value"))
    except:
        break

for i in lab_list:
    url = 'https://safe.knu.ac.kr/Home?LabNo=' + i 
    d.get(url)
    action=ActionChains(d)
    time.sleep(3)
    source=d.find_element_by_xpath('/html/body/div[6]/div[1]/button/span[1]')
    action.move_to_element(source).click().perform()
    d.find_element_by_xpath('//*[@id="main_bg_area_wrap"]/div[1]/div[1]/div[2]/ul/li[1]/a').click() #dailycheck click

    cur_url=d.current_url
    d.get(cur_url)

    for _ in range(cur_month-1):
        WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dtpicker"]/div/div/a[1]/span'))).click()
        source=d.find_element_by_xpath('//*[@id="dtpicker"]/div/div/a[1]/span')



    # row and column setting which is dependant on month and year
    month=1
    while month<cur_month+1:
        start_day, month_days=calendar.monthrange(year, month)
        start_row=1
        start_col=start_day+2 # it starts from sunday.
        end_row=math.ceil((start_col+month_days-1)/7)
        end_col=(start_col+month_days-1)%7
        
        # for each month, we will check all

        for i in range(start_row, end_row+1):
            if i==start_row:        
                for j in range(start_col, 7+1):
                    find_path(i, j)
            elif i==end_row:
                for j in range(1, end_col+1):
                    find_path(i, j)
                    time.sleep(1)
            else:
                for j in range(1, 8):
                    find_path(i, j)
                    

        month+=1
        try:
            d.find_element_by_xpath('//*[@id="dtpicker"]/div/div/a[2]/span').click()
            time.sleep(1)
        except:
            pass



