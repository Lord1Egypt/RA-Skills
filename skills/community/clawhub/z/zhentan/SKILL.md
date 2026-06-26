---
name: zhentan
description: Zhentan is your personal onchain security agent and co-signer. It monitors pending multisig transactions, screens them against behavioral patterns and security risk data, and auto-signs safe ones — blocking or flagging suspicious activity before it executes. Use when the user wants to review pending transactions, approve or reject a transaction, check risk scores, toggle screening mode, view transaction history, or queue and process an invoice.
metadata:
  openclaw:
    requires:
      bins: ["curl"]
      env: ["AGENT_SECRET"]
    primaryEnv: "AGENT_SECRET"
---

# Zhentan — Onchain Security Agent & Co-Signer

## Authentication & caller identity

Every request to the server MUST include two things:

**1. Agent secret** — proves the request came from this skill (not a random caller):
```
Authorization: Bearer $AGENT_SECRET
```
Always add `-H "Authorization: Bearer $AGENT_SECRET"` to every `curl` call.

**2. Caller identity** — identifies which Telegram user triggered the action. Extract the numeric user ID from your session context (`origin.from`) and build:
```json
"callerId": "telegram:<origin.from>"
```
Include this in all POST and PATCH request bodies, and as `?callerId=telegram:<origin.from>` on GET requests.

If `origin.from` is unavailable, omit `callerId` rather than sending a placeholder.

Zhentan acts as an intelligent co-signer on your Safe smart account. It learns how you transact — amounts, timing, tokens and recipients — and screens every pending transaction against your behavioral profile and external security scanners (GoPlus, Honeypot.is, De.fi) before execution.

Safe transactions are auto-signed and executed instantly. Borderline ones are surfaced for your review. Clearly malicious transactions are blocked outright.

Base URL: `https://api.zhentan.me`

## How it works

1. **Owner** proposes a transaction — signs 1-of-2, POSTs to `POST /queue`
2. **Server** runs inline risk analysis and either:
   - **APPROVE** (risk < 40): auto-executes on-chain, sends Telegram notification
   - **REVIEW** (risk 40–70): marks `inReview`, sends Telegram asking owner to approve/reject
   - **BLOCK** (risk > 70): marks `inReview`, sends urgent Telegram alert
3. **Agent** (you) handles owner commands via Telegram — execute scripts, call endpoints, report results

Your role is **conversational** — the server owns the deterministic pipeline.

## Transaction lifecycle

- `pending` → queued, not yet processed
- `in_review` → flagged by server (REVIEW or BLOCK), awaiting owner decision
- `executed` → co-signed and submitted on-chain
- `rejected` → owner rejected it

---

## Owner commands

Run each command immediately, wait for the result, then report the actual outcome. Never fabricate results.

### approve `tx-XXX`
When the owner says "approve tx-XXX" or taps ✅ Approve:

1. Co-sign and execute via the server:
```bash
curl -s -X POST https://api.zhentan.me/execute \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"txId":"tx-XXX","callerId":"telegram:<origin.from>"}'
```
   Parse the JSON: on success `status` is `executed` and `txHash` is the on-chain hash; if `status` is `already_executed`, use the returned `txHash`. On failure the body includes `error`.

2. Update the Telegram notification with the tx hash from step 1:
```bash
curl -s -X POST https://api.zhentan.me/notify-resolve \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"txId":"tx-XXX","action":"approved","txHash":"THE_TX_HASH","callerId":"telegram:<origin.from>"}'
```
3. Reply with the actual tx hash.

The tx-id includes the `tx-` prefix (e.g. `tx-cc34ee59`). Pass it exactly as written.

### reject `tx-XXX`
When the owner says "reject tx-XXX" or taps ❌ Reject:

1. Mark rejected (optionally include a reason):
```bash
curl -s -X PATCH https://api.zhentan.me/transactions/tx-XXX \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"action":"reject","reason":"Rejected by owner","callerId":"telegram:<origin.from>"}'
```
2. Update the Telegram notification:
```bash
curl -s -X POST https://api.zhentan.me/notify-resolve \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"txId":"tx-XXX","action":"rejected","callerId":"telegram:<origin.from>"}'
```
3. Reply confirming the rejection.

### mark for review `tx-XXX`
When you need to flag a transaction for manual review:
```bash
curl -s -X PATCH https://api.zhentan.me/transactions/tx-XXX \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"action":"review","reason":"Flagged for manual review","callerId":"telegram:<origin.from>"}'
```

### check pending
Check if there are pending transactions for a Safe:
```bash
# 1. Check screening mode
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/status?safe=0xSAFE_ADDRESS"

# 2. List transactions (filter client-side for !executedAt && !inReview && !rejected)
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/transactions?safeAddress=0xSAFE_ADDRESS"
```

### get status
Get screening mode, patterns, and global limits for a Safe:
```bash
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/status?safe=0xSAFE_ADDRESS"
```

### toggle screening
Turn screening on or off for a Safe:
```bash
# Turn on
curl -s -X PATCH https://api.zhentan.me/status \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"safe":"0xSAFE_ADDRESS","screeningMode":true,"callerId":"telegram:<origin.from>"}'

# Turn off
curl -s -X PATCH https://api.zhentan.me/status \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"safe":"0xSAFE_ADDRESS","screeningMode":false,"callerId":"telegram:<origin.from>"}'
```

### update limits
Update global limits for a Safe (any combination of fields):
```bash
curl -s -X PATCH https://api.zhentan.me/status \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{
    "safe": "0xSAFE_ADDRESS",
    "maxSingleTx": "5000",
    "maxDailyVolume": "20000",
    "riskThresholdApprove": 40,
    "riskThresholdBlock": 70,
    "learningEnabled": true,
    "callerId": "telegram:<origin.from>"
  }'
```

---

## Analysis commands

### quick risk score
Fetch the stored risk score for a transaction (computed at queue time):
```bash
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/transactions/tx-XXX"
# Returns: riskScore, riskVerdict, riskReasons
```

### deep analyze `tx-XXX`
Run immediately, wait for the response (5–15s), then report the actual findings.

When the owner taps 🔎 Deep Analyze or asks "analyze tx-XXX", "is this safe?", "why was this flagged?":

```bash
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/analyze/tx-XXX?callerId=telegram:<origin.from>"
```

Parse the JSON and present:
- `addressSecurity.flags` — scam, phishing, sanctions, money laundering
- `tokenSecurity.flags` — honeypot, mintable, blacklist, hidden owner, tax rates
- `honeypot` — simulation results (non-stablecoins only)
- `recipient.known` / `recipient.totalTxCount` — behavioral history

Highlight red flags prominently. If `safe: true` and `totalFlags: 0`, reassure the owner.

### behavioral event log
View the event history for a Safe:
```bash
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/events?safe=0xSAFE_ADDRESS&limit=50"
```

---

## Rules management

### list rules
```bash
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/rules?safe=0xSAFE_ADDRESS"
```

### create rule
```bash
curl -s -X POST https://api.zhentan.me/rules \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{
    "safe": "0xSAFE_ADDRESS",
    "name": "Block large transfers",
    "ruleType": "amount_limit",
    "conditions": {"maxAmount": "1000"},
    "action": "block",
    "priority": 10,
    "callerId": "telegram:<origin.from>"
  }'
```
Valid `ruleType`: `amount_limit`, `recipient_block`, `recipient_whitelist`, `time_restriction`, `velocity_limit`, `token_restriction`, `custom`
Valid `action`: `approve`, `review`, `block`

### update rule
```bash
curl -s -X PATCH https://api.zhentan.me/rules/RULE_ID \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"isActive": false, "callerId": "telegram:<origin.from>"}'
```

### delete rule
```bash
curl -s -X DELETE -H "Authorization: Bearer $AGENT_SECRET" https://api.zhentan.me/rules/RULE_ID
```

---

## Invoice detection

When a user sends an invoice file or message:

1. Extract fields:
   - **to** (wallet address, required)
   - **amount** (required), **token** (default: USDC)
   - **invoiceNumber**, **issueDate**, **dueDate**
   - **billedFrom**, **billedTo** — `{name, email}` objects
   - **services** — `[{description, quantity, rate, total}]`
   - **riskScore** (0–100) — assess based on: known vs unknown recipient (check `GET /status`), amount vs history, due date urgency
   - **riskNotes** — brief explanation

2. Queue it:
```bash
curl -s -X POST https://api.zhentan.me/invoices \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"to":"0x...","amount":"500","token":"USDC","invoiceNumber":"INV-001","riskScore":20,"sourceChannel":"telegram","callerId":"telegram:<origin.from>"}'
```

3. Confirm: "Invoice [number] for [amount] [token] queued. Check your Zhentan dashboard to approve."

If the invoice is missing a wallet address, ask the user to provide one.

### list invoices
```bash
curl -s -H "Authorization: Bearer $AGENT_SECRET" "https://api.zhentan.me/invoices"
```

### update invoice status
```bash
curl -s -X PATCH https://api.zhentan.me/invoices \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AGENT_SECRET" \
  -d '{"id":"inv-XXXXXXXX","status":"approved","txId":"tx-XXX","callerId":"telegram:<origin.from>"}'
```
Valid `status`: `queued`, `approved`, `executed`, `rejected`

---

## Risk scoring reference

| Factor | Score |
|--------|-------|
| Unknown recipient | +40 |
| Amount > 3× recipient average | +25 |
| Outside allowed hours (UTC) | +20 |
| Exceeds single-tx limit | +30 |
| Would exceed daily volume | +20 |
| Custom rule triggered | varies |

Verdicts: **APPROVE** (<40) · **REVIEW** (40–70) · **BLOCK** (>70)
Thresholds are per-Safe and configurable via `PATCH /status`.
