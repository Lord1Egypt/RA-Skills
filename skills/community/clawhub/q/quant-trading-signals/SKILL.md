---
name: quant-trading-signals
description: 量化交易信号系统。基于MACD、RSI、KDJ、均线、布林带等技术指标生成买卖信号。支持港股、美股、加密货币。
---

# 量化交易信号

基于技术指标的量化交易信号系统。

## 快速开始

```bash
pip3 install yfinance numpy --break-system-packages
python3 scripts/signals.py AAPL
python3 scripts/signals.py BTC-USD
```

## 信号指标

| 指标 | 信号 |
|------|------|
| **MACD** | 金叉/死叉/背离 |
| **RSI** | 超买(>70)/超卖(<30) |
| **KDJ** | 超买/超卖/金叉/死叉 |
| **均线** | 多头排列/空头排列 |
| **布林带** | 突破上轨/下轨 |

## 综合信号

- ⭐⭐⭐ 强烈信号：多个指标共振
- ⭐⭐ 中等信号：2个指标一致
- ⭐ 弱信号：单个指标

## 支持市场

- 港股: 0700.HK, 9988.HK, 3690.HK
- 美股: AAPL, MSFT, TSLA, NVDA
- 加密货币: BTC-USD, ETH-USD

## 输出示例

```
🎯 综合信号:
   多头信号: 2.0 | 空头信号: 1.0
   强度: ⭐⭐ 偏多
   建议: 可以适当关注
```

## 风险提示

⚠️ 仅供分析参考，不构成投资建议。
