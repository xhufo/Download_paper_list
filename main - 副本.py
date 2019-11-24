
# dir path & file path
beginpath = "F:\python_project\Download_paper_list"
foldername="test"
fullpath = os.path.join(beginpath, foldername)
print(fullpath)
if not os.path.exists(fullpath):
            os.makedirs(fullpath)

filename = os.path.join(fullpath, "html_info.txt")
filename2 = os.path.join(fullpath, "pdf_info_list.txt")
filename3 = os.path.join(fullpath, "fname.txt")
filename4 = os.path.join(fullpath, "download_url.txt")
print(filename)

def downLoadHtml():
    # 伪造cookies
    hea = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
     html=requests.get('http://library.seg.org/doi/pdf/10.1190/segam2016-13957987.1')
    # html=requests.get('http://library.seg.org/doi/pdf/10.1190/segam2016-13957987.1', proxies=proxies)
   # html = requests.get(
        'http://library.seg.org/doi/book/10.1190/segeab.35?ct=098151bb0cab683119c67758b3af4ade28bceffeca51199893262f7165646cc97c796d1fed0dacb8282c24a9d844ca799781c3448b014422bc6f56c6cf6e006e',
       # proxies=proxies)

    html.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
    print(html.headers['content-type'])

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html.text)
def downLoadPdf():
    return(0)
