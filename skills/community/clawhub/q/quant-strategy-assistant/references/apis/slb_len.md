# `slb_len` 接口文档

## 接口说明

- 中文说明：转融资交易汇总
- 动态方法：`pro.slb_len(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ob`, `auc_amount`, `repo_amount`, `repay_amount`, `cb`

## 调用示例

```python
df = pro.slb_len(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ob,auc_amount,repo_amount,repay_amount,cb",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
