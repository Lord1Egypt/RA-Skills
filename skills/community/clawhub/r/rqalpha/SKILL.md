---
name: rqalpha
description: RQAlpha 米筐开源事件驱动回测框架 - 支持A股和期货，模块化架构，可自由扩展。
version: 1.1.0
homepage: https://github.com/ricequant/rqalpha
metadata: {"clawdbot":{"emoji":"🍚","requires":{"bins":["python3"]}}}
---

# RQAlpha（米筐开源回测框架）

[RQAlpha](https://github.com/ricequant/rqalpha) 是 [米筐科技](https://www.ricequant.com) 开发的开源事件驱动回测框架。提供A股和期货市场的策略开发、回测和模拟交易完整解决方案。高度模块化，支持插件（Mod）系统扩展。

> Docs: https://rqalpha.readthedocs.io/

## 安装

```bash
pip install rqalpha

# 下载内置数据包（A股日线数据）
rqalpha download-bundle
```

## 策略结构

```python
def init(context):
    """策略启动时调用一次 — 设置订阅和参数"""
    context.stock = '000001.XSHE'
    context.fired = False

def handle_bar(context, bar_dict):
    """每根K线调用 — 主要交易逻辑"""
    if not context.fired:
        order_shares(context.stock, 1000)
        context.fired = True

def before_trading(context):
    """每个交易日开盘前调用"""
    pass

def after_trading(context):
    """每个交易日收盘后调用"""
    pass
```

## 运行回测

### 命令行

```bash
rqalpha run \
    -f strategy.py \
    -s 2024-01-01 \
    -e 2024-06-30 \
    --account stock 100000 \
    --benchmark 000300.XSHG \
    --plot
```

### Python API

```python
from rqalpha.api import *
from rqalpha import run_func

config = {
    "base": {
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "accounts": {"stock": 100000},
        "benchmark": "000300.XSHG",
        "frequency": "1d",
    },
    "extra": {
        "log_level": "warning",
    },
    "mod": {
        "sys_analyser": {"enabled": True, "plot": True},
    },
}

result = run_func(init=init, handle_bar=handle_bar, config=config)
print(result)
```

---

## 代码格式

| 市场 | 后缀 | 示例 |
|---|---|---|
| 上海A股 | `.XSHG` | `600000.XSHG`（浦发银行） |
| 深圳A股 | `.XSHE` | `000001.XSHE`（平安银行） |
| 指数 | `.XSHG/.XSHE` | `000300.XSHG`（沪深300） |
| 期货 | `.XSGE/.XDCE/.XZCE/.CCFX` | `IF2401.CCFX`（沪深300期货） |

---

## 下单函数

```python
# 按股数买卖
order_shares('000001.XSHE', 1000)       # 买入1000股
order_shares('000001.XSHE', -500)       # 卖出500股

# 按手买入（1手=100股）
order_lots('000001.XSHE', 10)           # 买入10手（1000股）

# 按金额买入
order_value('000001.XSHE', 50000)       # 买入5万元

# 按组合比例买入
order_percent('000001.XSHE', 0.5)       # 买入组合值50%的仓位

# 目标仓位
order_target_value('000001.XSHE', 100000)   # 调整到10万元
order_target_percent('000001.XSHE', 0.3)    # 调整到组合的30%

# 撤单
cancel_order(order_id)
```

## 数据查询函数

```python
def handle_bar(context, bar_dict):
    # 当前K线数据
    bar = bar_dict['000001.XSHE']
    price = bar.close
    volume = bar.volume
    dt = bar.datetime

    # 历史数据（返回DataFrame）
    prices = history_bars('000001.XSHE', bar_count=20, frequency='1d',
                          fields=['close', 'volume', 'open', 'high', 'low'])

    # 检查股票是否可交易
    tradable = is_valid_price(bar.close)

    # 检查是否停牌
    suspended = is_suspended('000001.XSHE')
```

## 投资组合与持仓

```python
def handle_bar(context, bar_dict):
    # 组合信息
    cash = context.portfolio.cash                    # 可用资金
    total = context.portfolio.total_value            # 总资产
    market_value = context.portfolio.market_value    # 持仓市值
    pnl = context.portfolio.pnl                      # 总盈亏
    returns = context.portfolio.daily_returns        # 日收益率

    # 持仓信息
    positions = context.portfolio.positions
    for stock, pos in positions.items():
        print(f'{stock}: quantity={pos.quantity}, '
              f'sellable={pos.sellable}, '
              f'avg_price={pos.avg_price:.2f}, '
              f'market_value={pos.market_value:.2f}, '
              f'pnl={pos.pnl:.2f}')
```

## 定时调度

```python
from rqalpha.api import *

def init(context):
    # 每个交易日指定时间运行函数
    scheduler.run_daily(rebalance, time_rule=market_open(minute=5))
    # 每周运行（每周一）
    scheduler.run_weekly(weekly_task, tradingday=1, time_rule=market_open(minute=5))
    # 每月运行（首个交易日）
    scheduler.run_monthly(monthly_task, tradingday=1, time_rule=market_open(minute=5))

def rebalance(context, bar_dict):
    pass
```

---

## Mod系统（插件）

RQAlpha的模块化架构允许通过Mod扩展功能：

```python
config = {
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True,
            "benchmark": "000300.XSHG",
        },
        "sys_simulation": {
            "enabled": True,
            "matching_type": "current_bar",    # 撮合方式：current_bar或next_bar
            "slippage": 0.01,                  # 滑点（元）
        },
        "sys_transaction_cost": {
            "enabled": True,
            "commission_rate": 0.0003,         # 手续费率
            "tax_rate": 0.001,                 # 印花税（仅卖出）
            "min_commission": 5,               # 最低手续费
        },
    },
}
```

### 可用内置Mod

| Mod | 说明 |
|---|---|
| `sys_analyser` | 绩效分析和图表绘制 |
| `sys_simulation` | 撮合模拟 |
| `sys_transaction_cost` | 手续费和税费计算 |
| `sys_accounts` | 账户管理 |
| `sys_benchmark` | 基准追踪 |
| `sys_progress` | 进度条显示 |
| `sys_risk` | 风险管理检查 |

---

## 进阶示例

### 双均线交叉策略

```python
import numpy as np
from rqalpha.api import *

def init(context):
    context.stock = '600000.XSHG'
    context.fast = 5
    context.slow = 20
    scheduler.run_daily(trade_logic, time_rule=market_open(minute=5))

def trade_logic(context, bar_dict):
    prices = history_bars(context.stock, context.slow + 1, '1d', fields=['close'])
    if len(prices) < context.slow:
        return

    closes = prices['close']
    fast_ma = np.mean(closes[-context.fast:])
    slow_ma = np.mean(closes[-context.slow:])

    pos = context.portfolio.positions.get(context.stock)
    has_position = pos is not None and pos.quantity > 0

    if fast_ma > slow_ma and not has_position:
        order_target_percent(context.stock, 0.9)
        logger.info(f'BUY: fast_ma={fast_ma:.2f} > slow_ma={slow_ma:.2f}')
    elif fast_ma < slow_ma and has_position:
        order_target_percent(context.stock, 0)
        logger.info(f'SELL: fast_ma={fast_ma:.2f} < slow_ma={slow_ma:.2f}')

def handle_bar(context, bar_dict):
    pass
```

### 多股等权重调仓

```python
from rqalpha.api import *

def init(context):
    context.stocks = ['600000.XSHG', '000001.XSHE', '601318.XSHG',
                       '600036.XSHG', '000858.XSHE']
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def rebalance(context, bar_dict):
    # 卖出不在目标列表中的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in context.stocks:
            order_target_percent(stock, 0)

    # 等权分配
    weight = 0.95 / len(context.stocks)
    for stock in context.stocks:
        if not is_suspended(stock):
            order_target_percent(stock, weight)
            logger.info(f'Rebalance: {stock} -> {weight:.1%}')

def handle_bar(context, bar_dict):
    pass
```

---

## 使用技巧

- RQAlpha是纯本地框架，无云端依赖，适合离线研究。
- 使用 `rqalpha download-bundle` 获取免费内置A股日线数据。
- Mod系统允许插入自定义数据源、券商接口和风控模块。
- 实盘交易可通过 `rqalpha-mod-vnpy` 连接vn.py的券商网关。
- 支持日线和分钟级回测。
- Docs: https://rqalpha.readthedocs.io/

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `Bundle not found` | 未下载数据包 | 运行 `rqalpha download-bundle` |
| `Insufficient cash` | 可用资金不足 | 检查 `context.portfolio.cash` |
| `Order Creation Failed: suspended` | 股票停牌 | 用 `is_suspended()` 提前检查 |
| `No data for instrument` | 股票代码错误 | 检查代码格式（如 `.XSHG` / `.XSHE`） |

## 绩效分析输出

运行回测后，`sys_analyser` Mod会输出以下指标：

| 指标 | 说明 |
|------|------|
| `total_returns` | 总收益率 |
| `annualized_returns` | 年化收益率 |
| `benchmark_total_returns` | 基准总收益率 |
| `alpha` | Alpha值 |
| `beta` | Beta值 |
| `sharpe` | 夏普比率 |
| `sortino` | Sortino比率 |
| `max_drawdown` | 最大回撤 |
| `tracking_error` | 跟踪误差 |
| `information_ratio` | 信息比率 |
| `volatility` | 波动率 |

## 进阶示例：RSI均值回归策略

```python
import numpy as np
from rqalpha.api import *

def init(context):
    context.stock = '000001.XSHE'
    context.rsi_period = 14
    context.oversold = 30
    context.overbought = 70

def handle_bar(context, bar_dict):
    prices = history_bars(context.stock, context.rsi_period + 2, '1d', fields=['close'])
    if len(prices) < context.rsi_period + 1:
        return

    closes = prices['close']
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-context.rsi_period:])
    avg_loss = np.mean(losses[-context.rsi_period:])

    if avg_loss == 0:
        rsi = 100
    else:
        rsi = 100 - 100 / (1 + avg_gain / avg_loss)

    pos = context.portfolio.positions.get(context.stock)
    has_pos = pos is not None and pos.quantity > 0

    if rsi < context.oversold and not has_pos:
        order_target_percent(context.stock, 0.9)
        logger.info(f'RSI={rsi:.1f} 超卖买入')
    elif rsi > context.overbought and has_pos:
        order_target_percent(context.stock, 0)
        logger.info(f'RSI={rsi:.1f} 超买卖出')
```

## 进阶示例：止损止盈策略

```python
from rqalpha.api import *
import numpy as np

def init(context):
    context.stock = '600519.XSHG'
    context.entry_price = 0
    context.stop_loss = 0.05
    context.take_profit = 0.15
    scheduler.run_daily(trade, time_rule=market_open(minute=5))

def trade(context, bar_dict):
    bar = bar_dict[context.stock]
    price = bar.close
    prices = history_bars(context.stock, 21, '1d', fields=['close'])
    ma20 = np.mean(prices['close'][-20:])

    pos = context.portfolio.positions.get(context.stock)
    has_pos = pos is not None and pos.quantity > 0

    if not has_pos:
        if price > ma20:
            order_target_percent(context.stock, 0.9)
            context.entry_price = price
            logger.info(f'买入: price={price:.2f}, ma20={ma20:.2f}')
    else:
        if context.entry_price > 0:
            pnl = (price - context.entry_price) / context.entry_price
            if pnl <= -context.stop_loss:
                order_target_percent(context.stock, 0)
                logger.info(f'止损: pnl={pnl:.2%}')
                context.entry_price = 0
            elif pnl >= context.take_profit:
                order_target_percent(context.stock, 0)
                logger.info(f'止盈: pnl={pnl:.2%}')
                context.entry_price = 0

def handle_bar(context, bar_dict):
    pass
```

## 进阶示例：期货双均线CTA策略

```python
import numpy as np
from rqalpha.api import *

def init(context):
    context.symbol = 'IF2401.CCFX'
    context.fast = 5
    context.slow = 20

def handle_bar(context, bar_dict):
    prices = history_bars(context.symbol, context.slow + 1, '1d', fields=['close'])
    if len(prices) < context.slow:
        return

    closes = prices['close']
    fast_ma = np.mean(closes[-context.fast:])
    slow_ma = np.mean(closes[-context.slow:])
    prev_fast = np.mean(closes[-context.fast-1:-1])
    prev_slow = np.mean(closes[-context.slow-1:-1])

    pos = context.portfolio.positions.get(context.symbol)
    long_qty = pos.buy_quantity if pos else 0

    if prev_fast <= prev_slow and fast_ma > slow_ma and long_qty == 0:
        buy_open(context.symbol, 1)
        logger.info(f'开多: fast_ma={fast_ma:.2f} > slow_ma={slow_ma:.2f}')
    elif prev_fast >= prev_slow and fast_ma < slow_ma and long_qty > 0:
        sell_close(context.symbol, long_qty)
        logger.info(f'平多: fast_ma={fast_ma:.2f} < slow_ma={slow_ma:.2f}')
```

---

---

## 🤖 AI Agent 高阶使用指南

对于 AI Agent，在使用该量化/数据工具时应遵循以下高阶策略和最佳实践，以确保任务的高效完成：

### 1. 数据校验与错误处理
在获取数据或执行操作后，AI 应当主动检查返回的结果格式是否符合预期，以及是否存在缺失值（NaN）或空数据。
* **示例策略**：在通过 API 获取数据框（DataFrame）后，使用 `if df.empty:` 进行校验；捕获 `Exception` 以防网络或接口错误导致进程崩溃。

### 2. 多步组合分析
AI 经常需要进行宏观经济分析或跨市场对比。应善于将当前接口与其他数据源或工具组合使用。
* **示例策略**：先获取板块或指数的宏观数据，再筛选成分股，最后对具体标的进行深入的财务或技术面分析，形成完整的决策链条。

### 3. 构建动态监控与日志
对于交易和策略类任务，AI 可以定期拉取数据并建立监控机制。
* **示例策略**：使用循环或定时任务检查特定标的的异动（如涨跌停、放量），并在发现满足条件的信号时输出结构化日志或触发预警。

---

## 社区与支持

由 **大佬量化** 维护 — 量化交易教学与策略研发团队。

微信客服: **bossquant1** · [Bilibili](https://space.bilibili.com/48693330) · 搜索 **大佬量化** — 微信公众号 / Bilibili / 抖音
