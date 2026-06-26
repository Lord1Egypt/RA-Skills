# `express` 接口文档

## 接口说明

- 中文说明：业绩快报
- 动态方法：`pro.express_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `start_date`(必填), `end_date`, `period`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `revenue`, `operate_profit`, `total_profit`, `n_income`, `total_assets`

## 调用示例

```python
df = pro.express_vip(
    ann_date="",
    start_date="",
    end_date="",
    period="",
    fields="ts_code,ann_date,end_date,revenue,operate_profit,total_profit,n_income,total_assets",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
