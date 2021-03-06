#Date: 2017.01.17
#Author: RyQ
#Name: jd_crawler
#Ver:0.9

# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import urllib2
import json
import random

reload(sys)
sys.setdefaultencoding('utf-8')

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
# proxy = urllib2.ProxyHandler({'http': '118.123.245.145:3128'})
# opener = urllib2.build_opener(proxy)
# urllib2.install_opener(opener)

def get_html(url):
    #print "Get html"
    html=requests.get(url,headers=head).text
    sec = random.randint(2, 5) 
    time.sleep(sec)
    return html

def initial(url1,url2):
    print "Initialization"
    url=url1+'1'+url2
    html=get_html(url)
    #print type(html)
    soup = BeautifulSoup(html,"html.parser")
    cur = soup(class_="fp-text")
    for sp in cur:
        all_page=sp.i.string
    print "There are "+all_page+" pages in total"
    all_page=int(all_page)
    #print type(all_page)
    return all_page

def get_item(url1,url2,page_curr):
    url = url1+str(page_curr)+url2
    html = get_html(url)
    soup = BeautifulSoup(html,"html.parser")
    cur = soup(class_="fp-text")
    for sp in cur:
        page=sp.b.string
        print "This is page: "+page

    reg_item = r'<li class="gl-item">(.*?)</li>'
    item = re.findall(reg_item,html,re.S)
    item = ''.join(item)

    #Get p_name
    item_soup = BeautifulSoup(item,"html.parser")
    _p_name = item_soup.find_all("div","p-name")
    p_name = []
    count = 0
    for sp in _p_name:
        temp = sp.em.string
        count+=1
        #print temp
        #print unicode(sp.em.string).decode('utf-8')
        p_name.append(temp)
        #if count==2: break
    #print p_name

    print "Total fine "+str(count)+" product name"

    #Get p_sku_id & p_price
    for i in range(count):
        reg_sku = r'j-sku-item"  data-sku="(.*?)" vender'
        p_sku_id = re.findall(reg_sku,item,re.S)
    print "Total fine ",i+1," product id"
    p_sku_id = [int(j) for j in p_sku_id]
    #print p_sku_id
    #print type(item)

    #Get p_price & p_comment
    p_price=[]
    p_page=[]
    p_count=[]
    p_comment5=[]
    p_comment4=[]
    p_comment3=[]
    p_comment2=[]
    p_comment1=[]

    count=0
    for skuid in p_sku_id:
        count+=1
        print count, '/', i+1, skuid
        p_page.append(int(page))
        p_count.append(count)

        url_price = 'http://p.3.cn/prices/get?type=1&area=1_72_2799&pdtk=&pduid=14834698456071940921980&pdpin=&pdbp=0&skuid=J_' + str(skuid)
        #print "Get price from: "+url_price
        try:
            price_json = json.load(urllib2.urlopen(url_price,timeout=10))[0]
        except:
            print 'Timeout!'
            price_json = '{"p":"-2"}'

        sec = random.randint(2, 5) 
        #price_json = json.load(requests.get(url_price,headers=head).text)[0]
        if price_json['p']:
            print price_json['p']
            p_price.append(float(price_json['p']))

        #print p_price

        time.sleep(sec)

        url_comment = 'http://s.club.jd.com/productpage/p-'+str(skuid)+'-s-0-t-0-p-1.html'
        #print "Get comment from: "+url_comment
        try:
            comment_json=json.loads(requests.get(url_comment).text.encode('utf-8'))['productCommentSummary']
            #comment_json=json.load(urllib2.urlopen(url_comment,timeout=10))['productCommentSummary']
        except:
            print 'Timeout!'
            comment_json = json.loads('{"score5Count":"-5","score4Count":"-4","score3Count":"-3","score2Count":"-2","score1Count":"-1"}')
        
        #price_json = json.load(requests.get(url_price,headers=head).text)[0]
        print comment_json['score5Count'],comment_json['score1Count']
        p_comment5.append(comment_json['score5Count'])
        #print p_comment5
        p_comment4.append(comment_json['score4Count'])
        p_comment3.append(comment_json['score3Count'])
        p_comment2.append(comment_json['score2Count'])
        p_comment1.append(comment_json['score1Count'])
        time.sleep(sec)

        #if count==2: break

    p_id = range(1,i+2)
    p_list = zip(p_id, p_page, p_count, p_sku_id, p_name, p_price, p_comment5, p_comment4, p_comment3, p_comment2, p_comment1)
    #p_list = zip(p_id, p_sku_id, p_price, p_comment)
    return(p_list)

def collect_data(url1,url2,page_num):
    print "collect_data"
    f=open('data-set.csv','w')
    print >> f, '"id","page","count","p_sku_id","p_name","p_price","p_comment5","p_comment4","p_comment3","p_comment2","p_comment1"'
    f.close()
    for i in range(1,page_num+1):
        p_list=get_item(url1,url2,i)
        #print p_list
        #print type(p_list)
        print "Get p_list! Write in data..."
        f=open('data-set.csv','a')
        for line in p_list:
            count=0
            for ch in line:
                count+=1
                if count==11:
                    print >> f,ch
                else:
                    print >> f,ch,',',

        f.close()
        print "Write-in over, next page."

url1='https://list.jd.com/list.html?cat=737,13297,1300&ev=3680_6820&trans=1&page='
url2='&JL=6_0_0#J_main'

all_page=initial(url1,url2)
#all_page=1
collect_data(url1,url2,all_page)


