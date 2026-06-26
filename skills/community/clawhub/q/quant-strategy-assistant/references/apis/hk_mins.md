# `hk_mins` 接口文档

## 接口说明

- 中文说明：港股分钟行情
- 动态方法：`pro.hk_mins(...)`
- 默认时间字段：`trade_time`
- 典型过滤参数：`ts_code`(必填)、`freq`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, trade_time, open, close, high, low, vol, amount`

## 调用示例

```python
df = pro.hk_mins(
    ts_code="",
    freq="",
    start_date="",
    end_date="",
    fields="ts_code,trade_time,open,close,high,low,vol,amount",
    order_by="trade_time",
    sort="desc",
    limit=50,
)
```

## 备注

`hk_mins` 是分片表（sharded table），查询时必须提供 `freq` 和 `ts_code` 参数。`freq` 支持的值为：`1min`、`5min`、`15min`、`30min`、`60min`。分片策略为 `freq_ts_code_hash`，不同频率的分片桶数不同（`1min` 为 32 个桶，其余频率为 10 个桶）。
