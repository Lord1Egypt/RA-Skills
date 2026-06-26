# `ggt_daily` 接口文档

## 接口说明

- 中文说明：港股通每日成交统计
- 动态方法：`pro.ggt_daily(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`, `ts_code`, `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `buy_amount`, `buy_volume`, `sell_amount`, `sell_volume`

## 调用示例

```python
df = pro.ggt_daily(
    trade_date="",
    ts_code="",
    start_date="",
    end_date="",
    fields="trade_date,buy_amount,buy_volume,sell_amount,sell_volume",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
