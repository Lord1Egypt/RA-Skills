# `stk_managers` 接口文档

## 接口说明

- 中文说明：上市公司管理层
- 动态方法：`pro.stk_managers(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`start_date`(必填)
- 主要字段：`ts_code`, `ann_date`, `name`, `gender`, `lev`, `title`, `edu`, `national`

## 调用示例

```python
df = pro.stk_managers(
    start_date="",
    fields="ts_code,ann_date,name,gender,lev,title,edu,national",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
