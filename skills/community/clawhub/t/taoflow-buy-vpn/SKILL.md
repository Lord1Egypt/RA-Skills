---
name: buy-taoflow-vpn
description: Guide users to choose and purchase Taoflow VPN plans safely and efficiently. Use when users ask about buying Taoflow VPN, selecting a plan, comparing billing cycles, payment methods, onboarding after purchase, refunds, or purchase troubleshooting.
---

# Buy Taoflow VPN

## Goal
Help users complete purchase with confidence, without fabricating pricing or policy details.

## Workflow
1. Clarify user intent: new purchase, renewal, upgrade, payment failure, or refund question.
2. Collect the minimum required info:
   - preferred billing cycle (monthly/yearly)
   - region/device count
   - budget sensitivity
   - preferred payment method
3. Provide recommendation with transparent trade-offs.
4. Give direct next step (official purchase URL + exact action).
5. Confirm post-purchase onboarding steps and support contact.

## Rules
- Never invent prices, discounts, guarantees, or refund terms.
- If price/policy is unknown, explicitly say so and point to official source.
- Prefer concise, action-oriented responses.
- Highlight account and payment security reminders when relevant.

## Response Template
Use this compact structure:

1) **Recommended plan**: <plan + who it fits>
2) **Why**: <2-3 short reasons>
3) **Cost & billing**: <known facts only>
4) **How to buy**: <official URL + steps>
5) **After purchase**: <login/setup/import/subscription check>
6) **Need help?**: <official support channel>

## Verified Facts (taoflow.network)
- Official site: https://taoflow.network
- Product flow: choose country/plan → pay with crypto → download WireGuard config
- Positioning: no account/email required, crypto payments, WireGuard delivery
- Claimed provisioning time: typically 5–15 minutes after on-chain confirmation
- Recovery flow exists: users can restore order via recovery key

## API Mode (Programmatic Purchase)
When the user asks for automated/programmatic purchase, switch to API mode.

### Discovery
- API guide: https://taoflow.network/api.html
- OpenAPI spec: https://taoflow.network/openapi.json
- Plugin manifest: https://taoflow.network/.well-known/ai-plugin.json

### Endpoints (verify against OpenAPI first)
- GET /plans
- GET /countries
- GET /payment-methods
- POST /orders (plan_id, country_code, optional pay_currency)
- GET /orders/{id} with Bearer access_token
- GET /orders/{id}/config with Bearer access_token
- POST /orders/recover (with recovery_key)

### API Flow
1. Read available plans/countries/payment methods.
2. Confirm plan, country, and payment currency with user.
3. Create order and return pay_amount/pay_address/order_id to user.
4. Require explicit user confirmation before any external payment-trigger action.
5. Poll order status until paid and provisioning completes.
6. Fetch wg_config and provide clean setup steps for WireGuard client.

### Security Rules (API mode)
- Never expose full access_token or recovery_key in chat logs unless user explicitly asks.
- Mask secrets when echoing results (e.g., first 4 + last 4 chars).
- Never claim payment is complete before order status confirms it.
- If provisioning delays, state expected wait and keep polling calmly.

## Missing-Info Handling
If pricing/policy details are missing, ask for:
- latest plan table (duration/country/price)
- accepted payment-method constraints (minimums, chain/network)
- refund and support policy links
Then continue with verified details only.
