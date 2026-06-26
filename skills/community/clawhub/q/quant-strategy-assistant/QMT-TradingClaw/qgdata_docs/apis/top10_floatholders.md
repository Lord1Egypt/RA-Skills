# `top10_floatholders` 接口文档

## 接口说明

- 中文说明：前十大流通股东
- 动态方法：`pro.top10_floatholders(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ts_code`(必填), `period`, `ann_date`, `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `holder_name`, `hold_amount`, `hold_ratio`, `hold_float_ratio`, `hold_change`

## 调用示例

```python
df = pro.top10_floatholders(
    ts_code="",
    period="",
    ann_date="",
    start_date="",
    end_date="",
    fields="ts_code,ann_date,end_date,holder_name,hold_amount,hold_ratio,hold_float_ratio,hold_change",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
