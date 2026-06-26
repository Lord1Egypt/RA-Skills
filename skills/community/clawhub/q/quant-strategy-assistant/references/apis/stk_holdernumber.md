# `stk_holdernumber` 接口文档

## 接口说明

- 中文说明：股东人数
- 动态方法：`pro.stk_holdernumber(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `ann_date`, `end_date`, `holder_num`

## 调用示例

```python
df = pro.stk_holdernumber(
    fields="ts_code,ann_date,end_date,holder_num",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
