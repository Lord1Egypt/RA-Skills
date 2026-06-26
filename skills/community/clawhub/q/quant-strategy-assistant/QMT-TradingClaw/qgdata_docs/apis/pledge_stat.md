# `pledge_stat` 接口文档

## 接口说明

- 中文说明：股权质押统计数据
- 动态方法：`pro.pledge_stat(...)`
- 默认时间字段：`end_date`
- 典型过滤参数：`ts_code`(必填), `end_date`
- 主要字段：`ts_code`, `end_date`, `pledge_count`, `unrest_pledge`, `rest_pledge`, `total_share`, `pledge_ratio`

## 调用示例

```python
df = pro.pledge_stat(
    ts_code="",
    end_date="",
    fields="ts_code,end_date,pledge_count,unrest_pledge,rest_pledge,total_share,pledge_ratio",
    order_by="end_date",
    sort="desc",
    limit=50,
)
```
