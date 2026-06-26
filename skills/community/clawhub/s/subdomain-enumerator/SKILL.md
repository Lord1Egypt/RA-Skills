---
name: Subdomain Enumerator
description: Discovers and enumerates all subdomains associated with a target domain using deep reconnaissance techniques.
---

# Overview

The Subdomain Enumerator is a powerful reconnaissance tool designed for security professionals, penetration testers, and bug bounty hunters who need to identify all active and inactive subdomains within a target domain. This API leverages multiple enumeration techniques to build a comprehensive map of an organization's subdomain infrastructure, which is critical for attack surface mapping and vulnerability assessment.

Subdomain enumeration is often the first step in a security assessment workflow. By discovering hidden or forgotten subdomains, security teams can identify overlooked assets that may contain vulnerabilities, outdated services, or misconfigurations. The Subdomain Enumerator automates this reconnaissance process, saving time and improving coverage compared to manual discovery methods.

This tool is ideal for security researchers conducting authorized penetration tests, red team operators performing scope definition, DevSecOps teams mapping their infrastructure, and organizations performing internal asset discovery for compliance purposes.

## Usage

### Sample Request

```json
{
  "domain": "example.com"
}
```

### Sample Response

```json
{
  "domain": "example.com",
  "subdomains": [
    {
      "subdomain": "www.example.com",
      "ip_address": "93.184.216.34",
      "status": "active"
    },
    {
      "subdomain": "mail.example.com",
      "ip_address": "93.184.216.35",
      "status": "active"
    },
    {
      "subdomain": "staging.example.com",
      "ip_address": "192.0.2.1",
      "status": "active"
    },
    {
      "subdomain": "old-api.example.com",
      "ip_address": null,
      "status": "inactive"
    }
  ],
  "total_found": 4,
  "enumeration_time_ms": 5420
}
```

## Endpoints

### POST /enumerate-deep

Performs deep enumeration of subdomains for a specified domain using multiple reconnaissance techniques.

**Method:** `POST`  
**Path:** `/enumerate-deep`

**Request Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| domain | string | Yes | The target domain to enumerate (e.g., `example.com`). Must be a valid domain name. |

**Response Schema:**

The response returns a JSON object containing:

| Field | Type | Description |
|-------|------|-------------|
| domain | string | The target domain that was enumerated |
| subdomains | array | Array of discovered subdomain objects, each containing `subdomain`, `ip_address`, and `status` fields |
| total_found | integer | Total count of subdomains discovered |
| enumeration_time_ms | integer | Time taken to complete enumeration in milliseconds |

**HTTP Status Codes:**

- `200 OK` — Enumeration completed successfully
- `422 Unprocessable Entity` — Validation error in request body (missing or invalid domain parameter)

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in — 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in)
- 🐾 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- 🚀 [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** `https://api.mkkpro.com/security/subdomain-enumerator`
- **API Docs:** `https://api.mkkpro.com:8006/docs`
