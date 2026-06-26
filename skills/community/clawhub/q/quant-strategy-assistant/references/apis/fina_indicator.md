# `fina_indicator` 接口文档

## 接口说明

- 中文说明：财务指标数据
- 动态方法：`pro.fina_indicator_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `start_date`(必填), `end_date`, `period`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `eps`, `dt_eps`, `total_revenue_ps`, `revenue_ps`, `capital_rese_ps`

## 调用示例

```python
df = pro.fina_indicator_vip(
    ann_date="",
    start_date="",
    end_date="",
    period="",
    fields="ts_code,ann_date,end_date,eps,dt_eps,total_revenue_ps,revenue_ps,capital_rese_ps",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
