# `tdx_member` 接口文档

## 接口说明

- 中文说明：通达信板块成分
- 动态方法：`pro.tdx_member(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `con_code`, `con_name`

## 调用示例

```python
df = pro.tdx_member(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,con_code,con_name",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
