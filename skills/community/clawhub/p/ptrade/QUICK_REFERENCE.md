# Ptrade API 快速参考

本文档提供最常用的 Ptrade 恒生量化 API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 策略框架

```python
def initialize(context):
    """策略初始化，启动时执行一次"""
    set_universe(['600519.SS', '000858.SZ'])

def handle_data(context, data):
    """行情事件处理，每个交易bar执行"""
    pass
```

## 设置股票池

```python
# 设置股票池
set_universe(['600519.SS', '000858.SZ', '000001.SZ'])
```

## 获取行情数据

```python
# 获取历史K线
df = get_history(10, '1d', 'close', security_list='600519.SS')

# 获取当前价格
price = get_price('600519.SS')

# 获取实时快照（Level2）
snapshot = get_snapshot('600519.SS')
# 返回：last_px, open_px, high_px, low_px, volume, amount 等
```

## 下单交易

```python
# 按数量下单（买入100股）
order('600519.SS', 100)

# 按数量下单（卖出100股）
order('600519.SS', -100)

# 目标持仓下单（调整到500股）
order_target('600519.SS', 500)

# 按金额下单
order_value('600519.SS', 100000)
```

## 查询持仓

```python
# 获取所有持仓
positions = get_position()
for stock, pos in positions.items():
    print(f"{stock}: 数量={pos.amount}, 可用={pos.available}")
```

## 账户信息

```python
# 通过 context.portfolio 获取账户信息
portfolio = context.portfolio
print(f"总资产: {portfolio.total_value}")
print(f"可用资金: {portfolio.available_cash}")
print(f"持仓市值: {portfolio.positions_value}")
```

## 定时任务

```python
def initialize(context):
    # 每日定时执行
    run_daily(context, market_open, time='09:31')
    run_daily(context, market_close, time='14:55')
    
    # 间隔执行（每60秒）
    run_interval(context, check_signal, seconds=60)

def market_open(context):
    log.info("开盘任务执行")

def market_close(context):
    log.info("收盘任务执行")

def check_signal(context):
    log.info("定时检查信号")
```

## 更多资源

- [Ptrade 官方文档](https://ptradeapi.com)
- 联系券商获取 Ptrade 开通权限
