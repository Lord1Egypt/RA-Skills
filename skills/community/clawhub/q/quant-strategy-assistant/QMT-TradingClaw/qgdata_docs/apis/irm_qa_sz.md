# `irm_qa_sz` 接口文档

## 接口说明

- 中文说明：深证互动易
- 动态方法：`pro.irm_qa_sz(...)`
- 默认时间字段：无
- 典型过滤参数：`ann_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `trade_date`, `q`, `a`, `pub_time`, `industry`

## 调用示例

```python
df = pro.irm_qa_sz(
    ann_date="",
    start_date="",
    end_date="",
    fields="ts_code,name,trade_date,q,a,pub_time,industry",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```

## 备注

接口有频率限制：每分钟最多访问3次，每小时最多访问10次。
