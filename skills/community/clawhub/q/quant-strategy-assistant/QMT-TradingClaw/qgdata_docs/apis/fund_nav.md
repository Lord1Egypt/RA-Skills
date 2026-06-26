# `fund_nav` 接口文档

## 接口说明

- 中文说明：基金净值
- 动态方法：`pro.fund_nav(...)`
- 默认时间字段：`无`
- 典型过滤参数：`nav_date`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, ann_date, nav_date, unit_nav, accum_nav, accum_div, net_asset, total_netasset`

## 调用示例

```python
df = pro.fund_nav(
    nav_date="",
    start_date="",
    end_date="",
    fields="ts_code,ann_date,nav_date,unit_nav,accum_nav,accum_div,net_asset,total_netasset",
    order_by="ts_code",
    sort="desc",
    limit=50,
)
```
