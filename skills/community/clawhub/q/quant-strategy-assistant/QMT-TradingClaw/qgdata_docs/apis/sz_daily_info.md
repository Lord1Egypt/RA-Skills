# `sz_daily_info` 接口文档

## 接口说明

- 中文说明：深圳市场每日交易概况
- 动态方法：`pro.sz_daily_info(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `count`, `amount`, `vol`, `total_share`, `total_mv`, `float_share`, `float_mv`

## 调用示例

```python
df = pro.sz_daily_info(
    trade_date="20260310",
    fields="trade_date,ts_code,count,amount,vol,total_mv,float_mv",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
