#!/usr/bin/env python3
"""知乎热榜抓取与分析"""
import json, sys
try:
    import requests
except ImportError:
    print("请安装 requests: pip3 install requests")
    sys.exit(1)

def fetch_zhihu_hotlist():
    """获取知乎热榜"""
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=10, verify=True)
        data = r.json()
    except Exception:
        # 降级：直接解析网页
        url2 = "https://www.zhihu.com/hot"
        r2 = requests.get(url2, headers=headers, timeout=10, verify=True)
        import re
        titles = re.findall(r'title:(.*?)', r2.text[:50000])
        results = []
        for i, t in enumerate(titles[:50]):
            results.append({"title": t, "heat": 0, "index": i+1})
        return results

    results = []
    for item in data.get("data", []):
        target = item.get("target", {})
        results.append({
            "title": target.get("title", ""),
            "excerpt": target.get("excerpt", ""),
            "heat": item.get("detail_text", "").replace("万热度", ""),
            "index": len(results) + 1
        })
    return results

def analyze_topics(topics):
    """分析话题并评分"""
    for t in topics:
        heat = float(t.get("heat", 0) or 0)
        title = t.get("title", "")
        # 简单评分：热度 + 长标题加分
        score = min(100, int(heat / 10000) * 20 + (10 if len(title) > 15 else 0))
        t["score"] = score
    topics.sort(key=lambda x: x.get("score", 0), reverse=True)
    return topics

if __name__ == "__main__":
    topics = fetch_zhihu_hotlist()
    analyzed = analyze_topics(topics)
    print(json.dumps(analyzed[:20], ensure_ascii=False, indent=2))
