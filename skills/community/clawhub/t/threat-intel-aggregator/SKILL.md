---
name: Threat Intelligence Aggregator
description: Aggregates and analyzes threat intelligence data to check targets against known threats and security risks.
---

# Overview

The Threat Intelligence Aggregator is a security-focused API that enables rapid threat assessment by cross-referencing targets against aggregated threat intelligence databases. Built for security teams, incident responders, and compliance professionals, this tool consolidates threat data from multiple sources to provide actionable intelligence on IPs, domains, file hashes, and other indicators of compromise.

This API is ideal for organizations that need real-time threat visibility without managing multiple third-party integrations. Whether you're conducting incident response, performing due diligence on external entities, or automating security workflows, the Threat Intelligence Aggregator delivers comprehensive threat context in a single API call.

Key capabilities include rapid threat lookups, multi-source threat correlation, and detailed risk assessment data—all accessible through a simple, RESTful interface designed for integration into SOAR platforms, security dashboards, and automated response systems.

## Usage

### Sample Request

```json
{
  "target": "192.168.1.100"
}
```

### Sample Response

```json
{
  "target": "192.168.1.100",
  "threat_status": "high_risk",
  "findings": [
    {
      "source": "abusech",
      "threat_type": "malware_c2",
      "confidence": 95,
      "last_seen": "2024-01-15T10:30:00Z"
    },
    {
      "source": "otx",
      "threat_type": "botnet",
      "confidence": 87,
      "last_seen": "2024-01-14T22:15:00Z"
    }
  ],
  "risk_score": 9.2,
  "recommendations": [
    "Block at firewall perimeter",
    "Investigate network connections",
    "Review logs for command execution"
  ],
  "aggregated_at": "2024-01-16T08:45:22Z"
}
```

## Endpoints

### POST /check-threat

Analyzes a target against aggregated threat intelligence sources to identify known threats and security risks.

**Method:** POST

**Path:** `/check-threat`

**Description:** Submits a target (IP address, domain, file hash, or URL) for threat assessment. The API queries multiple threat intelligence feeds and returns consolidated findings with risk scoring and remediation recommendations.

**Request Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| target | string | Yes | The indicator to check: IP address, domain name, file hash (MD5/SHA1/SHA256), or URL |

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| target | string | The checked indicator |
| threat_status | string | Overall threat assessment: `clean`, `low_risk`, `medium_risk`, `high_risk`, `critical_risk` |
| findings | array | Array of threat findings from individual sources |
| findings[].source | string | Threat intelligence source (e.g., `abusech`, `otx`, `abuseipdb`) |
| findings[].threat_type | string | Classification of threat detected |
| findings[].confidence | integer | Confidence score 0-100 |
| findings[].last_seen | string | ISO 8601 timestamp of most recent observation |
| risk_score | number | Aggregated risk score 0-10 |
| recommendations | array | List of recommended remediation actions |
| aggregated_at | string | ISO 8601 timestamp of aggregation time |

**HTTP Status Codes:**

- `200 OK` — Threat check completed successfully
- `422 Unprocessable Entity` — Invalid request body or malformed target parameter

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

- **Kong Route:** `https://api.mkkpro.com/security/threat-intel-aggregator`
- **API Docs:** `https://api.mkkpro.com:8009/docs`
