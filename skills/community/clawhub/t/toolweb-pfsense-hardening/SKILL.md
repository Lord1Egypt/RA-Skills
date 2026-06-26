---
name: pfSense Hardening Tool
description: Generates hardened pfSense firewall configurations based on specified security options.
---

# Overview

The pfSense Hardening Tool is a security-focused API that automates the generation of hardened configurations for pfSense firewalls. Built by CISSP and CISM certified professionals, this tool enables network administrators and security engineers to quickly apply industry best practices and security hardening standards to their pfSense deployments without manual configuration.

The tool accepts a set of hardening options and generates optimized pfSense configurations tailored to your security requirements. It supports session tracking, user identification, and timestamped requests to ensure audit compliance and change management. Whether you're deploying a new pfSense instance or enhancing an existing firewall, this tool streamlines the hardening process and reduces configuration errors.

Ideal users include network security teams, DevSecOps engineers, managed security service providers (MSSPs), and organizations seeking to standardize their firewall security posture across multiple pfSense installations.

## Usage

**Sample Request:**

```json
{
  "hardeningOptions": {
    "firewall_rules": ["block_all_inbound", "restrict_ssh_access"],
    "ssl_tls": ["disable_sslv3", "enable_tls_1_2_minimum"],
    "logging": ["enable_firewall_logging", "enable_dhcp_logging"]
  },
  "sessionId": "sess_a7f9d3c2b1e4f6h8",
  "userId": 42,
  "timestamp": "2025-01-15T14:30:00Z"
}
```

**Sample Response:**

```json
{
  "status": "success",
  "configurationId": "config_9x2k5m8l1p4q7r3t",
  "hardeningApplied": {
    "firewall_rules": ["block_all_inbound", "restrict_ssh_access"],
    "ssl_tls": ["disable_sslv3", "enable_tls_1_2_minimum"],
    "logging": ["enable_firewall_logging", "enable_dhcp_logging"]
  },
  "generatedConfig": {
    "version": "2.7.0",
    "firewall": {
      "rules": [
        {
          "id": 1,
          "action": "block",
          "direction": "in",
          "description": "Block all inbound traffic by default"
        }
      ]
    },
    "system": {
      "ssl_tls_version": "1.2",
      "logging_enabled": true
    }
  },
  "timestamp": "2025-01-15T14:30:15Z",
  "sessionId": "sess_a7f9d3c2b1e4f6h8"
}
```

## Endpoints

### POST /api/hardening/generate

**Description:** Generates a hardened pfSense configuration based on provided hardening options.

**Method:** POST

**Path:** `/api/hardening/generate`

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hardeningOptions` | Object (string array values) | **Required** | A map of hardening categories to arrays of hardening rules to apply. Examples: `firewall_rules`, `ssl_tls`, `logging`, `access_control`, etc. |
| `sessionId` | String | **Required** | Unique identifier for the current session, used for audit tracking and request correlation. |
| `userId` | Integer | Optional | User ID of the administrator requesting the hardened configuration. |
| `timestamp` | String | **Required** | ISO 8601 formatted timestamp indicating when the request was generated (e.g., `2025-01-15T14:30:00Z`). |

**Response (200 - Success):**

The endpoint returns a JSON object containing:
- `status`: String indicating success or failure
- `configurationId`: Unique identifier for the generated configuration
- `hardeningApplied`: Echo of the hardening options that were applied
- `generatedConfig`: The complete hardened pfSense configuration object
- `timestamp`: Server-side timestamp of the response
- `sessionId`: Echo of the provided session ID for correlation

**Response (422 - Validation Error):**

Returns an `HTTPValidationError` object with a `detail` array containing validation errors:

| Field | Type | Description |
|-------|------|-------------|
| `detail` | Array | Array of validation error objects |
| `detail[].loc` | Array | Location of the validation error (field path) |
| `detail[].msg` | String | Human-readable error message |
| `detail[].type` | String | Error type identifier |

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

- Kong Route: https://api.mkkpro.com/hardening/pfsense
- API Docs: https://api.mkkpro.com:8131/docs
