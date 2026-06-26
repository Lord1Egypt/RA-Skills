# 策略详解

## MaVolumeStrategy · 均线金叉 + 放量

**选股逻辑：**
1. MA5 上穿 MA20（金叉）
2. 当日成交量 > 20日均量的 1.5 倍

**默认参数：**
```python
MA_SHORT = 5    # 短周期均线
MA_LONG  = 20   # 长周期均线
VOL_MULT = 1.5  # 放量倍数
```

**调整建议：**
- 保守（少选）：MA_SHORT=10, MA_LONG=60, VOL_MULT=2.0
- 激进（多选）：MA_SHORT=3, MA_LONG=10, VOL_MULT=1.2

---

## TurtleTradeStrategy · 海龟交易

**选股逻辑：**
1. 今日收盘 > 前20日最高价（突破新高）
2. 成交额 > 1亿元
3. 今日实体阳线且真涨（过滤诱多）

**默认参数：**
```python
BREAKOUT_WINDOW = 20     # 突破前N日高点
MIN_TURNOVER    = 100_000_000  # 最低成交额（元）
```

**调整建议：**
- 保守：BREAKOUT_WINDOW=55（季线突破）, MIN_TURNOVER=200_000_000
- 激进：BREAKOUT_WINDOW=10, MIN_TURNOVER=5000_0000

---

## HighTightFlagStrategy · 高旗形整理

**选股逻辑：**
1. 40日内区间最高/最低 > 1.6（强动量，涨幅>60%）
2. 近10日区间最高/最低 < 1.15（极度收敛，振幅<15%）
3. 近10日最低价 > 40日最高价的80%（高位抗跌）
4. 今日成交量 < 20日均量的60%（缩量）

**默认参数：**
```python
MOMENTUM_RATIO   = 1.6   # 40日动量要求
CONSOLIDATION    = 1.15  # 10日收敛上限
HIGH_LEVEL       = 0.8   # 近10日低点相对40日高点的最低比例
SHRINK_RATIO     = 0.6   # 缩量比例上限
```

**调整建议：**
- 保守：MOMENTUM_RATIO=2.0（涨幅>100%才考虑）, CONSOLIDATION=1.10
- 激进：MOMENTUM_RATIO=1.4, CONSOLIDATION=1.20, SHRINK_RATIO=0.8

---

## LimitUpShakeoutStrategy · 涨停洗盘

**选股逻辑：**
涨停后回调筛选（详见源码）。

---

## UptrendLimitDownStrategy · 趋势中跌停

**选股逻辑：**
上升趋势中遭遇跌停的股票（详见源码）。

---

## RpsBreakoutStrategy · RPS突破

**选股逻辑：**
相对强度筛选（详见源码）。

---

## 添加自定义策略模板

```python
from sequoia_x.strategy.base import BaseStrategy

class MyStrategy(BaseStrategy):
    webhook_key: str = "my_strategy"

    def run(self) -> list[str]:
        symbols = self.engine.get_local_symbols()
        selected: list[str] = []

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < 20:
                    continue

                # 在这里写你的选股逻辑
                # df 包含: open, high, low, close, volume, turnover, symbol, date

                if <条件满足>:
                    selected.append(symbol)

            except Exception as exc:
                continue

        return selected
```

添加完策略后，在 `main.py` 的 `strategies` 列表中追加即可。
