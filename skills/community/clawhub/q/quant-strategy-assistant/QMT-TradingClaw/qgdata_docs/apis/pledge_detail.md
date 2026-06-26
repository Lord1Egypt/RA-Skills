# `pledge_detail` 接口文档

## 接口说明

- 中文说明：股权质押明细数据
- 动态方法：`pro.pledge_detail(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ts_code`(必填)
- 主要字段：`ts_code`, `ann_date`, `holder_name`, `pledge_amount`, `start_date`, `end_date`, `is_release`, `release_date`

## 调用示例

```python
df = pro.pledge_detail(
    ts_code="",
    fields="ts_code,ann_date,holder_name,pledge_amount,start_date,end_date,is_release,release_date",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
