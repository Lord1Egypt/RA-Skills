# 支付宝 AI 付 · 收款流程

单价 6 元/次，按成功交付计一次。收款走支付宝 AI 按量付费（A2M）的 402 流程。

## 1. 发起请求

```bash
curl -sS -D - -X POST "https://api.xinjianxue.com/api/xinjianxue/aipay/astro-natal" \
  -H "Content-Type: application/json" \
  -d '{"year":1995,"month":8,"day":4,"h":5,"m":52,"birth_place":"浙江杭州","country":"CN"}'
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
    "service_id": "API_03827B1FF76346B4"
  }
}
```

## 3. 付款

### 3.1 先确认支付能力已开通

付款依赖买家侧的 `@alipay/agent-payment`（装好后命令是 `alipay-bot`）。首次使用前必须完成一次开通授权，否则 402 之后没有任何东西能把付款拉起来。

先查状态：

```bash
alipay-bot check-wallet
```

| 返回 | 含义 | 下一步 |
|---|---|---|
| `code=200` + `已开启支付宝支付功能` | 已开通 | 直接进入 3.2 |
| `code=200` + `status=applied_unbound` | 已申请，等用户在支付宝里授权 | 让用户完成授权，再 `check-wallet` |
| `code=500` + `未开通` | 还没开通 | 走 3.1.1 |

#### 3.1.1 开通流程（四步，缺一步都付不了款）

1. **取开通入口**
   ```bash
   alipay-bot apply-wallet --agent-name "<你的名称>"
   ```
   返回的是开通入口。可能是链接，也可能是二维码图片（输出里带 `MEDIA:` 的那一行）。**原样交给用户，不要改写、不要自己拼链接**。

2. **用户在支付宝侧完成授权**
   - 手机上：点开链接，进入支付宝内的授权页，按提示确认开通。
   - 电脑上：用支付宝 App 扫二维码，或在手机支付宝里打开同一条链接，进入同一个授权页。

   这一步是**开通并授权支付宝 AI 支付能力**，不是付款，不会扣钱，也不需要用户把银行卡、支付密码或短信验证码交给 AI。页面里如有协议确认，由用户本人在支付宝里点。

3. **回填授权码**
   如果支付宝在授权完成后给出 6 位授权码（或 OTP / 验证码），让用户报给 AI，执行：
   ```bash
   alipay-bot bind-wallet -c '<6位码>'
   ```
   授权页没给码、且 `check-wallet` 已经显示已开启的，跳过这一步。

4. **确认已开启**
   ```bash
   alipay-bot check-wallet
   ```
   出现「已开启支付宝支付功能」才算完成。仍是 `applied_unbound` 就回到第 2 步；显示「未开通」就回到第 1 步重新取入口。

> 商家侧不能代为出码，也不能替用户开通。AI 只负责取入口、把入口原样交给用户、回填授权码、复查状态。没有终端能力时，按 SKILL.md「首次使用：先确认支付能力」里的手动教程交给用户自己完成。

### 3.2 拉起付款

把 `goods_name`、`amount`、`pay_before` 告知用户，由买家侧支付能力拉起付款。

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
