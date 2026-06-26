# `stk_holdertrade` 接口文档

## 接口说明

- 中文说明：股东增减持
- 动态方法：`pro.stk_holdertrade(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `ann_date`, `holder_name`, `holder_type`, `in_de`, `change_vol`, `change_ratio`, `after_share`

## 调用示例

```python
df = pro.stk_holdertrade(
    fields="ts_code,ann_date,holder_name,holder_type,in_de,change_vol,change_ratio,after_share",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
