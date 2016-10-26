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
url = 'http://www.zhihu.com' + '/question/26575882'
data = s.get(url, headers=headers)
soup = BeautifulSoup(data.content, 'lxml')
index = soup.find_all('div', {'tabindex': '-1'})
for i in range(len(index)):
    a = index[i].find('a', {'class': 'author-link'})
    if a == None:
        continue
    title =   '.' + a.string
    href = 'http://www.zhihu.com' + a['href']
    print href

