# `index_basic` 接口文档

## 接口说明

- 中文说明：指数基本信息
- 动态方法：`pro.index_basic(...)`
- 默认时间字段：`list_date`
- 典型过滤参数：`market`(必填)
- 主要字段：`ts_code`, `name`, `fullname`, `market`, `publisher`, `index_type`, `category`, `base_date`

## 调用示例

```python
df = pro.index_basic(
    market="",
    fields="ts_code,name,fullname,market,publisher,index_type,category,base_date",
    order_by="list_date",
    sort="desc",
    limit=50,
)
```
