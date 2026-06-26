# `hm_list` 接口文档

## 接口说明

- 中文说明：游资名录
- 动态方法：`pro.hm_list(...)`
- 默认时间字段：`name`
- 典型过滤参数：无
- 主要字段：`name`, `desc`, `orgs`

## 调用示例

```python
df = pro.hm_list(
    fields="name,desc,orgs",
    order_by="name",
    sort="desc",
    limit=50,
)
```
