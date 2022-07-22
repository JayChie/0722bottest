from selenium import webdriver
from linebot.models import *
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from flex_msg import *
from config import *
import time
import json
import random
import string
import os


def youtube_vedio_parser(keyword):
    #建立url跟目錄
    url = "https://www.dcard.tw/service/api/v2/posts?popular=true&limit=10"
    #建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    #設定瀏覽器的user agent
    #chromeOption.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    chromeOption.add_argument("start-maximized")
    #chromeOption.add_argument('--headless')
    chromeOption.add_argument('--no-sandbox')
    chromeOption.add_argument('--disable-dev-shm-usage')
    #開啟Chrome瀏覽器
    driver = webdriver.Chrome(options=chromeOption)
    #調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)

    #======================依關鍵字在Dcard網站上搜尋API===========================
    #進入指定網址
    driver.get(url)
    time.sleep(3)

    #滾動視窗捲軸，使瀏覽器獲取影片縮圖資訊
    '''
    for i in range(15):
        y_position = i*100
        driver.execute_script(f'window.scrollTo(0, {y_position});')
        time.sleep(0.1)
    #回到最頂端
    js = 'var q=document.documentElement.scrollTop=0'
    driver.execute_script(js)
    '''
    # ======================擷取網站API資訊===========================

    # 整個網頁資訊
    html_doc = driver.page_source

    # 解析網頁資訊
    page = bs(html_doc, 'html.parser')

    # print(page.prettify())

    # print(page.pre.string)

    # 取得json格式
    jsoon = page.pre.string

    # 讀取json
    reqsjson = json.loads(jsoon.text)

    # 列印篇數
    total_num = len(reqsjson)
    print(total_num)
    print('-' * 30)

    # ======================從網頁獲取文章連結===========================
    # 文章URL前墜
    Post_Urlfront = "https://www.dcard.tw/f/talk/p/"
    # 狄卡logo
    D_logo = "https://imgur.com/L5JSIaF"
    # 建立文章url列表
    vedio_url_list = []
    # 建立縮圖列表
    yt_vedio_images = []
    # 建立標題與副標列表
    yt_title_list = []
    yt_channel_infos_names = []
    # 小縮圖(圖片)
    yt_channel_infos_image_urls = []

    # 將每個文章連結放入連結list
    # print(len(yt_vedio_urls))

    #----------------------
    for i in range(0, total_num):
        # 判斷這文章圖的數量
        media_num = len(reqsjson[i]["media"])
        # 取得文章連結

        idd = reqsjson[i]["id"]
        okid = str(idd)
        vedio_url_list.append(Post_Urlfront+okid)

        # 取得文章標題

        title = reqsjson[i]["title"]
        yt_title_list.append(title)

        # 取得文章副標題

        post2_num = len(reqsjson[i]["excerpt"])
        if post2_num != 0:
            excerpt = reqsjson[i]["excerpt"]
            yt_channel_infos_names.append(excerpt)
        else:
            text = '...'
            yt_channel_infos_names.append(text)

        # 取得文章圖片連結


        if media_num != 0:
            image_url = reqsjson[i]['media'][0]['url']
            yt_vedio_images.append(image_url)

        else:
            print("狀態:沒有圖QQ")
            yt_vedio_images.append(D_logo)

        # 小圓縮圖取得

        yt_channel_infos_image_urls.append(D_logo)

        #print('-' * 30)

    print("爬完收工")

    print(len(vedio_url_list), '文章連結')
    print(len(yt_vedio_images), '圖片連結')
    print(len(yt_title_list), '標題')
    print(len(yt_channel_infos_names), '副標')
    print(len(yt_channel_infos_image_urls), 'last')

    #關閉瀏覽器連線
    driver.close()

    #==============將爬取到的資訊以FlexMessage回傳至主程式===================
    message = []

    #回傳搜尋結果的FlexMessage
    message.append(image_carousel('搜尋結果',yt_vedio_images,vedio_url_list,yt_title_list,yt_channel_infos_image_urls,yt_channel_infos_names))
    return message

#============================爬取指定看板=================================
#============================爬取指定看板=================================

def DCard_News_forbord(keyword):
    # 建立url跟目錄
    url = 'https://www.dcard.tw/f/'
    #newinfos = '?latest=true'
    # 建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    # 設定瀏覽器的user agent
    # chromeOption.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    chromeOption.add_argument("start-maximized")
    # chromeOption.add_argument('--headless')
    chromeOption.add_argument('--no-sandbox')
    chromeOption.add_argument('--disable-dev-shm-usage')
    # 開啟Chrome瀏覽器
    driver = webdriver.Chrome(options=chromeOption)
    # 調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)

    # ======================依關鍵字在Dcard網站上搜尋===========================
    # 進入指定網址
    driver.get(url + keyword)
    time.sleep(2)

    # 休息2秒
    time.sleep(5)

    # ======================從網頁獲取8個縮圖連結===========================
    # 建立影片url列表
    vedio_url_list = []
    # 以css選擇器搜尋Dcard的文章連結
    yt_vedio_urls = driver.find_elements_by_css_selector('.jNOCIa')
    # 將每個文章連結放入連結list
    # print(len(yt_vedio_urls))

    for url in yt_vedio_urls:
        # print(url.get_attribute('href'))
        if len(vedio_url_list) < 10:
            if url.get_attribute('href') != None:
                vedio_url_list.append(url.get_attribute('href'))

    print(len(vedio_url_list), 'v')
    count_nuber = int(len(vedio_url_list))

    # ======================從網頁獲得文章的前八張縮圖===========================

    # 建立縮圖列表
    yt_vedio_images = []
    yt_vedio_images_urls = driver.find_elements_by_css_selector('.eTRrRn div .fKyhRt')
    while True:
        if len(yt_vedio_images) < count_nuber:

            try:
                # 將每個圖片的縮圖放入圖片list
                for image in yt_vedio_images_urls:
                    if '.jpg' in image.get_attribute('src'):
                        if len(yt_vedio_images) < count_nuber:
                            yt_vedio_images.append(image.get_attribute('src'))
                            # print(image.get_attribute('src'))
            except:
                nonpic = 'http://www.tainan-hch.com.tw/site/themes/default/cht/images/nopic.jpg'
                yt_vedio_images.append(nonpic)
        else:
            break
    print(len(yt_vedio_images), 'b')

    # ======================從網頁獲取前八個文章標題與副標題===========================
    # 建立標題列表
    yt_title_list = []
    yt_channel_infos_names = []

    page = driver.page_source

    soup = bs(page, "html.parser")

    data = soup.find_all('article', class_='eTRrRn')

    # print('共有', (len(data)), '筆資料')  # 是列印出共有多少資料夾
    # print('-' * 60)
    for xx in data:
        if len(yt_title_list) < 8:
            # 主標頂
            titles = xx.find('a', class_='jNOCIa')
            title = titles.text
            # print(title.strip())
            yt_title_list.append(title.strip())

        if len(yt_channel_infos_names) < 8:
            # 副標題a
            sectitles = xx.find('div', class_='kAA-DIR')
            sectitle = sectitles.text[0:15]
            # print(sectitle.strip())
            yt_channel_infos_names.append(sectitle.strip())

    print(len(yt_title_list))
    print(len(yt_channel_infos_names))
    # ===================從網頁獲取前八個發布者縮圖========================
    # 資訊列表(圖片)
    yt_channel_infos_image_urls = []
    yt_channel_infos_image_list = driver.find_elements_by_css_selector('.eTRrRn div .fKyhRt')

    while True:
        if len(yt_channel_infos_image_urls) < count_nuber:

            try:
                # 將每個圖片的縮圖放入圖片list
                for infos in yt_channel_infos_image_list:
                    if len(yt_channel_infos_image_urls) < count_nuber:
                        yt_channel_infos_image_urls.append(infos.get_attribute('src'))
                        # print(infos.get_attribute('src'))
            except:
                nonpic = 'http://www.tainan-hch.com.tw/site/themes/default/cht/images/nopic.jpg'
                yt_vedio_images.append(nonpic)

        else:
            break
    print(len(yt_channel_infos_image_urls), 'last')

    # 關閉瀏覽器連線
    driver.close()

    # ==============將爬取到的資訊以FlexMessage回傳至主程式===================
    message = []

    # 回傳搜尋結果的FlexMessage
    message.append(image_carousel('搜尋結果', yt_vedio_images, vedio_url_list, yt_title_list, yt_channel_infos_image_urls,
                                  yt_channel_infos_names))
    return message
   
    
#可於本機中直接執行python web_crawler.py進行單元測試，但必須先將CHANNEL_ACCESS_TOKEN、USERID都在config.py設定好
if __name__=='__main__':
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *
    message = youtube_vedio_parser('facelift')
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID, message)
    