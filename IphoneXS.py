# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 07:36:09 2018

@author: Administrator
"""
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

 
class Spider(object):
    def __init__(self,num):
        self.num = num
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2727.400"}
        
        
    def get_html(self,url):
        #url = ("https://search.suning.com/emall/searchV1Product.do?keyword=iPhone%20XS&ci=20006&pg=01&cp=0&il=0&st=0&iy=0&adNumber=0&isDoufu=1&n=1&sesab=ACAABAAB&id=IDENTIFYING&cc=351&sub=1&jzq=491")
        content = requests.get(url,headers=self.headers).content.decode() 
        return content
    
    def get_content(self,url):
        names = []
        titles = []
        urls = []
        nums = []
        html = self.get_html(url)
        soup = BeautifulSoup(html,'lxml')
        #print(html)
        lis = soup.find('ul',attrs={'class':'general clearfix'}).find_all('li')
        for li in lis:
            name = li.find('div',attrs={'class':'store-stock'}).text.strip()
            title = li.find('div',attrs={'class':'title-selling-point'}).text.strip()
            url = 'https' + li.find('div',attrs={'class':'title-selling-point'}).find('a')['href']
            try:
                num = li.find('div',attrs={'class':'info-evaluate'}).text
            except:
                num = '暂无评价'
            names.append(name)
            titles.append(title)
            urls.append(url)
            nums.append(num)
        #print(names)
        return names,titles,urls,nums
        
    def main(self):
        total_name = []
        total_title = []
        total_url = []
        total_num = []
        for i in range(0,self.num):
            url=('https://search.suning.com/emall/searchV1Product.do?keyword=iPhone%20XS&ci=20006&pg=01&cp='+str(i)+'&il=0&st=0&iy=0&adNumber=0&isDoufu=1&n=1&sesab=ACAABAAB&id=IDENTIFYING&cc=351&sub=1&jzq=491')
            names,titles,urls,nums = self.get_content(url)
            print("正在爬取第%d页" %i)
            total_name.extend(names)
            total_title.extend(titles)
            total_url.extend(urls)
            total_num.extend(nums)
            time.sleep(2)
        #print(total_name)
       # print(total_title)
        #print(total_num)
        data = pd.DataFrame([total_name,total_title,total_url,total_num])
        data = data.T
        data.to_excel('suning.xlsx',index=None,header=None)


            
        



if __name__ == "__main__":
    spider = Spider(5)
    spider.main()