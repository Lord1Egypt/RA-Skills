---
name: today-trending
description: 获取今日微博、抖音、百度热搜排行榜 - 实时热门话题一站式查询
metadata: { "openclaw": { "emoji": "🔥", "requires": { "bins": ["python3"] } } }
---

# 今日热榜 (Today Trending)

一键获取微博、抖音、百度三大平台的热搜排行榜。

## Usage

```bash
python3 skills/today-trending/scripts/trending.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| platform | str | yes | 平台类型: weibo / douyin / baidu / all |

## Platform Types

| platform | Platform |
|----------|----------|
| weibo | 微博热搜 |
| douyin | 抖音热搜 |
| baidu | 百度热搜 |
| all | 全部平台 |

## Examples

```bash
# 微博热搜
python3 scripts/trending.py '{"platform":"weibo"}'

# 抖音热搜
python3 scripts/trending.py '{"platform":"douyin"}'

# 百度热搜
python3 scripts/trending.py '{"platform":"baidu"}'

# 全部平台
python3 scripts/trending.py '{"platform":"all"}'
```

## Output Format

返回热搜话题列表，每条包含标题和热度值。

## Current Status

Fully functional.

## Output Analysis

返回结果后，可以对话题进行总结分析归类，方便用户快速了解全网热点趋势。