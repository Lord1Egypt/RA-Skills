---
name: us-stock-radar
description: 美股行情与舆情监控工具。当用户询问「美股怎么样」「纳指」「标普」「道指」「美股大盘」「今晚美股」「US股」「美股行情」「美股期货」「NQ」「ES」时使用。支持Yahoo Finance获取实时行情，以及Google News RSS和X/Twitter舆情监控。📢微信公众号：PM熊叔（打造一人公司的投研团队）
---

# 美股雷达 (US-Stock Radar)

## 数据源总览

| 数据源 | 用途 | 稳定性 |
|--------|------|--------|
| Yahoo Finance | 主要指数（SPY/QQQ/DIA/IWM）实时行情 | ⭐⭐⭐ |
| Yahoo Finance | 个股行情（NVDA/AAPL/MSFT/TSLA等） | ⭐⭐⭐ |
| TradingView 嵌入页 | NQ/ES 期货实时图表（浏览器截图） | ⭐⭐ |
| Google News RSS | 美股突发新闻 | ⭐⭐⭐ |

## 实时行情查询

### NY Fed 宏观利率 API

```python
import requests

def get_macro_rates():
    """NY Fed 官方利率（SOFR/EFFR/OBFR/TGCR/BGCR）"""
    url = "https://markets.newyorkfed.org/api/rates/all/latest.json"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    r = requests.get(url, headers=headers, timeout=10)
    return r.json()["refRates"]
    # 返回: SOFR=3.64%, EFFR=3.64%, OBFR=3.64%, TGCR=3.62%, BGCR=3.62%
```

### FRED 国债收益率

```python
def get_treasury_yields():
    """10Y 和 2Y 国债收益率（无需 API key）"""
    for sid, name in [("DGS10", "10Y"), ("DGS2", "2Y")]:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&vintage_date=2026-04-24"
        r = requests.get(url, timeout=10)
        last = r.text.strip().split('\n')[-1]  # 格式: "2026-04-22,4.30"
```

### Yahoo Finance（主要指数）

```python
import requests

US_INDICES = {
    "^GSPC": "标普500",
    "^DJI": "道琼斯",
    "^IXIC": "纳斯达克",
    "^VIX": "VIX恐慌指数",
    "NQ=F": "纳斯达克期货(NQ)",
    "ES=F": "标普期货(ES)",
    "CL=F": "WTI原油",
    "GC=F": "黄金",
    "SI=F": "白银",
}

def get_us_indices():
    """批量获取美股指数 + 期货 + 大宗商品"""
    symbols = ",".join(US_INDICES.keys())
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    results = r.json()["quoteResponse"]["result"]
    out = {}
    for item in results:
        sym = item["symbol"]
        name = US_INDICES.get(sym, sym)
        price = item.get("regularMarketPrice", 0)
        prev = item.get("regularMarketPreviousClose", 0)
        chg = item.get("regularMarketChange", 0)
        pct = item.get("regularMarketChangePercent", 0)
        arrow = "🔴" if chg > 0 else "🟢" if chg < 0 else "⚪"
        out[sym] = f"{arrow} {name}: {price} {chg:+.2f}({pct:+.2f}%)"
    return out
```

### Yahoo Finance（个股行情）

```python
import requests

MAJOR_STOCKS = {
    "NVDA": "英伟达",
    "AAPL": "苹果",
    "MSFT": "微软",
    "GOOGL": "谷歌",
    "AMZN": "亚马逊",
    "META": "Meta",
    "TSLA": "特斯拉",
    "AMD": "AMD",
    "NFLX": "Netflix",
    "CRM": "Salesforce",
}

def get_us_stocks(symbols):
    """获取美股个股行情，支持多代码"""
    if isinstance(symbols, str):
        symbols = [symbols]
    sym_str = ",".join([s.upper() for s in symbols])
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={sym_str}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    results = r.json()["quoteResponse"]["result"]
    for item in results:
        sym = item["symbol"]
        name = item.get("shortName", sym)
        price = item.get("regularMarketPrice", 0)
        prev = item.get("regularMarketPreviousClose", 0)
        chg = item.get("regularMarketChange", 0)
        pct = item.get("regularMarketChangePercent", 0)
        arrow = "🔴" if chg > 0 else "🟢" if chg < 0 else "⚪"
        print(f"{arrow} {name}({sym}): {price} {chg:+.2f}({pct:+.2f}%)")
```

## 主流代码速查

| 股票/指数 | 代码 | 板块 |
|-----------|------|------|
| 标普500 ETF | SPY | 大盘 |
| 纳指100 ETF | QQQ | 科技 |
| 道指 ETF | DIA | 蓝筹 |
| 小盘股 | IWM | 风险偏好 |
| 英伟达 | NVDA | AI/芯片 |
| 苹果 | AAPL | 科技 |
| 特斯拉 | TSLA | 新能源 |
| AMD | AMD | 芯片 |
| 谷歌 | GOOGL | 科技/AI |
| 亚马逊 | AMZN | 电商/云 |
| Meta | META | 社交/AI |
| 微软 | MSFT | 科技/云 |

## 舆情监控

### Google News Live（突发新闻）

```
https://news.google.com/rss/search?q=US+stock+market+when:1h
https://news.google.com/rss/search?q=Nasdaq+S%26P+500+when:1h
https://news.google.com/rss/search?q=Treasury+yield+Fed+when:1h
https://news.google.com/rss/search?q=Nvidia+AI+stock+when:1h
```

### X/Twitter 美股舆情

使用 browser 工具访问 @bearfrom2077：

```
https://x.com/search?q=%24NVDA+%24TSLA+stock&f=live
https://x.com/search?q=nasdaq+fed+rate&f=live
https://x.com/search?q=S%26P+500+earnings&f=live
```

**核心关键词：**
- `$NVDA` / `$TSLA` / `$AMD` — 个股讨论
- `S&P 500` / `Nasdaq` — 大盘
- `Fed rate` / `Treasury` — 宏观
- `CPI` / `jobs report` — 数据发布

## 情报解读框架

| 指标 | 阈值 | 信号 |
|------|------|------|
| VIX | > 20 | 恐慌加剧 |
| VIX | < 15 | 乐观 |
| 纳指 vs 标普 | 纳指强 > 1% | 科技主线 |
| NQ期货 | 盘前大跌 > 1% | A股/港股承压 |
| 黄金 | 突破 2000 | 避险情绪 |
| 10年美债 | 突破 4.5% | 股市压力 |
| SOFR vs Fed Rate | 低于目标区间下限 | 流动性充裕 |
| 10Y - 2Y 利差 | 倒挂加深 | 经济衰退预警 |
| 10Y - 2Y 利差 | 利差扩大 | 衰退风险缓解 |

**分析顺序：**
1. SOFR/EFFR — 基准利率，了解美联储立场
2. 10Y/2Y 国债收益率 — 利率走廊和经济预期
3. 10Y-2Y 利差 — 衰退概率
4. VIX — 市场情绪温度计
5. NQ/ES 期货 — 盘前大盘方向
6. SPY/QQQ/DIA — 三大指数
7. 科技巨头（NVDA/AAPL/MSFT）— 主线
8. 黄金/原油 — 宏观背景
9. 给出综合判断

## Cron 配置建议

| 频率 | 内容 | 适用场景 |
|------|------|----------|
| 每15分钟 | NQ + ES 期货 | A股开盘前参考 |
| 每30分钟 | SPY + QQQ + VIX | 盘中监控 |
| 每小时 | 科技巨头 + 黄金原油 | 宏观背景 |
| 有问才查 | 个股行情 | 被动触发 |

## 快速查询命令

```bash
cd C:\Users\gold3\.openclaw\workspace\skills\us-stock-radar\scripts

# 美股主要指数+期货+大宗商品
python us_index.py

# 个股行情（传入股票代码）
python us_quote.py NVDA TSLA AAPL

# 科技巨头组合
python tech_giants.py

# 美股仪表盘（指数+巨头）
python dashboard.py
```
