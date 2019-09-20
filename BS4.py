# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 19:17:39 2019

@author: J10c

BeautifulSoup

"""


import requests
import json
from bs4 import BeautifulSoup  # BS
 
 
def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
 
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
        
        
def write_to_file(content, flag):
    with open('豆瓣电影TOP250(' + str(flag) + ').txt', 'a', encoding='utf-8')as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
 
 
def search(Num):
    url = 'https://movie.douban.com/top250?start=' + str(Num)
    html = get_one_page(url)
    for item in soup_parse(html):
        write_to_file(item, 'BS4')
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
