---
name: tqsdk
description: 天勤量化TqSdk - 开源Python期货/期权交易SDK，提供实时行情、回测和实盘交易功能。
version: 1.1.0
homepage: https://github.com/shinnytech/tqsdk-python
metadata: {"clawdbot":{"emoji":"📡","requires":{"bins":["python3"]}}}
---

# TqSdk（天勤量化SDK）

[TqSdk](https://github.com/shinnytech/tqsdk-python) 是信易科技开发的开源Python期货/期权量化交易SDK。通过统一的异步API提供实时行情、历史数据、回测和实盘交易功能。

> 文档：https://doc.shinnytech.com/tqsdk/latest/
> 免费版提供延时行情（15分钟延迟），专业版支持实时数据。

## 安装

```bash
pip install tqsdk
```

## 快速入门

```python
from tqsdk import TqApi, TqAuth, TqBacktest
from datetime import date

# 实盘模式（免费账户提供延时行情）
api = TqApi(auth=TqAuth("your_username", "your_password"))

# 获取实时行情
quote = api.get_quote("SHFE.cu2401")  # Shanghai copper futures
print(f"最新价: {quote.last_price}, 成交量: {quote.volume}")

# 获取K线数据
klines = api.get_kline_serial("SHFE.cu2401", duration_seconds=60)  # 1-min bars
print(klines.tail())

# 关闭API
api.close()
```

## 代码格式

```
EXCHANGE.CONTRACT
```

| 交易所 | 代码 | 示例 |
|---|---|---|
| 上海期货交易所 | `SHFE` | `SHFE.cu2401`（铜） |
| 大连商品交易所 | `DCE` | `DCE.m2405`（豆粕） |
| 郑州商品交易所 | `CZCE` | `CZCE.CF405`（棉花） |
| 中国金融期货交易所 | `CFFEX` | `CFFEX.IF2401`（沪深300期货） |
| 上海国际能源交易中心 | `INE` | `INE.sc2407`（原油） |
| 广州期货交易所 | `GFEX` | `GFEX.si2407`（工业硅） |
| 上交所期权 | `SSE` | `SSE.10004816`（50ETF期权） |
| 深交所期权 | `SZSE` | `SZSE.90000001`（300ETF期权） |

---

## 行情数据

### 实时行情

```python
from tqsdk import TqApi, TqAuth

api = TqApi(auth=TqAuth("user", "pass"))

quote = api.get_quote("CFFEX.IF2401")
# 关键字段：
# quote.last_price      — 最新价
# quote.bid_price1      — 买一价
# quote.ask_price1      — 卖一价
# quote.bid_volume1     — 买一量
# quote.ask_volume1     — 卖一量
# quote.highest         — 日最高价
# quote.lowest          — 日最低价
# quote.open            — 开盘价
# quote.close           — 昨收价
# quote.volume          — 总成交量
# quote.amount          — 总成交额
# quote.open_interest   — 持仓量
# quote.upper_limit     — 涨停价
# quote.lower_limit     — 跌停价
# quote.pre_settlement  — 昨结算价
# quote.settlement      — 今结算价

# 等待行情更新
while True:
    api.wait_update()
    if api.is_changing(quote, "last_price"):
        print(f"Price update: {quote.last_price}")
```

### K线数据

```python
# 获取K线序列（返回pandas DataFrame）
klines = api.get_kline_serial(
    "SHFE.cu2401",
    duration_seconds=60,     # K线周期：60=1分钟, 300=5分钟, 3600=1小时, 86400=日线
    data_length=200          # 获取K线数量
)
# 列：datetime, open, high, low, close, volume, open_oi, close_oi

# 多周期
klines_1m = api.get_kline_serial("SHFE.cu2401", 60)
klines_5m = api.get_kline_serial("SHFE.cu2401", 300)
klines_1d = api.get_kline_serial("SHFE.cu2401", 86400)
```

### Tick数据

```python
ticks = api.get_tick_serial("SHFE.cu2401", data_length=500)
# 列：datetime, last_price, highest, lowest, bid_price1, ask_price1,
#          bid_volume1, ask_volume1, volume, amount, open_interest
```

---

## 交易

### 下单

```python
from tqsdk import TqApi, TqAuth

api = TqApi(auth=TqAuth("user", "pass"))

# 限价单 — buy open 2 lots
order = api.insert_order(
    symbol="SHFE.cu2401",
    direction="BUY",           # "BUY" or "SELL"
    offset="OPEN",             # "OPEN", "CLOSE", "CLOSETODAY"
    volume=2,                  # Number of lots
    limit_price=68000.0        # Limit price (None for market order)
)

# 市价单（FAK — 即成剩撤）
order = api.insert_order(
    symbol="SHFE.cu2401",
    direction="BUY",
    offset="OPEN",
    volume=2
)

# 撤单
api.cancel_order(order)

# 检查委托状态
while True:
    api.wait_update()
    if order.status == "FINISHED":
        print(f"Order finished: filled={order.volume_orign - order.volume_left}")
        break
```

### 持仓与账户

```python
# 获取账户信息
account = api.get_account()
# account.balance        — 账户余额
# account.available      — 可用资金
# account.margin         — 已用保证金
# account.float_profit   — 浮动盈亏
# account.position_profit — 持仓盈亏
# account.commission     — 今日手续费

# 获取持仓
position = api.get_position("SHFE.cu2401")
# position.pos_long      — 多头持仓量
# position.pos_short     — 空头持仓量
# position.pos_long_today — 今多仓
# position.float_profit_long  — 多头浮动盈亏
# position.float_profit_short — 空头浮动盈亏
# position.open_price_long    — 多头平均开仓价
# position.open_price_short   — 空头平均开仓价
```

---

## 回测

```python
from tqsdk import TqApi, TqAuth, TqBacktest, TqSim
from datetime import date

# 创建回测API
api = TqApi(
    backtest=TqBacktest(
        start_dt=date(2024, 1, 1),
        end_dt=date(2024, 6, 30)
    ),
    account=TqSim(init_balance=1000000),  # 模拟账户，初始资金100万
    auth=TqAuth("user", "pass")
)

# 策略逻辑（同一套代码适用于实盘和回测）
klines = api.get_kline_serial("CFFEX.IF2401", 60 * 60)  # 1-hour bars
position = api.get_position("CFFEX.IF2401")

while True:
    api.wait_update()
    if api.is_changing(klines.iloc[-1], "close"):
        ma5 = klines["close"].iloc[-5:].mean()
        ma20 = klines["close"].iloc[-20:].mean()

        if ma5 > ma20 and position.pos_long == 0:
            api.insert_order("CFFEX.IF2401", "BUY", "OPEN", 1, klines.iloc[-1]["close"])
        elif ma5 < ma20 and position.pos_long > 0:
            api.insert_order("CFFEX.IF2401", "SELL", "CLOSE", 1, klines.iloc[-1]["close"])

api.close()
```

---

## 进阶示例

### 双合约价差交易

```python
from tqsdk import TqApi, TqAuth

api = TqApi(auth=TqAuth("user", "pass"))

quote_near = api.get_quote("SHFE.rb2401")   # Near-month rebar
quote_far = api.get_quote("SHFE.rb2405")    # Far-month rebar
pos_near = api.get_position("SHFE.rb2401")
pos_far = api.get_position("SHFE.rb2405")

SPREAD_OPEN = 100    # 开仓价差阈值
SPREAD_CLOSE = 20    # 平仓价差阈值

while True:
    api.wait_update()
    spread = quote_near.last_price - quote_far.last_price

    if spread > SPREAD_OPEN and pos_near.pos_short == 0:
        # 价差过大：卖近月，买远月
        api.insert_order("SHFE.rb2401", "SELL", "OPEN", 1, quote_near.bid_price1)
        api.insert_order("SHFE.rb2405", "BUY", "OPEN", 1, quote_far.ask_price1)
        print(f"Open spread trade: spread={spread:.0f}")

    elif spread < SPREAD_CLOSE and pos_near.pos_short > 0:
        # 价差收敛：双腿平仓
        api.insert_order("SHFE.rb2401", "BUY", "CLOSE", 1, quote_near.ask_price1)
        api.insert_order("SHFE.rb2405", "SELL", "CLOSE", 1, quote_far.bid_price1)
        print(f"Close spread trade: spread={spread:.0f}")
```

### 基于ATR的止损策略

```python
from tqsdk import TqApi, TqAuth
import numpy as np

api = TqApi(auth=TqAuth("user", "pass"))

symbol = "CFFEX.IF2401"
klines = api.get_kline_serial(symbol, 86400, data_length=50)  # 日线
position = api.get_position(symbol)

ATR_PERIOD = 14
ATR_MULTIPLIER = 2.0
entry_price = 0.0

while True:
    api.wait_update()
    if not api.is_changing(klines.iloc[-1], "close"):
        continue

    # 计算ATR
    highs = klines["high"].iloc[-ATR_PERIOD-1:]
    lows = klines["low"].iloc[-ATR_PERIOD-1:]
    closes = klines["close"].iloc[-ATR_PERIOD-1:]
    tr = np.maximum(highs.values[1:] - lows.values[1:],
                    np.abs(highs.values[1:] - closes.values[:-1]),
                    np.abs(lows.values[1:] - closes.values[:-1]))
    atr = np.mean(tr[-ATR_PERIOD:])

    current_price = klines.iloc[-1]["close"]
    ma20 = klines["close"].iloc[-20:].mean()

    if position.pos_long == 0:
        # 入场：价格在20日均线之上
        if current_price > ma20:
            api.insert_order(symbol, "BUY", "OPEN", 1, current_price)
            entry_price = current_price
            print(f"Entry: price={current_price:.2f}, ATR={atr:.2f}")
    else:
        # ATR跟踪止损
        stop_price = entry_price - ATR_MULTIPLIER * atr
        if current_price < stop_price:
            api.insert_order(symbol, "SELL", "CLOSE", position.pos_long, current_price)
            print(f"Stop loss: price={current_price:.2f}, stop={stop_price:.2f}")

api.close()
```

---

## 使用技巧

- 免费版提供延时行情（15分钟延迟），专业版支持实时数据。
- 同一套代码适用于回测和实盘，只需修改API初始化。
- `api.wait_update()` 是核心事件循环，所有数据更新通过它接收。
- 使用 `api.is_changing()` 检查特定数据是否已更新。
- 支持国内所有主要交易所的期货和期权。
- 文档：https://doc.shinnytech.com/tqsdk/latest/

## 目标持仓助手（TargetPosTask）

TqSdk提供便捷的目标持仓管理工具，自动完成开平仓操作：

```python
from tqsdk import TqApi, TqAuth, TargetPosTask

api = TqApi(auth=TqAuth("user", "pass"))
symbol = "SHFE.cu2401"
target = TargetPosTask(api, symbol)
klines = api.get_kline_serial(symbol, 86400, data_length=30)

while True:
    api.wait_update()
    if api.is_changing(klines.iloc[-1], "close"):
        ma5 = klines["close"].iloc[-5:].mean()
        ma20 = klines["close"].iloc[-20:].mean()
        if ma5 > ma20:
            target.set_target_volume(3)     # 自动调整到多头3手
        elif ma5 < ma20:
            target.set_target_volume(-3)    # 自动调整到空头3手
        else:
            target.set_target_volume(0)     # 自动平仓
api.close()
```

## 期权交易

```python
from tqsdk import TqApi, TqAuth

api = TqApi(auth=TqAuth("user", "pass"))

# 获取期权合约列表
options = api.query_options("SSE.510050")  # 50ETF期权
print(f"共 {len(options)} 个期权合约")

# 获取特定期权行情
quote = api.get_quote("SSE.10004816")
print(f"最新价: {quote.last_price}")
print(f"隐含波动率: {quote.implied_volatility}")
print(f"Delta: {quote.delta}, Gamma: {quote.gamma}")
print(f"Theta: {quote.theta}, Vega: {quote.vega}")
api.close()
```

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `Authentication failed` | 账户密码错误 | 检查TqAuth的用户名密码 |
| `Insufficient margin` | 保证金不足 | 检查 `account.available` |
| `Symbol not found` | 合约代码错误或已过期 | 检查代码格式和合约月份 |
| `Connection lost` | 网络断开 | TqSdk会自动重连 |
| `Backtest data not available` | 历史数据不可用 | 检查回测日期范围 |

## 支持的K线周期

| 周期 | duration_seconds | 说明 |
|------|-----------------|------|
| 3秒 | `3` | 超短线 |
| 5秒 | `5` | 超短线 |
| 10秒 | `10` | 短线 |
| 15秒 | `15` | 短线 |
| 30秒 | `30` | 短线 |
| 1分钟 | `60` | 最常用短线周期 |
| 5分钟 | `300` | 常用日内周期 |
| 15分钟 | `900` | 日内波段 |
| 30分钟 | `1800` | 日内波段 |
| 1小时 | `3600` | 中线周期 |
| 2小时 | `7200` | 中线周期 |
| 4小时 | `14400` | 中线周期 |
| 日线 | `86400` | 趋势跟踪 |

## 进阶示例：海龟交易策略

```python
from tqsdk import TqApi, TqAuth, TargetPosTask
import numpy as np

api = TqApi(auth=TqAuth("user", "pass"))
symbol = "CFFEX.IF2401"
klines = api.get_kline_serial(symbol, 86400, data_length=60)
target = TargetPosTask(api, symbol)

ENTRY_PERIOD = 20    # 唐奇安通道入场周期
EXIT_PERIOD = 10     # 唐奇安通道出场周期
ATR_PERIOD = 20      # ATR周期
RISK_RATIO = 0.01    # 单笔风险比例

while True:
    api.wait_update()
    if not api.is_changing(klines.iloc[-1], "close"):
        continue

    highs = klines["high"].values
    lows = klines["low"].values
    closes = klines["close"].values

    if len(closes) < ENTRY_PERIOD + 1:
        continue

    # 唐奇安通道
    entry_high = np.max(highs[-ENTRY_PERIOD-1:-1])
    entry_low = np.min(lows[-ENTRY_PERIOD-1:-1])
    exit_high = np.max(highs[-EXIT_PERIOD-1:-1])
    exit_low = np.min(lows[-EXIT_PERIOD-1:-1])

    # 计算ATR
    tr = np.maximum(highs[1:] - lows[1:],
                    np.abs(highs[1:] - closes[:-1]),
                    np.abs(lows[1:] - closes[:-1]))
    atr = np.mean(tr[-ATR_PERIOD:])

    current = closes[-1]
    account = api.get_account()
    position = api.get_position(symbol)
    unit_size = max(1, int(account.balance * RISK_RATIO / atr))

    if position.pos_long == 0 and position.pos_short == 0:
        if current > entry_high:
            target.set_target_volume(unit_size)      # 突码20日高点做多
        elif current < entry_low:
            target.set_target_volume(-unit_size)     # 突码20日低点做空
    elif position.pos_long > 0:
        if current < exit_low:
            target.set_target_volume(0)              # 跌码10日低点平多
    elif position.pos_short > 0:
        if current > exit_high:
            target.set_target_volume(0)              # 突码10日高点平空
api.close()
```

## 进阶示例：多品种强弱对冲

```python
from tqsdk import TqApi, TqAuth, TargetPosTask

api = TqApi(auth=TqAuth("user", "pass"))

# 黑色系品种：螺纹钢 vs 铁矿石
symbol_a = "SHFE.rb2405"
symbol_b = "DCE.i2405"
klines_a = api.get_kline_serial(symbol_a, 86400, data_length=30)
klines_b = api.get_kline_serial(symbol_b, 86400, data_length=30)
target_a = TargetPosTask(api, symbol_a)
target_b = TargetPosTask(api, symbol_b)
LOOKBACK = 20

while True:
    api.wait_update()
    if len(klines_a) < LOOKBACK or len(klines_b) < LOOKBACK:
        continue

    ret_a = (klines_a.iloc[-1]["close"] / klines_a.iloc[-LOOKBACK]["close"]) - 1
    ret_b = (klines_b.iloc[-1]["close"] / klines_b.iloc[-LOOKBACK]["close"]) - 1

    if ret_a > ret_b + 0.02:       # 强弱差大于2%
        target_a.set_target_volume(1)    # 做多强势品种
        target_b.set_target_volume(-1)   # 做空弱势品种
    elif ret_a < ret_b - 0.02:     # 强弱反转
        target_a.set_target_volume(0)
        target_b.set_target_volume(0)
api.close()
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
