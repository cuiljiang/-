import requests
from lxml import etree
import csv

#定义需要爬取每一篇文章需要爬取的信息
def spider(url,head):
    response = requests.get(url, headers = head)
    html = etree.HTML(response.text)
    title_list = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/text()')
    time_list = html.xpath('/html/body/section/div[1]/div/article/p[1]/time/text()')
    contents_url = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/@href')
    contents = content_(contents_url,head)
    save_(title_list,time_list,contents)

# 标题内容的爬取
def content_(contents_url,head):
    for content_url in contents_url:
        response = requests.get(content_url, headers = head)
        html = etree.HTML(response.text)
        print(html.xpath('string(//article[@class = "article-content"])'))
    return html.xpath('string(//article[@class = "article-content"])')

#  保存函数，保存爬取的数据
def save_(title_list,time_list,contents):
    for title,time in zip(title_list,time_list):
        item = [title,time,contents]
        with open('daqianduan.csv','a',encoding= 'utf-8', newline ='' ) as csvfile:
            writer = csv.writer(csvfile)
            try:
                # 注意，writerow（）方法只能给定一个参数，故不能直接用（title,time)
                writer.writerow(item)
            except Exception as e:
                print('保存错误：',e )
            #  显示正在爬取的内容
            print('正在下载：',title)

# 设定爬取的页码数据范围
def spider_page(i):
    for n in range(1,i+1):
        url = 'http://www.daqianduan.com/page/{}'.format(n)
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}
        spider(url,head)

# 执行需要爬取的页数
spider_page(3)
