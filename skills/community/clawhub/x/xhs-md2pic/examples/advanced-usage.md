# Advanced Usage

## Multi-Page with Manual Breaks

Use `---` to force page breaks at specific points.

### Input

```json
{
  "markdown": "## 日本旅行攻略 🇯🇵\n\n**东京篇**\n\n- 🗼 东京塔 — 经典地标\n- 🏯 浅草寺 — 必打卡\n- 🛒 涩谷109 — 购物天堂\n\n---\n\n**大阪篇**\n\n- 🏰 大阪城 — 历史名城\n- 🍣 道顿堀 — 美食一条街\n- 🎢 环球影城 — 超级马力\n\n---\n\n**京都篇**\n\n- ⛩️ 伏见稻荷 — 千本鸟居\n- 🍵 抹茶体验 — 宇治必去\n- 🎋 岚山竹林 — 拍照圣地\n\n> 收藏这篇，下次去日本不迷路！",
  "title": "日本三城攻略",
  "description": "东京·大阪·京都 完整指南",
  "theme": "default",
  "bg_style": "ai_art"
}
```

This produces 3+ card images (cover page + one per city section), each with an AI-generated subtle Japanese-themed decorative background.

## Deterministic Browser Screenshot (Recommended)

Use explicit geometry + viewport + pagination controls to stabilize multi-page output in browser services.

```json
{
  "markdown": "## 30天自律计划\\n\\n### 第1周：建立节奏\\n\\n- 每天固定起床时间\\n- 只做3件最重要的事\\n- 晚上10分钟复盘\\n\\n### 第2周：强化执行\\n\\n- 番茄钟 25/5\\n- 屏蔽分心应用\\n- 早晨先完成困难任务\\n\\n### 第3周：减少内耗\\n\\n- 每天只追踪一个核心指标\\n- 用模板降低决策成本\\n- 每周做一次任务清理\\n\\n### 第4周：固化习惯\\n\\n- 写一份可复用的周计划\\n- 保留有效动作，删除无效动作\\n- 给自己一次小奖励\\n\\n> 不是靠意志力，而是靠系统赢。",
  "title": "30天自律提升",
  "theme": "default",
  "font_family": "wenkai",
  "padding": "medium",
  "bg_style": "ai_art",
  "card_width": 375,
  "card_height": 500,
  "export_scale": 3,
  "viewport_width": 440,
  "viewport_height": 760,
  "page_gap": 20,
  "pagination_mode": "mixed",
  "max_pages": 10,
  "show_page_number": true,
  "avoid_orphan_heading": true,
  "last_page_compact": true,
  "screenshot_format": "png"
}
```

This produces multiple 1125x1500 PNG cards with stable line wrapping, controlled page breaks, and consistent XHS-like spacing.

## AI Background with Dark Theme

```json
{
  "markdown": "## Python 性能优化指南\n\n### 1. 使用列表推导式\n\n```python\n# 慢\nresult = []\nfor x in range(1000):\n    result.append(x ** 2)\n\n# 快\nresult = [x ** 2 for x in range(1000)]\n```\n\n### 2. 避免全局变量\n\n全局变量查找比局部变量慢 **20-30%**\n\n### 3. 使用 `@lru_cache`\n\n```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef fibonacci(n):\n    if n < 2:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n```\n\n> 优化前先用 cProfile 找到瓶颈",
  "title": "Python 性能优化",
  "theme": "monokai",
  "font_family": "sans-serif",
  "bg_style": "ai_art"
}
```

Produces dark-themed cards with Pygments syntax highlighting and a subtle tech-themed AI background at 18% opacity.

## Full Configuration

```json
{
  "markdown": "内容...",
  "title": "自定义标题",
  "author": "作者名",
  "description": "副标题描述",
  "theme": "nord",
  "font_family": "wenkai",
  "padding": "large",
  "show_cover": true,
  "bg_style": "ai_art"
}
```
