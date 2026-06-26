# Alipay Paid Access

Use this when the user wants to buy, unlock, pay for, or enter a paid scenario.

## Product

- Product name: 爽文模拟器V1.0虾舍出品
- SKU default: `scenario_apocalypse_space_folding_v1`
- Price: `CNY 9.90`
- Entitlement: one paid scenario Skill package.
- Default paid scenario: 末世囤货：空间折叠
- Default package id: `xiashe-apocalypse-space-folding-v1`

## Required Merchant Flow

The skill itself should not invent payment success. Use one of these real payment surfaces:

1. A merchant MCP/tool that creates an Alipay order and returns a cashier URL.
2. A merchant backend HTTP endpoint that creates the order and returns a cashier URL.
3. A pre-created Alipay cashier URL supplied by the operator for testing.

If using the bundled TRPGLegend reference MCP, the relevant tools are:

- `paid_catalog`: list paid SKUs and the 9.9 yuan unlock policy.
- `alipay_order_create`: call the configured merchant endpoint to create an Alipay cashier order.
- `entitlement_check`: verify whether the order/session is paid before unlocking.

Recommended merchant order fields:

```json
{
  "sku": "scenario_apocalypse_space_folding_v1",
  "title": "末世囤货：空间折叠",
  "amount": "9.90",
  "currency": "CNY",
  "description": "爽文模拟器V1.0付费剧本 Skill 包",
  "userSessionId": "<agent-session-id>",
  "scenarioId": "apocalypse-space-folding-v1",
  "fulfillmentType": "skill_package",
  "skillPackageId": "xiashe-apocalypse-space-folding-v1",
  "returnUrl": "<optional>",
  "notifyUrl": "<merchant-webhook-url>"
}
```

## Agent Payment Flow

When the player selects a paid scenario:

```text
你选择的是《末世囤货：空间折叠》。
解锁价：¥9.90。

付款后将返回真正的 Skill 安装包。安装后即可在当前 Agent 中开始完整游戏。
```

Then:

1. Call the merchant payment MCP/tool to create the order.
2. If a cashier URL is returned, pass the complete URL to the Alipay payment skill/MCP.
3. Wait for payment completion.
4. Query merchant order status or receive successful payment result.
5. Call `paid_skill_fulfill` or the operator fulfillment endpoint.
6. Return the real Skill package install URL/slug.
7. Only then start or install the full scenario.

If no payment tool is available:

```text
当前 Agent 没有接入虾舍的支付宝下单 MCP，所以我还不能生成真实 9.9 元订单。
请先接入支付 MCP，或提供一个真实支付宝收银台链接/下单接口。
```

If the reference MCP returns `configured: false`, tell the operator which env vars are missing and do not unlock.

## Alipay Skill Interop

If the environment provides official Alipay payment skills:

- Use the merchant skill/API to generate a real `cashier*.alipay.com` or `*excashier*.alipay.com` URL.
- Let the Alipay payment skill handle wallet authorization, payment submission, and payment status query.
- Preserve the URL exactly; do not truncate or rewrite query parameters.
- Treat payment URLs and QR codes as short-lived sensitive links.

## Entitlement State

Track:

```text
paymentStatus: pending | paid | failed | expired
tradeNo:
sku:
scenarioId:
skillPackageId:
installUrl:
paidAt:
entitlementExpiresAt:
```

If the Agent loses state, query the merchant backend. Do not unlock from memory alone.

## Operator Setup Needed

The operator must provide:

1. Alipay merchant account/app configuration.
2. A backend or MCP tool that creates fixed-price Alipay orders.
3. A payment notify webhook.
4. An order status query endpoint/tool.
5. A fulfillment endpoint that returns the paid Skill package.
6. A mapping from paid SKU to skill package id.

For the bundled TRPGLegend MCP, configure:

```text
XIASHE_ALIPAY_ORDER_ENDPOINT=<merchant endpoint that returns cashierUrl/paymentUrl>
XIASHE_ENTITLEMENT_ENDPOINT=<merchant endpoint that returns paid=true after confirmed payment>
XIASHE_SKILL_PACKAGE_BASE_URL=<base URL for signed paid Skill package downloads>
XIASHE_PAYMENT_API_TOKEN=<optional bearer token for those endpoints>
```

For international users, mirror the same entitlement logic with Stripe Checkout.
