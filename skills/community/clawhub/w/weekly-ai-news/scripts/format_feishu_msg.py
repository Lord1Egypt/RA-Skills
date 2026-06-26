#!/usr/bin/env python3
"""
发送周报消息到飞书
Usage: python send_feishu.py --news-json news.json --html-file weekly-ai-news.html
"""

import argparse
import json
import sys
import re
from datetime import datetime, timedelta

def strip_html(html):
    """去除 HTML 标签"""
    clean = re.sub(r'<[^>]+>', '', html)
    return clean[:200] + "..." if len(clean) > 200 else clean

def format_message(news_data, html_path):
    """格式化周报消息"""
    if not news_data:
        return "📰 **每周AI前沿动态**\n\n本周暂无符合条件的 AI 应用动态。"
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    date_range = f"{start_date.strftime('%Y.%m.%d')} - {end_date.strftime('%Y.%m.%d')}"
    
    lines = [
        f"📰 **每周AI前沿动态** ({date_range})",
        "",
        f"本期精选 **{len(news_data)}** 条 AI 应用向新闻：",
        "",
        "---",
        ""
    ]
    
    # 头条
    if len(news_data) > 0:
        headline = news_data[0]
        desc = strip_html(headline.get("description", ""))
        lines.extend([
            f"**【头条】{headline['title']}**",
            f"📍 来源：{headline['source']} | 📅 {headline['published'][:10]}",
            f"🔗 {headline['link']}",
            "",
            f"{desc}",
            "",
            "---",
            ""
        ])
    
    # 其他新闻
    for news in news_data[1:5]:  # 最多显示5条
        desc = strip_html(news.get("description", ""))
        lines.extend([
            f"**{news['title']}**",
            f"📍 {news['source']} | 📅 {news['published'][:10]}",
            f"🔗 {news['link']}",
            "",
            f"{desc}",
            "",
            "---",
            ""
        ])
    
    lines.extend([
        f"📎 **旧报纸风格 HTML 简报已生成**",
        f"文件路径：{html_path}",
        "",
        f"*本期筛选自 阮一峰的网络日志、36氪、虎嗅科技、钛媒体、IT之家*"
    ])
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='发送周报到飞书')
    parser.add_argument('--news-json', '-j', required=True, help='新闻 JSON 文件路径')
    parser.add_argument('--html-file', '-f', required=True, help='HTML 文件路径')
    args = parser.parse_args()
    
    # 读取新闻数据
    with open(args.news_json, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    # 生成消息
    message = format_message(news_data, args.html_file)
    
    # 输出消息（由调用方发送到飞书）
    print(message)

if __name__ == "__main__":
    main()
