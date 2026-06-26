# RQAlpha 米筐回测 Skill

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/ricequant/rqalpha)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

RQAlpha开源事件驱动回测框架，支持A股和期货，模块化架构。

## ✨ 特性

- 🆓 **开源免费** - Apache 2.0 开源，社区活跃
- 🔄 **事件驱动** - init() + handle_bar() 经典事件驱动架构
- 🔌 **Mod插件系统** - 模块化设计，通过 Mod 扩展功能
- 💻 **命令行+Python API** - 支持命令行运行和 Python API 调用
- 📦 **内置数据** - 自带数据下载工具，开箱即用

## 📥 安装

```bash
pip install rqalpha

# 下载数据包
rqalpha download-bundle
```

## 🚀 快速开始

```python
# strategy.py
from rqalpha.api import *

def init(context):
    """策略初始化"""
    context.stock = '000001.XSHE'
    logger.info("策略初始化完成")

def handle_bar(context, bar_dict):
    """每日行情处理"""
    price = bar_dict[context.stock].close
    
    if not context.portfolio.positions:
        order_shares(context.stock, 1000)
        logger.info(f"买入 {context.stock} 1000股")
```

```bash
# 命令行运行回测
rqalpha run -f strategy.py -s 2023-01-01 -e 2024-01-01 --account stock 100000 --plot
```

## 📊 核心功能

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| 下单 | 按股数/金额下单 | `order_shares()` / `order_value()` |
| 目标 | 目标仓位下单 | `order_target_percent()` |
| 行情 | 历史K线数据 | `history_bars()` |
| 账户 | 账户信息 | `context.portfolio` |
| 定时 | 定时任务 | `scheduler.run_daily()` |
| 日志 | 策略日志 | `logger.info()` |

## 📖 更多示例

```python
from rqalpha.api import *

def init(context):
    context.stocks = ['000001.XSHE', '600519.XSHG']
    scheduler.run_daily(rebalance, time_rule=market_open(minute=5))

def rebalance(context, bar_dict):
    """每日开盘5分钟后调仓"""
    target_weight = 1.0 / len(context.stocks)
    for stock in context.stocks:
        order_target_percent(stock, target_weight)

def handle_bar(context, bar_dict):
    # 获取历史数据
    prices = history_bars(context.stocks[0], 20, '1d', 'close')
    portfolio = context.portfolio
    logger.info(f"总资产: {portfolio.total_value}")
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.2.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.1.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持A股和期货事件驱动回测

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://github.com/ricequant/rqalpha
- **ClawHub**：https://clawhub.com
