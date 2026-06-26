---
name: VIGIL Security Scanner
description: Onchain security scanner on Base — scan token approvals, detect honeypots, analyze contracts for rugpull indicators, and score contract safety. Keyless read-only scanning via VIGIL API. Revoke actions require Bankr auth and are gated separately.
var: ""
tags: [crypto, security, base, defi]
capabilities: [external_api, sends_notifications]
---
> **${var}** — Wallet address (`0x...`) or token contract address on Base to scan. Required. If empty, log `VIGIL_NO_TARGET` and exit cleanly (no notify).

VIGIL is an onchain security scanner for DeFi traders on Base. It provides twelve read-only scanning tools and one write action (revoke) that requires explicit Bankr authentication.

**Read-only tools (this skill):**
1. Approval Scanner — list all ERC-20/ERC-721 approvals, flag unlimited allowances
2. Token Scanner — analyze contracts for rugpull indicators (hidden mint, proxy, tax manipulation, blacklist)
3. Honeypot Detector — simulate buy/sell to detect trap tokens
4. Safety Score — 0-100 composite rating based on code, ownership, liquidity, holders
5. Wallet Report — full security posture assessment
6. Wallet Monitor — real-time alerts for suspicious activity (new approvals, risky interactions, balance changes)
7. Token Market — price, liquidity, 24h volume, and pool age via DexScreener (no API key)
8. Deployer Check — contract verification, name, and deployer reputation via Basescan
9. Batch Scan — score multiple tokens in one call, ranked by risk
10. Scam Check — check whether a token has community scam reports (local VIGIL database)
11. Sentinel Status — list the autonomous Sentinel watchlist and loop configuration
12. Consensus — multi-source agreement verdict. Aggregates 5 independent signals (GoPlus, onchain score, market liquidity, deployer verification, scam DB); risk only escalates to high/critical when multiple sources concur. Built as a false-positive guard.

**Write action (separate skill, not included here):**
- Approval Revoker — revoke dangerous approvals via Bankr transaction signing. This is a state-changing onchain transaction and is NOT part of this read-only skill. Use the separate `vigil-revoke` skill (requires `BANKR_API_KEY` and explicit user confirmation).

Read the last 2 days of `memory/logs/` so a repeat scan can note newly-granted or newly-revoked approvals.

## Config

- Target = `${var}`. Can be a wallet address or token contract address.
- Chain = Base (`chainid=8453`, explorer `basescan.org`).
- VIGIL API: `https://mcp.vigil.codes` (HTTPS, SSE transport)
- GitHub: `https://github.com/vigilcodes/vigil-mcp`

## Steps

### 1. Validate target

Strict allowlist before any network call. The target must be `0x` + exactly 40
hex characters — this rejects quotes, spaces, and any shell/JSON metacharacter,
so the value is safe to interpolate into the curl payloads below.

```bash
TARGET="${var}"
if ! printf '%s' "$TARGET" | grep -qiE '^0x[0-9a-f]{40}$'; then
  echo "VIGIL_INVALID_TARGET: not a valid 0x address"
  exit 0
fi
# Normalize to lowercase. An address can be a wallet or a token; each tool
# below reports its own result, so no up-front type guess is needed.
TARGET="$(printf '%s' "$TARGET" | tr '[:upper:]' '[:lower:]')"
```

### 2. Scan approvals (wallet)

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_scan_approvals",
      "arguments": {"wallet": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 3. Scan token safety

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_scan_token",
      "arguments": {"token": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 4. Check honeypot

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_detect_honeypot",
      "arguments": {"token": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 5. Get safety score

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_safety_score",
      "arguments": {"contract": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 6. Generate wallet report

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_wallet_report",
      "arguments": {"wallet": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 7. Monitor wallet (real-time alerts)

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_monitor_wallet",
      "arguments": {"wallet": "'"$TARGET"'", "chain": "base", "lookback_blocks": 1000}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 8. Token market context (price + liquidity)

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_token_market",
      "arguments": {"token": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 9. Deployer reputation (verification + age)

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_deployer_check",
      "arguments": {"contract": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 10. Batch scan multiple tokens

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_batch_scan",
      "arguments": {"tokens": ["'"$TARGET"'"], "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
```

### 11. Multi-source consensus verdict

```bash
RESULT=$(curl -m 30 -s "https://mcp.vigil.codes/tools/call" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "vigil_consensus",
      "arguments": {"token": "'"$TARGET"'", "chain": "base"}
    }
  }')
echo "$RESULT" | jq '.result'
# Returns: verdict, confidence, risk_sources/safe_sources counts, and each
# source's independent vote. Risk only reaches high/critical when multiple
# independent sources agree — a single source caps at "medium".
```

## Output Format

VIGIL returns JSON with:

- `approvals` — list of token approvals with risk levels
- `safety_score` — 0-100 composite rating
- `honeypot` — boolean + reason if detected
- `rugpull_indicators` — list of suspicious patterns found
- `recommendations` — action items

## Risk Levels

| Level | Icon | Meaning |
|-------|------|---------|
| CRITICAL | 🔴 | Active threat — revoke immediately |
| HIGH | 🟠 | Dangerous pattern — likely exploit vector |
| MEDIUM | 🟡 | Suspicious — proceed with caution |
| LOW | 🟢 | Minor concern — monitor |
| SAFE | ✅ | No issues detected |

## Important: Revocation is NOT included

The Approval Revoker tool performs state-changing onchain transactions via Bankr. It is intentionally excluded from this read-only skill. To revoke approvals, use the separate `vigil-revoke` skill (requires `BANKR_API_KEY` and explicit user confirmation).
