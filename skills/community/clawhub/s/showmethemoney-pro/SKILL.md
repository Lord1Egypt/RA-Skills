---
name: showmethemoney-pro
description: execute the paid showmethemoney premium action through the merchant backend. use when the user wants to unlock or run the protected showmethemoney capability, and stablepay payment should be used before retrying the backend action.
---

# ShowMeTheMoney Pro

Execute the protected ShowMeTheMoney premium action only after merchant-backend verification and StablePay payment succeed. 
This skill is only for the protected premium action exposed by `GET /execute?agent_did=<buyer_did>`

## Main workflow

When the user asks to use the premium ShowMeTheMoney capability:

1. Resolve the current buyer DID from `stablepay_runtime_status`.
2. Call the merchant backend premium endpoint:
   - `GET http://127.0.0.1:8787/execute?agent_did=<buyer_did>`
3. Treat the merchant backend as the source of truth.
4. If the backend returns `200`, return the protected result.
5. If the backend returns `402 Payment Required`:
   - Parse the x402 response from `accepts[0]`:
     - `skill_did` → from `accepts[0].extra.skillDid`
     - `price` → from `accepts[0].maxAmountRequired` (convert from minor units to decimal: divide by 1,000,000)
     - `currency` → from `accepts[0].extra.currency`
     - `facilitator_url` → from `accepts[0].extra.facilitatorUrl`
   - **NEVER** use any hardcoded or fallback values
   - call `stablepay_pay_via_gateway` with the extracted values
6. If payment succeeds, retry the same `/execute` request once.
7. If the retry still does not return `200`, explain that the premium action is still locked or verification failed.

## Premium action contract

Use this request for the premium action:

- method: `GET`
- endpoint: `http://127.0.0.1:8787/execute`
- required query parameter: `agent_did`

Optional query parameters may be used when helpful:

- `q`
- `prompt`

These optional values are forwarded to the backend as request text for the premium action. The backend should:

1. receive the premium request
2. verify purchase state via StablePay
3. return `402` when the user has not purchased the skill
4. return `200` only after verification succeeds
5. return a merchant-generated proof token in the premium result

Treat the backend response as the final authority.

## Unlocked Store (Report Store)

After successful skill purchase, the backend returns `unlocked_store` in the 200 response. Present the unlocked store information to the user and offer to browse/purchase individual research reports. Each report requires separate payment using the same x402 payment flow.

## Payment rules

When payment is required:

1. Use `stablepay_pay_via_gateway`.
2. Use the requirement returned by the backend when present.
3. Respect local payment limits already configured in the StablePay plugin.
4. Never claim payment succeeded unless StablePay returns a successful result.
5. Retry the premium action only once after a successful payment.
