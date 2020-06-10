# -*- coding: utf-8 -*-
# @Time    : 2020/6/8 9:46
# @Author  : wanpeng
from multiprocessing.pool import Pool
from random import random

from psutil import Process
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import time
import requests


# 定义淘宝时间
def time_server():
    # 获取淘宝服务器的时间戳
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}
                      ).json()['data']['t']
    # 把时间戳格式/1000 获取毫秒
    timeNum = int(r1) / 1000
    # 格式化时间 (小数点后6为)
    time1 = datetime.datetime.fromtimestamp(timeNum)
    return time1


# 获取chrome实例
def getChrome() -> webdriver:
    options = webdriver.ChromeOptions()
    # options.add_argument('--log-level=3')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option("prefs", prefs)
    driver_path = "D:/driver/chromedriver83.exe"
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    return driver


def buy(driver: webdriver):
    url = 'https://market.m.taobao.com/app/sj/shop-membership-center/pages/index?spm=a1z10.4-b-s.w5003-22059585455.1.7f86274aL8QKmA' \
          '&wh_weex=true&wx_navbar_transparent=true&sellerId=2360209412&scene=taobao_shop'

    btn_buy = "//span[contains(text(),'1积分享兰蔻菁纯宝石唇膏 02')]/../following-sibling::div[1]//div[@class='gift-act-btn']"
    btn_word = "//span[contains(text(),'1积分享兰蔻菁纯宝石唇膏 02')]/../following-sibling::div[1]//span[@class='gift-act-btn-text']"
    btn = "//div[@class='btnWarp']"
    word = "//span[@class='btn']"
    count = 0
    login_time = "2020-06-10 13:23:00"
    buy_time = "2020-06-10 13:23:55"
    isFirst = True
    wait = WebDriverWait(driver, 10, 0.5)
    while True:
        if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') < buy_time:
            # 提前登录
            if isFirst and datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') >= login_time:
                driver.maximize_window()
                driver.get(url)
                driver.implicitly_wait(2)
                login(driver)
                isFirst = False
            continue
        else:
            # 如果连续抢60次都抢不到 那么就放弃吧
            count += 1
            if count > 60:
                break
            print("即将开始抢购...")
            print(datetime.datetime.now())
            # 重新进页面
            driver.refresh()

            # 开始页面的唇膏抢购按钮
            buy_btn = wait.until(lambda driver: driver.find_element_by_xpath(btn_buy))
            # 开始页面的唇膏抢购按钮上的文字
            word_btn = wait.until(lambda driver: driver.find_element_by_xpath(btn_word))
            if word_btn.text == '立即兑换':
                # 如果抢购按钮上的文字为立即兑换 则点击按钮跳转详情页
                buy_btn.click()
                # 详情页中的购买按钮
                targetBtn = wait.until(lambda driver: driver.find_element_by_xpath(btn))
                # 详情页中的购买按钮上的文字
                targetBtnWord = wait.until(lambda driver: driver.find_element_by_xpath(word))
                if targetBtnWord.text != "已抢光":
                    # 如果详情页中购买按钮上的文字不为已枪光 则点击购买
                    targetBtn.click()
                    time.sleep(5)
                    # 抢到了就退出...
                    break
    print("抢购结束...")


def login(driver):
    username = driver.find_element_by_id("fm-login-id")
    password = driver.find_element_by_id("fm-login-password")
    login_btn = driver.find_element_by_xpath("//div[@class='fm-btn']/button")
    action = ActionChains(driver)
    action.send_keys_to_element(username, "18717792412")
    action.send_keys_to_element(password, "Wphmy520")
    action.click(login_btn)
    action.perform()
    action = ActionChains(driver)
    dragger = driver.find_element_by_id("nc_1_n1z")
    if dragger:
        action.move_to_element(dragger)
        action.click_and_hold(dragger).perform()  # 鼠标左键按下不放
        action.move_by_offset(258, 0).perform()
        # time.sleep(1)
        login_btn.click()


# 真正的抢购方法
def run():
    driver = getChrome()
    buy(driver)


# 开启多进程 打开多个浏览器页面去抢 抢到的几率更大
def concurrency_run(num: int):
    pool = Pool(num)
    for k in range(num):
        pool.apply_async(func=run)
    pool.close()
    pool.join()


if __name__ == '__main__':
    # 1 代表开启一个浏览器实例  如果想多开 那么就改成大于1的整数
    # 你只需要改buy中的代码即可 其他代码不要动
    concurrency_run(1)
