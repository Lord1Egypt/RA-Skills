# `us_trycr` 接口文档

## 接口说明

- 中文说明：国债实际收益率曲线利率
- 动态方法：`pro.us_trycr(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `y5`, `y7`, `y10`, `y20`, `y30`

## 调用示例

```python
df = pro.us_trycr(
    start_date="",
    end_date="",
    fields="date,y5,y7,y10,y20,y30",
    order_by="date",
    sort="desc",
    limit=50,
)
```
