# `us_tycr` 接口文档

## 接口说明

- 中文说明：国债收益率曲线利率（日频）
- 动态方法：`pro.us_tycr(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `m1`, `m2`, `m3`, `m4`, `m6`, `y1`, `y2`

## 调用示例

```python
df = pro.us_tycr(
    start_date="",
    end_date="",
    fields="date,m1,m2,m3,m4,m6,y1,y2",
    order_by="date",
    sort="desc",
    limit=50,
)
```
