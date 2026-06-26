# `hk_daily_adj` 接口文档

## 接口说明

- 中文说明：港股复权行情
- 动态方法：`pro.hk_daily_adj(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, trade_date, close, open, high, low, pre_close, change`

## 调用示例

```python
df = pro.hk_daily_adj(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,close,open,high,low,pre_close,change",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
