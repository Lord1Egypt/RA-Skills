---
name: x402janus
description: >
  x402janus — autonomous on-chain wallet security for EVMs:
  scan approvals, trace fund flow, detect drainers, and build revoke transactions.
  Pay via x402 USDC on Base. No API keys. No accounts.
metadata:
  emoji: 🛡️
  homepage: https://x402janus.com
  repository: https://github.com/consensus-hq/agent-pulse
  acp_marketplace: https://app.virtuals.io/acp/agent-details/14804
  requires:
    bins: [node, npx]
    env: [JANUS_API_URL]
  optionalEnv:
    - PRIVATE_KEY
    - THIRDWEB_CLIENT_ID
  tags:
    - security
    - wallet
    - evm
    - base
    - ethereum
    - x402
    - micropayment
    - forensics
    - approvals
    - drainer-detection
    - ai-agent
    - defi
---

# x402janus — Wallet Security for AI Agents

**Nothing passes the gate unchecked.**

The security layer AI agents call before every financial transaction. Scans wallets, traces approval chains, detects drainers, builds revoke transactions — all paid via x402 micropayment. No API key. No account. No setup.

## Why This Exists

AI agents are getting wallets and transacting autonomously. Most have no idea what they've approved or who can drain them. x402janus is the gate — forensic analysis that any agent can call before making a financial decision.

**Score: 3.240** on ClawHub — the highest-rated security skill for autonomous agents.

## Quick Start

```bash
# Install
clawhub install x402janus
cd skills/x402janus && npm install

# Free scan (no wallet required)
JANUS_API_URL=https://x402janus.com \
  npx tsx scripts/scan-wallet.ts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --tier free --json

# Paid scan ($0.01 USDC via x402)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts 0xYOUR_TARGET --tier quick --json
```

**Exit codes for automation:**
- `0` — safe (health ≥ 75) → proceed with transaction
- `1` — medium risk (50–74) → flag for review
- `2` — high risk (< 50) → halt transaction
- `3` — critical (< 25) → block and alert

## Setup

```bash
cd skills/x402janus && npm install
```

| Variable | Required | Description |
|----------|----------|-------------|
| `JANUS_API_URL` | Yes | `https://x402janus.com` |
| `PRIVATE_KEY` | Paid tiers only | Agent wallet key for x402 payment signing |
| `THIRDWEB_CLIENT_ID` | No | thirdweb client ID (default: `x402janus-skill`) |

## Commands

### 1. Scan a Wallet

The primary command. Returns risk score, findings, approvals, and pre-built revoke transactions.

```bash
# Free tier — no payment required
JANUS_API_URL=https://x402janus.com \
  npx tsx scripts/scan-wallet.ts <address> --tier free --json

# Quick scan — $0.01 USDC
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts <address> --tier quick --json

# Standard scan — $0.05 USDC (AI threat analysis)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts <address> --tier standard --json

# Deep scan — $0.25 USDC (full graph + drainer fingerprinting)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts <address> --tier deep --chain base --json
```

**Output:**
```json
{
  "address": "0x...",
  "scannedAt": "2026-03-04T...",
  "payer": "0x...",
  "coverageLevel": "basic",
  "summary": {
    "totalTokensApproved": 3,
    "unlimitedApprovals": 2,
    "highRiskApprovals": 0,
    "healthScore": 80
  },
  "approvals": [...],
  "recommendations": [...],
  "revokeTransactions": [...]
}
```

### 2. List Approvals

```bash
# All approvals with risk flags
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/list-approvals.ts <address> --format json

# High-risk only
npx tsx scripts/list-approvals.ts <address> --risk high,critical --format json

# Unlimited approvals only
npx tsx scripts/list-approvals.ts <address> --unlimited-only --format json
```

### 3. Revoke Approval

```bash
# Dry run — outputs calldata
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/revoke-approval.ts <wallet> <token> <spender> --json

# Execute on-chain (sends real transaction)
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/revoke-approval.ts <wallet> <token> <spender> --execute --json
```

⚠️ `--execute` sends a real transaction. Confirm with user before executing.

### 4. Start Monitoring

```bash
# Webhook alerts
JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/start-monitoring.ts <address> --webhook https://your-webhook.com --json

# Telegram alerts
npx tsx scripts/start-monitoring.ts <address> --telegram @username --json
```

## Agent Integration Pattern

```bash
#!/bin/bash
# Pre-transaction security gate
RESULT=$(JANUS_API_URL=https://x402janus.com PRIVATE_KEY=$PRIVATE_KEY \
  npx tsx scripts/scan-wallet.ts "$TARGET_WALLET" --tier quick --json 2>/dev/null)
EXIT=$?

if [ $EXIT -eq 0 ]; then
  echo "✅ Wallet safe — proceeding with transaction"
  # ... execute your trade/transfer/approval
elif [ $EXIT -eq 1 ]; then
  echo "⚠️ Medium risk — requesting human review"
  # ... alert human operator
else
  echo "🚫 High risk detected — blocking transaction"
  # ... halt and report
fi
```

## Pricing

| Tier | Price | Speed | Coverage |
|------|-------|-------|----------|
| **Free** | $0.00 | <5s | Address validation, basic checksum, tier preview |
| **Quick** | $0.01 USDC | <3s | Deterministic risk score, approval list, revoke txs |
| **Standard** | $0.05 USDC | <10s | + AI threat analysis, deeper historical lookback |
| **Deep** | $0.25 USDC | <30s | + Full graph analysis, drainer fingerprinting, anomaly detection |

All payments settle via x402 micropayment (EIP-3009 TransferWithAuthorization) on Base. Your agent signs once, the Thirdweb facilitator settles USDC on-chain. No account needed.

## How x402 Payment Works

1. Agent calls the scan endpoint
2. Server returns HTTP 402 with payment requirements
3. thirdweb x402 SDK signs the payment authorization from agent wallet
4. SDK retries with payment header automatically
5. Facilitator verifies and settles USDC on Base
6. Scan result returned

No gas needed for payments (facilitator pays). Agent wallet only needs USDC on Base.

## ACP Marketplace

Also available via the Virtuals ACP marketplace for agent-to-agent hiring:
**https://app.virtuals.io/acp/agent-details/14804**

6 offerings: scan (quick/standard/deep), approvals listing, revoke (single/batch).

## API Endpoints (Direct)

For agents that prefer raw HTTP over the skill scripts:

```bash
# Free scan
curl -X POST "https://x402janus.com/api/guardian/scan/0xADDRESS?tier=free"

# Paid scan (x402 handles payment automatically via SDK)
# Or manually: server returns 402 → sign payment → retry with header

# Health check
curl "https://x402janus.com/api/guardian/status"

# Skill documentation (machine-readable)
curl "https://x402janus.com/api/skill-md"
```

## Wallet Requirements

For paid tiers, the agent wallet (`PRIVATE_KEY`) needs:
- **USDC on Base** — $0.01–$0.25 per scan
- **ETH on Base** — only needed for `--execute` on revoke (not for scan payments)

## Safety

- Free tier requires no key
- Paid tiers use thirdweb x402 signing — private key never logged or returned
- All scripts validate addresses before requests
- Revoke transactions are dry-run by default (`--execute` required for on-chain)
- x402 payments are exact amounts — facilitator cannot take more than specified
- Rate limiting: 10 free scans per IP window

## Links

- **Product**: https://x402janus.com
- **ACP Marketplace**: https://app.virtuals.io/acp/agent-details/14804
- **GitHub**: https://github.com/consensus-hq/agent-pulse
- **X**: [@x402janus](https://x.com/x402janus)
