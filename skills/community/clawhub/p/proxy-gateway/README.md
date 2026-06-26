# Proxy Gateway v0.3.0

> 🚀 **Secure HTTP Proxy for AI Agents** — Give your AI agent unrestricted internet access with pay-per-use pricing. Start with 10 free requests, then only $0.001 per API call.

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://proxy.easky.cn)
[![Security](https://img.shields.io/badge/security-audited-green.svg)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Network](https://img.shields.io/badge/network-Polygon-purple.svg)](https://polygon.technology)

## ⚠️ Security & Privacy Notice

**Please read carefully before using this service:**

### 🔒 Privacy Risks

**All requests transit through the proxy server**, including:
- Full request URLs
- All HTTP headers
- Request bodies
- Response content

**DO NOT use this proxy for:**
- API keys or access tokens
- Private keys or passwords
- Personal or sensitive data
- Internal/private network endpoints

### 💰 Trust Model

This service operates on a **custodial model**:
- You deposit USDC to a platform-controlled address
- The platform maintains your balance and authorizes access
- This requires trust in the platform operator

### 🏠 Self-Hosting Option

For maximum privacy and control, **self-host this service**:
- Full source code available (MIT License)
- Complete data sovereignty
- No third-party visibility
- Easy deployment with Docker or pip

---

## ✨ Features

- ✅ **10 FREE Requests** — Start instantly, no credit card required
- ✅ **Zero Configuration** — No local proxy setup, just call the API
- ✅ **Pay-Per-Use** — Only $0.001 per request, no subscriptions
- ✅ **Security Audited** — 6 security audits, 13 P0 vulnerabilities fixed
- ✅ **Open Source** — MIT licensed, fully auditable code
- ✅ **Multi-Region** — US, EU, Asia proxy nodes
- ✅ **Web3 Native** — Polygon blockchain, USDC payments
- ✅ **Self-Host Ready** — Deploy your own instance in minutes

---

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Self-Hosting Guide](#self-hosting-guide)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Quick Start

### Free Trial (10 Requests)

```python
import requests

response = requests.post(
    "https://proxy.easky.cn/api/v1/fetch",
    headers={"X-Client-ID": "my_agent_001"},
    json={
        "url": "https://api.github.com/users/github",
        "method": "GET"
    }
)

data = response.json()
print(data["content"])  # Response content
print(f"Remaining free calls: {data['remaining_calls']}")
```

### Paid Mode (After Free Trial)

```python
# Use your user_id as API Key after deposit
response = requests.post(
    "https://proxy.easky.cn/api/v1/fetch",
    headers={"X-API-Key": "my_agent_001"},
    json={
        "url": "https://api.example.com/data",
        "method": "GET"
    }
)
```

---

## Self-Hosting Guide

### Why Self-Host?

| Aspect | Hosted Service | Self-Hosted |
|--------|---------------|-------------|
| **Privacy** | Server sees all requests | Complete privacy |
| **Control** | Platform managed | Full control |
| **Cost** | Per-request fees | Server costs only |
| **Trust** | Requires trust | Trustless |
| **Setup** | Instant | 5-minute setup |

### Quick Deploy

```bash
# 1. Clone repository
git clone https://github.com/openclaw/proxy-gateway.git
cd proxy-gateway

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings:
# - HOSTED_WALLET: Your Polygon wallet address
# - ADMIN_TOKEN: Secure random string (16+ chars)

# 5. Start server
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker Deploy

```bash
# Build image
docker build -t proxy-gateway .

# Run container
docker run -d \
  -p 8080:8080 \
  -e NETWORK=mainnet \
  -e HOSTED_WALLET=0x... \
  -e ADMIN_TOKEN=... \
  proxy-gateway
```

---

## API Reference

### System Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/` | GET | Service info | None |
| `/health` | GET | Health check | None |
| `/network-info` | GET | Network configuration | None |

### Payment Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/deposit-info` | GET | Get deposit address | None |
| `/confirm-deposit` | POST | Confirm deposit | Admin Token |
| `/balance` | GET | Check balance | Client ID |
| `/reset-test-balance` | POST | Reset test balance | Admin Token |

### Proxy Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/v1/regions` | GET | Available proxy regions | None |
| `/api/v1/fetch` | POST | Fetch URL content | Client ID/API Key |

### Fetch API Request Format

```json
POST /api/v1/fetch
Headers:
  X-Client-ID: your_user_id

Body:
{
  "url": "https://example.com/api",
  "method": "GET",
  "headers": {
    "Accept": "application/json"
  },
  "body": null
}
```

### Fetch API Response Format

```json
{
  "status": "success",
  "content": { ... },
  "status_code": 200,
  "remaining_calls": 8,
  "balance": 95.0
}
```

---

## Architecture

### Layered Architecture

```
app/
├── core/           # Core layer
│   ├── config.py   # Pydantic Settings
│   ├── exceptions.py # Custom exceptions
│   └── security.py # Security utilities
├── managers/       # Business logic
│   ├── storage.py  # Storage abstraction
│   ├── factory.py  # Manager factory
│   ├── hosted_payment.py  # Mainnet payment
│   ├── testnet_payment.py # Testnet payment
│   └── proxy_manager.py   # Proxy management
└── routers/        # API routes
    ├── system.py   # System routes
    ├── payment.py  # Payment routes
    └── proxy.py    # Proxy routes
```

### Configuration-Driven

Single codebase supports mainnet/testnet:

```bash
# Testnet mode
NETWORK=testnet python -m app.main

# Mainnet mode  
NETWORK=mainnet python -m app.main
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NETWORK` | No | `testnet` | Network mode (mainnet/testnet) |
| `HOSTED_WALLET` | Mainnet | - | Platform wallet address |
| `ADMIN_TOKEN` | Yes | - | Admin authentication token |
| `REDIS_HOST` | No | `localhost` | Redis host |
| `REDIS_PORT` | No | `6379` | Redis port |
| `FREE_TRIAL_LIMIT` | No | `10` | Free trial requests |
| `COST_PER_REQUEST` | No | `0.001` | Price per request (USDC) |
| `CORS_ORIGINS` | No | `*` | Allowed CORS origins |

### Example .env File

```bash
# Network
NETWORK=mainnet
HOSTED_WALLET=0x1234567890123456789012345678901234567890
ADMIN_TOKEN=your_secure_admin_token

# Storage
REDIS_HOST=localhost
REDIS_PORT=6379

# Features
FREE_TRIAL_LIMIT=10
COST_PER_REQUEST=0.001

# CORS
CORS_ORIGINS=*
```

---

## Testing

### Run Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Run unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Coverage report
pytest --cov=app --cov-report=html
```

### Test Structure

```
tests/
├── conftest.py          # Test configuration
├── unit/                # Unit tests
│   ├── test_core.py     # Core functionality
│   └── test_managers.py # Manager tests
└── integration/         # Integration tests
    └── test_api.py      # API tests
```

---

## Pricing

| Item | Price |
|------|-------|
| Free Trial | **10 requests** |
| Per Request | **$0.001 USDC** |
| Minimum Deposit | None |
| Network | Polygon |

---

## Security Features

- ✅ 6 Security Audits
- ✅ 13 P0 Vulnerabilities Fixed
- ✅ Input Validation
- ✅ Anti-Replay Protection
- ✅ Atomic Deduction
- ✅ HTTPS/SSL
- ✅ Unified Exception Handling
- ✅ CORS Configuration

See [SECURITY.md](SECURITY.md) for detailed security information.

---

## Changelog

### v0.3.0 (2026-03-23)

- ✅ Architecture refactor: Layered design (core/managers/routers)
- ✅ Configuration: Pydantic Settings
- ✅ Unified codebase: Mainnet/testnet switch
- ✅ Storage abstraction: Redis/Memory auto-switch
- ✅ Security enhancement: 13 P0 fixes
- ✅ Test coverage: Unit + Integration tests
- ✅ Documentation: Security warnings, self-hosting guide

### v0.2.0

- ✅ API forwarding mode
- ✅ x402 payment integration
- ✅ Free trial feature

### v0.1.0

- 🎉 Initial release

---

## License

MIT
