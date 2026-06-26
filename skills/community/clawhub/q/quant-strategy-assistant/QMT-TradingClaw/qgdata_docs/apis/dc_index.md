# `dc_index` 接口文档

## 接口说明

- 中文说明：东方财富概念板块
- 动态方法：`pro.dc_index(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `name`, `leading`, `leading_code`, `pct_change`, `leading_pct`, `total_mv`

## 调用示例

```python
df = pro.dc_index(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,name,leading,leading_code,pct_change,leading_pct,total_mv",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
