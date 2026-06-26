---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100e7850c002ecf9161d5d71879089a94b1095df56ec13628323889c992c29891f9022100a69d2b1ce702a9dea17048fcc970086a95258780a6b39f4ddf45b7f66a4644bf
    ReservedCode2: 3046022100cd362c3427455fba481759795d572892908a07b8cef2bce2a84595342cf7de87022100efe93e8bacab56d03c2fe73ae95de1bd6cf00e215ed18208d017eee4e9c407fc
---

# PyWenCai API 参考

## 核心函数

### pywencai.get(**kwargs)

获取同花顺问财数据

## 参数详解

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| query | 是 | - | 查询语句（问财格式） |
| sort_key | 否 | - | 排序字段（列名） |
| sort_order | 否 | - | 排序方式：asc/desc |
| page | 否 | 1 | 页码 |
| perpage | 否 | 100 | 每页条数（最大100） |
| loop | 否 | False | 循环获取全量数据 |
| query_type | 否 | stock | 查询类型 |
| retry | 否 | 10 | 重试次数 |
| sleep | 否 | 0 | 请求间隔（秒） |
| log | 否 | False | 是否打印日志 |

## 查询类型 (query_type)

| 值 | 含义 |
|----|------|
| stock | 股票 |
| zhishu | 指数 |
| fund | 基金 |
| hkstock | 港股 |
| usstock | 美股 |
| threeboard | 新三板 |
| conbond | 可转债 |

## 常用查询语句

### 行情类
```
A股涨停
A股跌停
沪深A股涨幅前10
沪深A股跌幅前10
换手率最高的股票
成交额最大的股票
振幅最大的股票
量比最高的股票
```

### 财务类
```
净利润最高的公司
市盈率最低的股票
市净率最低的股票
ROE最高的股票
营收增长最快的公司
毛利率最高的股票
负债率最低的股票
```

### 资金类
```
主力净流入最多的股票
今日龙虎榜
大单净流入最多的股票
北向资金买入最多的股票
```

### 个股类
```
600519 财务指标
600519 行情
300502 龙虎榜
600519 股东户数
600519 研报
```

### 概念类
```
芯片概念股
人工智能概念股
新能源汽车概念股
光伏概念股
半导体概念股
```

## 返回处理

```python
import pywencai
import pandas as pd

# 获取数据
df = pywencai.get(query='A股涨停')

# 查看列名
print(df.columns.tolist())

# 查看前几行
print(df.head())

# 保存为CSV
df.to_csv('data.csv', encoding='utf-8-sig')

# 保存为Excel
df.to_excel('data.xlsx')
```
