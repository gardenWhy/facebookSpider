# -*- coding:utf-8 -*-

import requests
import pandas as pd 
from dateutil.parser import parse
from Base import randHeader


"""
需要在一个主页采集facebook 帖子的： 点赞数量，分享数量，图片/视频，链接，评论数量，文案
主页是无限加载的

图片/视频
"""


#一页的内容数
page_num = 5
#使用你自己的token
token ='EAACEdEosxxxczYu1MaxxxnbSCmWsZAvxxxxxM4fSbkDFxxxxRE0szagj1vefYR9ywOxxxetLJW6UqVpYsFUTlzT9SZA6GGskjbLSEM'
#Nike Facebook主页ID
fanpage_id = '15087023444'

#通过Facebook主页ID和access token，爬取推文时间、内容、点赞数和分享数
index_url = 'https://graph.facebook.com/v2.12/{}/posts?limit={}&access_token={}'.format(fanpage_id, page_num, token)
res = requests.get(url=index_url,headers=randHeader())
print(res)
print("单页抓取数量:",len(eval(res.text)["data"]))

#建立一个空的列表
posts = []
page = 1
while 'paging' in res.json():
    print('正在抓取第%d页...' % page)
 
    for post in res.json()['data']:
 
        #通过推文ID来爬取分享数和点赞数
        con_url = 'https://graph.facebook.com/v3.0/{}?fields=likes.summary(True),link,shares,comments.limit(0).summary(True)&access_token={}'.format(post['id'], token)
        # print(con_url)
        res2 = requests.get(url=con_url,headers=randHeader())
 
        #点赞数
        if 'likes' in res2.json():
            likes = res2.json()['likes']['summary'].get('total_count')
        else:
            likes = 0
 
        #分享数
        if 'shares' in res2.json():
            shares = res2.json()['shares'].get('count')
        else:
            shares = 0

        #评论数
        if 'comments' in res2.json():
            comments = res2.json()['comments']['summary'].get('total_count')
        else:
            comments = 0

        #文章URL   
        if 'link' in res2.json():
            article_url = res2.json().get('link')
        else:
            article_url = 0

        #文章内链接
        ArticleInnerURL = ""

        # print("点赞数:",likes)
        # print("分享数:",shares)

        #在列表中加入该条推文的信息
        posts.append([parse(post['created_time']), 
                      post['id'], 
                      post.get('message'), 
                      post.get('story'), 
                      likes, 
                      shares,
                      comments,
                      article_url,
                      ArticleInnerURL
                     ])
 
    #获取下一页
    if 'next' in res.json()['paging']:
        res = requests.get(res.json()['paging']['next'])
        page += 1
    else:
        break

    if page > 3: break


print('爬取结束!')


#保存为csv文件输出
df = pd.DataFrame(posts)
# df.columns = [
# 	'PostTime', 'PostID', 'PostContent',
# 	'ShareContent', 'LikesCounts', 'ShareCounts',
# 	'CommentCounts', 'ArticleURL', 'ArticleInnerURL'
# ]
df.columns = [
	'文章时间', '文章ID', '文章内容',
	'转发内容', '点赞数量', '分享数量',
	'评论数量', '文章链接', '文章内链'
]
df.to_csv('Molly\'s Game 主页点赞数和分享数.csv', index=False)

