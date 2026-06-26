# `fund_portfolio` 接口文档

## 接口说明

- 中文说明：基金持仓
- 动态方法：`pro.fund_portfolio(...)`
- 默认时间字段：`无`
- 典型过滤参数：`ann_date`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, ann_date, end_date, symbol, mkv, amount, stk_mkv_ratio, stk_float_ratio`

## 调用示例

```python
df = pro.fund_portfolio(
    ann_date="",
    start_date="",
    end_date="",
    fields="ts_code,ann_date,end_date,symbol,mkv,amount,stk_mkv_ratio,stk_float_ratio",
    order_by="ts_code",
    sort="desc",
    limit=50,
)
```
