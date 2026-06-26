#!/usr/bin/env python3
"""
fetch_zhihu.py — 抓取知乎热榜并标记 IT/科技相关话题

用法：
    python fetch_zhihu.py [--top N]

输出：
    JSON 格式的热榜列表，含 title, heat, url, is_tech 字段
"""

import json
import time
import random
import argparse
import urllib.request
import urllib.error

# IT/科技相关关键词，用于自动标记推荐话题
TECH_KEYWORDS = [
    "AI", "人工智能", "大模型", "LLM", "GPT", "ChatGPT", "Claude", "Gemini",
    "芯片", "半导体", "GPU", "英伟达", "AMD", "Intel", "高通",
    "苹果", "谷歌", "微软", "Meta", "字节", "腾讯", "阿里", "百度", "华为",
    "手机", "iPhone", "Android", "鸿蒙",
    "编程", "代码", "开源", "GitHub", "程序员", "软件", "算法",
    "互联网", "科技", "数据", "云计算", "量子", "机器人", "自动驾驶",
    "特斯拉", "马斯克", "OpenAI", "Anthropic",
    "5G", "6G", "卫星", "火箭", "SpaceX",
    "区块链", "Web3", "加密货币", "比特币",
    "网络安全", "黑客", "漏洞",
    "电商", "外卖", "滴滴", "美团", "拼多多",
]

ZHIHU_HOT_API = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.zhihu.com/hot",
    "x-requested-with": "fetch",
}


def fetch_hot_list(top_n: int = 20) -> list[dict]:
    """抓取知乎热榜，返回结构化数据列表"""
    req = urllib.request.Request(ZHIHU_HOT_API, headers=HEADERS)

    # 随机延迟，避免触发反爬
    time.sleep(random.uniform(0.5, 1.5))

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 知乎可能返回 400/403，尝试备用方式
        raise RuntimeError(f"知乎 API 请求失败: HTTP {e.code}. "
                           f"请尝试在浏览器登录知乎后复制 Cookie 配置。") from e
    except Exception as e:
        raise RuntimeError(f"网络请求异常: {e}") from e

    results = []
    for item in raw.get("data", [])[:top_n]:
        target = item.get("target", {})
        title = target.get("title", "")
        # 热度文字，如 "2341 万热度"
        heat_text = item.get("detail_text", "")
        # 话题 URL
        url = f"https://www.zhihu.com/question/{target.get('id', '')}"

        # 自动标记 IT/科技话题
        is_tech = any(kw in title for kw in TECH_KEYWORDS)

        results.append({
            "title": title,
            "heat": heat_text,
            "url": url,
            "excerpt": target.get("excerpt", ""),
            "is_tech": is_tech,
        })

    return results


def display_hot_list(items: list[dict]) -> str:
    """格式化展示热榜，返回可打印字符串"""
    lines = [
        "📊 今日知乎热榜（⭐ = IT/科技推荐）",
        "━" * 45,
    ]
    for i, item in enumerate(items, 1):
        star = "⭐" if item["is_tech"] else "  "
        lines.append(f"{star} {i:2d}. {item['title']}")
        lines.append(f"        热度: {item['heat']}")
    lines.append("━" * 45)
    lines.append("请告诉我你想写哪几条（如：1,3 或直接描述话题）")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="抓取知乎热榜")
    parser.add_argument("--top", type=int, default=20, help="获取前N条，默认20")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")
    args = parser.parse_args()

    items = fetch_hot_list(args.top)

    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        print(display_hot_list(items))


if __name__ == "__main__":
    main()
