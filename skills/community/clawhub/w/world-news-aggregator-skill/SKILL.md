name: world-news-aggregator
description: 全球信息参考 - 多元聚合全球科技、股市、AI 论文、军事技术、政策情报的智能新闻聚合助手
version: 1.0.0
author: Alex Bloomberg
tags: [news, aggregator, global, tech, stock, ai, policy]
---

# World News Aggregator Skill

全球信息参考 - 多元聚合全球科技、股市、AI 论文、军事技术、政策情报的智能新闻聚合助手。

## 核心特性

- 🌐 全球多源聚合：50+ 高价值信源
- 🤖 专为 OpenClaw 打造：即插即用
- 🆓 零配置：无需 API Key
- 🧠 AI 智能摘要：结构化情报报告
- 📊 多场景预设：综合/科技/财经/AI/政策
- 🔍 智能搜索：关键词/时间/来源筛选

## 使用方法

```bash
# OpenClaw 中使用
/world-news [topic] [options]

# 例子
/world-news tech          # 科技新闻
/world-news stock         # 股市新闻
/world-news ai            # AI 论文
/world-news military      # 军事技术
/world-news policy        # 政策情报
/world-news all           # 综合日报
参数

| 参数        | 说明        | 默认值 |
| --------- | --------- | --- |
| topic     | 新闻主题      | all |
| --sources | 指定来源      | 全部  |
| --limit   | 返回数量      | 10  |
| --hours   | 时间范围 (小时) | 24  |
主题分类

| 主题    | 代码         | 说明                                    |
| ----- | ---------- | ------------------------------------- |
| 全球科技  | tech       | TechCrunch, The Verge, Wired 等        |
| 开源社区  | opensource | Hacker News, GitHub, Product Hunt     |
| 国内科技  | cn-tech    | 36Kr, 虎嗅，少数派                          |
| 全球股市  | stock      | Yahoo Finance, Bloomberg, Reuters     |
| 国内股市  | cn-stock   | 东方财富，雪球                               |
| AI 论文 | ai         | arXiv, Papers With Code, Hugging Face |
| 军事技术  | military   | Defense News, Janes, The War Zone     |
| 国内政策  | cn-policy  | 国务院，发改委，工信部，网信办                       |
例子

shell

# 科技早报
/world-news tech --limit 10 --hours 24

# AI 周报
/world-news ai --limit 20 --hours 168

# 财经简报
/world-news stock --sources bloomberg,reuters --limit 5

# 政策速递
/world-news cn-policy --hours 48

# 综合日报
/world-news all --limit 20
依赖

• Python >= 3.8.0
• requests
• feedparser

许可证

MIT License
