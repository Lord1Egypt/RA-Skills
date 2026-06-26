#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取财经新闻（使用Web API）
用法: python get_news.py [国内|国际|all]
"""

import sys
import subprocess
import re
from datetime import datetime

def get_finance_news():
    """获取新浪财经要闻"""
    try:
        result = subprocess.run(
            ["curl", "-s", "https://finance.sina.com.cn/stock/"],
            capture_output=True,
            timeout=15
        )
        
        html = result.stdout.decode('utf-8', errors='ignore')
        # 提取新闻标题
        titles = re.findall(r'>([^<]{15,60})<', html)
        # 过滤有效标题
        valid_titles = []
        for t in titles:
            t = t.strip()
            if len(t) > 10 and len(t) < 80 and not t.startswith(('function', 'var', 'if', 'return')):
                valid_titles.append(t)
        return list(set(valid_titles))[:8]
    except Exception as e:
        return [f"获取失败: {e}"]

def main():
    news_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    print(f"\n{'='*60}")
    print(f"📰 财经要闻 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"{'='*60}")
    print("\n来源: 新浪财经")
    print()
    
    news = get_finance_news()
    for i, item in enumerate(news[:10], 1):
        print(f"{i}. {item}")
    
    print("\n💡 提示: 可使用 Tavily 搜索技能获取更全面的新闻")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
