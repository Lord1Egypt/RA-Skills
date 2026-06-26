#!/usr/bin/env python3
"""
search_article.py - 搜狗微信搜索追踪文章
Usage: python search_article.py "文章标题"
"""

import sys
import urllib.request
import urllib.parse
import re

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def search_article_sogou(title: str) -> dict:
    """搜狗微信搜索文章，返回匹配信息"""
    try:
        query = urllib.parse.quote(title)
        url = f"https://weixin.sogou.com/weixin?type=2&query={query}&ie=utf8"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        results = []

        # 提取文章标题和链接
        title_pattern = re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL)
        link_pattern = re.compile(r'href="(https://mp\.weixin\.qq\.com/s/[^"]+)"')

        titles = title_pattern.findall(html)
        links = link_pattern.findall(html)

        for t, l in zip(titles[:10], links[:10]):
            # 清理 HTML 标签
            clean_title = re.sub(r'<[^>]+>', '', t).strip()
            results.append({"title": clean_title, "link": l})

        return {"found": len(results) > 0, "results": results, "html": html[:500]}

    except Exception as e:
        return {"found": False, "error": str(e), "results": []}


def main():
    if len(sys.argv) < 2:
        print("Usage: python search_article.py \"文章标题\"")
        sys.exit(1)

    title = " ".join(sys.argv[1:])
    print(f"{YELLOW}搜索文章：{title}{NC}\n")

    result = search_article_sogou(title)

    if result.get("error"):
        print(f"{RED}搜索失败：{result['error']}{NC}")
        sys.exit(1)

    if result["found"]:
        print(f"{GREEN}找到 {len(result['results'])} 条结果：{NC}")
        for i, r in enumerate(result["results"], 1):
            print(f"  {i}. {r['title']}")
            print(f"     {r['link']}")
            print()
    else:
        print(f"{YELLOW}未找到结果（可能尚未被搜索引擎收录）{NC}")


if __name__ == "__main__":
    main()
