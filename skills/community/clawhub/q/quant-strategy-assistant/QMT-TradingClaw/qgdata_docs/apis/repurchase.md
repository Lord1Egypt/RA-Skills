# `repurchase` 接口文档

## 接口说明

- 中文说明：股票回购
- 动态方法：`pro.repurchase(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`(必填), `end_date`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `proc`, `exp_date`, `vol`, `amount`, `high_limit`

## 调用示例

```python
df = pro.repurchase(
    ann_date="",
    end_date="",
    fields="ts_code,ann_date,end_date,proc,exp_date,vol,amount,high_limit",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
