#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热点日报生成脚本
获取微博热搜并生成分段式分类日报
"""

import subprocess
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from collections import defaultdict


class WeiboHotParser(HTMLParser):
    """解析微博热搜页面"""

    def __init__(self):
        super().__init__()
        self.hot_items = []
        self.current_item = None
        self.in_list = False

    def handle_starttag(self, tag, attrs):
        if tag == 'ol':
            self.in_list = True
        elif tag == 'li' and self.in_list:
            self.current_item = {'rank': len(self.hot_items) + 1}
        elif tag == 'a' and self.current_item is not None:
            for attr in attrs:
                if attr[0] == 'href':
                    self.current_item['url'] = attr[1]

    def handle_data(self, data):
        if self.current_item is not None:
            data = data.strip()
            if data and 'title' not in self.current_item:
                if not data.startswith('<!--') and len(data) > 2:
                    self.current_item['title'] = data

    def handle_endtag(self, tag):
        if tag == 'li' and self.current_item:
            if 'title' in self.current_item:
                self.hot_items.append(self.current_item)
            self.current_item = None
        elif tag == 'ol':
            self.in_list = False


def fetch_weibo_hot(url: str = "https://weibo.g.renyuzhuo.cn/") -> list:
    """获取微博热搜数据"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-m', '15', url],
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:
            print(f"curl 错误: {result.stderr}")
            return []

        parser = WeiboHotParser()
        parser.feed(result.stdout)

        # 去重
        seen = set()
        unique_items = []
        for item in parser.hot_items:
            if item['title'] not in seen:
                seen.add(item['title'])
                unique_items.append(item)

        return unique_items[:50]

    except Exception as e:
        print(f"获取微博热搜失败: {e}")
        return []


def categorize_hot(title: str) -> str:
    """分类热点"""
    # 财经科技
    finance_keywords = [
        'A股', '股市', '指数', '股票', '经济', '公司', '企业', '科技',
        'AI', '互联网', '芯片', '新能源', '汽车', '股价', '涨停', '跌停',
        '小米', '华为', '苹果', '特斯拉', '茅台', '比特币', '基金',
        '月薪', '薪资', '裁员', '招聘', '就业', '房价'
    ]
    for kw in finance_keywords:
        if kw in title:
            return '财经科技'

    # 社会民生
    society_keywords = [
        '警方', '事故', '安全', '死亡', '受伤', '法院', '判决',
        '医院', '教育', '学校', '老师', '学生', '家长', '孩子',
        '幼儿园', '高中', '大学', '博士', '诈骗', '盗窃', '犯罪',
        '火灾', '地震', '暴雨', '台风', '灾害', '救援'
    ]
    for kw in society_keywords:
        if kw in title:
            return '社会民生'

    # 文体娱乐
    entertainment_keywords = [
        '电影', '电视剧', '综艺', '明星', '演员', '歌手', '导演',
        '国足', '足球', '篮球', 'NBA', '比赛', '冠军', '演唱会',
        '专辑', '歌曲', 'MV', '票房', '定档', '官宣', '恋情',
        '结婚', '离婚', '绯闻', '塌房', 'cp', '粉丝'
    ]
    for kw in entertainment_keywords:
        if kw in title:
            return '文体娱乐'

    return '网络热点'


def generate_daily_report(items: list, date: str = None) -> str:
    """生成分段式分类日报"""
    if not items:
        return "今日暂无热点数据"

    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    # 按分类整理
    categories = defaultdict(list)
    for item in items:
        category = categorize_hot(item['title'])
        categories[category].append(item['title'])

    # 生成日报
    lines = [f"【微博热点日报 | {date}】", ""]

    category_order = ['财经科技', '社会民生', '文体娱乐', '网络热点']
    category_emoji = {
        '财经科技': '📊',
        '社会民生': '📰',
        '文体娱乐': '🎬',
        '网络热点': '🔥'
    }

    for category in category_order:
        if category in categories and categories[category]:
            lines.append(f"{category_emoji[category]} {category}")
            for title in categories[category][:5]:  # 每类最多5条
                lines.append(f"- {title}")
            lines.append("")

    lines.append("---")
    lines.append("by OpenClaw")

    return "\n".join(lines)


def main():
    """主函数"""
    print("正在获取微博热搜...")
    items = fetch_weibo_hot()

    if not items:
        print("获取失败，请检查网络连接")
        return

    print(f"获取到 {len(items)} 条热搜\n")

    # 生成日报
    report = generate_daily_report(items)
    print(report)

    return report


if __name__ == '__main__':
    main()
