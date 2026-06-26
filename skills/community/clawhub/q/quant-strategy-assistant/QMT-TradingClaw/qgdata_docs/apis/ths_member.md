# `ths_member` 接口文档

## 接口说明

- 中文说明：同花顺概念板块成分
- 动态方法：`pro.ths_member(...)`
- 默认时间字段：`in_date`
- 典型过滤参数：`ts_code`(必填)
- 主要字段：`ts_code`, `con_code`, `con_name`, `weight`, `in_date`, `out_date`, `is_new`

## 调用示例

```python
df = pro.ths_member(
    ts_code="",
    fields="ts_code,con_code,con_name,weight,in_date,out_date,is_new",
    order_by="in_date",
    sort="desc",
    limit=50,
)
```
