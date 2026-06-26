# `disclosure_date` 接口文档

## 接口说明

- 中文说明：财报披露计划
- 动态方法：`pro.disclosure_date(...)`
- 默认时间字段：`end_date`
- 典型过滤参数：`ts_code`, `end_date`, `pre_date`, `ann_date`(必填), `actual_date`, `start_date`(必填)
- 主要字段：`ts_code`, `ann_date`, `end_date`, `pre_date`, `actual_date`, `modify_date`

## 调用示例

```python
df = pro.disclosure_date(
    ts_code="",
    end_date="",
    pre_date="",
    ann_date="",
    actual_date="",
    start_date="",
    fields="ts_code,ann_date,end_date,pre_date,actual_date,modify_date",
    order_by="end_date",
    sort="desc",
    limit=50,
)
```
