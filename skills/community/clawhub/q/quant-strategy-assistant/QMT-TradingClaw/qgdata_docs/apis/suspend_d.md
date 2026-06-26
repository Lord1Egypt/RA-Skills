# `suspend_d` 接口文档

## 接口说明

- 中文说明：每日停复牌信息
- 动态方法：`pro.suspend_d(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`, `trade_date`(必填), `start_date`(必填), `end_date`, `suspend_type`
- 主要字段：`ts_code`, `trade_date`, `suspend_timing`, `suspend_type`

## 调用示例

```python
df = pro.suspend_d(
    ts_code="",
    trade_date="",
    start_date="",
    end_date="",
    suspend_type="",
    fields="ts_code,trade_date,suspend_timing,suspend_type",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
