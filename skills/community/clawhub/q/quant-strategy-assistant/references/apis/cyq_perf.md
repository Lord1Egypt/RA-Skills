# `cyq_perf` 接口文档

## 接口说明

- 中文说明：每日筹码及胜率
- 动态方法：`pro.cyq_perf(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `trade_date`, `his_low`, `his_high`, `cost_5pct`, `cost_15pct`, `cost_50pct`, `cost_85pct`

## 调用示例

```python
df = pro.cyq_perf(
    fields="ts_code,trade_date,his_low,his_high,cost_5pct,cost_15pct,cost_50pct,cost_85pct",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
