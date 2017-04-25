#coding=utf-8

# Script Name:      nowcoder_spider.py
# Author:           lszero
# Created:          April 25, 2017
# Last Modified:    April 25, 2017
# Version:          1.0
# Description:      crawl 'www.nowcoder.com/discuss'.

import sys
import time
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

html_head = '''
<html>
<head>
  <title>nowcoder</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style type="text/css">
    a:link{text-decoration: none; color:#333; font-size: 16px; font-family: 微软雅黑;}
    a:visited{ color:#B5B5B5;}
    a:hover{text-decoration: underline; color:#40E0D0; font-size: 16px;}
    </style>
</head>\n\n<body>\n<table border="1" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">\n
'''

def main():
    t1 = time.time()
    home_url = "https://www.nowcoder.com"
    main_url = "https://www.nowcoder.com/discuss?type=2&order=3"
    output = open("nowcoder.html", "w")

    output.write(html_head)

    page_id = 0
    post_id = 0
    while True:
        page_id = page_id + 1
        url = main_url + "&page=" + str(page_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        post_list = soup.find("ul", class_ = "common-list")
        if post_list == None or len(post_list) == 0:
            break

        for item in post_list.find_all("li"):
            post_id = post_id + 1
            item = item.div.div
            
            title = item.a.text
            link = item.a["href"]
            link = home_url + link[:link.index('?')]
            # print title, link

            item = item.next_sibling.next_sibling
            time_str = item.div.a.next_sibling.string
            if len(time_str) != 20:
                time_str = time.strftime("%Y-%m-%d", time.localtime())
            else:
                time_str = time_str[3:13]
            # print time 
            
            output.write("<tr>\n  <td width=\"50\" align=\"center\">" + str(post_id) + "</td>\n  <td width=\"110\" align=\"center\">" + time_str + "</td>\n  <td style=\"padding: 0px 10px 0px 20px;\"><a href=\"" + link + "\" target=\"_blank\" >" + title + "</a></td>\n</tr>\n")


    output.write("</table>\n</body>\n</html>\n")
    output.close()

    t2 = time.time()
    print "Execution time: %.3f s." % (t2 - t1)

if __name__ == '__main__':
    main()

