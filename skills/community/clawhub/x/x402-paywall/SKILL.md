---
name: agent-economy
description: x402 payment layer for AI agents — charge USDC per skill call. Meta-skill that wraps any skill with per-call pricing and on-chain payment verification.
tags:
  - x402
  - payments
  - usdc
  - monetization
  - agents
  - economy
  - billing
  - web3
category: developer-tools
---

# Agent Economy — x402 Payment Layer for AI Agents

## What It Does

Agent Economy adds a paywall to any AI agent skill using the x402 protocol. When Agent A calls Agent B's paid skill, it gets an HTTP 402 "Payment Required" response with payment details. Agent A sends USDC on-chain, Agent B verifies the payment, then serves the result.

**One wrapper. Any skill. Real money.**

## How x402 Works

```
1. Agent A calls skill endpoint
2. Server responds: HTTP 402 + payment details (wallet, amount, token)
3. Agent A sends USDC to wallet on Base/Ethereum
4. Agent A retries with tx_hash in header
5. Server verifies payment on-chain
6. Server serves the response
```

No API keys to manage. No billing platforms. Just on-chain payments.

## Quick Start

### 1. Install

```python
from agent_economy import Paywall, Ledger

# Create a paywall with your wallet
paywall = Paywall(
    wallet_address="0xYourWalletAddress",
    network="base",  # or "ethereum", "polygon"
    price_per_call=0.01,  # $0.01 USDC per call
)
```

### 2. Wrap Any Skill

```python
# Your existing skill function
def analyze_server(metrics):
    return {"health": "ok", "score": 95}

# Wrap it with payment
paid_analyze = paywall.require_payment(analyze_server)

# Now it returns 402 until paid, then serves the result
result = paid_analyze(request)
```

### 3. FastAPI Integration

```python
from fastapi import FastAPI, Request, Response
from agent_economy import Paywall

app = FastAPI()
paywall = Paywall(wallet_address="0x...", network="base", price_per_call=0.05)

@app.post("/api/analyze")
async def analyze(request: Request):
    # Check payment first
    payment_result = paywall.check_payment(request)
    if payment_result.status == "payment_required":
        return payment_result.to_response()  # Returns HTTP 402

    # Payment verified — serve the skill
    data = await request.json()
    return {"result": "your analysis here"}
```

### 4. Calling a Paid Skill (Client Side)

```python
from agent_economy import PaymentClient

client = PaymentClient(
    wallet_private_key="0xYourPrivateKey",  # or wallet connect
    network="base"
)

# Call a paid skill — handles payment automatically
result = client.call(
    url="https://api.example.com/api/analyze",
    method="POST",
    json={"metrics": {...}},
    max_price=0.10  # Won't pay more than $0.10
)
```

## Pricing Models

### Per-Call
```python
paywall = Paywall(price_per_call=0.01)  # $0.01 every call
```

### Per-Token (Usage-Based)
```python
paywall = Paywall(
    price_per_call=0.00,  # Base price
    price_per_1k_tokens=0.002  # $0.002 per 1K tokens
)
```

### Tiered
```python
paywall = Paywall(pricing_tiers={
    "basic": 0.01,    # Basic analysis
    "premium": 0.05,  # Deep analysis
    "enterprise": 0.25  # Full audit
})
```

### Subscription (Time-Based)
```python
paywall = Paywall(
    subscription_price=9.99,  # $9.99/month
    subscription_duration_days=30
)
# Subscribers get unlimited calls for the period
```

## Ledger

Track all payments, usage, and revenue.

```python
from agent_economy import Ledger

ledger = Ledger(db_path="payments.db")

# Record a payment
ledger.record(
    payer="0xABC...",
    skill="analyze-server",
    amount=0.01,
    tx_hash="0x123...",
    network="base"
)

# Query revenue
revenue = ledger.get_revenue(period="30d")
# {"total_usd": 142.50, "calls": 14250, "unique_payers": 23}

# Query per-skill breakdown
skills = ledger.get_skill_breakdown()
# {"analyze-server": {"calls": 8000, "revenue": 80.00}, ...}

# Check if address has active subscription
active = ledger.is_subscribed("0xABC...", skill="analyze-server")
```

## On-Chain Payment Verification

Agent Economy verifies USDC transfers on-chain. No trust required.

```python
from agent_economy import PaymentVerifier

verifier = PaymentVerifier(network="base")

# Verify a transaction
valid = verifier.verify(
    tx_hash="0x123...",
    expected_sender="0xABC...",
    expected_recipient="0xYourWallet",
    expected_amount=0.01,  # USDC
    tolerance=0.001  # Allow small variance for gas
)

if valid:
    print("Payment confirmed on-chain")
```

### Supported Networks

| Network | Chain ID | USDC Contract |
|---------|----------|---------------|
| Base | 8453 | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| Ethereum | 1 | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 |
| Polygon | 137 | 0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 |
| Arbitrum | 42161 | 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 |

## HTTP 402 Response Format

When payment is required, the server responds:

```json
HTTP 402 Payment Required
Content-Type: application/json

{
  "error": "payment_required",
  "payment": {
    "recipient": "0xYourWalletAddress",
    "amount": "0.01",
    "token": "USDC",
    "network": "base",
    "chain_id": 8453,
    "description": "Per-call fee for analyze-server skill"
  },
  "retry": {
    "header": "X-Payment-Tx-Hash",
    "instructions": "Send USDC to recipient, then retry with tx hash in header"
  }
}
```

## Security Considerations

- **Never expose private keys** in code — use environment variables or vault
- **Validate amounts** — always check `expected_amount` with tolerance
- **Prevent replay** — track used tx hashes in the ledger to prevent double-spend
- **Rate limit** — prevent spam calls that waste verification gas
- **Refund policy** — define upfront, no on-chain refunds by default

## Architecture

```
┌──────────┐     HTTP      ┌──────────────┐    Verify    ┌──────────┐
│  Agent A  │ ────────────→ │  Your Skill   │ ──────────→ │  Blockchain │
│  (Caller) │ ←── 402 ──── │  (Server)     │ ←─ Confirmed │  (Base/ETH) │
│           │ ── + tx ────→│              │              │           │
│           │ ←─ 200 ─────│              │              │           │
└──────────┘              └──────────────┘              └──────────┘
                                │
                          ┌─────┴──────┐
                          │   Ledger    │
                          │  (SQLite)   │
                          └────────────┘
```

## Requirements

- Python 3.8+
- `requests` (for blockchain API calls)
- `web3` (optional, for direct on-chain verification)
- SQLite (built-in, for ledger)

## Install Dependencies

```bash
pip install agent-economy
# or
pip install requests web3  # manual
```

## Support

- Docs: https://agent-economy.io/docs
- x402 Spec: https://x402.dev
- Issues: https://github.com/agent-economy/agent-economy/issues
