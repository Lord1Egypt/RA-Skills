---
name: Mirrory API
description: Token generation and validation service for WordPress proxy and desktop application session management.
---

# Overview

Mirrory API is a secure token management service designed to handle authentication workflows between WordPress proxy systems and desktop applications. It provides robust token generation tied to WordPress user accounts and validates session tokens on application startup, ensuring secure and seamless user experiences across integrated platforms.

The API operates on a coin-based system where WordPress proxies deduct 200 coins before requesting token generation. This integration model allows for metered access control and usage tracking across enterprise deployments. Desktop applications leverage the validation endpoint to verify token authenticity and machine binding on each session initialization.

Ideal users include WordPress administrators managing multi-platform authentication, desktop application developers requiring secure session management, and enterprises implementing token-based access control across distributed systems.

## Usage

### Generate Token

A WordPress proxy generates a token after deducting 200 coins from a user account:

**Request:**
```json
{
  "wp_user_id": 12345,
  "proxy_secret": "your-proxy-secret-key-here"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400,
  "user_id": 12345
}
```

### Validate Token

A desktop application validates a token on startup to verify the session is active:

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "machine_id": "desktop-machine-uuid-1234567890"
}
```

**Response:**
```json
{
  "valid": true,
  "user_id": 12345,
  "machine_id": "desktop-machine-uuid-1234567890",
  "expires_at": "2024-12-31T23:59:59Z"
}
```

## Endpoints

### POST /mirrory/generate-token

Generates a new authentication token for a WordPress user after coin deduction by the proxy.

- **Method:** POST
- **Path:** `/mirrory/generate-token`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `wp_user_id` | integer | Yes | The WordPress user ID requesting the token |
| `proxy_secret` | string | Yes | Secret key from the WordPress proxy for authentication |

**Response:**

- **Status:** 200 (Success) / 422 (Validation Error)
- **Content-Type:** application/json
- **Schema:** Token object with expiration details

---

### POST /mirrory/validate-token

Validates an existing token and confirms it is bound to the specified machine, typically called by desktop applications on startup.

- **Method:** POST
- **Path:** `/mirrory/validate-token`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `token` | string | Yes | The JWT token to validate |
| `machine_id` | string | Yes | Unique identifier of the requesting machine |

**Response:**

- **Status:** 200 (Success) / 422 (Validation Error)
- **Content-Type:** application/json
- **Schema:** Validation result with user ID, machine binding, and expiration timestamp

---

### GET /mirrory/health

Health check endpoint to verify API service availability.

- **Method:** GET
- **Path:** `/mirrory/health`

**Response:**

- **Status:** 200
- **Content-Type:** application/json
- **Schema:** Health status object

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

- **Kong Route:** https://api.toolweb.in/tools/mirrory
- **API Docs:** https://api.toolweb.in:8202/docs
