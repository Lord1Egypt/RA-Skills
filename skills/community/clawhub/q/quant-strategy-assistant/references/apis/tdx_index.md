# `tdx_index` 接口文档

## 接口说明

- 中文说明：通达信板块信息
- 动态方法：`pro.tdx_index(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `name`, `idx_type`, `idx_count`, `total_share`, `float_share`, `total_mv`

## 调用示例

```python
df = pro.tdx_index(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,name,idx_type,idx_count,total_share,float_share,total_mv",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
