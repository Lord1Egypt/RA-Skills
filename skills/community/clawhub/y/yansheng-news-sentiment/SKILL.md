---
name: yansheng-news-sentiment
description: 研声Skill — 新闻舆情教学演示（规则与关键词打分，非完整NLP，不依赖实时新闻API）
---

# 研声 · 新闻舆情分析 (yansheng-news-sentiment)

> **⚠️ 数据来源与限制（重要披露）：**
> 本Skill为课程教学简化实现：基于公开新闻标题文本，使用**规则与关键词公式**进行情绪打分（非完整NLP情感分析模型），并支持内置示例新闻数据兜底（教学演示用），输出会标注处理方式。
> 情绪得分仅为教学演示，不代表真实舆情研判，不构成投资建议。

## 功能
1. **新闻采集** — 按标的尝试获取新闻文本（网络不可用时回退到内置示例数据）
2. **情绪打分** — 对每条新闻进行情绪分析（积极/中性/消极），基于规则与关键词公式
3. **热度评估** — 评估新闻关注度（基于文章计数等简化指标）
4. **事件驱动标记** — 标注重大事件及其潜在影响方向（基于关键词规则）

## 数据来源说明（重要）
- 本Skill为教学简化实现：情绪分析基于**规则与关键词公式**，**不是完整NLP情感分析模型**。
- 网络可用时尝试访问公开新闻页面获取标题文本；**网络不可用或接口受限时自动使用内置示例新闻数据兜底**，并在输出中标注处理方式。
- 情绪得分仅为教学演示，不代表真实舆情研判，不构成投资建议。

## 调用方式
```bash
python3 {baseDir}/scripts/analyze_sentiment.py [--codes sh600519,sz300750] [--hours 24] [--output json|text]
```

## 输出示例
```json
{
  "date": "2026-07-03",
  "total_articles": 156,
  "sentiment": {
    "positive": 45,
    "neutral": 82,
    "negative": 29,
    "sentiment_score": 0.62,
    "sentiment_label": "偏积极"
  },
  "hot_topics": [
    {"keyword": "白酒涨价", "mention_count": 28, "sentiment": "positive", "related_stocks": ["贵州茅台"]},
    {"keyword": "外资增持", "mention_count": 15, "sentiment": "positive", "related_stocks": ["贵州茅台", "宁德时代"]}
  ],
  "key_events": [
    {"title": "贵州茅台出厂价上调预期升温", "source": "证券时报", "impact": "positive", "confidence": "high"}
  ]
}
```
