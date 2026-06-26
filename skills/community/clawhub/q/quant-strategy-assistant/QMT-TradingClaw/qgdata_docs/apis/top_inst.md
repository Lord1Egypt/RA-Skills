# `top_inst` 接口文档

## 接口说明

- 中文说明：龙虎榜机构明细
- 动态方法：`pro.top_inst(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `exalter`, `side`, `buy`, `buy_rate`, `sell`, `sell_rate`

## 调用示例

```python
df = pro.top_inst(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,exalter,side,buy,buy_rate,sell,sell_rate",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
