# `stk_surv` 接口文档

## 接口说明

- 中文说明：机构调研表
- 动态方法：`pro.stk_surv(...)`
- 默认时间字段：`surv_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `surv_date`, `fund_visitors`, `rece_place`, `rece_mode`, `rece_org`, `org_type`

## 调用示例

```python
df = pro.stk_surv(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,name,surv_date,fund_visitors,rece_place,rece_mode,rece_org,org_type",
    order_by="surv_date",
    sort="desc",
    limit=50,
)
```
