# `dc_member` 接口文档

## 接口说明

- 中文说明：东方财富概念板块成分
- 动态方法：`pro.dc_member(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`(必填), `trade_date`(必填)
- 主要字段：`trade_date`, `ts_code`, `con_code`, `name`

## 调用示例

```python
df = pro.dc_member(
    ts_code="",
    trade_date="",
    fields="trade_date,ts_code,con_code,name",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
