# 支付宝 AI 付 · 收款流程

单价 6 元/次，按成功交付计一次。收款走支付宝 AI 按量付费（A2M）的 402 流程。

## 1. 发起请求

```bash
curl -sS -D - -X POST "https://api.xinjianxue.com/api/xinjianxue/aipay/report" \
  -H "Content-Type: application/json" \
  -d '{"birth":"1995-08-04 05:52","place":"浙江杭州","country":"CN","gender":"女"}'
```

## 2. 读响应

- `200` → 拿到业务结果，进入解读。
- `402` → 未付款。响应头 `Payment-Needed` 是 base64url 编码的 JSON，解码后为：

```json
{
  "protocol": {
    "out_trade_no": "订单号",
    "amount": "应付金额",
    "currency": "CNY",
    "resource_id": "资源标识",
    "pay_before": "付款截止时间，ISO8601 带时区",
    "seller_signature": "商家签名",
    "seller_sign_type": "RSA2",
    "seller_unique_id": "商家 ID"
  },
  "method": {
    "seller_name": "商家名称",
    "seller_id": "商家 ID",
    "seller_app_id": "支付宝应用 ID",
    "goods_name": "商品名",
    "seller_unique_id_key": "seller_id",
    "service_id": "API_114161C46CE74BDE"
  }
}
```

## 3. 付款

把 `goods_name`、`amount`、`pay_before` 告知用户，由买家侧支付能力拉起付款。买家需安装 `@alipay/agent-payment` 并在支付宝 App 内完成开通授权，商家侧不能代为出码。

## 4. 用支付凭证重试

付款完成后，用完全相同的请求体重试，增加请求头：

```
Payment-Proof: <买家侧支付能力产出的凭证>
```

该凭证为 base64url 编码的 JSON，含支付凭证与交易号。服务端校验通过后返回 `200` 与业务结果。

## 规则

- 一个 `out_trade_no` 只付一次；重试必须复用同一请求体与同一 `Payment-Proof`，不要重新下单。
- 超过 `pay_before` 后需重新发起请求获取新的 402。
- 未拿到 `200` 前不向用户交付解读，也不声称付款成功。
- 用户拒绝付款或支付失败：停止本次交付，不做降级输出。
