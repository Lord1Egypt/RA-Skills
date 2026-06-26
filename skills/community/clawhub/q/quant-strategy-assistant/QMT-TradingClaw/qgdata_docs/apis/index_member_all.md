# `index_member_all` 接口文档

## 接口说明

- 中文说明：申万行业成分构成(分级)
- 动态方法：`pro.index_member_all(...)`
- 典型过滤参数：`l3_code`(必填)
- 主要字段：`l1_code`, `l1_name`, `l2_code`, `l2_name`, `l3_code`, `l3_name`, `ts_code`, `name`, `in_date`, `out_date`, `is_new`

## 调用示例

```python
df = pro.index_member_all(
    l3_code="851011.SI",
    fields="l1_code,l1_name,l2_code,l2_name,l3_code,l3_name,ts_code,name,in_date,out_date,is_new",
    limit=50,
)
```
