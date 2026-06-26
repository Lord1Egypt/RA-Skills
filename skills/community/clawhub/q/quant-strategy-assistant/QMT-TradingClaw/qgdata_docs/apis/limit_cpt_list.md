# `limit_cpt_list` 接口文档

## 接口说明

- 中文说明：最强板块统计
- 动态方法：`pro.limit_cpt_list(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `trade_date`, `days`, `up_stat`, `cons_nums`, `up_nums`, `pct_chg`

## 调用示例

```python
df = pro.limit_cpt_list(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,name,trade_date,days,up_stat,cons_nums,up_nums,pct_chg",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
