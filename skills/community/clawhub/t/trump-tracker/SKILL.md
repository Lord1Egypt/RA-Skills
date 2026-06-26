---
name: trump-tracker
description: 川普动态实时监控及“不靠谱”预测模型 (Python 版)。
---

# 川普动态监控助手 (Trump Dynamic Tracker)

**版本 / Version**: 1.0.0

### 核心能力 / Core Capabilities:
1. **实时动态捕捉 / Real-time Dynamics**: 自动抓取全球新闻 RSS 关于川普的最新言论/行动。 (Auto-capture latest Trump news/actions via global RSS feeds.)
2. **不靠谱模型预测 / Unreliable Model Prediction**: 基于 TextBlob 的言论执行概率与市场冲击预测。 (Sentiment-based execution probability and market impact prediction.)

## 🛠️ 包含工具 / Tools Included

### 1. 动态抓取脚本 / News Monitor (`scripts/trump_monitor.py`)
使用 `feedparser` 监控新闻流。 (Monitors news streams using `feedparser`.)

### 2. 川普不靠谱预测模型 / Unreliable Predictor (`scripts/trump_predictor.py`)
Bilingual Prediction output.

**用法 / Usage**:
// turbo
```bash
python e:\py\.agent\skills\trump-tracker\scripts\trump_predictor.py
```

## 📦 依赖 / Dependencies
- requests, feedparser, beautifulsoup4, textblob

