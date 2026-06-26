---
name: OTPLY API
description: Email OTP Service - Simple, Fast, Reliable
---

# Overview

OTPLY is a straightforward email-based One-Time Password (OTP) service designed for developers who need reliable email verification without complexity. Whether you're building user authentication, account recovery, or sensitive transaction verification, OTPLY delivers OTP codes directly to user inboxes with minimal latency and maximum reliability.

The service handles the entire OTP lifecycle: registration, credential management, OTP generation, delivery, and verification. It supports customizable OTP expiry times, purpose-based tracking, and template flexibility. Real-time usage statistics let you monitor consumption against your plan limits, ensuring you stay within budget while maintaining frictionless user experiences.

OTPLY is ideal for SaaS platforms, fintech applications, healthcare portals, and any service prioritizing secure email-based identity verification. Built by security professionals and available through multiple integration channels, it combines enterprise-grade reliability with developer-friendly APIs.

## Usage

### Example: Send and Verify OTP

**Request to send OTP:**

```json
POST /api/v1/send-otp
Headers:
  X-API-Key: your_api_key_here
  X-API-Secret: your_api_secret_here
  Content-Type: application/json

{
  "email": "user@example.com",
  "purpose": "login_verification",
  "template": "default",
  "expiry_minutes": 15
}
```

**Response:**

```json
{
  "success": true,
  "message": "OTP sent successfully to user@example.com",
  "expires_in": 900,
  "reference_id": "ref_1a2b3c4d5e6f7g8h"
}
```

**Request to verify OTP:**

```json
POST /api/v1/verify-otp
Headers:
  X-API-Key: your_api_key_here
  X-API-Secret: your_api_secret_here
  Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "654321",
  "purpose": "login_verification"
}
```

**Response:**

```json
{
  "success": true,
  "message": "OTP verified successfully",
  "verified_at": "2024-01-15T10:30:45.123456Z"
}
```

## Endpoints

### GET /
**Root endpoint** - API root information.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | — | — | — |

**Response:** Returns API root metadata.

---

### GET /health
**Health Check** - Service health status endpoint.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | — | — | — |

**Response:** Returns HTTP 200 with service health information.

---

### POST /api/v1/register
**Register** - Create a new customer account.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string (email) | Yes | Customer email address |
| password | string | Yes | Account password |
| company_name | string | No | Company name (optional) |

**Response:**

```json
{
  "success": true,
  "message": "Registration successful"
}
```

**Errors:**
- 422: Validation error (invalid email format, missing required fields, etc.)

---

### POST /api/v1/login
**Login** - Authenticate and retrieve API credentials.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string (email) | Yes | Customer email address |
| password | string | Yes | Account password |

**Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt_token_here",
  "api_key": "key_1a2b3c4d5e6f7g8h",
  "api_secret": "secret_1a2b3c4d5e6f7g8h"
}
```

**Errors:**
- 422: Validation error (invalid email format, missing fields)

---

### POST /api/v1/send-otp
**Send OTP** - Send a one-time password to an email address.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| X-API-Key | string (header) | Yes | Your API key |
| X-API-Secret | string (header) | Yes | Your API secret |
| email | string (email) | Yes | Recipient email address |
| purpose | string | No | OTP purpose (e.g., "verification", "login", "recovery"); defaults to "verification" |
| template | string | No | Email template name; defaults to "default" |
| expiry_minutes | integer | No | OTP validity in minutes; defaults to 10 |

**Response:**

```json
{
  "success": true,
  "message": "OTP sent successfully",
  "expires_in": 600,
  "reference_id": "ref_1a2b3c4d5e6f7g8h"
}
```

**Errors:**
- 422: Validation error (invalid email, invalid expiry_minutes, etc.)

---

### POST /api/v1/verify-otp
**Verify OTP** - Validate an OTP code against a stored request.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| X-API-Key | string (header) | Yes | Your API key |
| X-API-Secret | string (header) | Yes | Your API secret |
| email | string (email) | Yes | Email address associated with OTP |
| otp | string | Yes | The OTP code to verify (typically 6 digits) |
| purpose | string | No | OTP purpose for matching; defaults to "verification" |

**Response:**

```json
{
  "success": true,
  "message": "OTP verified successfully",
  "verified_at": "2024-01-15T10:30:45.123456Z"
}
```

**Errors:**
- 422: Validation error (invalid email, missing OTP, etc.)

---

### GET /api/v1/usage
**Get Usage** - Retrieve current usage statistics and remaining credits.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| X-API-Key | string (header) | Yes | Your API key |
| X-API-Secret | string (header) | Yes | Your API secret |

**Response:**

```json
{
  "customer": "user@example.com",
  "plan": "Professional",
  "credits_remaining": 4500,
  "credits_total": 5000,
  "usage": {
    "send_otp": 450,
    "verify_otp": 50
  }
}
```

**Errors:**
- 422: Validation error (missing API credentials)

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

- **Kong Route:** https://api.toolweb.in/tools/otply
- **API Docs:** https://api.toolweb.in:8168/docs
