# `ccass_hold` 接口文档

## 接口说明

- 中文说明：中央结算系统持股汇总
- 动态方法：`pro.ccass_hold(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `name`, `shareholding`, `hold_nums`, `hold_ratio`

## 调用示例

```python
df = pro.ccass_hold(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,name,shareholding,hold_nums,hold_ratio",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
