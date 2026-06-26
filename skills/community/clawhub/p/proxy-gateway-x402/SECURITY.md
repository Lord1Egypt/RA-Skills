# Security Policy

## Overview

Proxy Gateway x402 is a pay-per-use HTTP proxy service using the x402 protocol for agent-to-agent commerce. This document outlines security considerations and best practices.

## ⚠️ Critical Security Warnings

### 1. Private Key Safety

**NEVER use your main wallet for automatic payments.**

- Create a dedicated wallet with minimal funds for `USER_EVM_PRIVATE_KEY`
- Set strict spending limits on the wallet
- Monitor transactions regularly
- Use hardware wallets when possible

### 2. Data Visibility

**All request data is visible to the proxy server operator:**

- Full request URLs
- All HTTP headers (including authorization headers if sent)
- Request bodies
- Response content

**DO NOT use this proxy for:**
- API keys or access tokens
- Private keys or passwords
- Personal or sensitive data
- Internal/private network endpoints

### 3. Trust Model

This service operates with the following trust assumptions:

- User trusts the developer to provide service after payment
- User trusts the hosted proxy server with request data
- No escrow or dispute resolution mechanism
- Payments are final and non-refundable

## Server Implementation Details

### Redis Lua Script Execution

The server uses Redis Lua scripts for atomic balance operations:

```python
# app/managers/storage.py - Redis Lua script execution
self._redis.eval(lua_script, num_keys, *args)
```

This is a standard Redis operation for atomic transactions and is not a security vulnerability.

### Local Port Probing

The server checks for local Clash proxy (127.0.0.1:7890, 127.0.0.1:9090) to use as upstream proxy:

```python
# app/managers/proxy_manager.py
self.clash_api_url = f"http://127.0.0.1:{clash_api_port}"
```

This only reads local environment state and does not expose services.

## Self-Hosting Recommendation

For maximum privacy and security:

1. **Self-host the service** instead of using hosted endpoints
2. Deploy in an isolated environment (Docker/container)
3. Configure your own RPC endpoint
4. Use dedicated Redis instance with authentication
5. Keep `ADMIN_TOKEN` secure and rotate regularly

## Environment Variables

### Required for Server

- `DEVELOPER_WALLET`: Your wallet to receive payments
- `ADMIN_TOKEN`: Secure random token for admin endpoints

### Optional

- `PRICE_PER_REQUEST`: Price per request (default: 0.001)
- `X402_CHAIN`: Network (base, base-sepolia, polygon)
- `RPC_URL`: Custom RPC endpoint
- `REDIS_HOST`/`REDIS_PORT`: Redis configuration

### Client-Side (User)

- `USER_EVM_PRIVATE_KEY`: For automatic payments (use dedicated wallet!)

## Reporting Security Issues

If you discover a security vulnerability, please:

1. Do not open a public issue
2. Contact the maintainer directly
3. Allow time for remediation before disclosure

## Security Audit History

- v0.1.0: Initial security review by ClawHub automated analysis
- Identified: Redis Lua script usage (expected behavior)
- Identified: Local port checking for Clash proxy (expected behavior)
- Status: No critical vulnerabilities found

## License

MIT License - See LICENSE file for details.
