# `sw_daily` 接口文档

## 接口说明

- 中文说明：申万行业日线行情
- 动态方法：`pro.sw_daily(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `name`, `open`, `low`, `high`, `close`, `change`, `pct_change`, `vol`, `amount`, `pe`, `pb`, `float_mv`, `total_mv`

## 调用示例

```python
df = pro.sw_daily(
    trade_date="20260310",
    fields="ts_code,trade_date,name,close,pct_change,vol,amount,pe,pb",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
