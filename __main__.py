from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

import time
from selenium import webdriver

# from konlpy.tag import Hannanum
# from eunjeon import Mecab

# han = Hannanum()#han.nouns(text)
# mcb = Mecab()
# morphology_analyzer = mcb

from crawlers.DaumNewsCrawler import DaumCrawler
from crawlers.NaverNewsCrawler import NaverCrawler
from crawlers.DaumNewsMultiCrawler import crawlLinks as daumCrawlLinks, crawlNews as daumCrawlNews
from crawlers.NaverNewsMultiCrawler import crawlLinks as naverCrawlLinks, crawlNews as naverCrawlNews

from utils.util import *

import json
import datetime

import numpy as np
 
import numba
from tqdm import trange

import sys
sys.setrecursionlimit(5000)


def info_time(dic, us_news, kr_news):
    dic_key = dic.keys()
    info_term_time = []

    date_dic = {}

    for i in dic_key:
        temp_time = [x.split('.')[1] for x in dic[i]]

        if len(temp_time) > 1:
            temp_time.sort()
            sum_time = 0

            for j in temp_time:
                '''
                j = kr_news[j]['date']
                year_ = int(j[:4])
                mon_ = int(j[4:6])
                day_ = int(j[6:8])
                '''
                hour_ = int(j[8:10])
                min_ = int(j[10:12])
                sec_ = int(j[12:14])
                sum_time += hour_*60*60 + min_*60 + sec_
            avg_time = sum_time / len(temp_time)

            end_year = temp_time[-1][:4]
            end_mon = temp_time[-1][4:6]
            end_day = temp_time[-1][6:8]
            end_hour = temp_time[-1][8:10]
            end_min = temp_time[-1][10:12]
            # end_sec = temp_time[-1][12:14]
            end_ = ''.join([str(i) for i in [end_year, end_mon, end_day, end_hour, end_min]])

            start_year = temp_time[0][:4]
            start_mon = temp_time[0][4:6]
            start_day = temp_time[0][6:8]
            start_hour = temp_time[0][8:10]
            start_min = temp_time[0][10:12]
            # start_sec = temp_time[0][12:14]
            start_ = ''.join([str(i) for i in [start_year, start_mon, start_day, start_hour, start_min]])

            diff = (datetime(int(end_year), int(end_mon), int(end_day), int(end_hour), int(end_min))  -  datetime(int(start_year), int(start_mon), int(start_day), int(start_hour), int(start_min))).total_seconds()
            info_term_time.append([i, us_news[i]['title'], us_news[i]['date'], start_, end_, diff, avg_time])

            this_date = us_news[i]['date'][:8]

            if this_date in date_dic.keys():
                date_dic[this_date].append(avg_time)
            else:
                date_dic[this_date] = [avg_time]

    for k, v in date_dic.items():
        date_dic[k] = round(np.mean(v)/3600, 1)

    return date_dic

    # dataframe = df(info_term_time, columns=['URL', 'Title', '미국기사 시간', '처음 한국기사 시간', '마지막 한국기사 시간', 'diff', '평균'])
    # dataframe.to_csv('Task2.csv', encoding='cp949')


if __name__ == "__main__":
    # 크롬 드라이버 링크
    driver_url = './chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--privileged')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # selenium으로 크롤링하여 저장된 링크를 가지고 requests로 다시 크롤링하여 json으로 저장
    # kr은 requests로 동기식, us는 grequests와 async로 비동기식 (kr은 비동기가 안먹힘(다음뉴스 500 오류))

    search = "포트폴리오"
    start_date = "20210801"
    # start_date = "20210530"
    end_date = "20211201"


    
    search = search.replace(' ', '+')


    # # 크롤러 객체 생성
    daum_crawler = DaumCrawler(driver_url, chrome_options)
    naver_crawler = NaverCrawler(driver_url, chrome_options)

    daum_crawler.crawlLinks(search, start_date, end_date) # 링크 크롤링(selenium)
    daum_crawler.crawlNews(search, start_date, end_date) # 뉴스 크롤링(async+grequest+bs4)
    
    naver_crawler.crawlLinks(search, start_date, end_date) # 링크 크롤링(selenium)
    naver_crawler.crawlNews(search, start_date, end_date) # 뉴스 크롤링(async+grequest+bs4)


    daumCrawlLinks(search, start_date, end_date, driver_url, chrome_options)
    daumCrawlNews(search, start_date, end_date, driver_url, chrome_options)
    
    naverCrawlLinks(search, start_date, end_date, driver_url, chrome_options)
    naverCrawlNews(search, start_date, end_date, driver_url, chrome_options)

    exit()

    dic = {}
    dic2 = {}


    
    # with open('result/daum_news/news_주한미군_daum_20200601_20210601__202006.json','r', encoding='utf8') as f:
    # # with open(f'result/daum_news/news_{search}_daum_{start_date}_{end_date}.json','r', encoding='utf8') as f:
    # # with open(f'result/naver_news/news_{search}_naver_{start_date}_{end_date}.json','r', encoding='utf8') as f:
    #     dic = json.load(f)



    # company = "naver"

    # start_date_ = datetime.date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
    # end_date_ = datetime.date(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:])) + datetime.timedelta(days=1)

    # date_list = [str(i).replace('-', '')[0:8] for i in daterange(start_date_, end_date_)]


    # for date in date_list:
    #     if date[:6] not in dic2.keys():
    #         dic2[date[:6]] = []

    # json_list = []
    # for date in dic2.keys():
    #     with open(f'result/{company}_news/news_주한미군_{company}_{start_date}_{end_date}__{date}.json','r', encoding='utf8') as f:
    #     # with open(f'result/daum_news/news_{search}_daum_{start_date}_{end_date}.json','r', encoding='utf8') as f:
    #     # with open(f'result/naver_news/news_{search}_naver_{start_date}_{end_date}.json','r', encoding='utf8') as f:
    #         dic2 = json.load(f)

    #     dic.update(dic2)

    # dic2 = {}
    # for date in dic.keys():
    #     if date[:6] not in dic2.keys():
    #         dic2[date[:6]] = []

    #     dic2[date[:6]].append(dic[date])


    # all = 0
    # for mon in dic2.keys():
    #     count = 0
    #     for dic3 in dic2[mon]:
    #         for url, contain in dic3.items():
    #             for comment in contain['comments']:
    #                 count += 1
    #     all += count
    #     print(f'{mon} : {count}')
    # print(f'all : {all}')

    # with open(f'result/{company}_news/news_{search}_{company}_{start_date}_{end_date}.json', 'w', encoding='utf8') as f:
    #     json.dump(dict(dic), f, indent=4, sort_keys=True, ensure_ascii=False)

        
    dic = {}
    start_date_ = datetime.date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
    end_date_ = datetime.date(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:])) + datetime.timedelta(days=1)

    date_list = [str(i).replace('-', '')[0:8] for i in daterange(start_date_, end_date_)]


    for date in date_list:
        if date not in dic.keys():
            dic[date] = {}

    all = 0
    for date in dic.keys():
        for company in ["daum", "naver"]:
            with open(f'result/{company}_news/news_주한미군_{company}_{start_date}_{end_date}__{date[:6]}.json','r', encoding='utf8') as f:
                dic2 = json.load(f)

            dic[date].update(dic2[date])


    dic2 = {}
    for date in dic.keys():
        if date[:6] not in dic2.keys():
            dic2[date[:6]] = []

        dic2[date[:6]].append(dic[date])


    all = 0
    for mon in dic2.keys():
        count = 0
        for dic3 in dic2[mon]:
            for url, contain in dic3.items():
                for comment in contain['comments']:
                    count += 1
        all += count
        print(f'{mon} : {count}')
    print(f'all : {all}')
    with open(f'result/news_{search}_all_{start_date}_{end_date}.json', 'w', encoding='utf8') as f:
        json.dump(dict(dic), f, indent=4, sort_keys=True, ensure_ascii=False)
    exit()