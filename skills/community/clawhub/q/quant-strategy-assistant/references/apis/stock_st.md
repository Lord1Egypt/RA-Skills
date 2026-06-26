# `stock_st` 接口文档

## 接口说明

- 中文说明：ST股票列表
- 动态方法：`pro.stock_st(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `trade_date`, `type`, `type_name`

## 调用示例

```python
df = pro.stock_st(
    trade_date="",
    end_date="",
    fields="ts_code,name,trade_date,type,type_name",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
