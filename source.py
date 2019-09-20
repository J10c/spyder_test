# from https://www.cnblogs.com/shuimohei/p/11345458.html
# 目标：爬取豆瓣电影排行榜TOP250的电影信息
# 信息包括：电影名字，上映时间，主演，评分，导演，一句话评价
# 解析用学过的几种方法都实验一下①正则表达式:
#Beautiful
#Soup
#xpath
import requests
import re  # 正则表达式
import json
from bs4 import BeautifulSoup  # BS
from lxml import etree  # xpath
 
 
def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
 
 
def zhengze_parse(html):
    pattern = re.compile(
        '<em class="">(.*?)</em>.*?<img.*?alt="(.*?)".*?src="(.*?)".*?property="v:average">(.*?)</span>.*?<span>(.*?)</span>.*?'
        + 'class="inq">(.*?)</span>',
        re.S)
    items = re.findall(pattern, html)
    # 因为125个影片没有描述，根本没有匹配到- -，更改也简单，描述单独拿出来，这里我就不改了
    for item in items:
        yield {
            'index': item[0],
            'image': item[2],
            'title': item[1],
            'people': item[4].strip()[:-2],
            'score': item[3],
            'Evaluation': item[5]
        }
 
 
def soup_parse(html):
    soup = BeautifulSoup(html, 'lxml')
    for data in soup.find_all('div', class_='item'):
        index = data.em.text
        image = data.img['src']
        title = data.img['alt']
        people = data.find_all('span')[-2].text[:-2]
        score = data.find('span', class_='rating_num').text
        # 第125个影片没有描述，用空代替
        if data.find('span', class_='inq'):
            Evaluation = data.find('span', class_='inq').text
        else:
            Evaluation = ''
        yield {
            'index': index,
            'image': image,
            'title': title,
            'people': people,
            'score': score,
            'Evaluation': Evaluation,
        }
 
 
def xpath_parse(html):
    html = etree.HTML(html)
    for data in html.xpath('//ol[@class="grid_view"]/li'):
        index = data.xpath('.//em/text()')[0]
        image = data.xpath('.//a/img/@src')[0]
        title = data.xpath('.//a/img/@alt')[0]
        people = data.xpath('.//div[@class="star"]/span[4]/text()')[0][:-2]
        score = data.xpath('.//div[@class="star"]/span[2]/text()')[0]
        # 第125个影片没有描述，用空代替
        if data.xpath('.//p[@class="quote"]/span/text()'):
            Evaluation = data.xpath('.//p[@class="quote"]/span/text()')[0]
        else:
            Evaluation = ''
        yield {
            'index': index,
            'image': image,
            'title': title,
            'people': people,
            'score': score,
            'Evaluation': Evaluation,
        }
 
 
def write_to_file(content, flag):
    with open('豆瓣电影TOP250(' + str(flag) + ').txt', 'a', encoding='utf-8')as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
 
 
def search(Num):
    url = 'https://movie.douban.com/top250?start=' + str(Num)
    html = get_one_page(url)
    for item in zhengze_parse(html):
        write_to_file(item, '正则表达式')
    for item in soup_parse(html):
        write_to_file(item, 'BS4')
    for item in xpath_parse(html):
        write_to_file(item, 'xpath')
    page = str(Num / 25 + 1)
    print("正在爬取第" + page[:-2] + '页')
 
 
def main():
    # 提供页码
    for i in range(0, 10):
        Num = i * 25
        search(Num)
    print("爬取完成")
 
 
if __name__ == '__main__':
    # 入口
    main()
