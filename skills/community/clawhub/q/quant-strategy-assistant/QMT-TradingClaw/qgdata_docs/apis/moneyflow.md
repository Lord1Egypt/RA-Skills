# `moneyflow` 接口文档

## 接口说明

- 中文说明：个股资金流向
- 动态方法：`pro.moneyflow(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `buy_sm_vol`, `buy_sm_amount`, `sell_sm_vol`, `sell_sm_amount`, `buy_md_vol`, `buy_md_amount`

## 调用示例

```python
df = pro.moneyflow(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,buy_sm_vol,buy_sm_amount,sell_sm_vol,sell_sm_amount,buy_md_vol,buy_md_amount",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
