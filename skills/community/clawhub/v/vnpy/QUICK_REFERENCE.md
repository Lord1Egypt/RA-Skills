# vn.py API 快速参考

本文档提供最常用的 vn.py 策略开发接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## CTA策略基类

```python
from vnpy_ctastrategy import CtaTemplate

class MyStrategy(CtaTemplate):
    author = "量化开发者"

    # 策略参数
    fast_window = 10
    slow_window = 20

    def on_init(self):
        """策略初始化"""
        self.load_bar(10)

    def on_start(self):
        """策略启动"""
        pass

    def on_bar(self, bar):
        """K线回调"""
        pass
```

## 下单接口

```python
# 买入开仓（做多）
self.buy(price, volume)

# 卖出平仓（平多）
self.sell(price, volume)

# 卖出开仓（做空）
self.short(price, volume)

# 买入平仓（平空）
self.cover(price, volume)

# 撤销所有委托
self.cancel_all()
```

## ArrayManager 技术指标

```python
from vnpy_ctastrategy import ArrayManager

am = ArrayManager(size=100)
am.update_bar(bar)

if am.inited:
    # 均线指标
    sma = am.sma(20)           # 简单移动平均
    ema = am.ema(20)           # 指数移动平均

    # MACD
    macd, signal, hist = am.macd(12, 26, 9)

    # RSI
    rsi = am.rsi(14)

    # 布林带
    upper, middle, lower = am.boll(20, 2)

    # ATR
    atr = am.atr(14)
```

## BarGenerator K线合成

```python
from vnpy_ctastrategy import BarGenerator

# 1分钟合成5分钟
bg = BarGenerator(self.on_bar, 5, self.on_5min_bar)

# 1分钟合成15分钟
bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)

# 1分钟合成1小时
bg = BarGenerator(self.on_bar, 1, self.on_hour_bar, interval=Interval.HOUR)

def on_tick(self, tick):
    self.bg.update_tick(tick)

def on_bar(self, bar):
    self.bg.update_bar(bar)
```

## 策略生命周期

| 方法 | 说明 | 触发时机 |
|------|------|----------|
| `on_init()` | 初始化 | 策略加载时 |
| `on_start()` | 启动 | 策略启动时 |
| `on_stop()` | 停止 | 策略停止时 |
| `on_tick(tick)` | Tick回调 | 收到Tick时 |
| `on_bar(bar)` | K线回调 | K线完成时 |
| `on_trade(trade)` | 成交回调 | 委托成交时 |
| `on_order(order)` | 委托回调 | 委托状态变化时 |

## 更多接口

完整接口列表请查看：
- [vn.py 官方文档](https://www.vnpy.com/docs)
- [GitHub](https://github.com/vnpy/vnpy)
