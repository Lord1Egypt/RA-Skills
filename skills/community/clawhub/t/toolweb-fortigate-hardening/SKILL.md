---
name: FortiGate Security Hardening Tool
description: Professional FortiGate security configuration generator based on CIS Benchmark standards for enterprise firewall hardening.
---

# Overview

The FortiGate Security Hardening Tool is a professional-grade API that generates hardened FortiGate firewall configurations aligned with CIS Benchmark security standards. Built for security teams, network architects, and compliance officers, this tool automates the creation of security configuration files that follow industry best practices and regulatory requirements.

This tool eliminates manual configuration errors and reduces deployment time by generating validated, production-ready FortiGate configurations. Organizations can quickly implement security hardening across their firewall infrastructure while maintaining consistency with established security frameworks. The API supports flexible configuration options, allowing teams to customize hardening profiles based on their specific security posture requirements and organizational policies.

Ideal users include enterprise security teams, managed security service providers (MSSPs), infrastructure-as-code practitioners, and compliance professionals who need to standardize and automate FortiGate security deployments at scale.

# Usage

**Generate a hardened FortiGate configuration with specific security options:**

```json
POST /api/fortigate/generate

{
  "sessionId": "sess_abc123def456",
  "userId": 42,
  "timestamp": "2025-01-15T10:30:00Z",
  "hardeningOptions": {
    "firewall_policies": ["strict_inbound", "deny_by_default"],
    "ssl_tls": ["tls_1_3_only", "strong_ciphers"],
    "admin_access": ["disable_telnet", "https_only", "change_default_port"],
    "logging": ["enable_threat_logging", "enable_traffic_logging"],
    "authentication": ["enable_2fa", "strong_password_policy"]
  }
}
```

**Sample Response:**

```json
{
  "status": "success",
  "configurationId": "cfg_xyz789abc123",
  "timestamp": "2025-01-15T10:30:15Z",
  "configuration": {
    "firewall_rules": [
      {
        "name": "Default_Deny_Inbound",
        "action": "deny",
        "direction": "inbound",
        "schedule": "always"
      }
    ],
    "ssl_tls_settings": {
      "min_version": "TLSv1.3",
      "cipher_suites": ["TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"]
    },
    "admin_settings": {
      "telnet_enabled": false,
      "http_enabled": false,
      "https_enabled": true,
      "admin_port": 8443
    },
    "logging": {
      "threat_logging": true,
      "traffic_logging": true,
      "log_level": "information"
    },
    "authentication": {
      "two_factor_enabled": true,
      "password_policy": {
        "min_length": 16,
        "require_uppercase": true,
        "require_numbers": true,
        "require_special_chars": true
      }
    }
  },
  "download_url": "https://api.mkkpro.com/hardening/fortigate/cfg_xyz789abc123"
}
```

# Endpoints

## GET /

**Health Check Endpoint**

Performs a basic health check to verify API availability and connectivity.

**Parameters:** None

**Response:**
- Status: `200 OK`
- Content-Type: `application/json`
- Body: Health status object

---

## POST /api/fortigate/generate

**Generate FortiGate Security Configuration**

Generates a complete hardened FortiGate firewall configuration file based on provided hardening options and CIS Benchmark standards.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hardeningOptions` | Object | Yes | A dictionary mapping hardening categories to arrays of specific hardening options. Example categories: `firewall_policies`, `ssl_tls`, `admin_access`, `logging`, `authentication`. Each value is an array of string option names. |
| `sessionId` | String | Yes | Unique session identifier for tracking and audit purposes. |
| `userId` | Integer or Null | No | Optional user ID associated with the configuration generation request. |
| `timestamp` | String | Yes | ISO 8601 formatted timestamp of the request (e.g., `2025-01-15T10:30:00Z`). |

**Response:**
- Status: `200 OK` on success, `422 Unprocessable Entity` on validation error
- Content-Type: `application/json`
- Body:
  ```json
  {
    "status": "success",
    "configurationId": "string",
    "timestamp": "string",
    "configuration": {
      "firewall_rules": "array",
      "ssl_tls_settings": "object",
      "admin_settings": "object",
      "logging": "object",
      "authentication": "object"
    },
    "download_url": "string"
  }
  ```

---

## GET /api/fortigate/options

**Retrieve Available FortiGate Hardening Options**

Returns a comprehensive list of all available FortiGate hardening configuration options, allowing clients to discover supported parameters before generating configurations.

**Parameters:** None

**Response:**
- Status: `200 OK`
- Content-Type: `application/json`
- Body: Object containing available hardening categories and their supported options:
  ```json
  {
    "firewall_policies": ["strict_inbound", "deny_by_default", "log_all_traffic"],
    "ssl_tls": ["tls_1_3_only", "strong_ciphers", "disable_weak_protocols"],
    "admin_access": ["disable_telnet", "https_only", "change_default_port", "restrict_admin_ips"],
    "logging": ["enable_threat_logging", "enable_traffic_logging", "centralized_logging"],
    "authentication": ["enable_2fa", "strong_password_policy", "disable_default_accounts"]
  }
  ```

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

- **Kong Route:** https://api.mkkpro.com/hardening/fortigate
- **API Docs:** https://api.mkkpro.com:8135/docs
