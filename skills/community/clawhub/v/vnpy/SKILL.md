---
name: vnpy
description: vn.py 开源量化交易框架 - 支持CTA、价差、期权策略，20+券商接口，覆盖国内外市场。
version: 1.1.0
homepage: https://www.vnpy.com
metadata: {"clawdbot":{"emoji":"🐍","requires":{"bins":["python3"]}}}
---

# vn.py（开源量化交易框架）

[vn.py](https://www.vnpy.com) is the most popular open-source quantitative trading framework in China, community-driven. Supports CTA strategies, spread trading, options volatility trading, and more. Connects to CTP, Femas, Hundsun, and 20+ broker gateways.

> Docs: https://www.vnpy.com/docs/cn/
> GitHub: https://github.com/vnpy/vnpy

## 安装

```bash
# Install core framework
pip install vnpy

# Install CTP gateway (futures)
pip install vnpy-ctp

# Install common components
pip install vnpy-ctastrategy    # CTA strategy module
pip install vnpy-spreadtrading  # Spread trading module
pip install vnpy-datamanager    # Data management module
pip install vnpy-sqlite         # SQLite database
pip install vnpy-rqdata         # RQData data service
```

## 架构概述

```
VeighNa Trader (GUI)
    ├── Gateway (Broker Interface)
    │   ├── CTP (Futures)
    │   ├── Femas (Futures)
    │   ├── Hundsun UFT (Securities)
    │   ├── EMT (Securities)
    │   └── IB / Alpaca (International)
    ├── App (Application Modules)
    │   ├── CtaStrategy (CTA Strategy)
    │   ├── SpreadTrading (Spread Trading)
    │   ├── OptionMaster (Options Trading)
    │   ├── PortfolioStrategy (Portfolio Strategy)
    │   └── AlgoTrading (Algorithmic Trading)
    └── DataService
        ├── RQData
        ├── TuShare
        └── Custom Data Sources
```

## 启动GUI

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# Import broker gateways
from vnpy_ctp import CtpGateway

# Import application modules
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_spreadtrading import SpreadTradingApp
from vnpy_datamanager import DataManagerApp

# Create application
qapp = create_qapp()
event_engine = EventEngine()
main_engine = MainEngine(event_engine)

# Add broker gateways
main_engine.add_gateway(CtpGateway)

# Add application modules
main_engine.add_app(CtaStrategyApp)
main_engine.add_app(SpreadTradingApp)
main_engine.add_app(DataManagerApp)

# Create and show main window
main_window = MainWindow(main_engine, event_engine)
main_window.showMaximized()
qapp.exec()
```

---

## CTA策略开发

CTA (Commodity Trading Advisor) strategies are the core strategy type in vn.py, suitable for trend following, mean reversion, etc.

### 策略模板

```python
from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)

class DoubleMaStrategy(CtaTemplate):
    """Dual Moving Average CTA Strategy"""
    author = "Quant Developer"

    # Strategy parameters (editable in GUI)
    fast_window = 10       # 快速均线周期
    slow_window = 20       # 慢速均线周期
    fixed_size = 1         # 每次交易手数

    # Strategy variables (displayed in GUI)
    fast_ma0 = 0.0
    slow_ma0 = 0.0

    # Parameter and variable lists (for GUI display and persistence)
    parameters = ["fast_window", "slow_window", "fixed_size"]
    variables = ["fast_ma0", "slow_ma0"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # Bar generator: synthesize ticks into 1-min bars, then into N-min bars
        self.bg = BarGenerator(self.on_bar)
        # Array manager: store bar data and compute technical indicators
        self.am = ArrayManager(size=100)  # Keep last 100 bars

    def on_init(self):
        """Strategy initialization — load historical data"""
        self.write_log("Strategy initializing")
        self.load_bar(10)  # Load last 10 days of historical bars

    def on_start(self):
        """Strategy started"""
        self.write_log("Strategy started")

    def on_stop(self):
        """Strategy stopped"""
        self.write_log("Strategy stopped")

    def on_tick(self, tick: TickData):
        """Tick data callback — synthesize into bars"""
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """Bar data callback — main trading logic"""
        self.am.update_bar(bar)
        if not self.am.inited:
            return  # Not enough data, wait

        # Calculate fast and slow moving averages
        fast_ma = self.am.sma(self.fast_window, array=False)
        slow_ma = self.am.sma(self.slow_window, array=False)

        # Detect golden cross / death cross
        cross_over = fast_ma > slow_ma    # 金叉
        cross_below = fast_ma < slow_ma   # 死叉

        if cross_over:
            if self.pos == 0:
                self.buy(bar.close_price, self.fixed_size)    # No position, go long
            elif self.pos < 0:
                self.cover(bar.close_price, abs(self.pos))    # Close short first
                self.buy(bar.close_price, self.fixed_size)    # Then go long

        elif cross_below:
            if self.pos == 0:
                self.short(bar.close_price, self.fixed_size)  # No position, go short
            elif self.pos > 0:
                self.sell(bar.close_price, abs(self.pos))     # Close long first
                self.short(bar.close_price, self.fixed_size)  # Then go short

        # Update GUI display variables
        self.fast_ma0 = fast_ma
        self.slow_ma0 = slow_ma
        self.put_event()  # Trigger GUI update

    def on_order(self, order: OrderData):
        """Order status update"""
        pass

    def on_trade(self, trade: TradeData):
        """Trade execution callback"""
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """Stop order status update"""
        pass
```

---

## 交易函数参考

| Method | Description |
|---|---|
| `self.buy(price, volume)` | Buy to open long position |
| `self.sell(price, volume)` | Sell to close long position |
| `self.short(price, volume)` | Sell to open short position |
| `self.cover(price, volume)` | Buy to close short position |
| `self.cancel_all()` | Cancel all pending orders |
| `self.write_log(msg)` | Write log message |
| `self.put_event()` | Trigger GUI update |
| `self.load_bar(days)` | Load N days of historical bars |
| `self.load_tick(days)` | Load N days of historical ticks |

## ArrayManager技术指标方法

The `ArrayManager` provides built-in technical indicator calculations:

```python
am = ArrayManager(size=100)

# Moving Averages
am.sma(n, array=False)          # Simple Moving Average
am.ema(n, array=False)          # Exponential Moving Average
am.kama(n, array=False)         # Kaufman Adaptive Moving Average

# Volatility
am.std(n, array=False)          # Standard Deviation
am.atr(n, array=False)          # Average True Range

# Momentum
am.rsi(n, array=False)          # Relative Strength Index
am.cci(n, array=False)          # Commodity Channel Index
am.macd(fast, slow, signal)     # MACD (returns dif, dea, macd)
am.adx(n, array=False)          # Average Directional Index

# Bollinger Bands
am.boll(n, dev, array=False)    # 收益率 (upper, lower) bands

# Donchian Channel
am.donchian(n, array=False)     # 收益率 (upper, lower) channel

# Other
am.aroon(n, array=False)        # Aroon indicator
am.trix(n, array=False)         # Triple EMA
```

---

## BarGenerator — 多周期K线

```python
from vnpy_ctastrategy import BarGenerator

class MyStrategy(CtaTemplate):
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # Synthesize ticks into 1-min bars, then 1-min bars into 15-min bars
        self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am = ArrayManager()

    def on_tick(self, tick: TickData):
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """1-minute bar callback — feed into 15-min generator"""
        self.bg.update_bar(bar)

    def on_15min_bar(self, bar: BarData):
        """15-minute bar callback — main trading logic"""
        self.am.update_bar(bar)
        if not self.am.inited:
            return
        # Trading logic here
```

Supported intervals for BarGenerator:
- Minutes: 1, 3, 5, 15, 30, 60
- Hours: pass `Interval.HOUR` as the interval parameter
- Custom: any integer N for N-minute bars

---

## 价差交易

```python
from vnpy_spreadtrading import (
    SpreadStrategyTemplate,
    SpreadAlgoTemplate,
    SpreadData,
    LegData,
    BacktestingEngine,
)

class SpreadArbitrageStrategy(SpreadStrategyTemplate):
    """Simple spread arbitrage strategy"""
    author = "Quant Developer"

    buy_price = 0.0
    sell_price = 0.0
    max_pos = 10
    payup = 10

    parameters = ["buy_price", "sell_price", "max_pos", "payup"]

    def on_init(self):
        self.write_log("Strategy initializing")

    def on_start(self):
        self.write_log("Strategy started")

    def on_spread_data(self):
        """Spread data update callback"""
        spread = self.get_spread_tick()
        if not spread:
            return

        if self.spread_pos < self.max_pos:
            if spread.last_price <= self.buy_price:
                self.start_long_algo(
                    spread.last_price, self.max_pos - self.spread_pos,
                    payup=self.payup
                )

        if self.spread_pos > -self.max_pos:
            if spread.last_price >= self.sell_price:
                self.start_short_algo(
                    spread.last_price, self.max_pos + self.spread_pos,
                    payup=self.payup
                )
```

---

## 实盘交易配置

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp

# Initialize engine
event_engine = EventEngine()
main_engine = MainEngine(event_engine)
main_engine.add_gateway(CtpGateway)
cta_engine = main_engine.add_app(CtaStrategyApp)

# Connect to CTP broker
ctp_setting = {
    "userid": "your_user_id",
    "password": "your_password",
    "brokerid": "9999",
    "td_address": "tcp://180.168.146.187:10201",
    "md_address": "tcp://180.168.146.187:10211",
    "appid": "simnow_client_test",
    "auth_code": "0000000000000000",
}
main_engine.connect(ctp_setting, "CTP")

# Initialize CTA engine and add strategy
cta_engine.init_engine()
cta_engine.add_strategy(
    DoubleMaStrategy,
    "double_ma_IF",
    "IF2401.CFFEX",
    {"fast_window": 10, "slow_window": 20}
)
cta_engine.init_strategy("double_ma_IF")
cta_engine.start_strategy("double_ma_IF")
```

---

## 数据管理

```python
from vnpy_datamanager import DataManagerApp

# Add data manager to main engine
dm_engine = main_engine.add_app(DataManagerApp)

# Download historical data from RQData
dm_engine.download_bar_data(
    symbol="IF2401",
    exchange="CFFEX",
    interval="1m",
    start=datetime(2024, 1, 1)
)
```

---

## 进阶示例

### RSI均值回归策略

```python
from vnpy_ctastrategy import CtaTemplate, BarData, BarGenerator, ArrayManager

class RsiStrategy(CtaTemplate):
    """RSI mean reversion strategy — buy oversold, sell overbought"""
    author = "Quant Developer"

    rsi_period = 14
    rsi_buy = 30       # Oversold threshold
    rsi_sell = 70      # Overbought threshold
    fixed_size = 1

    parameters = ["rsi_period", "rsi_buy", "rsi_sell", "fixed_size"]
    variables = ["rsi_value"]

    rsi_value = 0.0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am = ArrayManager()

    def on_init(self):
        self.write_log("Strategy initializing")
        self.load_bar(10)

    def on_start(self):
        self.write_log("Strategy started")

    def on_stop(self):
        self.write_log("Strategy stopped")

    def on_tick(self, tick):
        self.bg.update_tick(tick)

    def on_bar(self, bar):
        self.bg.update_bar(bar)

    def on_15min_bar(self, bar: BarData):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        self.rsi_value = self.am.rsi(self.rsi_period)

        if self.pos == 0:
            if self.rsi_value < self.rsi_buy:
                self.buy(bar.close_price, self.fixed_size)
            elif self.rsi_value > self.rsi_sell:
                self.short(bar.close_price, self.fixed_size)
        elif self.pos > 0:
            if self.rsi_value > self.rsi_sell:
                self.sell(bar.close_price, abs(self.pos))
                self.short(bar.close_price, self.fixed_size)
        elif self.pos < 0:
            if self.rsi_value < self.rsi_buy:
                self.cover(bar.close_price, abs(self.pos))
                self.buy(bar.close_price, self.fixed_size)

        self.put_event()

    def on_order(self, order):
        pass

    def on_trade(self, trade):
        self.put_event()

    def on_stop_order(self, stop_order):
        pass
```

### 布林带突破策略

```python
from vnpy_ctastrategy import CtaTemplate, BarData, BarGenerator, ArrayManager

class BollBreakoutStrategy(CtaTemplate):
    """Bollinger Band breakout strategy with ATR-based stop loss"""
    author = "Quant Developer"

    boll_period = 20
    boll_dev = 2.0
    atr_period = 14
    atr_multiplier = 2.0
    fixed_size = 1

    parameters = ["boll_period", "boll_dev", "atr_period", "atr_multiplier", "fixed_size"]
    variables = ["boll_up", "boll_down", "atr_value"]

    boll_up = 0.0
    boll_down = 0.0
    atr_value = 0.0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar, 30, self.on_30min_bar)
        self.am = ArrayManager()

    def on_init(self):
        self.write_log("Strategy initializing")
        self.load_bar(10)

    def on_start(self):
        self.write_log("Strategy started")

    def on_stop(self):
        self.write_log("Strategy stopped")

    def on_tick(self, tick):
        self.bg.update_tick(tick)

    def on_bar(self, bar):
        self.bg.update_bar(bar)

    def on_30min_bar(self, bar: BarData):
        self.cancel_all()
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        self.boll_up, self.boll_down = self.am.boll(self.boll_period, self.boll_dev)
        self.atr_value = self.am.atr(self.atr_period)

        if self.pos == 0:
            # Breakout above upper band — go long
            if bar.close_price > self.boll_up:
                self.buy(bar.close_price, self.fixed_size)
            # Breakout below lower band — go short
            elif bar.close_price < self.boll_down:
                self.short(bar.close_price, self.fixed_size)
        elif self.pos > 0:
            # Stop loss: ATR trailing stop
            stop_price = bar.close_price - self.atr_value * self.atr_multiplier
            self.sell(stop_price, abs(self.pos), stop=True)
        elif self.pos < 0:
            stop_price = bar.close_price + self.atr_value * self.atr_multiplier
            self.cover(stop_price, abs(self.pos), stop=True)

        self.put_event()

    def on_order(self, order):
        pass

    def on_trade(self, trade):
        self.put_event()

    def on_stop_order(self, stop_order):
        pass
```

---

## 支持的接口

| Gateway | Market | Protocol |
|---|---|---|
| CTP | China Futures | CTP |
| Femas | China Futures | Femas |
| Hundsun UFT | China Securities | UFT |
| EMT | China Securities | EMT |
| XTP | China Securities | XTP |
| IB | International | TWS API |
| Alpaca | US Stocks | REST API |
| Binance | Crypto | REST/WebSocket |

## 使用技巧

- vn.py is the go-to framework for live trading in Chinese futures and securities markets.
- Use `BarGenerator` to synthesize multi-timeframe bars from tick data.
- `ArrayManager` provides 20+ built-in technical indicators — no need for external libraries.
- For backtesting, use the built-in `BacktestingEngine` in `vnpy_ctastrategy`.
- CTP gateway requires a broker account with CTP access (e.g., SimNow for testing).
- The modular architecture allows mixing gateways and strategy types freely.
- Docs: https://www.vnpy.com/docs/cn/

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
