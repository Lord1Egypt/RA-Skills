# `cashflow` 接口文档

## 接口说明

- 中文说明：现金流量表
- 动态方法：`pro.cashflow_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `f_ann_date`, `start_date`(必填), `end_date`, `period`, `report_type`, `comp_type`, `is_calc`
- 主要字段：`ts_code`, `ann_date`, `f_ann_date`, `end_date`, `comp_type`, `report_type`, `end_type`, `net_profit`

## 调用示例

```python
df = pro.cashflow_vip(
    ann_date="",
    f_ann_date="",
    start_date="",
    end_date="",
    period="",
    report_type="",
    comp_type="",
    is_calc="",
    fields="ts_code,ann_date,f_ann_date,end_date,comp_type,report_type,end_type,net_profit",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
