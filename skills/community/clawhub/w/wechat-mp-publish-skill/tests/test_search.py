#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试免 API 的搜索方案
"""

import requests
from bs4 import BeautifulSoup
import json

def search_freebuf(keyword):
    """搜索 FreeBuf"""
    url = "https://www.freebuf.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # FreeBuf 首页文章列表
        for item in soup.select('.newslist li, .posts-list li')[:10]:
            title_el = item.select_one('h3 a, h2 a')
            if title_el:
                articles.append({
                    'title': title_el.text.strip(),
                    'url': title_el.get('href', ''),
                })
        
        return articles
    except Exception as e:
        print(f"搜索失败：{e}")
        return []

def search_anquanke(keyword):
    """搜索安全客"""
    url = "https://www.anquanke.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for item in soup.select('.article-item, .post-item')[:10]:
            title_el = item.select_one('a.title, h3 a')
            if title_el:
                articles.append({
                    'title': title_el.text.strip(),
                    'url': title_el.get('href', ''),
                })
        
        return articles
    except Exception as e:
        print(f"搜索失败：{e}")
        return []

# 测试
print("=" * 60)
print("测试免 API 搜索方案")
print("=" * 60)

print("\n1. 测试 FreeBuf...")
freebuf_results = search_freebuf("数据泄露")
print(f"找到 {len(freebuf_results)} 篇文章")
for i, article in enumerate(freebuf_results[:5], 1):
    print(f"  {i}. {article['title']}")

print("\n2. 测试安全客...")
anquanke_results = search_anquanke("网络安全")
print(f"找到 {len(anquanke_results)} 篇文章")
for i, article in enumerate(anquanke_results[:5], 1):
    print(f"  {i}. {article['title']}")

print("\n✅ 测试完成！")
