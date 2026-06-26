---
name: weibo-trending-topics
description: >
  Track Weibo hot search trends (微博热搜) in real-time. Fetches live trending topics, 
  categories (娱乐/社会/科技/体育), and historical trend data. Zero config required.
  Triggers: "微博热搜", "weibo trending", "微博趋势", "热搜榜".
version: 1.0.0
tags:
  - latest
  - chinese-platform
  - trending
  - social-media
---

# Weibo Trending Topics

Track real-time trending topics on Weibo (微博热搜榜) with category filtering and historical comparison.

## 🔵 Zero Config — Works Immediately

No API keys, no login needed. Uses Weibo's public API endpoints.

## Usage

```python
import requests

# 微博热搜实时榜单 (Top 50)
url = "https://weibo.com/ajax/side/hotSearch"
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
data = resp.json()

for item in data.get("realtime", []):
    print(f"{item.get('flag_desc','')} {item.get('word')} | 🔥 {item.get('num')}")
```

## Historical Comparison

```python
def compare_trends(old_file, new_file):
    with open(old_file) as f:
        old = {item["word"] for item in json.load(f).get("realtime", [])}
    with open(new_file) as f:
        new = {item["word"] for item in json.load(f).get("realtime", [])}
    print(f"🆕 新上榜: {new - old}")
    print(f"📉 已掉榜: {old - new}")
```

## Tags

`weibo` `微博` `热搜` `trending` `social-media` `chinese-platform` `news` `hot-search`
