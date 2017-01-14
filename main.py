#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import time

def get_html(url):
    head={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',\
    'Accept-Encoding': 'gzip, deflate, sdch, br',\
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',\
    'Cache-Control': 'max-age=0',\
    'Connection': 'keep-alive',\
    'Cookie': '__jdv=122270672|direct|-|none|-|1484366011881; ipLoc-djd=1-72-4137-0; areaId=1; listck=906e47d625ec80903addb1013e3d934c; __jda=122270672.1484366011879587586832.1484366012.1484366012.1484366012.1; __jdb=122270672.6.1484366011879587586832|1.1484366012; __jdc=122270672; __jdu=1484366011879587586832',\
    'Host': 'list.jd.com',\
    #'If-Modified-Since': 'Sat, 14 Jan 2017 03:44:02 GMT',\
    'Upgrade-Insecure-Requests': '1',\
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    print "Get html"
    html=requests.get(url,headers=head).text.encode('utf-8')
    time.sleep(3)
    return html

def initial(url1,url2):
    print "Intialization"
    url=url1+'1'+url2
    html=get_html(url)
    #print type(html)
    soup = BeautifulSoup(html,"html.parser")
    cur = soup(class_="fp-text")
    for sp in cur:
        all_page=sp.i.string
    print "There are "+all_page+" pages in total"
    all_page=int(unicode(all_page).encode('utf-8'))
    print type(all_page)
    return all_page

def collect_data(page_num):
    print "Collect data"
    for i in range(1,page_num+1):
        url='https://list.jd.com/list.html?cat=737,13297,1300&ev=3680_6820&trans=1&page='+str(i)+'&JL=6_0_0#J_main'
        html=get_html(url)
        soup = BeautifulSoup(html,"html.parser")
        cur = soup(class_="fp-text")
        for sp in cur:
            page=sp.b.string
            print page


f = open('data-set.txt','w')
f.close()
all_page=initial('https://list.jd.com/list.html?cat=737,13297,1300&ev=3680_6820&trans=1&page=','&JL=6_0_0#J_main')
collect_data(all_page)

# url='https://list.jd.com/list.html?cat=737,13297,1300&ev=3680_6820&trans=1&page=1&JL=6_0_0#J_main'
# html=get_html(url)
# #print type(html)
# soup = BeautifulSoup(html,"html.parser")
# cur = soup(class_="fp-text")
# for sp in cur:
#     page=sp.b.string
#     all_page=sp.i.string
# print "There are "+all_page+" pages in total"
# print "This is page No."+page

