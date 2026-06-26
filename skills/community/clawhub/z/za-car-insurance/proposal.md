# proposal — 核保、支付与出单

---

## 一、流程概览

```
用户回复「确认投保」
    ↓
Step 1：核保+获取支付链接（整合接口）
    POST <gateway域名>/api/quickInsure/quickConfirmAndPay
    仅需传 vehicleNo + insureFlowCode，返回 zaPayUrl
    ↓
Step 2：打开支付页面（Chrome DevTools MCP）
    → 移动端适配展示支付触点
    → 用户浏览器内完成条签+支付
    ↓
Step 3：查询出单结果（支付后轮询）
    POST <gateway域名>/api/quickInsure/getCreatePolicy
```

---

## 二、Step 1：核保+获取支付链接

### `POST /api/quickInsure/quickConfirmAndPay`

**入参：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `vehicleNo` | string | ✅ | 车牌号 |
| `insureFlowCode` | string | ✅ | quickQuote 返回的流程主键 |
| `payChannel` | string | ❌ | 支付方式，默认 `wxpay`，可选 `alipay`/`unionpay` |
| `promoCode` | string | ❌ | 推广码 |

> 投保人/车主信息字段无需传入，后端自动多源回填。如需覆盖自动值，可按字段名显式传入。

**成功出参：**

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "0",
    "resultMessage": "操作成功",
    "zaPayUrl": "<支付页面链接>",
    "zaOrderNo": "<众安订单号>",
    "outTradeNo": "<外部交易订单号>",
    "expiryTime": "<核保有效期，如2026-05-26 23:30:00>",
    "insureFlowCode": "<流程主键>"
  }
}
```

| 字段 | 说明 | 用途 |
|------|------|------|
| `zaPayUrl` | 支付流程链接 | 浏览器打开 |
| `zaOrderNo` | 众安订单号 | 传给 `getCreatePolicy` |
| `outTradeNo` | 外部交易订单号 | 传给 `getCreatePolicy` |
| `expiryTime` | 核保有效期 | 展示用户，过期需重新核保 |

**错误处理：**

| result | 说明 | 处理方式 |
|--------|------|---------|
| `P11002` | 实名校验失败 | **立即终止** |
| `22015` | 证件号不能为空 | 检查字段是否传入 |
| 其他非 `0` | 核保失败 | 原文返回，最多重试 3 次 |

**CURL 示例：**

```bash
curl -X POST "<gateway域名>/api/quickInsure/quickConfirmAndPay" \
  -H "car-api-key: $CAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicleNo": "<车牌号>",
    "insureFlowCode": "<流程主键>"
  }'
```

---

## 三、Step 2：生成支付二维码（供用户手机扫码）

> **核心原则**：支付链接通过二维码展示，用户用手机扫码完成条签和支付，所有支付操作在手机端进行，不在桌面端直接打开 zaPayUrl。

拿到 `zaPayUrl` 后，调服务端二维码接口，在浏览器展示扫码页面：

### Step 2-1：构造二维码页面 URL

```
GET <gateway域名>/api/quickInsure/payQrcode
  ?url=<zaPayUrl（需 URL encode）>
  &orderNo=<outTradeNo>
  &expiryTime=<expiryTime（需 URL encode）>
  &car-api-key=<$CAR_API_KEY（需 URL encode）>
```

示例：
```
<gateway域名>/api/quickInsure/payQrcode?url=<zaPayUrl（需 URL encode）>&car-api-key=<encoded_key>
```

> 需要鉴权，`car-api-key` 作为 query 参数传入（与 header 等效）。服务端生成二维码 PNG 内嵌在 HTML 中返回，完全离线渲染，无外部依赖。

### Step 2-2：用浏览器打开二维码页面

优先用 Chrome DevTools MCP：
```javascript
mcp__plugin_chrome_devtools__new_page(url="<上一步构造的 URL>")
```

MCP 不可用时降级：
```bash
open "<上一步构造的 URL>"
```

### Step 2-3：在对话中展示提示

```
✅ 核保通过！

📱 已为您打开支付二维码页面，请用手机扫码完成条款签署和支付。

⏰ 支付截止：[expiryTime]
📋 订单号：[outTradeNo]

完成支付后告诉我，我将为您查询出单结果。
```

> ⚠️ **不要**直接在浏览器里打开 zaPayUrl，支付链接仅适配手机端。

> 缓存 `zaOrderNo` 和 `outTradeNo`，用于出单查询。

---

## 四、Step 3：出单结果查询

### `POST /api/quickInsure/getCreatePolicy`

```bash
curl -X POST "<gateway域名>/api/quickInsure/getCreatePolicy" \
  -H "car-api-key: $CAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicleNo": "<车牌号>",
    "zaOrderNo": "<众安订单号>",
    "outTradeNo": "<外部交易订单号>"
  }'
```

**出单结果展示：**

```
🎉 保单已出单！

商业险保单号：[businessPolicyNo]
交强险保单号：[compelPolicyNo]

电子保单将在 5 分钟内发送至投保人手机，请注意查收。
```

若 `recordId` = 0，提示用户"出单处理中，请稍后再次查询"。
