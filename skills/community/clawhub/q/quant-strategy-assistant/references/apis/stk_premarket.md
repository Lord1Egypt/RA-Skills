# `stk_premarket` 接口文档

## 接口说明

- 中文说明：股本情况（盘前）
- 动态方法：`pro.stk_premarket(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`
- 主要字段：`trade_date`, `ts_code`, `total_share`, `float_share`, `pre_close`, `up_limit`, `down_limit`

## 调用示例

```python
df = pro.stk_premarket(
    trade_date="",
    fields="trade_date,ts_code,total_share,float_share,pre_close,up_limit,down_limit",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
