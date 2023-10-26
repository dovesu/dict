#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
词典 for goldendict
author: 'oldoldstone'
Created on 2020-9-30 12:04:00
USAGE:
python3 bingdict.py  <text to be translated>
python3 bingdict.py 'hello world!'
"""

import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import quote
import string
HTML_TMPL = """
<title>词典</title>
   <img src="http://tu.dddd.ooo/i/s/202310/bjfsj.png" alt="voice" onclick="playMusic()" style="cursor: pointer;">
<script>
function playMusic() {
var music = document.getElementById("music");
music.play();
}
</script>
<link href="//ps.dddd.ooo/phone/Style.css" rel="stylesheet" type="text/css" /> 
<hr/>
{{content}}
"""


def parse(gwords):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                             Chrome/42.0.2311.90 Safari/537.36"
               }
    # urlstr = 'https://cn.bing.com/dict/search?q=' + keyword
    urlstr = 'https://cn.bing.com/dict/clientsearch?mkt=zh-CN&setLang=zh&form=BDVEHC&ClientVer=BDDTV3.5.1.4320&q='
    url = quote(urlstr, safe=string.printable) + gwords
    try:
        r = requests.post(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Connection Error !')
        exit()
    except Exception as e:
        print(e)
        exit()
    return BeautifulSoup(r.text, 'html.parser')  # transfer to html files easy to analyse


if __name__ == '__main__':
    keyword = ' '.join(sys.argv[1:])
    soup = parse(keyword)
    content = u""
    nextNode = soup.find('span', id='anchor0')
    if nextNode is None:
        output = soup.prettify()
    else:
        while True:
            nextNode = nextNode.nextSibling
            if nextNode.attrs == {'id': 'anchor1'} or nextNode.attrs == {'class': ['client_def_image_bar']}:
                break
            content = content + nextNode.prettify()
        output = HTML_TMPL.replace('{{content}}', content)
    resaudio="<br><br><h2><form><a class=‘page-navi’><audio id='music' src='https://dict.youdao.com/dictvoice?audio=" + keyword + "&type=2'></audio>"

    print(resaudio+output+"</a></form></h2>")
