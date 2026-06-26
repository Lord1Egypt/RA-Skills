# XtData API 快速参考

本文档提供最常用的 XtData 行情数据接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 连接行情服务

```python
from xtquant import xtdata

# 连接行情服务（需miniQMT运行）
xtdata.connect()
```

## 下载历史数据

```python
# 下载日线数据
xtdata.download_history_data('000001.SZ', '1d', start_time='20240101')

# 下载分钟线
xtdata.download_history_data('000001.SZ', '1m', start_time='20240101')

# 批量下载
for code in ['000001.SZ', '600000.SH']:
    xtdata.download_history_data(code, '1d', start_time='20240101')
```

## 获取K线数据

```python
# 获取日K线
data = xtdata.get_market_data_ex([], ['000001.SZ'], period='1d', start_time='20240101')
df = data['000001.SZ']
# 返回字段：open, high, low, close, volume, amount

# 获取分钟K线
data = xtdata.get_market_data_ex([], ['000001.SZ'], period='1m', start_time='20240101')

# 多股票查询
data = xtdata.get_market_data_ex([], ['000001.SZ', '600000.SH'], period='1d', start_time='20240101')
```

## 订阅实时行情

```python
# 订阅Tick行情
def on_data(data):
    print(data)

xtdata.subscribe_quote('000001.SZ', period='tick', callback=on_data)

# 订阅1分钟K线
xtdata.subscribe_quote('000001.SZ', period='1m', callback=on_data)

# 取消订阅
xtdata.unsubscribe_quote(subscribe_id)
```

## 全市场快照

```python
# 获取全市场Tick快照
snapshot = xtdata.get_full_tick(['SH', 'SZ'])
# 返回所有沪深股票的最新Tick数据
```

## 财务数据

```python
# 获取财务数据
fin_data = xtdata.get_financial_data(['000001.SZ'], table_list=['Balance', 'Income', 'CashFlow'])
# table_list: Balance(资产负债表), Income(利润表), CashFlow(现金流量表)
```

## 板块成分股

```python
# 获取板块成分股
stocks = xtdata.get_stock_list_in_sector('沪深A股')

# 其他板块
stocks = xtdata.get_stock_list_in_sector('上证50')
stocks = xtdata.get_stock_list_in_sector('沪深300')
```

## 常用周期参数

| 周期 | 参数值 | 说明 |
|------|--------|------|
| Tick | `tick` | 逐笔数据 |
| 1分钟 | `1m` | 1分钟K线 |
| 5分钟 | `5m` | 5分钟K线 |
| 日线 | `1d` | 日K线 |

## 更多接口

完整接口列表请查看：
- [XtData 官方文档](http://dict.thinktrader.net/nativeApi/xtdata.html)
