#!/usr/bin/env python3
"""
政治新聞抓取腳本
Political News Fetcher

使用方法：
    python3 fetch-news.py                    # 抓取默認來源
    python3 fetch-news.py --region tw        # 只看台灣
    python3 fetch-news.py --region cn        # 只看中國
    python3 fetch-news.py --region int       # 只看國際
    python3 fetch-news.py --limit 10         # 限制數量
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Optional

# 新聞來源配置
NEWS_SOURCES = {
    "tw": {
        "中央社": "https://www.cna.com.tw/list/aall.aspx",
        "自由時報": "https://news.ltn.com.tw/list/politics",
        "聯合報": "https://udn.com/news/media/breaknews/1",
        "ETtoday": "https://www.ettoday.net/news/politics.htm",
    },
    "cn": {
        "新華社": "http://www.xinhuanet.com/politics/",
        "人民網": "http://politics.people.com.cn/",
        "鳳凰網": "https://news.ifeng.com/politics/",
    },
    "int": {
        "BBC": "https://www.bbc.com/news/politics",
        "CNN": "https://www.cnn.com/politics",
        "Reuters": "https://www.reuters.com/politics-news/",
        "Al Jazeera": "https://www.aljazeera.com/tag/politics/",
    }
}

# 政治關鍵詞過濾
POLITICAL_KEYWORDS = [
    "總統", "總理", "首相", "主席", "書記", "議會", "國