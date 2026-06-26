# `fund_div` 接口文档

## 接口说明

- 中文说明：基金分红
- 动态方法：`pro.fund_div(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, ann_date, imp_anndate, base_date, div_proc, record_date, ex_date, pay_date`

## 调用示例

```python
df = pro.fund_div(
    ann_date="",
    start_date="",
    end_date="",
    fields="ts_code,ann_date,imp_anndate,base_date,div_proc,record_date,ex_date,pay_date",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
