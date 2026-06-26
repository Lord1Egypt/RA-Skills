# `moneyflow_ind_ths` 接口文档

## 接口说明

- 中文说明：同花顺行业资金流向（THS）
- 动态方法：`pro.moneyflow_ind_ths(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `industry`, `lead_stock`, `close`, `pct_change`, `company_num`, `pct_change_stock`

## 调用示例

```python
df = pro.moneyflow_ind_ths(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,industry,lead_stock,close,pct_change,company_num,pct_change_stock",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
