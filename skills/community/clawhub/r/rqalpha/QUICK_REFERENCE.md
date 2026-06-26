# RQAlpha API 快速参考

本文档提供最常用的 RQAlpha 米筐回测 API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 策略框架

```python
from rqalpha.api import *

def init(context):
    """策略初始化，启动时执行一次"""
    context.stock = '000001.XSHE'

def handle_bar(context, bar_dict):
    """每日行情处理"""
    pass
```

## 下单交易

```python
# 按股数下单
order_shares('000001.XSHE', 1000)    # 买入1000股
order_shares('000001.XSHE', -500)    # 卖出500股

# 按金额下单
order_value('000001.XSHE', 50000)    # 买入5万元

# 目标股数
order_target_value('000001.XSHE', 100000)  # 调整到10万元市值
```

## 目标仓位下单

```python
# 目标仓位百分比
order_target_percent('000001.XSHE', 0.3)   # 调整到30%仓位
order_target_percent('000001.XSHE', 0)     # 清仓
```

## 获取历史数据

```python
# 获取历史K线
prices = history_bars('000001.XSHE', 20, '1d', 'close')
# 返回 numpy array

# 获取多个字段
bars = history_bars('000001.XSHE', 10, '1d', ['open', 'high', 'low', 'close', 'volume'])

# 分钟级数据
bars_5m = history_bars('000001.XSHE', 48, '5m', 'close')
```

## 账户信息

```python
# 通过 context.portfolio 获取账户信息
portfolio = context.portfolio
print(f"总资产: {portfolio.total_value}")
print(f"可用资金: {portfolio.cash}")
print(f"持仓市值: {portfolio.market_value}")

# 持仓信息
positions = context.portfolio.positions
for stock, pos in positions.items():
    print(f"{stock}: 数量={pos.quantity}, 市值={pos.market_value}")
```

## 定时任务

```python
def init(context):
    # 每日开盘后5分钟执行
    scheduler.run_daily(rebalance, time_rule=market_open(minute=5))
    
    # 每周一执行
    scheduler.run_weekly(weekly_task, weekday=1, tradingday=1)
    
    # 每月第一个交易日执行
    scheduler.run_monthly(monthly_task, tradingday=1)

def rebalance(context, bar_dict):
    logger.info("执行调仓")

def weekly_task(context, bar_dict):
    logger.info("每周任务")

def monthly_task(context, bar_dict):
    logger.info("每月任务")
```

## 命令行运行

```bash
# 基本回测
rqalpha run -f strategy.py -s 2023-01-01 -e 2024-01-01 --account stock 100000

# 带图表输出
rqalpha run -f strategy.py -s 2023-01-01 -e 2024-01-01 --account stock 100000 --plot

# 期货回测
rqalpha run -f strategy.py -s 2023-01-01 -e 2024-01-01 --account future 1000000
```

## 更多资源

- [RQAlpha 官方文档](https://rqalpha.readthedocs.io/)
- [GitHub](https://github.com/ricequant/rqalpha)
