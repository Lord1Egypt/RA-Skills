---
name: proxy-gateway-client
description: |
  Client SDK for Proxy Gateway - Access internet through pay-per-use proxy service.
  Install this skill to route your AI agent's traffic through proxy.easky.cn
  
  Features:
  - Automatic proxy configuration
  - x402 crypto payment handling
  - Multi-region proxy selection
  - Transparent traffic routing
  
  Usage: Install → Configure API Key → Access internet freely
version: 0.2.1
author: laoke
license: MIT
requirements:
  python: ">=3.10"
  dependencies:
    - requests>=2.31.0
    - httpx>=0.28.0
---

# Proxy Gateway Client

## Overview

This is the **client SDK** for connecting to Proxy Gateway service (https://proxy.easky.cn).

**Architecture**:
```
Your AI Agent (this skill) → Proxy Gateway API → Clash Proxy → Internet
                              (proxy.easky.cn)    (90+ nodes)
```

## How It Works

1. **You install this client skill** → Get ability to call proxy service
2. **Configure your API Key** → Authenticate with gateway
3. **Request proxy allocation** → Pay 0.001 USDC per call
4. **Auto-configure system proxy** → All traffic routes through proxy
5. **Access internet freely** → GitHub, Google, etc.

## Installation

```bash
clawhub install proxy-gateway-client
```

Or manual:
```bash
git clone https://github.com/laoke/proxy-gateway.git
cd proxy-gateway/client
pip install -e .
```

## Configuration

### 1. Get API Key

Contact the service provider or visit:
```
https://proxy.easky.cn/register
```

### 2. Configure Environment

```bash
export PROXY_GATEWAY_API_KEY="your_api_key_here"
export PROXY_GATEWAY_URL="https://proxy.easky.cn"  # Optional, default is official
```

Or create `.env` file:
```
PROXY_GATEWAY_API_KEY=pg_xxxxxxxxxxxx
```

## Usage

### Basic Usage

```python
from proxy_gateway_client import ProxyGatewayClient

# Initialize client
client = ProxyGatewayClient(
    api_key="your_api_key",
    base_url="https://proxy.easky.cn"  # Optional
)

# Get proxy allocation
proxy = client.get_proxy(region="us", duration=300)
print(f"Proxy allocated: {proxy['host']}:{proxy['port']}")

# Enable system proxy
client.enable_proxy()

# Now all requests go through proxy
import requests
response = requests.get("https://api.github.com")
print(response.json())

# Disable when done
client.disable_proxy()
```

### Advanced Usage with x402 Payment

```python
from proxy_gateway_client import ProxyGatewayClient, x402PaymentHandler

# For x402 payment mode
client = ProxyGatewayClient(
    api_key="your_api_key",
    payment_handler=x402PaymentHandler(
        wallet="your_polygon_wallet",
        private_key="your_private_key"
    )
)

# Auto-pay and get proxy
proxy = client.get_proxy_auto_pay(region="us")
```

### Using with OpenClaw

```python
# In your OpenClaw agent code
from proxy_gateway_client import ProxyGatewayClient

class MyAgent:
    def __init__(self):
        self.proxy = ProxyGatewayClient()
    
    def fetch_data(self, url):
        # Automatically uses proxy
        with self.proxy.session():
            import requests
            return requests.get(url)
```

## CLI Usage

```bash
# Set proxy for current shell
proxy-gateway enable --region us --duration 300

# Test connection
proxy-gateway test

# Check balance
proxy-gateway balance

# Disable proxy
proxy-gateway disable
```

## Pricing

| Service | Cost |
|---------|------|
| Proxy allocation (5 min) | 0.001 USDC |
| Per request through proxy | Included |

**Payment Flow**:
1. First request → Returns 402 Payment Required
2. Client signs payment (x402) → Sends signature
3. Server verifies → Returns proxy
4. Subsequent requests use same proxy until expiry

## API Methods

### `get_proxy(region, duration)`

Request a proxy allocation.

**Parameters**:
- `region`: "us", "eu", "sg", "jp"
- `duration`: Seconds (default: 300)

**Returns**:
```python
{
    "success": True,
    "proxy": {
        "host": "127.0.0.1",
        "port": 7890,
        "type": "http"
    },
    "expires_at": "2026-03-05T10:00:00Z"
}
```

### `enable_proxy()`

Configure system-wide proxy.

Sets:
- `HTTP_PROXY`
- `HTTPS_PROXY`
- `http_proxy`
- `https_proxy`

### `disable_proxy()`

Remove system proxy configuration.

### `session()`

Context manager for temporary proxy usage.

```python
with client.session(region="us"):
    # All requests in this block use proxy
    requests.get("https://api.github.com")
# Proxy auto-disabled after block
```

## Troubleshooting

**Q: "Payment Required" error**
A: You need to deposit USDC on Polygon network and sign payment.
```bash
# Check payment requirements
curl https://proxy.easky.cn/api/v1/payment-requirements
```

**Q: "Invalid API Key"**
A: Contact service provider to get valid API key.

**Q: Proxy not working**
A: Check if proxy is still valid:
```python
client.check_proxy_status()
```

## Links

- **Service**: https://proxy.easky.cn
- **Documentation**: https://docs.proxy.easky.cn
- **Support**: https://github.com/laoke/proxy-gateway/issues

## License

MIT © laoke
