# `idx_factor_pro` 接口文档

## 接口说明

- 中文说明：指数技术因子(专业版)
- 动态方法：`pro.idx_factor_pro(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `macd_bfq`, `macd_dif_bfq`, `macd_dea_bfq`, `kdj_k_bfq`, `kdj_d_bfq`, `kdj_bfq`, `rsi_bfq_6`, `rsi_bfq_12`, `rsi_bfq_24`, `boll_upper_bfq`, `boll_mid_bfq`, `boll_lower_bfq`

## 调用示例

```python
df = pro.idx_factor_pro(
    trade_date="20260310",
    fields="ts_code,trade_date,close,macd_bfq,macd_dif_bfq,macd_dea_bfq,kdj_k_bfq,rsi_bfq_6",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
