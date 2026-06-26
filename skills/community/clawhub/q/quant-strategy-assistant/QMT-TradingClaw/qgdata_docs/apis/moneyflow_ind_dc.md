# `moneyflow_ind_dc` 接口文档

## 接口说明

- 中文说明：东财概念及行业板块资金流向（DC）
- 动态方法：`pro.moneyflow_ind_dc(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `content_type`, `ts_code`, `name`, `pct_change`, `close`, `net_amount`, `net_amount_rate`

## 调用示例

```python
df = pro.moneyflow_ind_dc(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,content_type,ts_code,name,pct_change,close,net_amount,net_amount_rate",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
