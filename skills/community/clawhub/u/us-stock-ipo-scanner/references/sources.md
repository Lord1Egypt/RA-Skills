# 美股IPO信号源详细列表

## 一、Layer 1 新机会发现（核心）

### 1.1 Invezz IPO Feed（强烈推荐）
- **URL**: https://invezz.com/news/stocks/ipos/feed/
- **特点**: 覆盖全球IPO + listing + 新基金
- **优先级**: ⭐⭐⭐⭐⭐

### 1.2 Nasdaq IPO 页面
- **URL**: https://www.nasdaq.com/market-activity/ipos
- **用法**: 需要用 RSS.app 转 RSS
- **特点**: 隐藏金矿，官方没有RSS
- **优先级**: ⭐⭐⭐⭐

### 1.3 CNBC IPO News
- **URL**: https://www.cnbc.com/id/100003114/device/rss/rss.html
- **特点**: 偏慢，但有确认价值
- **优先级**: ⭐⭐⭐

### 1.4 Seeking Alpha IPO
- **URL**: https://seekingalpha.com/market-news/ipos.xml
- **特点**: 更偏交易视角
- **优先级**: ⭐⭐⭐

### 1.5 Reddit IPO 搜索 RSS
- IPO: https://www.reddit.com/search.rss?q=IPO
- new listing: https://www.reddit.com/search.rss?q=new+listing
- AI stock: https://www.reddit.com/search.rss?q=AI+stock

---

## 二、Layer 2 起飞信号

### 2.1 Benzinga（必须接）
- **通用新闻**: https://www.benzinga.com/feed
- **Markets**: https://www.benzinga.com/markets.rss
- **Trading Ideas**: https://www.benzinga.com/trading-ideas.rss
- **Stock Ideas**: https://www.benzinga.com/stock-ideas.rss
- **优先级**: ⭐⭐⭐⭐⭐（最应该重仓的信号源）

### 2.2 Invezz AI 热点
- **URL**: https://invezz.com/news/stocks/artificial-intelligence/feed/
- **用途**: 补 VCX 这种叙事

### 2.3 Twitter → RSS
- **工具**: https://rss.app
- **示例**:
  - https://x.com/search?q=$VCX&src=typed_query
  - https://x.com/search?q=new+listing+stock&src=typed_query

---

## 三、Layer 3 爆发确认

### 3.1 Reddit WSB
- **URL**: https://www.reddit.com/r/wallstreetbets/.rss
- **用途**: 妖股爆发前夜

### 3.2 Reddit stocks
- **URL**: https://www.reddit.com/r/stocks/.rss

### 3.3 Benzinga Breaking
- **URL**: https://www.benzinga.com/feed

---

## 四、VCX类标的专用关键词

监控这些关键词捕捉类似机会：

```
new listing
direct listing
closed-end fund
AI exposure
pre IPO exposure
SpaceX fund
VC fund
new ETF
```

---

## 五、自动雷达实现方案

如需实现"类似VCX的标的出现就推送"：

1. **RSS采集**: 汇总上述所有RSS源
2. **NLP处理**: 提取标的、关键词、情绪
3. **打标签**: 分类（IPO/新基金/并购等）
4. **规则匹配**: 匹配关键词库
5. **推送提醒**: 推送到指定渠道

### 关键词权重

| 关键词 | 权重 | 场景 |
|--------|------|------|
| direct listing | +3 | 直接上市 |
| closed-end fund | +3 | 封闭式基金 |
| pre IPO | +2 | IPO前 |
| AI exposure | +2 | AI叙事 |
| SpaceX | +3 | 热门概念 |
| $XXX | +1 | 具体代码 |

---

## 六、推荐扫描频率

| Layer | 频率 | 原因 |
|-------|------|------|
| Layer 1 | 每天1-2次 | 新机会发现 |
| Layer 2 | 每2-3小时 | 起飞信号 |
| Layer 3 | 实时/每小时 | 爆发确认 |

---

## 七、信号优先级总结

**正确顺序：Twitter → Reddit → Benzinga → 新闻媒体**

❌ 错误：只看新闻
✅ 正确：抓早期信号源