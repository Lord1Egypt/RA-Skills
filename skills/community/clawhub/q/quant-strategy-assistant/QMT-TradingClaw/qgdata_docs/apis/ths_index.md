# `ths_index` 接口文档

## 接口说明

- 中文说明：同花顺概念和行业指数
- 动态方法：`pro.ths_index(...)`
- 默认时间字段：`list_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `name`, `count`, `exchange`, `list_date`, `type`

## 调用示例

```python
df = pro.ths_index(
    fields="ts_code,name,count,exchange,list_date,type",
    order_by="list_date",
    sort="desc",
    limit=50,
)
```
