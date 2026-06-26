---
name: tianji-data
description: "| 优先级 | 数据源 | 方式 | 延迟 | 覆盖品种 |。触发词：搜索, search, skill, 优化, 数据, data。"
---

# 天玑数据层 · 数据采集规范

## 数据源优先级（¥0免费方案）

| 优先级 | 数据源 | 方式 | 延迟 | 覆盖品种 |
|--------|--------|------|------|---------|
| P0 | **腾讯实时行情** | `realtime.py` | <3秒 | A股全板块 |
| P0 | **新浪期货** | `free_market.py` | ~5秒 | 黄金/白银/铜/原油/螺纹钢/铁矿石/焦煤/焦炭/豆粕 |
| P0 | **QDII ETF** | `free_market.py` | <3秒 | 纳指/标普（美股情绪代理） |
| P0 | **港股指数** | `free_market.py` | <3秒 | 恒生指数/恒生科技 |
| P1 | 东方财富/新浪财经 | `extract_content_from_websites` | 实时 | 资讯/资金流 |
| P1 | batch_web_search（外盘/新闻）| 搜索 | 分钟级 | 政策/宏观 |
| P2 | huangjinjiage.cn（黄金） | `extract_content_from_websites` | 日更 | 仅黄金 |

### 腾讯实时行情接口（盘中必备）
```python
from skills.tianji_data.realtime import get_batch, get_realtime

r = get_batch(['000001', '000791', '600938', '601857'])
d = get_realtime('000791')  # 自动判断深/沪交所
# 返回字段：name, price, change_pct, open, high, low, turnover_yi, time
```

### 免费全市场快照（天枢核心接口）
```python
from skills.tianji_data.free_market import (
    get_full_market_snapshot,  # 一站式全市场数据
    format_snapshot,           # 格式化输出
)

snap = get_full_market_snapshot()
print(format_snapshot(snap))
# 输出：国际商品(黄金/白银/铜/原油) + 国内商品(螺纹钢/铁矿/焦煤/焦炭/豆粕)
#     + 港股指数(恒生/恒科) + QDII ETF(纳指/标普/恒科) + 人民币估算
```

### 专项数据接口
```python
from skills.tianji_data.free_market import (
    get_commodities,   # 国际黄金/白银/铜/原油
    get_cn_futures,   # 国内螺纹钢/铁矿石/焦煤/焦炭/豆粕
    get_hk_indices,    # 港股恒生/恒科指数
    get_us_etf_cn,    # QDII ETF（纳指/标普）
    get_cny_estimate,  # 人民币方向估算
)
```

> ⚠️ 搜索无法替代实时行情。盘中价格以腾讯+新浪接口为准。
> ⚠️ Yahoo Finance / A50 / 美元指数已验证不可用（IP被屏蔽/数据为空）

## 标准化数据格式

所有采集数据必须转换为以下格式存入 `/workspace/data/tianji-system/data/YYYY-MM-DD.json`：

```json
{
  "timestamp": "2026-03-26T06:00:00+08:00",
  "market": {
    "sh_index": 3931.84,
    "sz_index": 13801.0,
    "cy_index": 3316.97,
    "change_pct": 1.30,
    "volume": 218000000000,
    "limit_up": 105,
    "limit_down": 5
  },
  "sectors": {
    "top3": ["电力", "CPO", "军工"],
    "bottom3": ["黄金", "煤炭", "石油"]
  },
  " commodities": {
    "gold_usd": 4560.68,
    "oil_wti": 95.0,
    "oil_brent": 101.0
  },
  "fund_flow": {
    "north_flow": "+45亿",
    "main_sectors": {"电力": 70.75, "CPO": 63.62},
    "main_out": {"石油": -17.8, "煤炭": -8.1}
  },
  "macro": {
    "us_cepi_index": 103.2,
    "rmb_usd": 6.89,
    "news_keywords": ["停火", "MLF", "降息"]
  }
}
```

## 各数据类型采集指令

### 1. A股实时行情（开盘/盘后）
```
extract_content_from_websites:
  - 东方财富沪指: https://quote.eastmoney.com/zs000001.html
  - 东方财富深成: https://quote.eastmoney.com/sz399001.html
  - 创业板: https://quote.eastmoney.com/sz399006.html
```

### 2. 黄金/原油（24h）
```
extract_content_from_websites:
  - http://www.huangjinjiage.cn/
  - batch_web_search: "黄金价格 原油价格 今日"
```

### 3. 国内政策新闻（每日首轮）
```
batch_web_search:
  - "中国 重大政策 今日 2026年"
  - "国务院 部委 新规 今日"
  - "证监会 央行 工信部 最新消息"
```

### 4. 全球政策一览（每日夜报用）
```
batch_web_search:
  - "Federal Reserve policy announcement today 2026"
  - "US China trade policy latest 2026"
  - "EU regulation tech AI policy today"
  - "G7 summit outcome 2026"
  - "global central bank rate decision"
```
重点关注：**美联储政策、美中贸易摩擦、欧盟AI/科技监管、G7/IMF会议、全球央行利率决议**。

### 4. 板块资金流
```
batch_web_search:
  - "A股 板块资金流向 今日 东方财富"
```

## 数据质量规则

1. **时效性检查**：标记数据采集时间，超过30分钟的数据注明"可能滞后"
2. **交叉验证**：黄金/原油价格用至少2个来源比对
3. **异常检测**：单日涨跌>5%自动标记为"需核实"
4. **缺失值处理**：无法获取的数据标记为 `null`，不填0

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 页面JS动态加载无法提取 | 改用 `batch_web_search` |
| 页面404/无内容 | 跳过该数据源，标记来源失败 |
| 数据明显异常（涨跌>20%）| 标记异常，不用于预判 |

## 相关文件

- 数据存储：`/workspace/data/tianji-system/data/`
- 采集日志：`/workspace/data/tianji-system/data/collect.log`
- 参考文档：`references/data-sources.md`
