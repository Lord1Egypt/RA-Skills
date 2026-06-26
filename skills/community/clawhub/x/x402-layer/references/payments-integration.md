# Integrating Payments Into Your App

Use this reference when the goal is not just "pay for an API", but "add Singularity payments to a product, app, bot, or platform".

## Choose the Right Payment Shape

### 1. Direct endpoint payments
Use this when every request should be paid at the moment it is made.

Good for:
- one-shot API calls
- premium actions behind a button
- low-volume or high-value requests

Core flow:
1. create or reuse an endpoint
2. point the endpoint at your origin
3. let the caller hit the endpoint URL
4. x402 returns a `402 Payment Required` challenge
5. caller signs locally and retries with `X-Payment`

Primary scripts:
- `create_endpoint.py`
- `pay_base.py`
- `pay_solana.py`

### 2. Credits-based endpoint payments
Use this when the caller may hit the same endpoint repeatedly and you want lower latency after the initial purchase.

Good for:
- chat apps
- repeated inference
- high-frequency automations
- cases where blockchain wait per request is too slow

Core flow:
1. endpoint is configured for credits
2. buyer purchases a credit pack once
3. later calls spend credits with header-based access

Primary scripts:
- `recharge_credits.py`
- `check_credits.py`
- `consume_credits.py`

### 3. Product purchases
Use this when the payment unlocks a file, digital asset, or one-time download.

Good for:
- datasets
- templates
- media files
- downloadable deliverables

Primary script:
- `consume_product.py`

## Hosted UI vs Custom UI

### Route A: Hosted payment pages
Fastest path if you do not want to build UI yet.

Examples:
- product page: `https://studio.x402layer.cc/pay/<slug>`
- endpoint request page: `https://studio.x402layer.cc/pay/request/<slug>`
- credits page: `https://studio.x402layer.cc/pay/credits/<slug>`

Use this when:
- you want a payment page immediately
- you do not want to build wallet/payment UI yourself
- you only need checkout plus fulfillment

### Route B: Custom UI on your platform
Use this when you want your own buttons, cards, or checkout flow.

Core pattern:
1. your app calls the x402 endpoint or product URL
2. the API returns a `402` challenge
3. your wallet/client signs locally
4. your app retries with `X-Payment`
5. your server fulfills after webhook and/or receipt verification

This is the default route for agentic integrations today.

## Recommended Agent Workflow

For a new integration, do this in order:

1. Decide the payment shape:
   - direct endpoint
   - credits
   - product
2. Create or reuse the monetized resource.
3. Verify your origin checks `x-api-key` if you are using an endpoint.
4. Add a webhook for server-side fulfillment.
5. Verify the webhook signature.
6. Verify the receipt JWT if the action unlocks something important.
7. Only after successful verification, grant access, update state, or deliver the item.

## Can One Generic Endpoint Also Be the Payment Endpoint?

Yes.

A normal monetized endpoint can be:
- the endpoint that receives paid traffic
- the backend action your UI button ultimately calls
- the source slug you verify in webhook and receipt checks

You only need separate endpoints when you want different pricing, isolated accounting, or different fulfillment logic.

## Passing Custom Data Through Payments

Append query parameters to any payment URL and they will appear in the webhook `metadata` field after payment succeeds.

### Hosted pay page
```
https://studio.x402layer.cc/pay/credits/my-api?order_id=abc-123&plan=pro
```

### Direct endpoint
```
https://api.x402layer.cc/e/my-api?factory_payment_id=f1ee6b40-...
```

### Embed / iframe
When building payment links in embedded components, append query params to the endpoint URL the component navigates to. The params survive through the full payment flow.

### Correlation

Use `?client_reference_id=<your-id>` for a dedicated top-level field in the webhook, or use any custom param name for passthrough into `metadata`.

See `references/webhooks-verification.md` for the full payload schema, supported patterns, reserved params, and limits.

## Fulfillment Patterns

### Pattern 1: Server-side webhook unlock
Best for:
- subscriptions
- credit grants
- order state updates
- internal entitlement changes

Flow:
1. buyer completes payment
2. x402 sends webhook to your server
3. your server verifies signature and receipt
4. your server marks order as paid

### Pattern 2: Immediate response unlock
Best for:
- instant API consumption
- one-shot product responses

Flow:
1. client retries with `X-Payment`
2. x402 verifies and forwards
3. origin returns the protected response immediately

### Pattern 3: Hybrid
Use both:
- immediate client success for UX
- webhook/receipt verification for durable state

This is the safest default for real products.

## Receipt Verification

Use receipt verification when:
- the payment unlocks something valuable
- you need auditability
- you want strong proof beyond just trusting a client-side success message

Primary helper:
- `verify_webhook_payment.py`

SDK docs:
- `https://studio.x402layer.cc/docs/developer/sdk-receipts`

## Suggested Defaults

If the user asks for the "best default" path:

- use **Base** first for the simplest production flow
- use **direct endpoint payments** for low-volume premium actions
- use **credits** for repeated API usage
- use **webhook + receipt verification** for fulfillment
- use hosted pay pages only when you want speed over custom UI

## Minimal Launch Checklist

- endpoint or product created
- API schema attached (if your origin has multiple routes/params)
- origin verifies `x-api-key` when using endpoints
- webhook configured
- signing secret stored securely
- webhook signature verification implemented
- receipt verification implemented for valuable unlocks
- one real Base payment tested end-to-end
