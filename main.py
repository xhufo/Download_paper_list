# -*- coding:utf-8 -*-
# 下载石油地球物理勘探期刊文章目录
# 1.网站解析
# 给网址-保存html-html解析，找到年、期刊期数、名字，生成目录
#   1.1 解析主页，找到年目录，生成字典[年-链接]，保存文件
#   1.2 解析年目录链接，找到期数，生成[年-期数-链接]，保存文件
#   1.3 解析期数链接，找到每一期的网页，解析出[年-期数-题目-摘要链接-pdf下载链接]，保存文件
#   1.4 解析摘要链接，返回摘要内容，第一作者名字，生成[年-期数-作者-题目-摘要内容-pdf下载链接]，保存文件
# 2.内容保存
# 3.内容分析，生成杂志目录列表
# 4.保存文本文件
# Author : Hao Xue
# Email  : xhufoxc@gmail.com

import os
from urllib.request import urlopen
from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
import re
import json


# response = requests.get('http://www.baidu.com')
# print(response.status_code)  # 打印状态码
# print(response.url)          # 打印请求url
# print(response.headers)      # 打印头信息
# print(response.cookies)      # 打印cookie信息
# print(response.text)  #以文本形式打印网页源码
# print(response.content) #以字节流形式打印

def checkDir(dir, filename):
    if not os.path.exists(dir):
        os.makedirs(dir)
    fullpath = os.path.join(dir, filename)
    return fullpath

def downLoadHtml(filename, url):
    # 伪造cookies
    hea = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    html = requests.get(url)
    # html=requests.get('http://library.seg.org/doi/pdf/10.1190/segam2016-13957987.1', proxies=proxies)
    # html = requests.get(
    #    'http://library.seg.org/doi/book/10.1190/segeab.35?ct=098151bb0cab683119c67758b3af4ade28bceffeca51199893262f7165646cc97c796d1fed0dacb8282c24a9d844ca799781c3448b014422bc6f56c6cf6e006e',
       # proxies=proxies)

    html.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
    # print(html.headers['content-type'])
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html.text)

def findPaperYear(filename):
    soup = bs(open((filename),"r"))

    print(soup.prettify())  # 可以美化这段html并打印出来
def downLoadPdf():
    return 0

# step 1:
def get_year_list_in_shiyoudiqiuwulikantan(filename,url):
    html = open(filename, 'r', encoding='utf-8')
    soup = bs(html, 'html.parser', from_encoding='utf-8')
    # nameList = soup.findAll("table", height="30", width="100%")
    # nameList = soup.findAll("a", href=re.compile("nian"))
    soup.findAll("a")
    yearLinkListStr = soup.findAll(href=re.compile("nian"))
    # yearLinkList = re.findall('<a href="(.*?)">', str(yearLinkListStr), re.S)
    yearLinkList = re.findall('<a href="(.*?)">', str(yearLinkListStr), re.S)
    year = re.findall('<b>(.*?)<\/b>', str(yearLinkListStr), re.S)
    # print(yearLinkList)
    urlnew = []
    for link in yearLinkList:
        urlnew.append(url+link)
    # print(urlnew)
    dict_new = {}
    for i in range(len(year)):
        dict_new.update({year[i]: urlnew[i]})
    # print(dict)
    return dict_new

# step 2:
def get_volume_list_inOneYear_in_shiyoudiqiuwulikantan(filename,url):
    html = open(filename, 'r', encoding='utf-8')
    soup = bs(html, 'html.parser', from_encoding='utf-8')
    volume1 = soup.findAll("table", height="30", width="100%", border="0", cellpadding="5", cellspacing="1")
    volume2 = volume1[1]
    volume3 = volume2.findAll('a')
    dict_new = {}

    print('volume3')
    num = 1
    for k in volume3:
        urlnew = parse.urljoin(url, k['href'])
        # print(urlnew)
        t1 = k.get_text()
        t2 = t1.replace('\t', '')
        t3 = t2.replace('\n',  '')
        volnamenew = t3.replace('\u00a0', ' ')

        dict_new.update({num: [urlnew, volnamenew]})
        num += 1
    return dict_new

# step 3:
def get_paper_list_inOneYearVolume_in_shiyoudiqiuwulikantan(filename,url):
    html = open(filename, 'r', encoding='utf-8')
    soup = bs(html, 'html.parser', from_encoding='utf-8')
    soup.findAll('td', align='center')
    t1 = soup.findAll('form')
    t2 = t1[1]
    # t3 = t2.table
    t3 = t2.findAll('table', {'class': 'td42'})
    title = re.findall('<strong>(.*?)</strong>', str(t3), re.S)
    link1 = t2.findAll('a')
    link_abst1 = t2.findAll('a', target='_blank')
    link_pdf1 = t2.findAll('a', text='PDF')

    link_abst = []
    link_pdf = []
    for k in range(len(link_abst1)):
        link_abst.append(parse.urljoin(url, link_abst1[k]['href']))
        link_pdf.append(parse.urljoin(url, link_pdf1[k]['href']))
    # print(link1)
    # link = []
    # for k in range(len(link1)):
    #     link.append(k)
    # link = link1['href']
    author = re.findall('</strong><br/>(.*?)<br/>', str(t3), re.S)
    for k in range(len(author)):
        tmp = author[k].replace('\n', '')
        tmp1 = tmp.split(',')
        author[k] = tmp1[0]

    dict_new = {}
    abstract = []
    num = 1
    for k in range(len(title)):
        dict.update({num: [title[k], author[k], link_abst[k], link_pdf[k]]})
        tmp = abstract_obtain(link_abst[k])
        abstract.append(tmp)
        dict_new[num] = [title[k], author[k], link_abst[k], link_pdf[k], abstract[k]]
        num += 1
        if k == 1:
            print(dict_new)

    return dict_new

# sub function
def abstract_obtain(url):
    html = requests.get(url)
    html.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
    # print(html.headers['content-type'])
    text = html.text
    tmp = re.findall(' <b>摘要</b>(.*?)</td>', str(text), re.S)
    tmp = ''.join(tmp)
    print(type(tmp))
    print(tmp)
    abstract = tmp
    abstract = abstract.replace('&nbsp;', '')
    abstract = abstract.replace('\t', '')
    abstract = abstract.replace('\r', '')
    abstract = abstract.replace('\n', '')
    abstract = abstract.replace('<sup>', '').replace('</sup>', '')
    abstract = abstract.replace('<i>', '').replace('</i>', '')
    abstract = abstract.replace('<sub>', '').replace('</sub>', '')
    return abstract

def main():
    url = 'http://www.ogp-cn.com.cn/CN/article/showTenYearOldVolumn.do'
    url1 = 'http://www.ogp-cn.com.cn/CN/article/'
    # dir path & file path
    path = "F:\python_project\Download_paper_list\\test"
    filename = checkDir(path, 'mainpage.html')
    print(filename)
    downLoadHtml(filename, url)
    # html = urlopen(url)
    year_link = get_year_list_in_shiyoudiqiuwulikantan(filename, url1)
    # print(year_link)
    filename_json = filename.replace('.html', '.json')
    if not os.path.exists(filename):
        with open(filename_json, 'w', encoding='utf-8') as f:
            str1 = json.dumps(year_link, indent=4)
            f.writelines(str1)
    # loop year
    for year in year_link:
        # print(year)
        if year == '2017':
            path1 = os.path.join(path, year)
            filename = checkDir(path1, year+'.html')
            downLoadHtml(filename, year_link[year])
            url = year_link[year]
            volume_link = get_volume_list_inOneYear_in_shiyoudiqiuwulikantan(filename, url)
            filename_json = filename.replace('.html', '.json')
            if not os.path.exists(filename):
                with open(filename_json, 'w', encoding='utf-8') as f:
                    str1 = json.dumps(volume_link, indent=4, ensure_ascii=False)
                    f.writelines(str1)
            # loop volume
            for volume in volume_link:
                print(volume)
                if str(volume) == '1':
                    path2 = os.path.join(path1, str(volume_link[volume][1]))
                    filename = checkDir(path1, year + '-' + str(volume)+'.html')
                    downLoadHtml(filename, volume_link[volume][0])
                    paperDict = get_paper_list_inOneYearVolume_in_shiyoudiqiuwulikantan(filename, url)
                    filename_json = filename.replace('.html', '.json')
                    if not os.path.exists(filename):
                        with open(filename_json, 'w', encoding='utf-8') as f:
                            # f.write(str(t3))
                            # f.write(str(title))
                            # f.write(str(author))
                            str1 = json.dumps(paperDict, indent=4, ensure_ascii=False)
                            f.writelines(str1)


if __name__ == '__main__':
    main()
