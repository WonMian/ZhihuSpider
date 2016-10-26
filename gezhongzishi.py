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

def get_voters(ans_id): #获取所有点赞者的信息
    # 直接输入问题id(这个id在点击“等人赞同”时可以通过监听网络得到)，关注者保存在以问题id命名的.txt文件中
    # login()

    file_name = str(ans_id) + '.txt'
    f = open(file_name, 'w')
    source_url = Zhihu + '/answer/' +str(ans_id) +'/voters_profile'
    source = s.get(source_url, headers=headers)
    print source
    content = source.content
    # print content    # json语句
    data = json.loads(content)   # 包含总赞数、一组点赞者的信息、指向下一组点赞者的资源等的数据
    txt1 = '总赞数'
    print txt1.decode('utf-8')
    total = data['paging']['total']   # 总赞数
    print data['paging']['total']   # 总赞数
    # 通过分析，每一组资源包含10个点赞者的信息（当然，最后一组可能少于10个），所以需要循环遍历
    nextsource_url = source_url     # 从第0组点赞者开始解析
    num = 0
    while nextsource_url!=Zhihu:
        try:
            nextsource = s.get(nextsource_url, headers=headers)
        except:
            time.sleep(2)
            nextsource = s.get(nextsource_url, headers=headers)
        # 解析出点赞者的信息
        nextcontent = nextsource.content
        nextdata = json.loads(nextcontent)
        # 打印每个点赞者的信息
        # txt2 = '打印每个点赞者的信息'
        # print txt2.decode('utf-8')
        # 提取每个点赞者的基本信息
        for each in nextdata['payload']:
            num += 1
            print num
            try:
                soup = BeautifulSoup(each, 'lxml')
                tag = soup.a
                title = tag['title']    # 点赞者的用户名
                href = 'http://www.zhihu.com' + str(tag['href'])    # 点赞者的地址
                # 获取点赞者的数据
                list = soup.find_all('li')
                votes = list[0].string  # 点赞者获取的赞同
                tks = list[1].string  # 点赞者获取的感谢
                ques = list[2].string  # 点赞者提出的问题数量
                ans = list[3].string  # 点赞者回答的问题数量
                # 打印点赞者信息
                string = title + '  ' + href + '  ' + votes + tks + ques + ans
                f.write(string + '\n')
                print string
            except:
                txt3 = u'有点赞者的信息缺失'
                f.write(txt3)
                f.write('\n')
                print txt3
                continue
        # 解析出指向下一组点赞者的资源
        nextsource_url = Zhihu + nextdata['paging']['next']
    f.close()

def get_followees(username):   #抓取关注者名单
    # 直接输入用户名，关注者保存在以用户名命名的.txt文件中
    followers_url = 'http://www.zhihu.com/people/' + username + '/followees'
    file_name = username + '.txt'
    f = open(file_name, 'w')
    data = s.get(followers_url, headers=header_info)
    print data  # 访问服务器成功，返回<responce 200>
    content = data.content  # 提取出html信息
    soup = BeautifulSoup(content, "lxml")   # 对html信息进行解析
    # 获取关注者数量
    totalsen = soup.select('span[class*="zm-profile-section-name"]')
    total = int(str(totalsen[0]).split(' ')[4])     # 总的关注者数量
    txt1 = '总的关注者人数：'
    print txt1.decode('utf-8')
    print total
    follist = soup.select('div[class*="zm-profile-card"]')  # 记录有关注者信息的list
    num = 0 # 用来在下面显示正在查询第多少个关注者
    for follower in follist:
        tag =follower.a
        title = tag['title']    # 用户名
        href = 'http://www.zhihu.com' + str(tag['href'])    # 用户地址
        # 获取用户数据
        num +=1
        print '%d   %f' % (num, num / float(total))
        # Alist = follower.find_all(has_attrs)
        Alist = follower.find_all('a', {'target': '_blank'})
        votes = Alist[0].string  # 点赞者获取的赞同
        tks = Alist[1].string  # 点赞者获取的感谢
        ques = Alist[2].string  # 点赞者提出的问题数量
        ans = Alist[3].string  # 点赞者回答的问题数量
        # 打印关注者信息
        string = title + '  ' + href + '  ' + votes + tks + ques + ans
        try:
            print string.decode('utf-8')
        except:
            print string.encode('gbk', 'ignore')
        f.write(string + '\n')

    # 循环次数
    n = total/20-1 if total/20.0-total/20 == 0 else total/20
    for i in range(1, n+1, 1):
        # if num%30 == 0:
          #   time.sleep(1)
        # if num%50 == 0:
          #   time.sleep(2)
        raw_hash_id = re.findall('hash_id(.*)', content)
        hash_id = raw_hash_id[0][14:46]
        _xsrf = login.get_xsrf()
        offset = 20*i
        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
        payload = {"method":"next", "params": params, "_xsrf": _xsrf}
        click_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
        data = s.post(click_url, data=payload, headers=header_info)
        # print data
        source = json.loads(data.content)
        for follower in source['msg']:
            soup1 = BeautifulSoup(follower, 'lxml')
            tag =soup1.a
            title = tag['title']    # 用户名
            href = 'http://www.zhihu.com' + str(tag['href'])    # 用户地址
            # 获取用户数据
            num +=1
            print '%d   %f' % (num, num/float(total))
            # Alist = soup1.find_all(has_attrs)
            Alist = soup1.find_all('a', {'target': '_blank'})
            votes = Alist[0].string  # 点赞者获取的赞同
            tks = Alist[1].string  # 点赞者获取的感谢
            ques = Alist[2].string  # 点赞者提出的问题数量
            ans = Alist[3].string  # 点赞者回答的问题数量
            # 打印关注者信息
            string = title + '  ' + href + '  ' + votes + tks + ques + ans
            try:
                print string.decode('utf-8')
            except:
                print string.encode('gbk', 'ignore')
            f.write(string + '\n')
    f.close()

def get_avatar(userId):   #提取头像
    url = 'https://www.zhihu.com/people/' + userId
    response = s.get(url, headers=header_info)
    response = response.content
    soup = BeautifulSoup(response, 'lxml')
    name = soup.find_all('span', {'class': 'name'})[1].string
    # print name
    temp = soup.find('img', {'alt': name})
    avatar_url = temp['src'][0:-6] + temp['src'][-4:]
    filename = 'pics/' + userId + temp['src'][-4:]
    f = open(filename, 'wb')
    f.write(requests.get(avatar_url).content)
    f.close()

def get_answer(questionID):  #获取所有回答
    url = 'http://www.zhihu.com/question/' + str(questionID)
    data = s.get(url, headers=headers)
    soup = BeautifulSoup(data.content, 'lxml')
    # print str(soup).encode('gbk', 'ignore')
    title = soup.title.string.split('\n')[2]    # 问题题目
    path = os.path.abspath(os.path.dirname("gezhongzishi.py")) + '/title'
    if not os.path.isdir(path):
        os.mkdir(path)
    description = soup.find('div', {'class': 'zm-editable-content'}).strings    # 问题描述，可能多行
    file_name = path + '/description.txt'
    fw = open(file_name, 'w')
    for each in description:
        each = each + '\n'
        fw.write(each)
    # description = soup.find('div', {'class': 'zm-editable-content'}).get_text() # 问题描述
        # 调用.string属性返回None（可能是因为有换行符在内的缘故）,调用get_text()方法得到了文本，但换行丢了
    answer_num = int(soup.find('h3', {'id': 'zh-question-answer-num'}).string.split(' ')[0]) # 答案数量
    num = 1
    index = soup.find_all('div', {'tabindex': '-1'})
    for i in range(len(index)):
        print ('Scrapying the ' + str(num) + 'th answer......').encode('gbk', 'ignore')
        # print ('正在抓取第' + str(num) + '个答案......').encode('gbk', 'ignore')
        try:
            a = index[i].find('a', {'class': 'author-link'})
            title = str(num) + '__' + a.string
            href = 'http://www.zhihu.com' + a['href']
        except:
            title = str(num) + '__匿名用户'
        answer_file_name = path + '/' + title + '__.txt'
        fr = open(answer_file_name, 'w')
        try:
            answer_content = index[i].find('div', {'class': 'zm-editable-content clearfix'}).strings
        except:
            answer_content = ['作者修改内容通过后，回答会重新显示。如果一周内未得到有效修改，回答会自动折叠。']
        for content in answer_content:
            fr.write(content + '\n')
        fr.write(u'链接:'+href)
        num += 1

    _xsrf = login.get_xsrf()
    url_token = re.findall('url_token(.*)', data.content)[0][8:16]
    # 循环次数
    n = answer_num/10-1 if answer_num/10.0-answer_num/10 == 0 else answer_num/10
    for i in range(1, n+1, 1):
        # _xsrf = xsrf
        # url_token = re.findall('url_token(.*)', data.content)[0][8:16]
        offset = 10*i
        params = json.dumps({"url_token": url_token, "pagesize": 10, "offset": offset})
        payload = {"method":"next", "params": params, "_xsrf": _xsrf}
        click_url = 'https://www.zhihu.com/node/QuestionAnswerListV2'
        data = s.post(click_url, data=payload, headers=headers)
        data = json.loads(data.content)
        for answer in data['msg']:
            print ('Scrapying the ' + str(num) + 'th answer......').encode('gbk', 'ignore')
            # print ('正在抓取第' + str(num) + '个答案......').encode('gbk', 'ignore')
            soup1 = BeautifulSoup(answer, 'lxml')
            try:
                a = soup1.find('a', {'class': 'author-link'})
                title = str(num) + '__' + a.string
                href = 'http://www.zhihu.com' + a['href']
            except:
                title = str(num) + '__匿名用户'
            answer_file_name = path + '/' + title + '__.txt'
            fr = open(answer_file_name, 'w')
            try:
                answer_content = soup1.find('div', {'class': 'zm-editable-content clearfix'}).strings
            except:
                answer_content = ['作者修改内容通过后，回答会重新显示。如果一周内未得到有效修改，回答会自动折叠。']
            for content in answer_content:
                fr.write(content + '\n')
            fr.write(u'链接:'+href)
            num += 1

get_answer(43667227)