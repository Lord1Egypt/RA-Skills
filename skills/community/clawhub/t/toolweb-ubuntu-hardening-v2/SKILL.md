---
name: Ubuntu Linux Security Hardening Tool
description: Professional Ubuntu 22.04 LTS security configuration generator for STIG-compliant hardening.
---

# Overview

The Ubuntu Linux Security Hardening Tool is a professional-grade security configuration generator designed for Ubuntu 22.04 LTS systems. It automates the creation of STIG-compliant hardening configurations, eliminating manual security baseline setup and reducing human error in system hardening processes.

This tool enables security engineers, system administrators, and DevOps teams to generate comprehensive hardening configuration files tailored to their specific security requirements. By leveraging industry-standard hardening categories and options, users can quickly deploy security best practices across their infrastructure while maintaining compliance with established security frameworks.

The tool is ideal for organizations implementing Zero Trust architectures, preparing for security audits, managing multi-server deployments, or standardizing security baselines across development, staging, and production environments.

# Usage

## Example Request

Generate a hardening configuration with kernel hardening, SSH security, and firewall policies enabled:

```json
{
  "hardeningOptions": {
    "kernel_hardening": [
      "kptr_restrict",
      "dmesg_restrict",
      "unprivileged_namespaces"
    ],
    "ssh_security": [
      "disable_password_auth",
      "disable_root_login",
      "change_default_port"
    ],
    "firewall": [
      "enable_ufw",
      "default_deny_incoming"
    ]
  },
  "sessionId": "sess_a1b2c3d4e5f6g7h8",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Example Response

```json
{
  "status": "success",
  "configId": "cfg_9x8y7w6v5u4t3s2r",
  "timestamp": "2024-01-15T10:30:15Z",
  "configurations": {
    "kernel_hardening": {
      "file": "hardening-kernel.conf",
      "settings": [
        {
          "parameter": "kernel.kptr_restrict",
          "value": "2",
          "description": "Hide kernel pointers in dmesg and /proc"
        },
        {
          "parameter": "kernel.dmesg_restrict",
          "value": "1",
          "description": "Restrict dmesg access to root only"
        },
        {
          "parameter": "kernel.unprivileged_userns_clone",
          "value": "0",
          "description": "Disable unprivileged user namespaces"
        }
      ]
    },
    "ssh_security": {
      "file": "hardening-sshd_config",
      "settings": [
        {
          "directive": "PasswordAuthentication",
          "value": "no",
          "description": "Disable password-based authentication"
        },
        {
          "directive": "PermitRootLogin",
          "value": "no",
          "description": "Disable direct root login"
        },
        {
          "directive": "Port",
          "value": "2222",
          "description": "Change SSH listening port from default 22"
        }
      ]
    },
    "firewall": {
      "file": "hardening-ufw.rules",
      "settings": [
        {
          "command": "ufw enable",
          "description": "Enable UFW firewall"
        },
        {
          "command": "ufw default deny incoming",
          "description": "Set default policy to deny all incoming"
        }
      ]
    }
  },
  "totalConfigurations": 3,
  "downloadUrl": "https://api.mkkpro.com/hardening/ubuntu-v2/cfg_9x8y7w6v5u4t3s2r/download"
}
```

# Endpoints

## GET /

**Description:** Health check endpoint to verify API availability.

**Parameters:** None

**Response:** 
- Status 200: JSON object confirming API health status

---

## POST /api/hardening/generate

**Description:** Generate Ubuntu security hardening configuration files based on specified hardening options.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| hardeningOptions | Object | Yes | Map of hardening categories to arrays of specific options to enable. Categories may include: `kernel_hardening`, `ssh_security`, `firewall`, `apparmor`, `audit_logging`, `user_account_security`, `file_permissions`, `network_hardening` |
| sessionId | String | Yes | Unique session identifier for tracking and logging purposes |
| userId | Integer or null | No | Optional user identifier for audit trail and usage tracking |
| timestamp | String | Yes | ISO 8601 formatted timestamp when the request is generated |

**Response:**
- Status 200: JSON object containing generated configurations, config ID, and download URL
- Status 422: Validation error with details about invalid request parameters

---

## GET /api/hardening/options

**Description:** Retrieve all available hardening options across all categories that can be used in configuration generation.

**Parameters:** None

**Response:**
- Status 200: JSON object containing complete list of all hardening categories and their available options with descriptions

---

## GET /api/hardening/categories

**Description:** Retrieve hardening categories and their associated options for use in building hardening requests.

**Parameters:** None

**Response:**
- Status 200: JSON object containing structured hardening categories, available options within each category, and option metadata including descriptions and impact levels

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

- **Kong Route:** https://api.mkkpro.com/hardening/ubuntu-v2
- **API Docs:** https://api.mkkpro.com:8129/docs
