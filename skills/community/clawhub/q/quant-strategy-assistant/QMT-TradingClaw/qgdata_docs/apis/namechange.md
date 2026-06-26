# `namechange` 接口文档

## 接口说明

- 中文说明：股票曾用名
- 动态方法：`pro.namechange(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ts_code`, `start_date`, `end_date`
- 主要字段：`ts_code`, `name`, `start_date`, `end_date`, `ann_date`, `change_reason`

## 调用示例

```python
df = pro.namechange(
    ts_code="",
    start_date="",
    end_date="",
    fields="ts_code,name,start_date,end_date,ann_date,change_reason",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
