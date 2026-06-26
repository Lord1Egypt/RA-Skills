# `index_dailybasic` 接口文档

## 接口说明

- 中文说明：大盘指数每日指标
- 动态方法：`pro.index_dailybasic(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `total_mv`, `float_mv`, `total_share`, `float_share`, `free_share`, `turnover_rate`, `pe`, `pe_ttm`, `pb`

## 调用示例

```python
df = pro.index_dailybasic(
    trade_date="20260310",
    fields="ts_code,trade_date,total_mv,float_mv,pe,pe_ttm,pb",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
