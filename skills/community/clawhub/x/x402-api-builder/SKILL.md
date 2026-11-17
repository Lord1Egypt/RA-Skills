---
name: "x402-api-builder"
description: "Build your own pay-per-call API with the x402 standard: FastAPI + payment manifest + API keys + MCP wrapper. Sell your data/services per call (USDC). Template with ON-CHAIN payment verification (secure-by-default)."
metadata: {"x402-api-builder": {"requires": {"python3": true, "network": ["https://mainnet.base.org", "https://api.telegram.org"], "env": ["PAYMENT_RPC_URL", "X402_BASE"], "files": ["api_keys.json"]}}}
---

# X402 API Builder 💳🔌

Turn your data/service into a **paid pay-per-call API** in under an hour.

## What you get

1. **FastAPI server** with paid endpoints (template)
2. **x402 manifest** (`/.well-known/x402`) — so other agents can discover you
3. **Payment flow**: customer pays USDC → sends txHash → gets API key
4. **401/402 gates** — no free calls
5. **MCP wrapper** — your API as MCP tools (get_signals, get_market, etc.)

## Quick start

```bash
# 1) Install
pip install fastapi uvicorn

# 2) Copy the template
cp scripts/server.py .
cp scripts/mcp_server.py .

# 3) Add YOUR endpoints (see TODO in server.py)
# 4) Run
uvicorn server:app --host 0.0.0.0 --port 8791 &

# 5) Verify manifest
curl http://YOUR_IP:8791/.well-known/x402
```

## Pricing (recommended)

| Product | Price |
|---------|-------|
| Per call | $0.005 (market: $0.001-0.01) |
| Monthly (unlimited) | $25 |
| Premium (live + alerts) | $100 |
| Enterprise (SLA + white-label) | $500 |

## Security (critical)

- **On-chain verification (secure-by-default):** `/v1/purchase` only issues an API key after the txHash is verified on-chain (eth_getTransactionByHash + receipt status against Base RPC). Unreachable RPC or invalid tx = purchase denied (402).
- **Never** commit api_keys.json (gitignore it!)
- API key = HMAC of txHash (verifiable, not guessable)
- 401 without key · 402 when call usage is exhausted or payment is not verified
- **Client:** refuses to send the key over plain HTTP to non-local hosts (use X402_BASE=https://...)
- Rate-limit per key

## Files

```
x402-api-builder/
├── SKILL.md
└── scripts/
    ├── server.py      # FastAPI template (manifest + purchase + gates)
    ├── mcp_server.py  # MCP wrapper (fastmcp)
    └── client.py      # Test client
```
