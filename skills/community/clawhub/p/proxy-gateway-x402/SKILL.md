# Proxy Gateway x402

> 🚀 **Agent-to-Agent Commerce Proxy** — Unrestricted internet access with pay-per-use via x402 protocol. No custody, no KYC, direct USDC payments.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/yourname/proxy-gateway-x402)
[![Protocol](https://img.shields.io/badge/protocol-x402-orange.svg)](https://x402.org)
[![Network](https://img.shields.io/badge/network-Base-blue.svg)](https://base.org)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## ⚡ Key Features

| Feature | Benefit |
|---------|---------|
| 💰 **Pay-Per-Use** | Only pay when you use, no subscriptions |
| 🔗 **x402 Protocol** | Agent-to-Agent commerce, automatic payments |
| 🏦 **No Custody** | Funds go directly to developer, no middleman |
| 🔓 **No KYC** | Crypto-native, no identity verification |
| ⚡ **Instant** | Sub-second confirmation on Base L2 |
| 🛡️ **Self-Host** | Full source code, deploy your own |

---

## 💰 Pricing

| Item | Details |
|------|---------|
| **Price** | 0.001 USDC per request |
| **Token** | USDC |
| **Network** | Base (Ethereum L2) |
| **Gas** | ~$0.0001 per transaction |

---

## 🚀 Quick Start

### For Users

#### 1. Install the Skill

```bash
clawhub install proxy-gateway-x402
```

#### 2. Set Up Auto-Pay (Recommended)

```bash
# Set your private key for automatic payments
export USER_EVM_PRIVATE_KEY=0xYourPrivateKey

# ⚠️ Security: Use a dedicated wallet with limited funds
```

#### 3. Use the Proxy

```python
import requests
import json

# Method 1: Auto-pay (if USER_EVM_PRIVATE_KEY is set)
response = requests.post(
    "https://proxy-gateway-x402.easky.cn/api/v1/fetch",
    json={
        "url": "https://api.github.com/users/github",
        "method": "GET"
    }
)
print(response.json()["content"])

# Method 2: Manual payment
# First call returns 402 Payment Required
response = requests.post(
    "https://proxy-gateway-x402.easky.cn/api/v1/fetch",
    json={"url": "https://example.com/api", "method": "GET"}
)
# Response: {"error": "Payment Required", "x402": {...}}

# Pay 0.001 USDC to the specified address
# Then retry with payment proof
response = requests.post(
    "https://proxy-gateway-x402.easky.cn/api/v1/fetch",
    headers={"X-Payment-Response": json.dumps({"tx_hash": "0x..."})},
    json={"url": "https://example.com/api", "method": "GET"}
)
```

---

## 🔧 For Developers

### Deploy Your Own Instance

#### 1. Clone & Install

```bash
git clone https://github.com/yourname/proxy-gateway-x402.git
cd proxy-gateway-x402

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings:
# - DEVELOPER_WALLET: Your wallet to receive payments
# - PRICE_PER_REQUEST: Set your price (default: 0.001)
# - X402_CHAIN: base or base-sepolia (for testing)
```

#### 3. Run

```bash
# Development
uvicorn app.main:app --reload --port 8080

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker Deployment

```bash
docker build -t proxy-gateway-x402 .

docker run -d \
  -p 8080:8080 \
  -e DEVELOPER_WALLET=0xYourWallet \
  -e PRICE_PER_REQUEST=0.001 \
  proxy-gateway-x402
```

---

## 📖 API Reference

### POST /api/v1/fetch

Fetch any URL through the proxy.

**Headers:**
- `X-Payment-Response` (optional): Payment proof JSON `{"tx_hash": "0x..."}`

**Request Body:**
```json
{
  "url": "https://api.example.com/data",
  "method": "GET",
  "headers": {"Authorization": "Bearer token"},
  "body": null,
  "region": "us"
}
```

**Response (Success):**
```json
{
  "success": true,
  "content": "...",
  "status_code": 200,
  "payment": {
    "verified": true,
    "tx_hash": "0x...",
    "amount": "0.001",
    "token": "USDC"
  }
}
```

**Response (402 Payment Required):**
```json
{
  "success": false,
  "error": "Payment Required",
  "x402": {
    "version": "0.1.0",
    "scheme": "exact",
    "network": "base",
    "required": {
      "amount": "0.001",
      "token": "USDC",
      "recipient": "0x..."
    }
  }
}
```

### GET /api/v1/price

Query current pricing.

**Response:**
```json
{
  "price": "0.001",
  "token": "USDC",
  "network": "base",
  "recipient": "0x..."
}
```

---

## 🛡️ Security

### For Users

⚠️ **Private Key Safety**
- Use a hardware wallet or dedicated hot wallet
- Never use your main wallet for auto-pay
- Set daily spending limits on your wallet
- Monitor transactions regularly

⚠️ **Payment Verification**
- All payments are verified on-chain
- Transactions cannot be forged or replayed
- Payment proofs are cached for 5 minutes

### For Developers

⚠️ **Smart Contract Risks**
- USDC contract is standard ERC-20
- No custom smart contracts in this implementation
- All verification happens on-chain

---

## ⚠️ Disclaimer

**This is experimental software.** Use at your own risk.

- No refunds for failed requests
- Network fees are paid by the user
- Developer receives payments directly, no escrow
- This is NOT financial advice

---

## 🔗 Links

- [x402 Protocol](https://x402.org)
- [Base Network](https://base.org)
- [USDC on Base](https://www.circle.com/en/usdc/developers/base)

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

Built with ❤️ for the Agent Commerce ecosystem.
