---
name: tenyuan-cloud-shop
description: "十元云铺万元利——一句话或一张产品图，自动生成可分享的小批发部迷你网站（云铺档口页），含产品图、口播音频、分享文案、电话/微信联系方式。当用户说「开个云铺」「我有货想卖」「帮我做个卖货页面」「生成档口页」「云南沃柑 5 斤 29.9」这类想快速获得卖货展示页的请求时使用。纯展示导流，成交线下对接，平台不参与交易。 | TenYuan Cloud Shop: turn one sentence or one product photo into a shareable mini shop page with AI voiceover, hosted at ruancyai.com/cloud."
version: 0.3.2
# ====== Pay Skill 计费声明（v0.3.2 起启用）======
# 计费单元：成功创建 1 个云铺档口页（不含二维码上传、不含页面修改）
# 计费时机：后端返回 shop_id 后，按扣费确认页提示确认即扣
# 失败规则：API 返回 5xx 或 AI 生成失败则不扣费
# 退款：未生成链接不扣费；已生成链接 24h 内删除全额退
pricing:
  model: per_call
  amount_fen: 990
  currency: CNY
  unit: 次
  display_price: ¥9.9/次
---

# 十元云铺万元利 — TenYuan Cloud Shop

普通人的云端小批发部：一句话或一张图，立刻拥有专属卖货档口页。

## 什么时候用本 Skill

用户上传产品图片，或用文字描述「我有什么货」，想要一个能发给客户、发朋友圈/抖音/微信群的展示页时。

不适用：需要在线支付/下单系统（本产品不参与交易）、需要企业官网级定制。

## 使用流程

1. 用户发图（可选，最多 3 张）或文字描述（产品名 + 特点 + 价格 + 联系方式更好）
2. 调用后端 `POST /cloud/api/shops` 创建云铺（接口契约见 `references/api.md`）
3. 把返回的档口链接、店名、分享文案、口播音频地址交给用户，引导直接转发
4. 用户后续提供微信二维码时，调用 `POST /cloud/api/shops/{shopId}/qrcode` 挂到档口页

## 关键约束（必须遵守）

- **实拍与示意要如实转达**：返回中 `isAiGenerated: true` 的图是 AI 示意图，转述给用户时必须说明「示意图」，不得说成实拍。
- **不承诺交易能力**：本产品只做展示导流，不得向用户承诺在线支付、担保、代收货款。
- **联系方式如实传递**：电话/微信号按用户提供的原文填入，不得代拟。
- **后端未部署时的降级**：若 `https://ruancyai.com/cloud` 不可达，如实告知用户「云铺服务尚未上线」，不得编造链接。
- **价格与承诺归用户**：生成内容中的价格、产地、卖点均来自用户描述，Agent 不得自行加价、夸大或补充未经用户确认的功效宣称（尤其食品、酒类不得宣传保健疗效）。

## 后端服务

- 线上地址：`https://ruancyai.com/cloud`
- 档口页：`https://ruancyai.com/cloud/shop/{shopId}`
- 接口契约：`references/api.md`（创建档口 / 上传二维码 / 获取分享素材）
- 后端版本对应关系见 `CHANGELOG.md`

## 版本

- 当前版本：0.3.2（Pay Skill 收费版：¥9.9/次 = 990 分；后端 ruancy-cloud-market 新增 `src/pay.ts` X402 支付模块，完整实现微信 Native 下单 → X402 AI 预下单 → HTTP 402 支付触发 → 回调验签 → 退款 全链路）
- 上一版：缩略图墙、备案号、OG 分享卡片、上传白名单 + 魔数校验 + 限流

## Pay Skill 改造（X402 协议 — 代码级实现）

本 Skill 已按 SkillHub 官方《升级为 Pay Skill》教程完成 **代码级** X402 协议集成。后端 `src/pay.ts` 模块实现了完整的微信支付 Agent Pay X402 流程，`src/server.ts` 在建店接口中集成了支付闸门。

### 整体架构（4 步）

```
Agent 调用 POST /cloud/api/shops
  → 后端创建微信 Native 订单（拿 code_url）
  → 后端用 SkillHub 开发者密钥签名，调 X402 AI 预下单（拿 payment_code）
  → 后端返回 HTTP 402 + WeixinPay-Required 头
  → Agent 调 weixinpay_pay 触发用户支付授权
  → 用户支付成功后 Agent 重试原请求（带 X-PAYMENT 头）
  → 后端验签放行，执行业务逻辑（AI 识别 → TTS → 落库）
```

### Step 1：开发者密钥（RSA-2048）

在 SkillHub 商户中心「开发者密钥」页面生成 RSA-2048 密钥对：
- `pub_key_id`：形如 `PUB_KEY_` + 32 位大写 HEX，填入 X402 预下单请求
- `private_key_pem`：RSA-2048 私钥（PEM 格式），用于 SHA256withRSA 签名
- 存储在服务器 `.env` 的 `SKILLHUB_PRIVATE_KEY_PEM` 中

### Step 2：微信 Native 下单

后端 `createNativeOrder()` 调用微信支付 Native 下单接口获取 `code_url`：

```
POST https://api.mch.weixin.qq.com/v3/pay/transactions/native
Authorization: WECHATPAY2-SHA256-RSA2048 mchid="...",signature="..."
Body: { appid, mchid, description, out_trade_no, notify_url, amount: { total: 990, currency: "CNY" } }
→ { "code_url": "weixin://wxpay/bizpayurl?pr=..." }
```

使用微信商户 API v3 证书私钥签名（`WECHAT_PRIVATE_KEY_PEM` + `WECHAT_SERIAL_NO`）。

### Step 3：X402 AI 预下单

后端 `x402Preorder()` 用 SkillHub 开发者密钥签名，调 X402 预下单接口换取 `payment_code`：

**3.1 构造 L2 业务 JSON** → Base64 编码 → `payment_required`

```json
{
  "skill_info": { "skill_id": "tenyuan-cloud-shop", "skill_version": "0.3.2" },
  "pay_type": "SKILL_PAY",
  "pay_mode": "AUTH_AND_PAY",
  "pay_items": [{ "product_id": "SP...", "pay_data": { "type": "code_url", "value": "<code_url>" } }],
  "expires_at": "<unix_ts + 15min>"
}
```

**3.2 构造 5 行签名串**（每行以 `\n` 结尾，包括最后一行）：

```
POST\n/palmpayminiapp/clawagentpay/preorder\n{timestamp}\n{nonce_str}\n{payment_required}\n
```

**3.3 SHA256withRSA 签名**（PKCS#1 v1.5，用 SkillHub 开发者私钥）→ Base64 → `signature`

**3.4 组装 L1 请求体并发送**：

```
POST https://payapp.weixin.qq.com/palmpayminiapp/clawagentpay/preorder
Content-Type: application/json
Body: { signature_type: "SKILLHUB-SHA256-RSA2048", developer_platform: "SKILLHUB",
        developer_id, pub_key_id, nonce_str, timestamp, signature, payment_required }
→ { "payment_code": "xY9zAbc123def456" }
```

### Step 4：返回支付触发标识（HTTP 402）

后端 `buildPayment402()` 构建标准 X402 响应：

```
HTTP/1.1 402 Payment Required
WeixinPay-Required: <payment_code>
Content-Type: application/json

{
  "data": { "message": "本次创建档口需要付费", "out_trade_no": "cloud_...", "amount_fen": 990 },
  "WeixinPay": {
    "WeixinPay-Required": "<payment_code>",
    "prompt": "本次使用微信支付，请将 WeixinPay-Required 的值作为 paymentCode 交给 weixinpay_pay，以向用户申请支付授权。"
  }
}
```

### 重试机制

支付成功后，Agent 携带 `X-PAYMENT` 请求头（值为 `payment_code`）重试原业务请求：

```
POST /cloud/api/shops
Headers:
  X-PAYMENT: <payment_code>
```

后端收到 `X-PAYMENT` 后执行前置检查：
1. 查 `payments` 表确认 `payment_code` 对应订单状态
2. 若 DB 未标记已付 → 主动调微信支付查询 API（`GET /v3/pay/transactions/out-trade-no/{out_trade_no}`）确认
3. 已付 → 放行执行业务逻辑；未付 → 再次返回 402

### 微信支付回调

后端 `decryptNotify()` 处理微信支付异步通知（`POST /cloud/api/pay/notify`）：
- 使用 API v3 密钥（AES-256-GCM）解密 `resource.ciphertext`
- 解密成功且 `trade_state=SUCCESS` → 更新 `payments` 表 `status='paid'`
- 返回 `{"code":"SUCCESS"}` 停止微信重试

### 退款

后端 `POST /cloud/api/pay/refund/{out_trade_no}` 发起微信支付退款：
- 调用 `POST /v3/refund/domestic/refunds`（微信商户私钥签名）
- 退款成功 → 更新 `payments` 表 `status='refunded'`
- 适用场景：AI 生成失败、用户 24h 内撤销

### 异常处理与配置检查

- **配置检查**：后端 `isPayConfigured()` 在服务启动时检查 8 个环境变量是否全部就位；未就位时自动降级为免费模式（建店不收 402），就位后自动激活付费模式
- **订单号传递**：从微信 Native 下单 → X402 预下单 → 回调验签 → 退款，全程以 `out_trade_no`（order_id）作为唯一订单号传递
- **支付超时**：`payment_code` 15 分钟后自动过期，用户需重新发起建店请求
- **重复支付**：`out_trade_no` 唯一约束 + DB 状态校验防止重复扣费
- **回调丢失**：若微信异步通知未到达，重试时主动调微信查询 API 补偿（`queryPaymentStatus()`）

### 环境变量清单

```env
# 微信支付商户 API v3
WECHAT_APPID=wx...
WECHAT_MCHID=1733356762
WECHAT_APIV3_KEY=<32位APIv3密钥>
WECHAT_SERIAL_NO=<商户证书序列号>
WECHAT_PRIVATE_KEY_PEM=<商户API证书私钥PEM>

# SkillHub 开发者密钥
SKILLHUB_DEVELOPER_ID=sh-XXXXXXXX
SKILLHUB_PUB_KEY_ID=PUB_KEY_XXXXXXXXXXXXXXXX
SKILLHUB_PRIVATE_KEY_PEM=<SkillHub开发者RSA私钥PEM>

# 支付配置
PAY_AMOUNT_FEN=990
PAY_NOTIFY_URL=https://ruancyai.com/cloud/api/pay/notify
```

### 数据库

`payments` 表记录每笔支付订单：

| 字段 | 说明 |
|---|---|
| `out_trade_no` | 商户订单号（唯一） |
| `payment_code` | X402 预下单返回的支付凭据 |
| `amount_fen` | 金额（分） |
| `status` | pending → paid → refunded |
| `transaction_id` | 微信支付交易号 |
| `paid_at` / `refunded_at` | 时间戳 |

### 关键词索引（供 SkillHub 改造检查器识别）

`X402`、`402 Payment`、`X-PAYMENT`、`WeixinPay-Required`、`WeixinPay`、`facilitator`、`payment challenge`、`payment_code`、`out_trade_no`、`order_id`、`code_url`、`preorder`、`palmpayminiapp/clawagentpay/preorder`、`SHA256withRSA`、`SKILLHUB-SHA256-RSA2048`、`developer_id`、`pub_key_id`、`AUTH_AND_PAY`、`SKILL_PAY`、`payment_required`、`nonce_str`、`refund`、`notify_url`、`quota`、`proof`、`前置检查`、`订单号传递`、`异常处理`、`decryptNotify`、`isPayConfigured`

### 计费边界

按 0.3.2 计费声明：成功创建 1 个云铺档口页（shop_id 落库即扣 1 次 ¥9.9）。**不算付费的项**：

- 调用 `POST /cloud/api/shops/{shopId}/qrcode` 上传微信二维码
- 调用 `GET /cloud/api/shops/{shopId}/share` 获取分享素材
- 调用 `GET /cloud/api/pay/status/{outTradeNo}` 查询支付状态
- 5xx/AI 生成失败导致的自动退款
- 用户取消支付（X402 协议保证 payment_code 过期不扣）
