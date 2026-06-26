#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金十数据浏览器搜索辅助脚本
"""

def get_jin10_search_url(theme: str) -> str:
    """获取金十数据搜索 URL"""
    return f"https://xnews.jin10.com/search?keyword={theme}"

NEWS_SOURCES = {
    "jin10": {"name": "金十数据", "search_url": "https://xnews.jin10.com/search?keyword={keyword}"},
    "eastmoney": {"name": "东方财富", "search_url": "https://so.eastmoney.com/news.aspx?q={keyword}"},
    "cls": {"name": "财联社", "search_url": "https://www.cls.cn/search?keyword={keyword}"}
}
