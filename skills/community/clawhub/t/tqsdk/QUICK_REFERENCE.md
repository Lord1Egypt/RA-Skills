# TqSdk API 快速参考

本文档提供最常用的 TqSdk 天勤期货 API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 初始化

```python
from tqsdk import TqApi, TqAuth

# 创建API实例（实盘模式）
api = TqApi(auth=TqAuth("your_username", "your_password"))
```

## 创建API

```python
from tqsdk import TqApi, TqAuth, TqSim, TqBacktest
from datetime import date

# 模拟交易
api = TqApi(TqSim(), auth=TqAuth("username", "password"))

# 实盘交易（需要期货账户）
api = TqApi(TqAccount("broker", "account", "password"), auth=TqAuth("username", "password"))
```

## 实时行情

```python
# 获取实时行情
quote = api.get_quote("SHFE.rb2501")
print(f"最新价: {quote.last_price}")
print(f"买一价: {quote.bid_price1}, 卖一价: {quote.ask_price1}")
print(f"成交量: {quote.volume}, 持仓量: {quote.open_interest}")
```

## K线数据

```python
# 1分钟K线（最近200根）
klines = api.get_kline_serial("SHFE.rb2501", duration_seconds=60)

# 5分钟K线
klines_5m = api.get_kline_serial("SHFE.rb2501", duration_seconds=300)

# 日K线
klines_daily = api.get_kline_serial("SHFE.rb2501", duration_seconds=86400)

# 返回 DataFrame，包含 open, high, low, close, volume 等字段
```

## 下单交易

```python
# 开多仓（限价单）
order = api.insert_order("SHFE.rb2501", direction="BUY", offset="OPEN", volume=1, limit_price=3800)

# 开空仓
order = api.insert_order("SHFE.rb2501", direction="SELL", offset="OPEN", volume=1, limit_price=3900)

# 平多仓
order = api.insert_order("SHFE.rb2501", direction="SELL", offset="CLOSE", volume=1, limit_price=3850)

# 市价单（不指定 limit_price）
order = api.insert_order("SHFE.rb2501", direction="BUY", offset="OPEN", volume=1)

# 撤单
api.cancel_order(order)
```

## 持仓查询

```python
# 获取持仓
position = api.get_position("SHFE.rb2501")
print(f"多头持仓: {position.pos_long}")
print(f"空头持仓: {position.pos_short}")
print(f"多头均价: {position.open_price_long}")
print(f"持仓盈亏: {position.float_profit_long}")
```

## 账户信息

```python
# 获取账户信息
account = api.get_account()
print(f"账户权益: {account.balance}")
print(f"可用资金: {account.available}")
print(f"持仓盈亏: {account.float_profit}")
print(f"保证金: {account.margin}")
```

## 回测模式

```python
from tqsdk import TqApi, TqAuth, TqBacktest
from datetime import date

# 创建回测API
api = TqApi(
    backtest=TqBacktest(start_dt=date(2023, 1, 1), end_dt=date(2024, 1, 1)),
    auth=TqAuth("username", "password")
)

# 回测逻辑与实盘代码完全一致
quote = api.get_quote("SHFE.rb2501")
while True:
    api.wait_update()
    # 策略逻辑...
```

## 更多资源

- [TqSdk 官方文档](https://doc.shinnytech.com/tqsdk/latest/)
- [GitHub](https://github.com/shinnytech/tqsdk-python)
