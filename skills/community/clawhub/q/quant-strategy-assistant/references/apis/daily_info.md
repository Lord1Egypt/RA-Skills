# `daily_info` 接口文档

## 接口说明

- 中文说明：市场交易统计
- 动态方法：`pro.daily_info(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `ts_name`, `com_count`, `total_share`, `float_share`, `total_mv`, `float_mv`, `amount`, `vol`, `trans_count`, `pe`, `tr`, `exchange`

## 调用示例

```python
df = pro.daily_info(
    trade_date="20260310",
    fields="trade_date,ts_code,ts_name,total_mv,float_mv,amount,vol,pe",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
