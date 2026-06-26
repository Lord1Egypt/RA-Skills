#!/usr/bin/env python3
"""
多平台热榜数据抓取脚本
用法：
  python3 fetch-hotlist.py weibo       # 抓取微博热搜
  python3 fetch-hotlist.py douyin      # 抓取抖音热榜（需要 Cookie）
  python3 fetch-hotlist.py zhihu       # 抓取知乎热榜
  python3 fetch-hotlist.py baidu       # 抓取百度热搜
  python3 fetch-hotlist.py bilibili    # 抓取B站热门
  python3 fetch-hotlist.py all         # 抓取所有平台（并行）
"""

import sys
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 可选：在此填入 Cookie（抖音、小红书需要）
COOKIES = {
    "douyin": "",   # 填入抖音 Cookie
    "xiaohongshu": "",  # 填入小红书 Cookie
}


def fetch_url(url, extra_headers=None):
    req = urllib.request.Request(url, headers={**HEADERS, **(extra_headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def fetch_weibo():
    """微博实时热搜（无需 Cookie）"""
    data = fetch_url("https://weibo.com/ajax/side/hotSearch")
    if "error" in data:
        return {"platform": "微博热搜", "error": data["error"], "items": []}
    items = []
    for i, item in enumerate(data.get("data", {}).get("realtime", [])[:20], 1):
        items.append({
            "rank": i,
            "title": item.get("word", ""),
            "hot": item.get("num", 0),
            "label": item.get("label_name", ""),
        })
    return {"platform": "微博热搜", "items": items, "fetched_at": datetime.now().isoformat()}


def fetch_zhihu():
    """知乎热榜（无需 Cookie）"""
    data = fetch_url(
        "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20",
        extra_headers={"Referer": "https://www.zhihu.com/"}
    )
    if "error" in data:
        return {"platform": "知乎热榜", "error": data["error"], "items": []}
    items = []
    for i, item in enumerate(data.get("data", [])[:20], 1):
        target = item.get("target", {})
        items.append({
            "rank": i,
            "title": target.get("title", ""),
            "hot": item.get("detail_text", ""),
            "url": f"https://www.zhihu.com/question/{target.get('id', '')}",
        })
    return {"platform": "知乎热榜", "items": items, "fetched_at": datetime.now().isoformat()}


def fetch_baidu():
    """百度实时热点（无需 Cookie）"""
    data = fetch_url("https://top.baidu.com/api/board?platform=wise&tab=realtime")
    if "error" in data:
        return {"platform": "百度热搜", "error": data["error"], "items": []}
    items = []
    cards = data.get("data", {}).get("cards", [])
    content = cards[0].get("content", []) if cards else []
    for i, item in enumerate(content[:20], 1):
        items.append({
            "rank": i,
            "title": item.get("word", ""),
            "hot": item.get("hotScore", 0),
        })
    return {"platform": "百度热搜", "items": items, "fetched_at": datetime.now().isoformat()}


def fetch_bilibili():
    """B站热门视频（无需 Cookie）"""
    data = fetch_url("https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1")
    if "error" in data:
        return {"platform": "B站热门", "error": data["error"], "items": []}
    items = []
    for i, item in enumerate(data.get("data", {}).get("list", [])[:20], 1):
        stat = item.get("stat", {})
        items.append({
            "rank": i,
            "title": item.get("title", ""),
            "author": item.get("owner", {}).get("name", ""),
            "views": stat.get("view", 0),
            "likes": stat.get("like", 0),
            "url": f"https://www.bilibili.com/video/{item.get('bvid', '')}",
        })
    return {"platform": "B站热门", "items": items, "fetched_at": datetime.now().isoformat()}


def fetch_douyin():
    """抖音热榜（需要 Cookie）"""
    cookie = COOKIES.get("douyin", "")
    if not cookie:
        return {"platform": "抖音热榜", "error": "未配置 Cookie，请在脚本顶部 COOKIES['douyin'] 填入抖音 Cookie", "items": []}
    data = fetch_url(
        "https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383",
        extra_headers={"Cookie": cookie, "Referer": "https://www.douyin.com/"}
    )
    if "error" in data:
        return {"platform": "抖音热榜", "error": data["error"], "items": []}
    items = []
    for i, item in enumerate(data.get("data", {}).get("word_list", [])[:20], 1):
        items.append({
            "rank": i,
            "title": item.get("word", ""),
            "hot": item.get("hot_value", 0),
        })
    return {"platform": "抖音热榜", "items": items, "fetched_at": datetime.now().isoformat()}


PLATFORM_MAP = {
    "weibo": fetch_weibo,
    "zhihu": fetch_zhihu,
    "baidu": fetch_baidu,
    "bilibili": fetch_bilibili,
    "douyin": fetch_douyin,
}


def print_result(result):
    platform = result.get("platform", "未知平台")
    if "error" in result:
        print(f"\n❌ {platform}: {result['error']}")
        return
    items = result.get("items", [])
    print(f"\n📊 {platform}（{len(items)} 条）")
    print("-" * 50)
    for item in items:
        rank = item.get("rank", "?")
        title = item.get("title", "")
        hot = item.get("hot", "")
        hot_str = f"  🔥{hot}" if hot else ""
        print(f"  {rank:2d}. {title}{hot_str}")


def main():
    platform = sys.argv[1] if len(sys.argv) > 1 else "all"

    if platform == "all":
        print(f"🚀 并行抓取所有平台热榜... ({datetime.now().strftime('%H:%M:%S')})")
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(fn): name for name, fn in PLATFORM_MAP.items()}
            for future in as_completed(futures):
                results.append(future.result())
        for r in sorted(results, key=lambda x: x.get("platform", "")):
            print_result(r)
    elif platform in PLATFORM_MAP:
        print(f"🚀 抓取 {platform} 热榜...")
        result = PLATFORM_MAP[platform]()
        print_result(result)
        # 同时输出 JSON 供管道使用
        print("\n--- JSON ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 未知平台: {platform}")
        print(f"支持的平台: {', '.join(PLATFORM_MAP.keys())} 或 all")
        sys.exit(1)


if __name__ == "__main__":
    main()
