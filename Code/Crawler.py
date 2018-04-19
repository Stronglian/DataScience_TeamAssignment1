# -*- coding: utf-8 -*-
"""
from Team Assignment 1 - part1 - crawler_scroll
windows 7
"""
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from datetime import datetime
import json
import codecs

#滾動畫面 3秒滾動一次
def execute_times(times, driver, sleepTimeSec = 3):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*arguments[0]);",i*100)
        time.sleep(sleepTimeSec)
    return
def ArticleCrawler(TAG, base_url, driver, scollTime = 10):
    #print("#START")
    #指定 driver
    #driver=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    #文章暫存
    #print("#文章暫存")
    article_amount = 0
    article_nums = []
    article_titles = []
    article_links = [] 
    article_content = []
    #網站讀取
    url = base_url +'/'+TAG
    #print("#網站讀取")
    driver.get(url)
    execute_times(scollTime, driver)
    #撈文章列表
    #print("#撈文章列表")
    yahoo_html    = driver.page_source
    yahoo_soup    = BeautifulSoup(yahoo_html,'html.parser')
    yahoo_findTAG = yahoo_soup.find_all('li','js-stream-content Pos(r)')
    #網站關閉 #考慮放後面
    #driver.quit()
    #處理文章標題、連結
    #print("#處理文章標題、連結")
    for info in yahoo_findTAG:
        link = ""
        try:
            title = info.find('a') #滿滿的 title
            link = info.find_all('a', href=True)[0]
            #title = title.split(';')[4].split(':')[1] #切割出 主要的標題
            #print(link.get("href"))
            if link.get('href') != '#':
                #跳過贊助廣告
                if info.svg['data-icon'] == "sponsor": 
                    #print("Sponsored")
                    #print('===')
                    continue
                #處理影片連結
                #elif link.get("href").split(':', 1)[0][:4] == "http":
                elif link.get("href")[0] != "/":
                    #print("error link:", link.get("href"))
                    #print(info)
                    #print('===')
                    #continue
                    link_temp = link.get("href")
                else:
                    link_temp = base_url + link.get("href")
                #處理 " 的問題
                if '"' in title.text:
                    #print('title with "')
                    tempList = title.split('"')
                    for part in tempList:
                        title += part
                    #continue
                #組成 list
                article_titles.append(title.text)
                article_links.append(link_temp)
                article_amount+=1
                #print(title.text)
                #print(link_temp)
                #print('===')
        except:
            link = None
    #處理文章內容
    #print("#處理文章內容")
    for link in article_links:
        try:
            #print(link)
            article_res     = requests.get(link)
            article_soup    = BeautifulSoup(article_res.text,'html.parser')
            article_findTAG = article_soup.find_all('p')
            #利用網址內的數字做編號
            number_temp = link
            number_temp = str(number_temp).split("-")[-1]
            number_temp = str(number_temp).split(".")[0]
            #文章內文
            content = ""
            for content_temp in article_findTAG:
                #串起文字
                content += content_temp.text
            #處理 " 的問題
            if '"' in content:
                #print(number_temp,'content with "')
                tempList = content.split('"')
                #content = ""
                content = tempList[0]
                for part in tempList[1:]:
                    #content += part
                    content += "\\\"" + part
            #處理 \n 的問題
            if '\n' in content:
                #print(number_temp,'content with "')
                tempList = content.split('\n')
                #content = ""
                content = tempList[0]
                for part in tempList[1:]:
                    #content += part
                    content += "\\n" + part
        except: #處理未避掉的錯誤
            print(link)
            content = "None"
            number_temp = "None"
        article_content.append(content)
        article_nums.append(number_temp)
    #print("#END")
    return article_amount, article_titles, article_nums, article_links, article_content
    
def StroeArticleToJSON(wholeData,TAG):
    filename= str(str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) +"_"+TAG+".json")
    article_amount, article_titles, article_nums, article_links, article_content = wholeData
    
    with codecs.open(filename, "w+", encoding='utf-8') as f:
        f.write('{'+'\n')
        f.write(' "article_amount":'+str(article_amount)+',\n')
        f.write(' "article_TAG":"'+str(TAG)+'",\n')
        f.write(' "article":'+'{\n')
        #f.write(" {"+"\n")
        for j in range(article_amount):
            f.write(' "'+str(article_nums[j])+'":{'+'\n')
            #f.write('  {'+'\n')
            f.write('   "article_titles":"' +str(article_titles[j]) +'",\n')
            f.write('   "article_links":"'  +str(article_links[j])  +'",\n')
            f.write('   "article_content":"'+str(article_content[j])+'"\n')
            if j != article_amount-1:
                f.write('  },'+'\n')
            else: #最後
                f.write('  }'+'\n')
        f.write(' }'+'\n')
        f.write('}'+'\n')
    return

def CrawlerTimer(TAGs, base_url, delayTime = 3600, repeatTime = 1):
    repeatCount = 0
    while repeatTime > repeatCount:
        print(repeatCount, str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        #指定 driver
        driver=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        for i in range(len(TAGs)):
            TAG = TAGs[i]
            url = base_url +'/'+TAG
            print(TAG, url)
            wholeData = ArticleCrawler(TAG, base_url, driver)
            StroeArticleToJSON(wholeData, TAG)
            print("DONE")
        driver.quit()
        repeatCount +=1
        if repeatTime > repeatCount:
            print('wait', end="")
            for i in range(10):
                print('.', end="")
                time.sleep(delayTime//10)
            time.sleep(delayTime-(delayTime//10 * 10))
            print("|")
    return

if __name__ == '__main__':
    base_url = "https://tw.news.yahoo.com"
    TAGs = ["politics", "entertainment"]
    CrawlerTimer(TAGs, base_url, repeatTime = 1)