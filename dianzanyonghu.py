#coding:utf-8

import requests
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


Zhihu = 'http://www.zhihu.com'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}

def get_voters(ans_id):
    # 直接输入问题id(这个id在点击“等人赞同”时可以通过监听网络得到)，关注者保存在以问题id命名的.txt文件中
    # login()
    s = requests.session()
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

get_voters(5430533)