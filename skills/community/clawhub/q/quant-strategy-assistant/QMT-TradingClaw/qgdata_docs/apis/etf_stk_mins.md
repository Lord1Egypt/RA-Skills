# `etf_stk_mins` 接口文档

## 接口说明

- 中文说明：ETF历史分钟行情
- 动态方法：`pro.stk_mins(...)`
- 默认时间字段：`trade_time`
- 典型过滤参数：`ts_code`(必填), `freq`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_time`, `open`, `close`, `high`, `low`, `vol`, `amount`

## 调用示例

```python
df = pro.stk_mins(
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

- 该接口为分表查询，必须同时传 `freq` 与 `ts_code`
- 建议始终传 `start_date/end_date` 控制查询范围
- 当时间字段为 `trade_time` 时，服务端会自动补齐交易时段边界
