---
name: sentiment-analyzer
description: Analyze market sentiment from news articles, social media posts, and financial headlines. Extract bullish/bearish signals, keyword trends, and sentiment scores for Chinese and English markets.
emoji: 🔍
tags: [sentiment, market-analysis, nlp, news, social-media, trading-signals]
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Sentiment Analyzer — 市场情绪分析

Extract and quantify market sentiment from financial news, social media, and headlines. Supports Chinese and English with domain-specific keyword dictionaries.

## Quick Start

### Core Sentiment Analysis

```python
# Chinese/English sentiment keywords
BULLISH = {
    "利好", "大涨", "突破", "反弹", "看多", "做多", "抄底", "放量上涨",
    "金叉", "上攻", "拉升", "启动", "触底反弹", "企稳回升",
    "增持", "回购", "政策支持", "降息", "放水", "宽松",
    "rally", "breakout", "bullish", "surge", "upgrade", "outperform",
    "beat earnings", "guidance up", "buyback", "dividend increase"
}

BEARISH = {
    "利空", "大跌", "跌破", "回调", "看空", "做空", "逃顶", "放量下跌",
    "死叉", "下探", "杀跌", "出货", "暴雷", "崩盘", "阴跌",
    "减持", "解禁", "加息", "收紧", "紧缩", "贸易战",
    "crash", "plunge", "bearish", "downgrade", "sell-off", "underperform",
    "miss earnings", "guidance down", "layoff", "investigation"
}

def analyze_text(text):
    """Analyze sentiment of a single text."""
    bullish = sum(1 for kw in BULLISH if kw in text)
    bearish = sum(1 for kw in BEARISH if kw in text)
    total = bullish + bearish
    
    if total == 0:
        return {"sentiment": "neutral", "score": 0.0, "bullish": 0, "bearish": 0}
    
    score = (bullish - bearish) / total
    if score > 0.2: sent = "bullish"
    elif score < -0.2: sent = "bearish"
    else: sent = "neutral"
    
    return {"sentiment": sent, "score": round(score, 2), "bullish": bullish, "bearish": bearish}
```

### Batch Analysis

```python
def batch_analyze(headlines):
    """Analyze a list of headlines."""
    results = [analyze_text(h) for h in headlines]
    bullish = sum(1 for r in results if r["sentiment"] == "bullish")
    bearish = sum(1 for r in results if r["sentiment"] == "bearish")
    neutral = sum(1 for r in results if r["sentiment"] == "neutral")
    avg = sum(r["score"] for r in results) / len(results) if results else 0
    
    return {
        "total": len(headlines),
        "bullish": bullish,
        "bearish": bearish,
        "neutral": neutral,
        "bullish_pct": round(bullish / len(headlines) * 100, 1) if headlines else 0,
        "avg_score": round(avg, 2),
        "overall": "bullish" if bullish > bearish else ("bearish" if bearish > bullish else "mixed")
    }
```

### Trending Keywords

```python
from collections import Counter
import re

def extract_keywords(headlines, top_n=10):
    """Extract most frequent market keywords from headlines."""
    all_words = []
    for h in headlines:
        words = re.findall(r'[\w\u4e00-\u9fff]+', h)
        all_words.extend(w for w in words if len(w) > 1)
    counter = Counter(all_words)
    return counter.most_common(top_n)
```

## Data Sources

```bash
# Sina Finance headlines
curl -s "https://finance.sina.com.cn/" | grep -oP '(?<=<a[^>]*>)[^<]+' | head -20

# East Money news
curl -s "https://quote.eastmoney.com/" | grep -oP '[\u4e00-\u9fff]{4,}' | head -30

# Weibo trending (public)
curl -s "https://weibo.com/ajax/side/hotSearch"
```

## Format Output

### Daily Sentiment Report
```
🔍 市场情绪快报 (2026-05-22)

📰 新闻情绪分析 (共15条)
• 看多: 6条 (40.0%) 🟢
• 看空: 4条 (26.7%) 🔴
• 中性: 5条 (33.3%) ⚪
• 平均得分: +0.15 (偏多)

🔥 热门关键词
利好(3) 突破(2) 政策支持(2) 反弹(2)
利空(2) 回调(2) 加息(1) 放量(1)

📊 品种情绪分时
• 焦炭 🟢 +0.45  螺纹 🟢 +0.30
• 沪铜 🟡 +0.10  原油 🟡 +0.05
• 纯碱 🔴 -0.35  玻璃 🔴 -0.28

⚠️ 情绪分析仅供参考，不构成交易建议
```

### News Item Analysis
```
📰 [标题] 央行降准0.5个百分点 释放长期资金约1万亿
📊 情绪: bullish 🟢 (得分: +0.67)
🔑 关键词: 降准(利好), 释放资金(利好), 宽松
💡 影响: 利好股市，利多银行/地产板块
```

### Trend Tracking
```
📈 品种情绪趋势 (近7天)
品种    周一  周二  周三  周四  周五  方向
焦炭    +0.2  +0.3  +0.1  +0.4  +0.5  ↗️
螺纹    -0.1  -0.3  -0.2   0.0  +0.3  ↗️
纯碱    -0.4  -0.5  -0.3  -0.6  -0.4  ↘️
```

## Use Cases
- **Pre-market check:** Scan overnight news sentiment before trading
- **Position monitoring:** Track sentiment changes for held positions
- **Earnings season:** Analyze sentiment around earnings reports
- **Contrarian signals:** Extreme sentiment (90%+ one direction) often signals reversal
- **Sector rotation:** Compare sentiment across sectors to identify rotation

## Notes
- This is keyword-based sentiment analysis, NOT deep NLP
- Works better with longer texts (headlines + first paragraph)
- Chinese sentiment keywords need regular maintenance (new slang emerges)
- Combine with volume/price data for confirmation signals
- For production, consider finBERT or other pre-trained financial NLP models
