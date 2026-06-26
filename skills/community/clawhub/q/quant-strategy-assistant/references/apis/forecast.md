# `forecast` 接口文档

## 接口说明

- 中文说明：业绩预告
- 动态方法：`pro.forecast_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `start_date`(必填), `end_date`, `period`, `type`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `type`, `p_change_min`, `p_change_max`, `net_profit_min`, `net_profit_max`

## 调用示例

```python
df = pro.forecast_vip(
    ann_date="",
    start_date="",
    end_date="",
    period="",
    type="",
    fields="ts_code,ann_date,end_date,type,p_change_min,p_change_max,net_profit_min,net_profit_max",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
