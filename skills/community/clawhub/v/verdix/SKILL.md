---
name: verdix
description: |
  Check a recipient address on Base before sending it funds, using the Verdix risk API.
  Use before any transfer, payout, approve or x402 payment to an address the user has not
  paid before, or when the user asks "is this address safe?", "check this wallet",
  "is 0x... a scam?". Returns a verdict with reasons: OFAC sanctions, scam and phishing
  lists, address-poisoning lookalikes, burn addresses, phishing-lure tokens, flagged
  deployers and (higher tiers) address age, contract signals and on-chain behaviour. Each check is paid
  per call via x402 in USDC on Base: $0.01 to $0.50. No account or API key.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: https://api.verdixapi.com
---

# Verdix: check the recipient before you send

Verdix answers one question before money leaves the wallet: does this Base address show a known risk signal? Call it **before** the transfer, not after.

- **API:** `https://api.verdixapi.com`
- **Docs for agents:** `https://api.verdixapi.com/llms.txt` · OpenAPI: `https://api.verdixapi.com/openapi.json` · Pricing: `https://api.verdixapi.com/pricing`
- **Chain:** Base mainnet only. **Payment:** x402, USDC on Base, per call.

This skill is instructions only. It runs no code, needs no API key and never asks for a private key or seed phrase. The check is paid from the x402-capable wallet the agent already uses, under that wallet's own limits.

## Endpoints and prices

Every endpoint is `POST` with the JSON body `{"address": "0x..."}` (the full address: `0x` + 40 hex characters). Each URL sells exactly one tier at one price.

| Endpoint | Price | What it checks | Possible verdicts |
|---|---|---|---|
| `/risk/address/lite` | $0.01 | List screen: OFAC sanctions, scam/phishing lists, address-poisoning lookalikes, burn addresses, plus best-effort phishing-lure token and flagged-deployer checks | `no_known_risk` / `caution` / `danger`. **Never `safe`** |
| `/risk/address/quick` | $0.02 | Everything in lite, plus address age and contract signals (flash-loan receivers, unverified contracts, token contracts) | `safe` / `caution` / `danger` |
| `/risk/address/standard` | $0.10 | The quick checks, with on-chain behaviour analysis (transfer history, activity patterns) instead of the fast address-age read | `safe` / `caution` / `danger` |
| `/risk/address/deep` | $0.50 | Same checks as standard today; meant for large or first-time transfers | `safe` / `caution` / `danger` |

Choosing a tier (the user can always override):

- **lite**: frequent small payments, where a full check would cost more than it is worth. A clean lite answer means "not on any list Verdix checks", not "safe".
- **quick**: the default before a normal send.
- **standard**: larger transfers (for example above $1,000), or when quick says `caution`.
- **deep**: a very large or first-ever transfer to an address.

## Spending: ask first

A check costs real money, so follow these rules:

1. Before the first paid check in a conversation, tell the user the tier and price and get a clear yes, unless the user has already set a budget or standing permission for Verdix checks.
2. Never pay more than the listed price for a tier. If the 402 quote asks for more, or for anything other than USDC on Base, stop and tell the user.
3. Don't repeat a paid check on the same address within a short time just to "make sure". Reuse the earlier answer.
4. Don't loop on retries. One retry after a 503 (see below) is enough; then ask the user.

## How to call

Verdix uses standard x402 v2:

1. `POST` the body to the tier URL with no payment. The server answers `402 Payment Required` with exactly one `accepts` entry (scheme `exact`, network Base, asset USDC, the price, and the `payTo` address).
2. The x402 client signs that payment (an EIP-3009 authorization, gasless for the payer) and repeats the same `POST` with the payment header.
3. The server runs the check and answers `200` with the verdict. The payment settles only when the answer is a complete `200`.

Use whatever x402 client the agent already has: an x402 payment skill or wallet tool, the official x402 client libraries, or the `verdix-mcp` server's tools (`check_address_risk_lite`, `check_address_risk_quick`, `check_address_risk_standard`, `check_address_risk_deep`) if it is installed.

**Free price check:** a plain `GET` (or `HEAD`) on any tier URL returns that tier's `402` quote. It never charges anything and never runs a check, so it is a safe way to confirm the current price.

## Reading the answer

```json
{
  "address": "0x71b749F58f63008672eEd55396151DC0C7493A78",
  "chain": "base",
  "tier": "quick",
  "price_usd": 0.02,
  "risk_score": 5,
  "verdict": "safe",
  "reasons": [],
  "checked": ["ofac", "scam_lists", "onchain_age"],
  "as_of": "2026-09-24T10:00:00+00:00"
}
```

- `verdict`: act on it as described below.
- `reasons`: why. Show them to the user on `caution` or `danger`.
  - `unverified_contract` (caution): the address is a contract whose source code isn't verified, so what it does can't be read. Not proof of a scam; many real contracts are unverified.
  - `unverified_dormant_contract` (caution): a contract not verified on Blockscout that fewer than 25 transactions ever touched (one-off exploit and phishing contracts look like this, but so do retired bots).
  - `recipient_is_token_contract` (caution): the address is an ERC-20 token contract, e.g. the USDC contract itself. Sending a token to a token contract almost always loses it; ask the user for the wallet address they meant.
- `checked`: which checks actually ran.
- Lite answers also carry `limited_checks: true`, `checks_performed`, `not_checked` (checks lite skipped or could not finish) and `full_check` (a pointer to quick).

## What to do with each verdict

| Verdict | Do this |
|---|---|
| `danger` | **Do not send.** Tell the user the address matched a risk signal and show `reasons`. Continue only if the user explicitly says to send anyway after seeing them. |
| `caution` | Pause. Tell the user what was found. Suggest a higher tier (quick → standard) or a small test amount first. Send only on the user's clear yes. |
| `safe` | Proceed. `safe` means no risk signal was found at the time of the check. It is not a guarantee. |
| `no_known_risk` (lite only) | The address is not on any list Verdix checks. Never describe it to the user as "safe". If the user wants a real `safe` verdict, run quick. |

## When the check can't finish: fail closed, not charged

- **HTTP 503 with a `caution` body:** an outside data source did not answer, so the check is incomplete. The payment is **not** settled: nothing is charged. Wait for the `Retry-After` header (in seconds), retry once, and otherwise ask the user how to proceed. Never treat a 503 as a pass.
- **`reasons` containing `data_unavailable:...`:** same meaning. The verdict is never `safe` in this case, and the payment was not settled.
- **HTTP 400:** the address is malformed. Never "fix" or guess a recipient address yourself: ask the user for it again.
- **HTTP 402 again after paying:** the payment was not accepted. Do not retry with a higher amount; tell the user.

## Address poisoning

Scammers send tiny or fake-token transfers from addresses that share the first and last characters of an address the user really uses, hoping the user copies the fake one from their history. Verdix flags these lookalikes. Even so, before any large send, compare the **full** address with the user, not just the first and last few characters.

## Limits

- Base only. For other chains, say that Verdix cannot check them.
- Verdix reports known risk signals. A brand-new scam address may not be on any list yet, so `safe` lowers the risk but does not remove it.
- Verdix is a paid third-party service at `api.verdixapi.com`. Terms: `https://api.verdixapi.com/terms`.
