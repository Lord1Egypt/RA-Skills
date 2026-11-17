---
name: crypto-payments
description: Create a Shieldz crypto payment link or tip jar for a wallet the USER explicitly provides, and read payment status back. Use ONLY when the user directly asks to create a crypto payment link or tip jar (or to check what a Shieldz link has received), has named or confirmed the destination wallet, and has confirmed the amount. Do not infer or auto-create from vague phrasing. Every creation sends data to the external Shieldz service (shieldz.cash) and must be confirmed with the user first.
---

# Shieldz crypto payments

Turn a wallet address the **user controls** into a hosted crypto payment link or a
reusable tip jar via Shieldz, and read back how much has been paid. Non-custodial:
funds settle straight to the user's wallet; Shieldz never holds funds or keys.
Keyless: no account and no API key.

## Read this before using it (data & privacy)

This skill calls **external Shieldz network services**, the keyless REST API at
`https://shieldz.cash/api/v1/...` and, optionally, the remote MCP server at
`https://shieldz.cash/mcp`. It is **not** a local or offline flow.

On each action, the following is transmitted to Shieldz (a third party):

- the destination **wallet address**, chain, and asset
- the **amount** and any **memo / title** the user provides
- an **email address**, only if the user explicitly provides one (see below)
- when reading status, the **manage_token**

Treat every `manage_url` / `manage_token` as a **private access credential**:
anyone holding it can read the account's totals and settings. Do not post them
publicly, paste them into shared contexts, or write them to logs.

Only proceed if the user is comfortable sending the above to Shieldz's external
infrastructure. This skill does **not** collect credentials, read local files,
harvest environment variables, run dynamic code, or persist anything on the
machine. It contacts `shieldz.cash` and nothing else.

## When to use, and when NOT to

Use this skill only when **all** of these hold:

- the user **explicitly asks** to create a Shieldz crypto payment link or tip jar,
  or to check what a specific Shieldz link received, **and**
- the user has **named or confirmed the destination wallet address**, **and**
- for a fixed-amount link, the user has **confirmed the amount**.

Do **not** activate on vague or adjacent phrasing such as "I need to get paid",
"how do payments work", or "set something up". If the intent, the wallet, or the
amount is unclear, **ask, do not create anything**.

**Confirm before every external call.** Before creating a link or tip jar,
restate the exact wallet address, chain, asset, amount, memo, and whether an
email will be sent, then get an explicit "yes". Never create autonomously and
never batch-create.

## Email is optional and consent-gated

`email` is optional and only lets the human owner claim a dashboard later.
Because it is **personal data sent to a third party**, do **not** include it
unless the user explicitly provides an address and agrees to send it. Omit it by
default, settlement works without it.

## Create a payment link (fixed amount)

Keyless, no `Authorization` header. Only call this after the confirmation above.

```bash
curl https://shieldz.cash/api/v1/links \
  -H "Content-Type: application/json" \
  -d '{
    "settlement": { "chain": "BASE", "asset": "USDC", "address": "0xUserProvidedWallet" },
    "amount_usd_cents": 4900,
    "memo": "Order #1234"
  }'
```

- `chain`: `BASE`, `ARBITRUM`, `OPTIMISM`, `POLYGON`, or `ETHEREUM`. `asset`: `USDC` or `USDT`.
- `amount_usd_cents`: amount in USD cents (`4900` = `$49.00`, range `$1`-`$100k`).
- Response includes `pay_url` (share this with the payer), and `manage_url` +
  `manage_token` (**private**, keep secret per the rules above).

Give the payer the `pay_url`. Do not add `email` unless the user opted in.

## Create a tip jar (pay-what-you-want, reusable)

```bash
curl https://shieldz.cash/api/v1/tip-jars \
  -H "Content-Type: application/json" \
  -d '{
    "settlement": { "chain": "BASE", "asset": "USDC", "address": "0xUserProvidedWallet" },
    "title": "Buy me a coffee",
    "suggested_amounts_usd_cents": [300, 500, 1000]
  }'
```

Response includes `url` (share this) and `manage_token` (**private**).

## Read status (how much has been paid)

```bash
curl https://shieldz.cash/a/<manage_token>.json
```

Returns totals and the invoice list. The `manage_token` is a capability secret,
only use one the user has given you, never guess it, and never share it.

## Optional: MCP instead of REST

If the agent uses MCP, the same three actions are available keyless via the
Shieldz MCP server: remote at `https://shieldz.cash/mcp`, or local with a
**pinned** version `npx -y @shieldz/mcp@0.3.0`. Tools: `create_payment_link`,
`create_tip_jar`, `get_account_status`. The same confirmation, data-disclosure,
and email-consent rules above apply unchanged.

## Safety summary

- Contacts `shieldz.cash` only. No other network destination.
- Confirms wallet + amount + email-choice with the user before every creation.
- Never creates from vague intent, and never creates without an explicit "yes".
- `manage_url` / `manage_token` are private, protect them like a password.
- `email` is optional, consent-gated, and off by default.
- No local persistence, no credential / environment / file access, no dynamic
  code execution, and a pinned MCP dependency.
