---
name: realtime-finance
description: "实时财经数据查询技能 - 支持A股、港股、美股、黄金、原油、VIX、美债等"
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
  triggers:
    - "股价"
    - "行情"
    - "实时"
    - "大盘"
    - "指数"
    - "涨跌"
    - "外汇"
    - "期货"
    - "VIX"
    - "黄金"
    - "原油"
    - "美债"
    - "美元指数"
    - "A股"
    - "美股"
    - "港股"
---

# 实时财经数据技能

使用新浪财经 + Yahoo Finance 获取实时财经数据。

## 支持的数据

| 市场 | 数据源 | 示例 |
|------|--------|------|
| A股 | 新浪财经 | 茅台、宁德时代、上证指数 |
| 港股 | 新浪财经 | 腾讯、阿里、美团 |
| 美股 | Yahoo Finance | AAPL、TSLA、NVDA |
| 大宗商品 | Yahoo Finance | 黄金(GC=F)、原油(CL=F) |
| 指数 | Yahoo Finance | VIX、美债收益率(TNX) |
| 外汇 | Yahoo Finance | 美元指数(DXY) |

## 工具调用

当用户询问财经数据时，自动调用：

```bash
python3 ~/.openclaw/workspace/skills/realtime-finance/realtime_finance.py <查询内容>
```

## 触发条件

- "查一下茅台股价"
- "今天大盘怎么样"
- "VIX多少"
- "黄金价格"
- "美股行情"
- "美债收益率"

## 依赖

- Python 3
- yfinance: `pip3 install yfinance`

## 文件位置

`~/.openclaw/workspace/skills/realtime-finance/`
