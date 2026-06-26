# `adj_factor` 接口文档

## 接口说明

- 中文说明：复权因子
- 动态方法：`pro.adj_factor(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `adj_factor`

## 调用示例

```python
df = pro.adj_factor(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,adj_factor",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
