---
name: showmethemoney-lite
description: paid stablepay demo skill for openclaw. use when the user wants to try a monetized skill flow with a visible price, stablepay wallet setup, and in-chat payment handling, but without strict backend purchase enforcement.
---

# ShowMeTheMoney Lite

Provide a weak-protection paid demo skill that can guide the user through a StablePay purchase flow for a lightweight premium action.

## Merchant configuration

Use the following merchant placeholders for this skill:

- skill_name: `{{SKILL_NAME}}`
- skill_did: `{{SKILL_DID}}`
- default_price_usdc: `{{PRICE_USDC}}`
- currency: `{{CURRENCY}}`
- stablepay_gateway_base_url: `{{STABLEPAY_GATEWAY_BASE_URL}}`
- lite_preview_endpoint: `{{LITE_PREVIEW_ENDPOINT}}`
- lite_paid_demo_endpoint: `{{LITE_PAID_DEMO_ENDPOINT}}`

Replace all placeholders before publishing a real version.

## Required runtime assumptions

Proceed only if all of the following are true:

- the StablePay plugin is installed and enabled
- a local wallet runtime is available
- the StablePay backend is reachable
- this skill's demo endpoint is reachable if the paid demo action needs it

If any dependency is missing, explain what is unavailable and stop.

## Preflight workflow

Before attempting any paid action:

1. Call `stablepay_runtime_status`
2. If no local wallet exists, call `stablepay_create_local_wallet`
3. If no backend DID is registered, call `stablepay_register_local_did`
4. If payment limits are missing, call `stablepay_configure_payment_limits`
5. If no payment policy exists, call `stablepay_build_payment_policy`

Do not continue to the paid action if wallet setup, DID registration, or payment policy setup is incomplete.

## Public preview behavior

When the user asks what this skill does, provide a free preview first.

The free preview may include:

- a short explanation of the demo
- a teaser result
- a sample response showing what the premium result would look like

Do not claim that the free preview means the user has purchased the premium action.

## Paid demo behavior

When the user explicitly requests the paid demo action:

1. Explain that this skill requires payment for the premium demo action.
2. Show the configured price and currency using:
   - price: `{{PRICE_USDC}}`
   - currency: `{{CURRENCY}}`
   - skill_did: `{{SKILL_DID}}`
3. Attempt the paid demo endpoint if one exists.
4. If the backend or demo flow returns HTTP `402 Payment Required`, explain that payment is required.
5. Use the StablePay plugin to complete payment:
   - prefer `stablepay_pay_via_gateway`
   - use `stablepay_execute_paid_skill_demo` only for the dedicated demo route
6. Only continue after the StablePay backend confirms purchase or payment completion.
7. After payment succeeds, retry the premium demo action once.
8. If payment fails, verification fails, or the retry still fails, stop and explain the failure.

## Purchase integrity rules

- Treat local wallet state and local policy state as setup information only.
- Do not treat local state as proof of purchase.
- Treat StablePay backend confirmation as the source of truth for whether payment succeeded.
- Do not claim purchase success unless the backend or payment response confirms it.

## Intended protection level

This skill is a weak-protection paid skill.

That means:

- it may still use StablePay and trigger a real payment flow
- it is suitable for demos and lightweight premium actions
- it does not rely on strict backend verification for every protected capability
- it should not be presented as a fully tamper-resistant commercial skill

## Safety

- Never expose private keys, mnemonic material, decrypted local state, API keys, or backend secrets.
- Never invent a successful purchase.
- Treat local payment limits as user protection only.
- Never bypass StablePay when this skill declares that a premium action is paid.