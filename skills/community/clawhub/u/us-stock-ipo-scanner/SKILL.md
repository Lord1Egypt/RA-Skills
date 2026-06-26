---
name: us-stock-ipo-scanner
description: |
  美股IPO机会扫描与早期信号捕获。用于发现美股新股、IPO、直接上市、基金等投资机会。
  当用户提到：美股、IPO、新股、上市、new listing、IPO scanner、IPO机会、错过股票、VCX、Fundrise等关键词时触发此技能。
  包含三层信号源架构：Layer 1新机会发现、Layer 2起飞信号、Layer 3爆发确认，以及关键词监控列表。
---

# 美股IPO机会扫描 🍇

## 核心理念

**真正有价值的信号顺序是：Twitter → Reddit → Benzinga → 新闻媒体**

大多数人的问题是"只看新闻"，错过了早期信号。

---

## 三层信号源架构

### 🟢 Layer 1：新机会发现（核心）

| 来源 | RSS地址 | 用途 |
|------|---------|------|
| Invezz IPO Feed（强烈推荐） | https://invezz.com/news/stocks/ipos/feed/ | 覆盖全球IPO + listing + 新基金 |
| Nasdaq IPO页面 | 需用RSS.app转：https://www.nasdaq.com/market-activity/ipos | 隐藏金矿 |
| CNBC IPO News | https://www.cnbc.com/id/100003114/device/rss/rss.html | 偏慢但有确认价值 |
| Seeking Alpha IPO | https://seekingalpha.com/market-news/ipos.xml | 交易视角 |

**Reddit搜索RSS：**
- https://www.reddit.com/search.rss?q=IPO
- https://www.reddit.com/search.rss?q=new+listing
- https://www.reddit.com/search.rss?q=AI+stock

### 🟡 Layer 2：起飞信号

| 来源 | RSS地址 | 用途 |
|------|---------|------|
| Benzinga 通用新闻 | https://www.benzinga.com/feed | 必须重仓的信号源 |
| Benzinga Markets | https://www.benzinga.com/markets.rss | 市场异动 |
| Benzinga Trading Ideas | https://www.benzinga.com/trading-ideas.rss | 交易思路 |
| Benzinga Stock Ideas | https://www.benzinga.com/stock-ideas.rss | 个股推荐 |
| Invezz AI热点 | https://invezz.com/news/stocks/artificial-intelligence/feed/ | 题材热点 |

**Twitter关键词RSS（最重要）：**
用 https://rss.app 生成，监控关键词：
- $VCX（已有标的变化）
- "new listing"
- "direct listing"
- "closed-end fund"
- "AI exposure"
- "pre IPO exposure"
- "SpaceX fund"
- "new ETF"

### 🔴 Layer 3：爆发确认

| 来源 | RSS地址 | 用途 |
|------|---------|------|
| Reddit WSB | https://www.reddit.com/r/wallstreetbets/.rss | 妖股爆发前夜 |
| Reddit stocks | https://www.reddit.com/r/stocks/.rss | 股票讨论 |
| Benzinga Breaking | https://www.benzinga.com/feed | 突发新闻 |

---

## VCX类标的专用关键词

当发现类似VCX（Fundrise Innovation Fund）的机会时，监控这些关键词：

```
new listing
direct listing
closed-end fund
AI exposure
pre IPO exposure
SpaceX fund
VC fund
new ETF
$XXX (具体股票代码)
```

---

## 进阶：自动雷达（可选）

如需更自动化，可以实现：

1. **RSS → NLP → 打标签 → 自动提醒**
2. **设置类似VCX标的出现的推送**

详细内容见 [sources.md](references/sources.md)

---

## 使用方式

1. 定期扫描 Layer 1 sources 获取新机会
2. 发现潜在标的后，用 Layer 2 关键词监控进一步确认
3. 参考 Layer 3 确认市场情绪
4. 符合条件时推送提醒用户

---

## 输出格式

扫描报告包含：
- 📌 新发现标的（来源、关键词、初步分析）
- 🔥 起飞信号（Layer 2 验证情况）
- 📊 市场情绪（Layer 3 参考）
- 💡 建议（是否需要深入研究）