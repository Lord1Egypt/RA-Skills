
#!/usr/bin/env python3
"""
搜索微信公众号文章
用法: python search.py "关键词" [数量]
"""

import sys
import os

# 添加脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from wechat_articles import search_articles, print_article_summary


def main():
    if len(sys.argv) < 2:
        print("用法: python search.py \"关键词\" [数量]")
        print("示例: python search.py \"绿电直连政策\" 10")
        sys.exit(1)
    
    query = sys.argv[1]
    top_num = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"正在搜索: {query}")
    print("=" * 60)
    
    articles = search_articles(query, top_num)
    
    if not articles:
        print("未找到相关文章")
        return
    
    print(f"找到 {len(articles)} 篇文章:\n")
    
    for i, article in enumerate(articles, 1):
        print(f"【{i}】")
        print_article_summary(article)


if __name__ == "__main__":
    main()
