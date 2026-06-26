# `stk_ah_comparison` 接口文档

## 接口说明

- 中文说明：AH股比价
- 动态方法：`pro.stk_ah_comparison(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`hk_code`, `ts_code`, `trade_date`, `hk_name`, `hk_pct_chg`, `hk_close`, `name`, `close`

## 调用示例

```python
df = pro.stk_ah_comparison(
    trade_date="",
    start_date="",
    end_date="",
    fields="hk_code,ts_code,trade_date,hk_name,hk_pct_chg,hk_close,name,close",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
