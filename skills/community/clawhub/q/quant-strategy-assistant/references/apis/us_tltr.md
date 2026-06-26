# `us_tltr` 接口文档

## 接口说明

- 中文说明：国债长期利率
- 动态方法：`pro.us_tltr(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `ltc`, `cmt`, `e_factor`

## 调用示例

```python
df = pro.us_tltr(
    start_date="",
    end_date="",
    fields="date,ltc,cmt,e_factor",
    order_by="date",
    sort="desc",
    limit=50,
)
```
