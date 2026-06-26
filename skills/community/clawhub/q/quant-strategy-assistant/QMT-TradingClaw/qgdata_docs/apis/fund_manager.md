# `fund_manager` 接口文档

## 接口说明

- 中文说明：基金经理
- 动态方法：`pro.fund_manager(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, ann_date, name, gender, birth_year, edu, nationality, begin_date`

## 调用示例

```python
df = pro.fund_manager(
    ann_date="",
    start_date="",
    end_date="",
    fields="ts_code,ann_date,name,gender,birth_year,edu,nationality,begin_date",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
