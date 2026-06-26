---
name: stock-monitor-hkus
description: 港股/美股/加密货币实时监控。使用 Yahoo Finance (yfinance) 获取实时价格、技术指标监控。支持自定义股票池、涨跌提醒、均线/RSI/MACD信号。
---

# 港股/美股/加密货币监控

实时监控价格，支持技术指标分析和信号提醒。

## 快速开始

### 安装依赖
```bash
pip3 install yfinance numpy --break-system-packages
```

### 运行监控
```bash
python3 scripts/monitor.py
```

### 自定义股票池
编辑 `scripts/monitor.py` 中的 `STOCKS` 字典

## 功能

### 实时数据
- 实时价格、涨跌幅
- 5日涨跌幅度
- 成交量统计

### 技术指标
- **均线**: MA5 / MA10 / MA20
- **RSI**: 相对强弱指标
- **MACD**: 趋势判断

### 信号判断
| 信号 | 条件 |
|------|------|
| 多头 | MA5 > MA10 |
| 空头 | MA5 < MA10 |
| 超买 | RSI > 70 |
| 超卖 | RSI < 30 |
| 金叉 | MACD DIF上穿DEA |
| 死叉 | MACD DIF下穿DEA |

## 默认股票池

### 港股 (5只)
0700.HK 腾讯 | 9988.HK 阿里 | 3690.HK 美团 | 1810.HK 小米 | 0005.HK 汇丰

### 美股 (5只)
AAPL 苹果 | MSFT 微软 | GOOGL 谷歌 | TSLA 特斯拉 | NVDA 英伟达

### 加密货币 (2只)
BTC-USD 比特币 | ETH-USD 以太坊

## 定时任务

```bash
# 每5分钟监控
*/5 * * * * cd /path/to && python3 scripts/monitor.py >> monitor.log 2>&1
```

## 输出示例

```
📊 港股/美股监控 - 2026-03-07 20:45
============================================================
📈 苹果(AAPL): $257 +0.05% | RSI:45 多头
📉 腾讯(0700.HK): HK$519 +0.00% | RSI:38 空头
📈 BTC: $68,000 +1.2% | RSI:52 多头
```

## 状态文件

`memory/stocks_monitor.json`
