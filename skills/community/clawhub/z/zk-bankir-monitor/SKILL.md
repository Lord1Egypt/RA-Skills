---
name: zk-bankir-monitor
description: Monitor a ZK-Bankir sovereign banking treasury via API — health checks, balance queries, decision ledger tracking, and hash-chain verification.
homepage: https://gitlab.com/1Beekeeper/zk-bankir
metadata:
  openclaw:
    requires:
      bins: ["curl"]
    os: ["linux", "darwin"]
---

# ZK-Bankir Monitor

Monitor a ZK-Bankir sovereign personal banking treasury via its REST API. This skill provides health monitoring, multi-asset balance queries (BTC/PUSD/Kraken), decision ledger tracking, and hash-chain integrity verification — all through secure read-only API endpoints. No private keys are ever exposed.

## Prerequisites

- A running ZK-Bankir Rails server (default: `http://localhost:3000`)
- `curl` and `jq` available on PATH
- API access — ZK-Bankir has no authentication layer yet (Phase 1); requests are plain HTTP

## Core Commands

### Health Check

Verify the ZK-Bankir server is alive:

```bash
curl -s http://ZK_BANKIR_HOST/health -H "Accept: application/json" | jq .
```

Expected response:
```json
{"status": "ok", "timestamp": "2026-07-04T12:00:00Z"}
```

Use `ZK_BANKIR_HOST` as the base URL. Default to `localhost:3000` unless the user has configured a different host.

### Treasury Balances

Get all treasury balances across BTC, PUSD, and Kraken:

```bash
curl -s http://ZK_BANKIR_HOST/api/v1/treasury/balances -H "Accept: application/json" | jq .
```

Also available as individual endpoints:
- **BTC only (COLDCARD watch-only):** `GET /api/v1/treasury/btc`
- **PUSD only (Payy Network ZK):** `GET /api/v1/treasury/pusd`
- **Kraken only (exchange):** `GET /api/v1/treasury/kraken`

### Decision Ledger

List all decisions (append-only, hash-chained audit trail):

```bash
curl -s http://ZK_BANKIR_HOST/api/v1/decisions -H "Accept: application/json" | jq .
```

Get a single decision by ID:
```bash
curl -s http://ZK_BANKIR_HOST/api/v1/decisions/ID -H "Accept: application/json" | jq .
```

Create a new decision (policy-gated: auto <$1k, approval $1k-$10k, deny >$10k):
```bash
curl -s -X POST http://ZK_BANKIR_HOST/api/v1/decisions \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"decision":{"action":"BUY_BTC","amount":500}}' | jq .
```

### Hash-Chain Verification

Verify the integrity of the Decision Ledger's SHA-256 hash chain:

```bash
cd /path/to/zk-bankir && bin/rails runner "puts Decision.verify_chain ? 'VERIFIED: Chain intact' : 'BROKEN: Chain corrupted'"
```

This must be run on the ZK-Bankir server itself (not via HTTP API — it's a local-only integrity check per Doctrine §6).

### Operator Console (Admin)

View pending human-approval decisions:
```bash
curl -s http://ZK_BANKIR_HOST/admin/decisions -H "Accept: application/json" | jq .
```

## Usage Patterns

### Daily Health Summary

When the user asks for a treasury summary, run all three in sequence:

1. Health check — confirm server is up
2. Treasury balances — get all asset balances
3. Hash-chain verification — confirm audit trail integrity

Format the output as a clean summary table showing asset, balance, and status.

### Decision Monitoring

When the user asks about recent decisions:
1. Fetch decision list from `/api/v1/decisions`
2. Flag any decisions with `status: "pending"` that require human approval
3. Note any `status: "denied"` decisions (Policy Engine blocked)
4. Highlight decisions above $1,000 as they require manual approval per Gebud 4

### Alert Thresholds (Premium)

The premium tier adds monitoring thresholds:
- BTC balance drop >5% in 24h → alert
- Any denied decision → alert
- Hash chain break → alert (critical)
- Server health check failure → alert

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| 404 on treasury endpoints | Server not running | `bundle exec rails server -p 3000 -d` |
| Empty treasury balances | No treasuries seeded | `bin/rails db:seed` |
| Hash chain broken | DB corruption | Run `Decision.verify_chain` to identify the break, restore from backup |
| PUSD balance shows 0 | Beam CLI not installed or wallet not created | Check `beam wallets list` |

## Configuration

Set these environment variables or pass them in each command:

| Variable | Default | Description |
|----------|---------|-------------|
| `ZK_BANKIR_HOST` | `http://localhost:3000` | Base URL of the ZK-Bankir Rails server |
| `ZK_BANKIR_PATH` | `~/App/domains/finance/zk-bankir` | Path to the ZK-Bankir project (for hash-chain verification) |

## Gebuden Compliance

This skill is **read-only** and complies with De 10 Gebuden:
- §5 Watch-Only — never exposes or stores private keys
- §6 Audit Trail — queries the append-only Decision Ledger
- §8 Risk-Weighted — respects the auto/approve/deny Policy Engine tiers
- §2 Simplicity — uses curl/jq, no frameworks

## Freemium Tiers

**Free (Basic):**
- Health check
- Treasury balance queries (all assets)
- Decision ledger listing (last 10)
- Hash-chain verification status

**Premium ($19):**
- Historical balance tracking with alert thresholds
- Decision monitoring with approval alerts
- Automated daily health summary (cron-compatible)
- Slack/Telegram webhook integration for alerts
