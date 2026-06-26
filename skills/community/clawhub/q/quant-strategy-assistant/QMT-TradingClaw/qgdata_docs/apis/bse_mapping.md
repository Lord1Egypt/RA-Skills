# `bse_mapping` 接口文档

## 接口说明

- 中文说明：北交所新旧代码对照表
- 动态方法：`pro.bse_mapping(...)`
- 默认时间字段：`list_date`
- 典型过滤参数：`o_code`, `n_code`
- 主要字段：`name`, `o_code`, `n_code`, `list_date`

## 调用示例

```python
df = pro.bse_mapping(
    o_code="",
    n_code="",
    fields="name,o_code,n_code,list_date",
    order_by="list_date",
    sort="desc",
    limit=50,
)
```
