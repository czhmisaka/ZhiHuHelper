import json
import os
import re
import time
import requests
from log import log

def getDesktopPath():
    '''
    获取桌面路径
    '''
    return os.path.join(os.path.expanduser('~'),"Desktop")+'/'

class zhihuHelper():
    def __init__(self):
        self.interval = 20
        self.rank = 100
        self.novels_count = dict()
        self.log = log()
        self.select = re.compile(r'>.+?<')
        self.path = getDesktopPath()
        self.headers =  {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"
        }
    def __SaveAsText(self,data):
        self.log.log('保存路径为：'+self.path+'History.txt')
        try:
            with open(self.path+'History.txt','w',encoding='utf-8') as f:
                for x in data:
                    f.write(str(x))
        except:
            self.log.err('保存失败\n'+str(data))

    def __SaveAsjson(self,data):
        self.log.log('保存路径为：'+self.path+'History.json')
        try:
            with open(self.path+'History.json','w') as f:
                json.dump(data,f)
        except:
            self.log.err('保存失败\n'+str(data))
    def __cleanPtab(self,data):
        return data.split('>')[1].split('<')[0]

    def getByQID(self,qid,save=True,max=-1):
        try:
            index = 1
            offset = 0
            data = []
            while True:
                self.log.log(offset)
                baseUrl = f'https://www.zhihu.com/api/v4/questions/{qid}/answers?include=content&limit={self.interval}&offset={offset}&sort_by=default'
                html = requests.get(baseUrl,headers = self.headers)
                answers = html.json()['data']
                if len(answers) == 0:
                    self.log.log('没有这个问题或者该问题回答数量为【0】 参数='+str(qid))
                    return 0
                for answer in answers:
                    data.append('\nindex:'+str(index)+'\n')
                    results = set(re.findall(self.select,answer['content']))
                    for x in results:
                        if self.__cleanPtab(x) != '':    
                            data.append(self.__cleanPtab(x)+'\n')
                    index = index + 1
                offset = offset + self.interval
                if max!=-1 and offset>max:
                    break
            if save:
                self.__SaveAsText(data)
            return data
        except:
            self.log.err('getByQID出问题啦! 参数='+str(qid))