# `sf_month` 接口文档

## 接口说明

- 中文说明：社会融资规模数据
- 动态方法：`pro.sf_month(...)`
- 默认时间字段：无
- 典型过滤参数：无
- 主要字段：`month`, `inc_month`, `inc_cumval`, `stk_endval`

## 调用示例

```python
df = pro.sf_month(
    fields="month,inc_month,inc_cumval,stk_endval",
    order_by="month",
    sort="desc",
    limit=50,
)
```
