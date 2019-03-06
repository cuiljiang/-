import requests
from lxml import etree
import csv

def spider_detail(url,head):
    response = requests.get(url, headers = head)
    html = etree.HTML(response.text)
    title_list = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/text()')
    time_list = html.xpath('/html/body/section/div[1]/div/article/p[1]/time/text()')
    contents_url = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/@href')
    contents = spider_detail_content(contents_url,head)
    save_content_to_csv(title_list,time_list,contents)

def spider_detail_content(contents_url,head):
    contents = []
    for content_url in contents_url:
        response = requests.get(content_url, headers = head)
        html = etree.HTML(response.text)
        content = html.xpath('string(//article[@class = "article-content"])').strip()
        contents.append(content)
    return contents

def save_content_to_csv(title_list,time_list,contents):
    for title,time,content in zip(title_list,time_list,contents):
        item = [title,time,content]
        items =  {'='*60}
        with open('daqianduan.csv','a',encoding= 'utf-8', newline ='' ) as csvfile:
            writer = csv.writer(csvfile)
            try:
                writer.writerow(item)
                writer.writerow(items)
            except Exception as e:
                print('保存错误：',e )
            #  显示正在爬取的内容
            print('正在下载：',title)


def spider_to_page(i):
    for n in range(1,i+1):
        url = 'http://www.daqianduan.com/page/{}'.format(n)
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}
        spider_detail(url,head)

# 执行需要爬取的页数
spider_to_page(1)
