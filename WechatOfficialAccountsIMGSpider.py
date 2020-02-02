#!/usr/bin/env python
# coding: utf-8

# In[7]:


from re import findall
from urllib.request import urlopen

url ='https://mp.weixin.qq.com/s?__biz=MjM5OTA2NDkzNw==&mid=2654713308&idx=1&sn=ee6708512ba1d6a29465cf2e14a2999b&chksm=bd0e31da8a79b8cc2dc96cb4c2c489f662988cd84acbfaac888c13b0d1efb66bc214da8f681c&scene=0&xtrack=1#rd'



with urlopen(url) as fp:
    content = fp.read().decode()
    
pattern = 'data-type="png" data-src="(.+?)"'

result = findall(pattern,content)
for index,item in enumerate(result):
    with urlopen(str(item)) as fp:
        with open(str(index)+'.jpg','wb') as fp1:
            fp1.write(fp.read())


# In[9]:


import os
import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://weibo.com/2419425757/profile?topnav=1&wvr=6&is_all=1',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': ''
}


def main():

    if not os.path.exists('pic'):
        os.mkdir('pic')

    for i in range(0, 10):
        for j in range(0, 2):
            url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_hot=1&pagebar=%s&pl_name=Pl_Official_MyProfileFeed__21&id=1005052651221301&script_uri=/u/2651221301&feed_type=0&page=%s&pre_page=%s&domain_op=100505&__rnd=1545271176219' % (str(j), str(i), str(i))

            print(url)
            res = requests.get(url, headers=headers)
            res_data = res.json()
            html = res_data['data']
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup.prettify())  # 格式化html内容
            ul_list = soup.select('.WB_detail .media_box ul')
            for ul in ul_list:
                # print(ul)
                action_data = ul.attrs.get('action-data', '')
                for item in action_data.split('&'):
                    if 'clear_picSrc' in item:
                        pic_urls = item.split('=')[1].replace('%2F', '/').split(',')
                        for pic_url in pic_urls:
                            pic_name = pic_url.split('/')[-1]
                            res_of_pic = requests.get('http:' + pic_url)
                            if res_of_pic.status_code == 200:
                                with open('pic/' + pic_name, 'wb') as f:
                                    f.write(res_of_pic.content)
                                    print('抓取成功', pic_name)


if __name__ == '__main__':
    main()


# In[ ]:




