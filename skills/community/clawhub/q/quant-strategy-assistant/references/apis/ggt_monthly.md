# `ggt_monthly` 接口文档

## 接口说明

- 中文说明：港股通每月成交统计
- 动态方法：`pro.ggt_monthly(...)`
- 默认时间字段：`month`
- 典型过滤参数：`month`, `start_date`(必填), `end_date`
- 主要字段：`month`, `day_buy_amt`, `day_buy_vol`, `day_sell_amt`, `day_sell_vol`, `total_buy_amt`, `total_buy_vol`, `total_sell_amt`

## 调用示例

```python
df = pro.ggt_monthly(
    month="",
    start_date="",
    end_date="",
    fields="month,day_buy_amt,day_buy_vol,day_sell_amt,day_sell_vol,total_buy_amt,total_buy_vol,total_sell_amt",
    order_by="month",
    sort="desc",
    limit=50,
)
```
