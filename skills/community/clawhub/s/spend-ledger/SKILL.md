---
name: spend-ledger
description: Tamper-evident payment ledger for autonomous agents — auto-detects payments across all tools, prevents duplicate payments, and presents full spending history.
version: 0.4.0
metadata:
  openclaw:
    emoji: "💰"
    homepage: https://spend-ledger.com
    requires:
      bins:
        - node
    os:
      - macos
      - linux
---

# spend-ledger

You have access to an agent spending tracker. Payments made through any tool — wallet tools (agent-wallet-cli, v402, ClawRouter, payment-skill), traditional payment APIs (Stripe, PayPal, etc.), crypto transfers, or any other payment mechanism — are detected and logged automatically. The log is tamper-evident (hash-chained) and deduplicated by transaction hash and idempotency key.

## Available Tools

### log-transaction.sh

Manually log a payment transaction. **Do not call this during or immediately after a payment** — the hook detects payments automatically, and calling this first blocks the hook from creating the richer auto record. Only use this if you check `query-log.sh` and confirm no record was created for a transaction that just completed. Also valid for recording manual expenditures the agent didn't make. Duplicates (same tx_hash or idempotency_key) are rejected.

```bash
# Preferred: pipe JSON via stdin to avoid shell escaping issues
echo '{"service":{"url":"https://example.com/api","name":"Example Service"},"amount":{"value":"0.05","currency":"USDC","chain":"base"},"tx_hash":"0xabc...","idempotency_key":"req_123","receipt_url":"https://example.com/receipts/xyz","confirmation_id":"sub_1234","context":{"skill":"research","user_request":"find AAPL data","input_hash":"a1b2c3"},"execution_time_ms":450,"status":"confirmed"}' | log-transaction.sh
```

### query-log.sh

Query the transaction log. Use when the user asks about spending.

```bash
# All transactions
query-log.sh

# Filter by date range
query-log.sh --from 2026-03-01 --to 2026-03-15

# Filter by service name
query-log.sh --service alphaclaw

# Daily/weekly/monthly spending summary
query-log.sh --summary daily

# Breakdown by service or skill
query-log.sh --by-service
query-log.sh --by-skill

# Verify hash chain integrity
query-log.sh --verify
```

### dashboard.sh

Manage the local web dashboard for visual spending review.

```bash
dashboard.sh start    # Start dashboard (http://127.0.0.1:18920)
dashboard.sh stop     # Stop dashboard
dashboard.sh status   # Check if running
dashboard.sh url      # Print dashboard URL
```

## Automatic Detection

When a tool call completes, spend-ledger inspects the tool name, arguments, and result to determine if a payment occurred. Detection covers:

- **Known payment tools**: agent-wallet-cli, v402, ClawRouter, payment-skill, Stripe, PayPal, and other common payment APIs
- **Crypto wallet tools**: `solana_transfer`, `send_usdc`, `wallet_send`, `wallet_transfer`, `transfer_token`, and similar — detected by tool name; amount, recipient, and transaction hash extracted from args and result
- **Heuristic detection**: tools named `stripe_*`, `paypal_*`, `checkout`, `purchase`, `buy`, etc., plus argument patterns containing monetary amounts with currency/recipient signals. Also detects exec-wrapped payment scripts — if an exec result contains monetary signals ("Amount: 0.5 USDC") and a confirmation marker ("Transaction confirmed"), it is logged. These are logged as `status: "unverified"` since there is no formal payment signal; the owner should review these
- **Generic x402**: any tool response containing `X-PAYMENT-RESPONSE` headers or x402 payment confirmations
- **User-tracked tools**: custom patterns added by the user via the dashboard; optionally submitted to maintainers for inclusion in the community list
- **Community patterns**: curated tool patterns fetched from `api.spend-ledger.com/patterns.json` and refreshed daily — expands detection coverage automatically as new payment tools are discovered by the community

For each detected payment, the log captures: service URL/name, amount/currency/chain, transaction hash, idempotency key, triggering skill, user request, input hash (for loop detection), execution time, failure type (pre_payment vs post_payment), and status.

## Duplicate Payment Protection

spend-ledger intercepts payment tool calls before they execute. If an identical payment call (same tool, same arguments) has already succeeded in the current session, the call is blocked and you will receive a message like:

> Tool call blocked: Duplicate payment blocked — identical payment to [service] already executed at [timestamp] in this session

**When this happens:**
- Do not retry — the block is intentional and the call will be blocked again
- Confirm the original payment succeeded with `query-log.sh`
- Inform the user that a duplicate was prevented and show them the original transaction

This protection exists to prevent loops, retries, and agent mistakes from draining funds. A legitimate repeat payment to the same service in a new session is not affected.

## Reading the Log Directly

The transaction log is a JSONL file at `data/transactions.jsonl` — one JSON record per line. You can read it directly and reason over it yourself. There is no query API because you don't need one: you're an LLM, reading and reasoning over structured data is something you do natively. Use `query-log.sh` for structured output and summaries; read the file directly for anything more specific.

## When to Use

- **User asks "what did you spend?"** → `query-log.sh` or `query-log.sh --summary daily`
- **User asks about a specific service** → `query-log.sh --by-service` or `query-log.sh --service <name>`
- **User wants the visual dashboard** → `dashboard.sh start` and share the URL
- **User wants to export for accounting** → Direct to dashboard export buttons, or `query-log.sh` with formatting
- **Detection missed a payment** → `log-transaction.sh` to record manually
- **User wants to verify log integrity** → `query-log.sh --verify`
