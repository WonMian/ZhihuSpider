#coding:utf-8

import requests
import json
from bs4 import BeautifulSoup
import sys
import os
import login
import re


reload(sys)
sys.setdefaultencoding( "utf-8" )
Zhihu = 'http://www.zhihu.com'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
s = requests.session()
path = os.path.abspath(os.path.dirname("gezhongzishi.py")) + '/list'
if not os.path.isdir(path):
    os.mkdir(path)
dog_name = path + '/' + 'WuhanFemale' + '.txt'
fr = open(dog_name, 'w')
holenum = 1
def get_answer(href):  #提取每个问题下面的前10个回答
    global holenum
    url = 'http://www.zhihu.com' + href
    data = s.get(url, headers=headers)
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        question = soup.find('span',{'class':'zm-editable-content'}).get_text()
        print question
    except:
        pass
    index = soup.find_all('div', {'tabindex': '-1'})
    for i in range(len(index)):
        a = index[i].find('a', {'class': 'author-link'})
        if a == None:
            continue
        title = str(holenum) + '.' + a.string
        href = 'http://www.zhihu.com' + a['href']
        people = s.get(href, headers=headers) #去每个回答者的页面,如果粉丝大于100,则视为优秀

        followNum = re.findall(u'<span.*?>关注者.*?strong>(.*?)</strong>',people.content.decode("utf-8", 'ignore'),re.S)
        try:
            try:
                if int(followNum[0]) > 50:
                    sex = re.findall(u'<span class="item gender.*?icon-profile-(.*?)"></i>',people.content,re.S)[0]
            except:
                print u'无法确定性别'
            if sex == 'female':  #判断是不是男生
                soup = BeautifulSoup(people.content,'lxml')
                try:
                    introduce = soup.find_all('span',{'class':'content'})[0].string.strip()
                except:
                    introduce = 'None'
                votes = re.findall('<span class="zm-profile-header.*?strong>(.*?)</strong>',people.content.decode("utf-8", 'ignore'),re.S)[0]
                tks = re.findall('<span class="zm-profile-header.*?strong>(.*?)</strong>',people.content.decode("utf-8", 'ignore'),re.S)[1]
                fr.write(title + "\t关注者:"+followNum[0]+"\t点赞数:" + votes +"\t感谢数"+ tks + "\n" + "简介:" + introduce + "\n链接:" + href+'\n')
                print u"采集第 %d 位 %s" % (holenum,a.string)
                holenum += 1
        except:
            print u"有数据缺失"


def find_SingleDog():
    baseurl = 'https://www.zhihu.com/topic/19570564/top-answers'
    num1 = 1
    questionList = []
    for num in range(1,51):
        url = baseurl + '?page=' + str(num)
        data = s.get(url, headers=headers)
        questions = re.findall('<a class="question_link.*?f="(.*?)"',data.content.decode("utf-8", 'ignore'),re.S)
        for question in questions:
            print u'正在获取第%d个话题' % num1
            i = question[-8:]
            if str(i) in questionList:
                continue
            else:
                questionList.append(question[-8:])
                get_answer(question)
                num1 += 1


# if __name__ == '__main__':
find_SingleDog()
fr.close()