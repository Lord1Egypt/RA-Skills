# `hk_tradecal` 接口文档

## 接口说明

- 中文说明：港股日历
- 动态方法：`pro.hk_tradecal(...)`
- 默认时间字段：`无`
- 典型过滤参数：`start_date`(必填)、`end_date`
- 主要字段：`cal_date, is_open, pretrade_date`

## 调用示例

```python
df = pro.hk_tradecal(
    start_date="",
    end_date="",
    fields="cal_date,is_open,pretrade_date",
    order_by="cal_date",
    sort="desc",
    limit=50,
)
```
