---
name: yanlin-market-data
description: 研林Skill — 采集A股大盘指数、行业板块排名、核心权重股行情数据
---

# 研林 · 市场数据采集 (yanlin-market-data)

## 功能
采集A股当日市场核心数据：
1. **大盘指数行情** — 上证/深证/创业板/科创50/沪深300/上证50/中证500/中证1000
2. **行业板块排名** — 申万一级行业涨跌幅TOP30（含涨跌幅数据）
3. **概念板块排名** — 热门概念板块涨跌幅TOP20
4. **核心权重股行情** — 约30只A股核心标的的实时行情

## 数据源
| 数据类别 | 来源 | URL | 说明 |
|---------|------|-----|------|
| 指数行情 | 新浪财经 | `hq.sinajs.cn/list=sh000001,...` | 实时数据，无需token |
| 行业排名 | 同花顺 | `q.10jqka.com.cn/thshy/` | 每日收盘后更新 |
| 个股行情 | 新浪财经 | `hq.sinajs.cn/list=sh600519,...` | 实时数据 |

## 调用方式
```bash
python3 {baseDir}/scripts/fetch_market_data.py [--output json|text]
```

## 输出示例（JSON结构）
```json
{
  "date": "2026-07-03",
  "indices": {
    "sh000001": {"name":"上证指数","close":4043.64,"change_pct":0.37},
    "sz399001": {"name":"深证成指","close":15597.51,"change_pct":0.64}
  },
  "sectors_top": [
    {"rank":1,"name":"贵金属","change_pct":6.17},
    {"rank":2,"name":"电机","change_pct":5.59}
  ],
  "sectors_bottom": [...],
  "stocks": {
    "sh600519": {"name":"贵州茅台","close":1194.45,"change_pct":-0.71}
  },
  "market_summary": {
    "up_count": 2800,
    "down_count": 1800,
    "total_volume_estimate": "1.2万亿"
  }
}
```
