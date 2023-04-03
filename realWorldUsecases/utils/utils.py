import os
import urllib
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from pprint import pprint

url1 = "https://www.reuters.com/article/us-qualcomm-m-a-broadcom-5g/\
what-is-5g-and-who-are-the-major-players-idUSKCN1GR1IN"

def download_article(url):
    filename = url.split("/")[-1] + ".html"
    print(f"{filename=}")
    if not os.path.isfile(filename):
        r = requests.get(url)
        print(type(r))
        with open(filename, "w") as f:
            f.write(r.text)    
    
    
def parse_article(article_file):
    with open(article_file, "r") as f:
        html = f.read()
    r = {}
    soup = BeautifulSoup(html, "html.parser")
    r["id"] = soup.select_one("div.StandardArticle_inner-container")['id']
    r["url"] = soup.find("link" , {'rel': 'canonical'})['href']
    r["headline"] = soup.h1.text
    r["section"] = soup.select_one("div.ArticleHeader_channel a").text
    r['text'] = soup.select_one("div.StandardArticleBody_body").text
    r['authors'] = [a.text for a in soup.select("div.BylineBar_first-container.\
    ArticleHeader_byline-bar\
    div.BylineBar_byline span")]
    r['time'] = soup.find("meta", { 'property':
    "og:article:published_time"})['content']
    return r


download_article(url1)
parse_article("./what-is-5g-and-who-are-the-major-players-idUSKCN1GR1IN.html")