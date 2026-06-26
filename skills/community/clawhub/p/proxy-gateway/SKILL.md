---
name: proxy-gateway
description: |
  Secure HTTP Proxy for AI Agents — Give your AI agent unrestricted internet access 
  with pay-per-use pricing. 10 free requests to start, then only $0.001 per API call.
  
  Use when you need web scraping, API integrations, data collection, or research automation.
  6 security audits completed, 13 critical vulnerabilities fixed. Self-hosting supported.
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      anyBins: ["python3", "pip3"]
      python: ">=3.10"
    os: ["linux", "darwin", "win32"]
---

# Proxy Gateway

> 🚀 **Secure HTTP Proxy for AI Agents** — Unrestricted internet access with pay-per-use pricing. Start with 10 free requests, then only $0.001 per API call.

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://proxy.easky.cn)
[![Security](https://img.shields.io/badge/security-audited-green.svg)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Network](https://img.shields.io/badge/network-Polygon-purple.svg)](https://polygon.technology)

## When to Use

Use this skill when you need to:

- **Give AI agents internet access** — No local proxy setup required, just call the API
- **Web scraping and data extraction** — Collect data from public websites at scale
- **API integrations** — Connect AI agents to external APIs without network configuration
- **Research automation** — Automate web research and content aggregation tasks
- **Multi-region proxy needs** — Access content through US, EU, or Asia proxy nodes
- **Cost-effective proxy solution** — Pay only $0.001 per request instead of monthly subscriptions
- **Self-hosted proxy option** — Run your own proxy server for maximum privacy

---

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
- Banking or financial credentials

### 💰 Trust Model & Risk Disclosure

This service operates on a **custodial model** with the following risks:

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Custody Risk** | User funds are held in platform-controlled wallets | Use small amounts, withdraw frequently |
| **Operator Risk** | Platform operator could mismanage funds | Open source, audited code |
| **Smart Contract Risk** | Payment verification relies on external contracts | Multi-sig, timelock protections |
| **Privacy Risk** | All requests visible to proxy operator | Self-host for complete privacy |

**Recommendations:**
- Only deposit amounts you are willing to risk
- Monitor your balance regularly
- Consider self-hosting for sensitive use cases
- Withdraw unused balances periodically

### 🏠 Self-Hosting Option

For maximum privacy and control, **self-host this service**:
- Full source code available (MIT License)
- Complete data sovereignty
- No third-party visibility
- Easy deployment with Docker or pip

---

## 📋 System Requirements

### Runtime Dependencies

| Component | Version | Required | Notes |
|-----------|---------|----------|-------|
| Python | 3.10+ | ✅ | Core runtime |
| Redis | 6.0+ | ⚠️ | Required for production (multi-process safety) |
| Polygon RPC | - | ✅ | Mainnet or testnet endpoint |

### Python Packages

```
fastapi>=0.100.0
uvicorn>=0.23.0
redis>=4.6.0
web3>=6.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
httpx>=0.24.0
```

### Network Requirements

- **Inbound**: Port 8080 (configurable via `PORT` env var)
- **Outbound**: HTTPS (443) for proxy requests
- **Outbound**: WebSocket (optional) for blockchain events

### Optional Components

- **Nginx**: For SSL termination and reverse proxy
- **Docker**: For containerized deployment
- **Systemd**: For service management on Linux

---

## ✨ Why Proxy Gateway?

| Feature | Benefit |
|---------|---------|
| 🎁 **10 Free Requests** | Start instantly, no credit card required |
| ⚡ **Zero Configuration** | No local proxy setup, just call the API |
| 💵 **Pay-Per-Use** | Only $0.001 per request, no subscriptions |
| 🔐 **Security Audited** | 6 security audits, 13 P0 vulnerabilities fixed |
| 📖 **Open Source** | MIT licensed, fully auditable code |
| 🌍 **Multi-Region** | US, EU, Asia proxy nodes |
| 🔗 **Web3 Native** | Polygon blockchain, USDC payments |
| 🏠 **Self-Host Ready** | Deploy your own instance in minutes |

---

## 🚀 Quick Start

### 1. Start with Free Trial (10 Requests)

```python
import requests

try:
    response = requests.post(
        "https://proxy.easky.cn/api/v1/fetch",
        headers={"X-Client-ID": "my_agent_001"},
        json={
            "url": "https://api.github.com/users/github",
            "method": "GET"
        },
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()
    print(data["content"])  # Response content
    print(f"Remaining free calls: {data['remaining_calls']}")
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("Error: Rate limit exceeded or free trial exhausted. Please deposit USDC to continue.")
    elif e.response.status_code == 401:
        print("Error: Invalid or missing API key.")
    else:
        print(f"HTTP Error: {e}")
except requests.exceptions.Timeout:
    print("Error: Request timed out. The target server may be slow.")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### 2. Continue with Paid Mode

After free trial, deposit USDC to continue:

```python
import requests

# Use your user_id as API Key after deposit
headers = {"X-API-Key": "my_agent_001"}

try:
    response = requests.post(
        "https://proxy.easky.cn/api/v1/fetch",
        headers=headers,
        json={
            "url": "https://api.example.com/data",
            "method": "GET"
        },
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()
    print(f"Response: {data['content']}")
    print(f"Balance remaining: {data.get('balance', 'N/A')} USDC")
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 402:
        print("Error: Insufficient balance. Please deposit more USDC.")
    elif e.response.status_code == 429:
        print("Error: Rate limit exceeded.")
    else:
        print(f"HTTP Error: {e}")
except requests.exceptions.Timeout:
    print("Error: Request timed out.")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Free Trial** | **FREE** | 10 requests, no registration |
| **Pay-Per-Use** | **$0.001/request** | Unlimited calls, pay as you go |
| **Self-Hosted** | **FREE** | Run your own server |

- **Currency**: USDC on Polygon
- **Minimum Deposit**: None (top up any amount)
- **Network Fees**: Paid by user for deposits

---

## 🌐 API Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/` | GET | Service info | None |
| `/health` | GET | Health check | None |
| `/network-info` | GET | Network configuration | None |
| `/api/v1/regions` | GET | Available proxy regions | None |
| `/api/v1/fetch` | POST | Fetch any URL via proxy | Client ID or API Key |
| `/deposit-info` | GET | Get deposit address | None |
| `/balance` | GET | Check balance | Client ID |

---

## 🏠 Self-Hosting Guide

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

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

## 🔒 Security Features

- ✅ **6 Security Audits** Completed by independent reviewers
- ✅ **13 P0 Vulnerabilities Fixed** All critical issues resolved
- ✅ **Input Validation** Strict validation on all inputs (amount limits: 0 < x ≤ 1000 USDC)
- ✅ **Lua Script Sandboxing** Redis Lua execution with parameter validation
- ✅ **Anti-Replay Protection** Transaction replay attack prevention
- ✅ **Atomic Deduction** Balance updates are atomic
- ✅ **HTTPS/TLS** All communications encrypted
- ✅ **Open Source** Full code transparency

**Security Policy**: See [SECURITY.md](SECURITY.md) for detailed security information and vulnerability reporting.

---

## 🛡️ Best Practices

### ✅ DO
- Use for public API access
- Use for web scraping public data
- Use for research automation
- Use for content aggregation
- Self-host for sensitive operations

### ❌ DON'T
- Send API keys through the proxy
- Send passwords or credentials
- Access private/internal networks
- Send personal information
- Send financial data

---

## 📝 Environment Variables

### Required (for self-hosting)

| Variable | Description | Example |
|----------|-------------|---------|
| `HOSTED_WALLET` | Polygon address for USDC deposits | `0x1234...abcd` |
| `ADMIN_TOKEN` | Admin authentication token | `random_string_16+` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `NETWORK` | `testnet` | Network mode (mainnet/testnet) |
| `REDIS_HOST` | `localhost` | Redis server host |
| `REDIS_PORT` | `6379` | Redis server port |
| `FREE_TRIAL_LIMIT` | `10` | Free trial request limit |
| `COST_PER_REQUEST` | `0.001` | Price per request (USDC) |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

See [.env.example](.env.example) for complete configuration template.

---

## 🤝 Contributing

Contributions are welcome! Please see our contributing guidelines and submit PRs.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Documentation**: https://proxy.easky.cn
- **Issues**: GitHub Issues
- **Email**: support@proxy.easky.cn

---

## 💡 Tips

### Free Trial Tips
- **Start instantly**: Use `X-Client-ID` header with any unique identifier to get 10 free requests without registration
- **Monitor usage**: Check `remaining_calls` in response to track free trial usage
- **No credit card**: Free trial requires no payment information

### Cost Optimization
- **Batch requests**: Combine multiple data needs into fewer requests when possible
- **Use caching**: Cache responses locally to avoid redundant proxy calls
- **Self-host for high volume**: If using >1000 requests/day, self-host to eliminate per-request fees

### Error Handling Best Practices
- **Always check status codes**: 429 = rate limit/insufficient balance, 402 = payment required, 401 = invalid auth
- **Implement retry logic**: Use exponential backoff for 429 errors
- **Set timeouts**: Use 30-second timeout for most requests, 60+ for slow endpoints

### Privacy & Security
- **Never send secrets**: API keys, passwords, tokens should never pass through the proxy
- **Self-host for sensitive data**: Run your own instance for internal APIs or sensitive operations
- **Monitor balance regularly**: Check `/balance` endpoint to avoid unexpected service interruptions

### Development Tips
- **Test with free tier**: Use free trial for development and testing
- **Use consistent Client-ID**: Reuse the same `X-Client-ID` to maintain balance across sessions
- **Check regions**: Call `/api/v1/regions` to see available proxy locations

### Troubleshooting
- **Connection refused**: Verify target URL is accessible and not blocking proxy IPs
- **Slow responses**: Try a different proxy region closer to your target server
- **Balance not updating**: Blockchain confirmations may take 1-2 minutes on Polygon

---

**Built with ❤️ for the AI Agent ecosystem**
