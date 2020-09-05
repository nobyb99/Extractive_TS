from bs4 import BeautifulSoup
import requests
import urllib
from textsummarizer import compressor

txt = 'https://en.wikipedia.org/wiki/Mohanlal'


def spider(txt):
    url = txt
    response = requests.get(url)

    # resp = urllib.request.urlopen(url).read().encode('utf-8')
    soup = BeautifulSoup(response.content, 'lxml')

    tit = soup.find('h1').get_text()

    par = soup.find_all('p')
    lis = []
    for p in par[1:5]:
        lis.append(p.get_text().replace('\n', ''))
    return ' '.join(lis), tit
