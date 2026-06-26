# `share_float` 接口文档

## 接口说明

- 中文说明：限售股解禁
- 动态方法：`pro.share_float(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ts_code`(必填), `float_date`
- 主要字段：`ts_code`, `ann_date`, `float_date`, `float_share`, `float_ratio`, `holder_name`, `share_type`

## 调用示例

```python
df = pro.share_float(
    ts_code="",
    float_date="",
    fields="ts_code,ann_date,float_date,float_share,float_ratio,holder_name,share_type",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
