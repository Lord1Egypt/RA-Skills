# `limit_list_d` 接口文档

## 接口说明

- 中文说明：涨跌停列表（新）
- 动态方法：`pro.limit_list_d(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `industry`, `name`, `close`, `pct_chg`, `amount`, `limit_amount`

## 调用示例

```python
df = pro.limit_list_d(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,industry,name,close,pct_chg,amount,limit_amount",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
