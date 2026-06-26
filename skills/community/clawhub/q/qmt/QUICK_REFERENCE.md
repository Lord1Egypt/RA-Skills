# QMT API 快速参考

本文档提供最常用的 QMT 迅投量化 API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 策略框架

```python
def init(ContextInfo):
    """策略初始化，启动时执行一次"""
    ContextInfo.set_universe(['600519.SH', '000858.SZ'])

def handlebar(ContextInfo):
    """每个bar执行"""
    pass
```

## 获取行情数据

```python
# 获取实时/历史行情
data = ContextInfo.get_market_data(
    ['close', 'open', 'high', 'low', 'volume'],
    stock_code=['600519.SH'],
    period='1d',
    count=10
)
# 返回 DataFrame，字段为列，时间为索引
```

## 获取历史数据

```python
# 获取历史K线
history = ContextInfo.get_history_data(10, '1d', 'close')
# 返回字典 {stock_code: [close_values]}

# 指定周期
history_5m = ContextInfo.get_history_data(20, '5m', 'close')
```

## 下单交易

```python
# 买入股票（100股，市价委托）
order_shares('600519.SH', 100, 'fix', 0, ContextInfo, '市价委托')

# 卖出股票
order_shares('600519.SH', -100, 'fix', 0, ContextInfo, '市价委托')

# 限价委托
order_shares('600519.SH', 100, 'fix', 1800.00, ContextInfo, '限价委托')
```

## 查询持仓与委托

```python
# 查询持仓
positions = get_trade_detail_data('account_id', 'stock', 'position')
for pos in positions:
    print(f"代码: {pos.m_strInstrumentID}")
    print(f"数量: {pos.m_nVolume}")
    print(f"可用: {pos.m_nCanUseVolume}")

# 查询委托
orders = get_trade_detail_data('account_id', 'stock', 'order')

# 查询成交
deals = get_trade_detail_data('account_id', 'stock', 'deal')
```

## 设置股票池

```python
def init(ContextInfo):
    # 设置股票池
    ContextInfo.set_universe(['600519.SH', '000858.SZ', '000001.SZ'])
```

## 板块成分股

```python
# 获取板块成分股
stocks = get_stock_list_in_sector('沪深300')
stocks = get_stock_list_in_sector('上证50')
stocks = get_stock_list_in_sector('中证500')
```

## 定时任务

```python
def init(ContextInfo):
    # 设置定时执行
    ContextInfo.run_time('market_open', '9:31:00', 'SH')
    ContextInfo.run_time('market_close', '14:55:00', 'SH')

def market_open(ContextInfo):
    """每日开盘后执行"""
    pass

def market_close(ContextInfo):
    """每日收盘前执行"""
    pass
```

## 更多资源

- [QMT 官方文档](http://dict.thinktrader.net/freshman/rookie.html)
- 联系券商获取 QMT 开通权限
