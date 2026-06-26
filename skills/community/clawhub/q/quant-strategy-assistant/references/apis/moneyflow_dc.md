# `moneyflow_dc` 接口文档

## 接口说明

- 中文说明：个股资金流向（DC）
- 动态方法：`pro.moneyflow_dc(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `name`, `pct_change`, `close`, `net_amount`, `net_amount_rate`, `buy_elg_amount`

## 调用示例

```python
df = pro.moneyflow_dc(
    ts_code="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,name,pct_change,close,net_amount,net_amount_rate,buy_elg_amount",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
