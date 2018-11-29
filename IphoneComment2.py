# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:22:09 2018

@author: Administrator
"""
import requests
import time
import re
import json

class SuNingspider(object):
    def __init__(self):
        #self.url = "https://review.suning.com/ajax/cluster_review_lists/general-30193812-000000010606649857-0000000000-total-1-default-10-----reviewList.htm?callback=reviewList"
        self.headers =  {"User_Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2727.400"}
        self.offset = 1
        self.file = open("222.json","w",encoding="utf-8")
        
    def start_request(self):
        #url = "https://review.suning.com/ajax/cluster_review_lists/general-30193812-000000010606649857-0000000000-total-1-default-10-----reviewList.htm?callback=reviewList"
        for i in range(1,100):
            url = ("https://review.suning.com/ajax/cluster_review_lists/general-30193812-000000010606649857-0000000000-total-%d-default-10-----reviewList.htm?callback=reviewList" %i)
            print("正在爬取第%d页" %i)
            #print(url)
            html = requests.get(url,headers=self.headers).content.decode()          
            #html = response.text
            time.sleep(1)
            self.content_re(html)
 
        
    def content_re(self,html):
        user = re.findall(r'"nickName":"(.*?)"',html,re.S)
        store = re.findall(r'"shopName":"(.*?)"',html,re.S)
        #score = re.findall(r'"qualityStar":(.*?/(\d+)).*?,',html)
        score=re.findall(r'"qualityStar":(.?)',html,re.S)
        commentDate = re.findall(r'"publishTime":"(.*?)"',html,re.S)
        comment = re.findall(r'"content":"(.*?)"',html,re.S)
        for user,store,score,commentDate,comment in zip(user,store,score,commentDate,comment):
            items = {"用户名":user,"店铺名":store,"评分":score,"评论时间":commentDate,"评论内容":comment}
            i = json.dumps(items,ensure_ascii=False) + "," +"\n"
            self.file.write(i)
        
        
if __name__ == "__main__":
    spider = SuNingspider()
    spider.start_request()