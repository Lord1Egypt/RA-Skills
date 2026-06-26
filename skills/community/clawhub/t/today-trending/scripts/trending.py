#!/usr/bin/env python3
import sys
import json
import requests
from lxml import etree
import urllib.parse


class HotSearch:
    def __init__(self):
        self.headers = {
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
    
    def weibo_hotsearch(self):
        """微博热搜榜"""
        headers = {
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://weibo.com/hot/search',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        url = 'https://weibo.com/ajax/side/hotSearch'
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data_json = r.json()
            words = []
            for i in data_json["data"]["realtime"][:20]:
                word = i["word"]
                words.append(word)
            return words
        except Exception as e:
            print(f"微博error：{e}")
            return None

    def douyin_hotsearch(self):
        """抖音热搜"""
        url = 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/'
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            data_json = r.json()
            words = []
            for i in data_json["word_list"][:20]:
                word = i["word"]
                words.append(word)
            return words
        except Exception as e:
            print(f"抖音error：{e}")
            return None

    def baidu_hotsearch(self):
        """百度热搜"""
        url = 'https://top.baidu.com/board?tab=realtime'
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            html = etree.HTML(r.text)
            words = []
            for i in html.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div[*]')[:20]:
                word = i.xpath('string(div[2]/a/div[1])').strip()
                if word:
                    words.append(word)
            return words
        except Exception as e:
            print(f"百度error：{e}")
            return None


def format_weibo_url(word):
    """生成微博搜索链接"""
    encoded = urllib.parse.quote(word, safe='')
    return f"https://s.weibo.com/weibo?q={encoded}"


def format_douyin_url(word):
    """生成抖音搜索链接"""
    encoded = urllib.parse.quote(word, safe='')
    return f"https://www.douyin.com/search?keyword={encoded}"


def format_baidu_url(word):
    """生成百度搜索链接"""
    encoded = urllib.parse.quote(word, safe='')
    return f"https://www.baidu.com/s?wd={encoded}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trending.py <JSON>")
        sys.exit(1)
    
    query = sys.argv[1]
    parse_data = {}
    try:
        parse_data = json.loads(query)
        print(f"success parse request body: {parse_data}")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)
    
    if "platform" not in parse_data:
        print("Error: platform must be present in request body.")
        sys.exit(1)
    
    platform = parse_data["platform"]
    hs = HotSearch()
    
    result = {}
    
    if platform in ["weibo", "all"]:
        result["weibo"] = hs.weibo_hotsearch() or []
    
    if platform in ["douyin", "all"]:
        result["douyin"] = hs.douyin_hotsearch() or []
    
    if platform in ["baidu", "all"]:
        result["baidu"] = hs.baidu_hotsearch() or []
    
    print(json.dumps(result, indent=2, ensure_ascii=False))