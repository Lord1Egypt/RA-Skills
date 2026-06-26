---
name: Central Key Management System
description: Enterprise-grade API key generation, verification, and lifecycle management with centralized administrative control.
---

# Overview

The Central Key Management System is a secure, centralized platform for managing cryptographic API keys across distributed applications and services. Designed for organizations that require strict control over key generation, distribution, and revocation, this system provides administrators with a comprehensive dashboard to oversee all key lifecycle operations.

This system enables secure authentication through admin-controlled key generation, real-time key verification, and immediate revocation capabilities. The platform maintains detailed audit trails and session management, making it ideal for enterprises operating under regulatory compliance frameworks such as SOC 2, ISO 27001, and PCI-DSS.

Organizations use the Central Key Management System to enforce key rotation policies, prevent unauthorized access through rapid revocation, and maintain centralized visibility into all API key operations across their infrastructure.

## Usage

### Generate a New API Key

**Request:**
```json
{
  "client_name": "payment-service-prod",
  "expires_at": "2025-12-31T23:59:59Z"
}
```

**cURL:**
```bash
curl -X POST https://api.mkkpro.com/career/linproopt/generate-key-ui \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_name=payment-service-prod&expires_at=2025-12-31T23:59:59Z"
```

**Response:**
```json
{
  "api_key": "sk_prod_a7f9d3e2c1b5f8g4h6j2k9m1n3p5r7t9",
  "client_name": "payment-service-prod",
  "created_at": "2024-01-15T10:30:22Z",
  "expires_at": "2025-12-31T23:59:59Z",
  "status": "active"
}
```

### Verify an API Key

**Request:**
```bash
curl -X POST https://api.mkkpro.com/career/linproopt/verify-key \
  -H "Content-Type: application/json" \
  -d '{"api_key": "sk_prod_a7f9d3e2c1b5f8g4h6j2k9m1n3p5r7t9"}'
```

**Response:**
```json
{
  "valid": true,
  "client_name": "payment-service-prod",
  "expires_at": "2025-12-31T23:59:59Z",
  "status": "active",
  "last_used": "2024-01-15T14:22:10Z"
}
```

## Endpoints

### Authentication

#### GET `/login`
Retrieve the login page interface.

**Response:**
- **200 OK** - HTML login page (text/html)

---

#### POST `/login`
Authenticate using an admin key to access the management dashboard.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `admin_key` | string | Yes | Administrative key for authentication |

**Response:**
- **200 OK** - Authentication successful, returns JSON with session token
- **422 Validation Error** - Missing or invalid admin_key parameter

---

#### GET `/logout`
Terminate the current session and invalidate the session token.

**Response:**
- **200 OK** - Successfully logged out

---

### Key Management

#### POST `/generate-key-ui`
Generate a new API key for a client with specified expiration.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `client_name` | string | Yes | Unique identifier for the client or service requesting the key |
| `expires_at` | string | Yes | ISO 8601 timestamp indicating key expiration (e.g., `2025-12-31T23:59:59Z`) |

**Response:**
- **200 OK** - Key successfully generated, returns API key details
- **422 Validation Error** - Missing or malformed parameters

---

#### GET `/get-random-key`
Retrieve a randomly generated key from the system's key pool.

**Response:**
- **200 OK** - Returns a random API key object

---

#### POST `/verify-key`
Validate an API key and retrieve its metadata and status.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `api_key` | string | Yes | The API key to validate |

**Response:**
- **200 OK** - Key validation result with client name, expiration, and status

---

#### POST `/revoke-key`
Immediately revoke an active API key, preventing further use.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `api_key` | string | Yes | The API key to revoke |

**Response:**
- **200 OK** - Key successfully revoked
- **422 Validation Error** - Missing or invalid api_key parameter

---

### Administrative & Diagnostic

#### GET `/admin`
Access the administrative dashboard for key management and system oversight.

**Response:**
- **200 OK** - HTML admin panel interface (text/html)

---

#### GET `/debug-session`
Retrieve current session information for debugging and audit purposes.

**Response:**
- **200 OK** - Session details in JSON format

---

#### GET `/healthz`
Health check endpoint for monitoring system availability and readiness.

**Response:**
- **200 OK** - System is operational

---

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/career/linproopt
- **API Docs:** https://api.mkkpro.com:8100/docs
