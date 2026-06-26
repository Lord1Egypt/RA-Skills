# `moneyflow_hsgt` 接口文档

## 接口说明

- 中文说明：沪深港通资金流向
- 动态方法：`pro.moneyflow_hsgt(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ggt_ss`, `ggt_sz`, `hgt`, `sgt`, `north_money`, `south_money`

## 调用示例

```python
df = pro.moneyflow_hsgt(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ggt_ss,ggt_sz,hgt,sgt,north_money,south_money",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
