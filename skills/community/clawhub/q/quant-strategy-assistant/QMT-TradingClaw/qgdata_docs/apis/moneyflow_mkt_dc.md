# `moneyflow_mkt_dc` 接口文档

## 接口说明

- 中文说明：大盘资金流向（DC）
- 动态方法：`pro.moneyflow_mkt_dc(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `close_sh`, `pct_change_sh`, `close_sz`, `pct_change_sz`, `net_amount`, `net_amount_rate`, `buy_elg_amount`

## 调用示例

```python
df = pro.moneyflow_mkt_dc(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,close_sh,pct_change_sh,close_sz,pct_change_sz,net_amount,net_amount_rate,buy_elg_amount",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
