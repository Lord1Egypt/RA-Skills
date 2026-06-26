---
name: uah-mono-payouts
description: Use when a user wants an agent to convert USDT BEP20 into UAH payout instructions through a verified exchanger flow with approval, expiry, and payment monitoring.
homepage: https://mcp-wallet.mandate.md
metadata:
  openclaw:
    emoji: "💳"
    category: finance
    tags:
      - payments
      - mcp
      - usdt
      - bep20
      - uah
      - exchanger
      - approval
      - telegram
    requires:
      mcp:
        - https://mcp-wallet.mandate.md/mcp
---

# UAH Mono Payouts

Use this skill when a user asks you to convert USDT BEP20 into a UAH payout through an exchanger.

MVP scope is narrow:

- Source asset: USDT.
- Source network: BEP20 / BNB Smart Chain.
- Destination: UAH.
- Contact source: agent-owned context, usually `./mandate-wallet/contacts.csv`.
- Human approval: web approval link.
- Status monitoring: poll the MCP order status every 60 seconds.

Do not use this skill for other tokens, other chains, portfolio management, generic wallet operations, or unrelated exchange flows.

## Mandatory Rules

You must fail closed.

- Never invent exchange rates, deposit addresses, comments, order IDs, expiry times, or support contacts.
- Never scrape exchanger pages yourself.
- Never tell the user to send funds before the order is approved.
- Never tell the user to send funds when the order expires in under 60 seconds.
- Never continue if MCP is unavailable or order status is unclear.
- Always show the network as `BEP20 / BNB Smart Chain`, not just `USDT`.
- Always warn that wrong network, wrong amount, missing memo/comment, or reused expired orders can lose funds.
- Always preserve exchanger name, order ID, order link, created time, expiry time, and support path.

## Mandatory Flow

1. Parse the user's payout intent.
2. Resolve the recipient from your own context, usually `./mandate-wallet/contacts.csv`.
3. If no contact matches, ask the user to add the recipient locally or provide exact Monobank UAH details.
4. If multiple UAH accounts match, ask which account to use.
5. If the UAH amount is ambiguous, ask whether the user means:
   - receive that UAH amount, or
   - send USDT worth that UAH amount.
6. Build a `payout` object with exact bank details.
7. Call `quote_uah_payout`.
8. Present the best route briefly.
9. Call `create_uah_payout_order`.
10. Send the approval URL.
11. Wait for approval.
12. Call `render_payment_instructions`.
13. Show the exact payment instructions only if `can_send` is true.
14. Call `get_order_status` every 60 seconds until the order reaches a final state.

Final states:

- `completed`
- `expired`
- `rejected`
- `failed`
- `cancelled`

If status becomes `support_needed`, show exchanger support details and stop automatic retries.

## Contact Resolution

Contacts usually live in the agent's local project:

```text
./mandate-wallet/contacts.csv
```

Supported UAH rails:

- `monobank_uah_card`
- `monobank_uah_iban`

For `monobank_uah_card`, the contact must include a card number.

For `monobank_uah_iban`, the contact must include IBAN, EDRPOU, and recipient full name.

Pass selected details to MCP as `payout`. For a Monobank card:

```json
{
  "rail": "monobank_uah_card",
  "currency": "UAH",
  "card_number": "4441111122223333",
  "recipient_full_name": "Swift Adviser",
  "telegram": "@SwiftAdviser",
  "email": "swiftadviser@gmail.com"
}
```

For a Monobank IBAN:

```json
{
  "rail": "monobank_uah_iban",
  "currency": "UAH",
  "iban": "UA...",
  "edrpou": "12345678",
  "recipient_full_name": "Swift Adviser LLC",
  "telegram": "@SwiftAdviser",
  "email": "swiftadviser@gmail.com"
}
```

If an exchanger asks for Telegram, use the contact Telegram if present. If missing and the flow requires a fallback, use:

```text
@SwiftAdviser
```

If an exchanger requires email and the contact has none, use:

```text
swiftadviser@gmail.com
```

Do not invent bank details.

## Amount Semantics

Plain language like this is ambiguous:

```text
переведи мне USDT в 5000 гривен
```

Ask one clarifying question:

```text
5000 UAH should be the amount received, or should I send USDT worth about 5000 UAH?
```

If the user says they want to receive 5000 UAH, use:

```json
{ "amount_semantics": "receive_fixed_uah" }
```

If the user says they want to send a 5000 UAH equivalent, use:

```json
{ "amount_semantics": "send_uah_equivalent" }
```

For a request like:

```text
выведи 500 usdt bep20 на mono uah
```

Treat `500` as fixed USDT to send:

```json
{
  "amount": "500",
  "amount_currency": "USDT",
  "amount_semantics": "send_uah_equivalent",
  "source_token": "USDT",
  "source_network": "BEP20"
}
```

## MCP Tools

Use the MCP server:

```text
https://mcp-wallet.mandate.md/mcp
```

Expected tools:

- `contacts_search`
- `quote_uah_payout`
- `create_uah_payout_order`
- `get_order_status`
- `cancel_order`
- `render_payment_instructions`
- `check_usdt_bep20_balance`

### `contacts_search`

Optional compatibility helper for deployments that expose server-side demo contacts. Do not depend on it for the normal personal-agent flow.

If `requires_disambiguation` is true, ask the user which account to use before quoting.

### `quote_uah_payout`

Use after payout details and amount semantics are known. Include the selected `payout` object when available.

The backend ranks BestChange-derived exchanger options. You do not manually choose rates from websites.

Show one best route unless the user asks for alternatives.

### `create_uah_payout_order`

Use after the user has implicitly confirmed the route or asks to proceed. Include the same `payout` object used for quoting.

This creates an exchanger order and returns an approval URL. It does not mean the user should send funds yet.

### `render_payment_instructions`

Use only after approval.

If the tool returns `can_send: false`, show its message and do not add payment instructions.

### `get_order_status`

Poll every 60 seconds after payment instructions are shown.

Stop polling when the order is final.

### `check_usdt_bep20_balance`

Use only as a diagnostic probe for a known deposit address. It does not replace order status and must not be used to infer approval.

## User-Facing Messages

Keep messages short and operational.

### Route Found

```text
Found route

You receive: 5000 UAH
You send: 119.84 USDT
Network: BEP20 / BNB Smart Chain
Exchanger: Swap-line
Rate: 41.72 UAH
Expires: 18:42 WITA

Approve:
https://mcp-wallet.mandate.md/approve/...
```

### Payment Instructions

```text
Send now

Amount: 119.84 USDT
Network: BEP20 / BNB Smart Chain
Address: 0x...
Comment: SL-483920
Expires: 18:42 WITA

Send the exact amount. Do not use another network. Do not reuse this order after expiry.
```

### Under 60 Seconds

```text
Do not send.

This order expires in under 60 seconds. I will create a fresh one if you want to continue.
```

### Completed

```text
Payment received.

Order: SL-483920
Tx: 0x...
Status: completed
```

### Support Needed

```text
Support needed.

Order: SL-483920
Exchanger: Swap-line
Reason: partial payment detected
Support: https://...
```

## What Not To Do

Do not say:

```text
Send any amount around 120 USDT.
```

Say:

```text
Send exactly 119.84 USDT.
```

Do not say:

```text
Send USDT.
```

Say:

```text
Send USDT on BEP20 / BNB Smart Chain.
```

Do not say:

```text
The order is probably still valid.
```

Say:

```text
I need to check the order status before you send.
```

## Fail-Closed Behavior

If any required tool fails, stop the payment flow and explain the precise blocker:

- contacts unavailable
- contact details incomplete
- quotes unavailable
- order creation failed
- approval expired
- order expires in under 60 seconds
- payment status unclear
- provider status unclear

Never continue by guessing.
