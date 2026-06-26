---
name: Active Directory Hardening Tool
description: Enterprise-grade API for generating optimized Active Directory security configuration files with hardening best practices.
---

# Overview

The Active Directory Hardening Tool is an enterprise-grade security API designed to generate comprehensive Active Directory (AD) hardening configuration files based on industry best practices and CISSP-aligned security standards. This tool automates the complex process of configuring AD security settings, reducing manual configuration errors and ensuring consistent security posture across AD environments.

Organizations managing large-scale Active Directory deployments require robust security configurations to protect against lateral movement, privilege escalation, and unauthorized access. This tool streamlines the generation of hardening configurations by accepting flexible hardening options and producing deployment-ready configuration files. It is ideal for security architects, system administrators, and organizations undergoing AD security assessments or compliance initiatives.

The API provides enumeration of available hardening options, allowing teams to understand all supported configurations before generating customized hardening profiles. This enables organizations to tailor security configurations to their specific risk profiles and operational requirements.

# Usage

## Sample Request

Generate an AD hardening configuration with multiple security options:

```json
{
  "sessionId": "sess_abc123def456",
  "userId": 12345,
  "timestamp": "2025-01-15T10:30:00Z",
  "hardeningOptions": {
    "passwordPolicy": ["enforceComplexity", "minLength14", "historyCount24"],
    "accountLockout": ["threshold5", "duration30minutes", "resetCounterAfter30"],
    "kerberosHardening": ["enableAESEncryption", "disableRC4", "setMaxTicketLifetime"],
    "groupPolicy": ["enableAudit", "disableAnonymousAccess", "restrictNetworkAccess"]
  }
}
```

## Sample Response

```json
{
  "status": "success",
  "configurationId": "config_xyz789uvw",
  "timestamp": "2025-01-15T10:30:15Z",
  "configurations": {
    "passwordPolicy": {
      "enforceComplexity": true,
      "minimumLength": 14,
      "passwordHistoryCount": 24,
      "maximumPasswordAge": 90
    },
    "accountLockout": {
      "lockoutThreshold": 5,
      "lockoutDuration": 30,
      "resetCounterAfterMinutes": 30
    },
    "kerberosHardening": {
      "encryptionTypes": ["AES256", "AES128"],
      "disabledEncryption": ["RC4"],
      "maxTicketLifetimeHours": 10
    },
    "groupPolicy": {
      "auditingEnabled": true,
      "anonymousAccessDisabled": true,
      "networkAccessRestricted": true
    }
  },
  "deploymentScript": "powershell_script_content_here",
  "auditLog": {
    "requestId": "req_123456",
    "userId": 12345,
    "action": "AD_HARDENING_GENERATED",
    "timestamp": "2025-01-15T10:30:15Z"
  }
}
```

# Endpoints

## GET /

**Health Check Endpoint**

Verifies API availability and returns service status.

**Method:** GET  
**Path:** `/`

**Parameters:** None

**Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** Service status object confirming API health

---

## POST /api/ad-hardening/generate

**Generate AD Hardening Configuration**

Generates enterprise-ready Active Directory hardening configuration files based on specified security options. Returns deployable configurations and scripts.

**Method:** POST  
**Path:** `/api/ad-hardening/generate`

**Request Body (application/json):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hardeningOptions` | Object (string arrays) | Yes | Map of hardening categories to configuration options. Keys represent hardening domains (e.g., passwordPolicy, accountLockout, kerberosHardening); values are arrays of specific settings to apply. |
| `sessionId` | String | Yes | Unique session identifier for request tracking and audit logging. Used to correlate multiple requests within a session. |
| `userId` | Integer \| null | No | Optional user identifier for audit trail association. Useful for tracking which user generated the configuration. |
| `timestamp` | String | Yes | ISO 8601 formatted timestamp of request generation. Must be in UTC format (e.g., "2025-01-15T10:30:00Z"). |

**Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** Configuration object containing hardened AD settings, deployment scripts, and audit trail metadata
- **Status Code:** 422 (on validation error)
- **Content-Type:** application/json
- **Body:** HTTPValidationError object with detailed field-level validation errors

---

## GET /api/ad-hardening/options

**Retrieve Available Hardening Options**

Enumerates all supported Active Directory hardening options, categories, and their descriptions. Use this endpoint to discover available configurations before generating hardening profiles.

**Method:** GET  
**Path:** `/api/ad-hardening/options`

**Parameters:** None

**Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** Object containing hierarchical hardening options with descriptions:
  - Available hardening categories (passwordPolicy, accountLockout, kerberosHardening, groupPolicy, etc.)
  - Supported settings within each category
  - Parameter descriptions and recommended values
  - Security impact and compliance mappings

# Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

# About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

# References

- **Kong Route:** https://api.mkkpro.com/hardening/active-directory
- **API Documentation:** https://api.mkkpro.com:8127/docs
