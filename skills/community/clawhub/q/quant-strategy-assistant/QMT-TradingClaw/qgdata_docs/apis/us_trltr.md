# `us_trltr` 接口文档

## 接口说明

- 中文说明：国债实际长期利率平均值
- 动态方法：`pro.us_trltr(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `ltr_avg`

## 调用示例

```python
df = pro.us_trltr(
    start_date="",
    end_date="",
    fields="date,ltr_avg",
    order_by="date",
    sort="desc",
    limit=50,
)
```
