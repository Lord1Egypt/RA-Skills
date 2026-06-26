# `bak_basic` 接口文档

## 接口说明

- 中文说明：股票历史列表
- 动态方法：`pro.bak_basic(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`, `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `name`, `industry`, `area`, `pe`, `float_share`, `total_share`

## 调用示例

```python
df = pro.bak_basic(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,name,industry,area,pe,float_share,total_share",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
