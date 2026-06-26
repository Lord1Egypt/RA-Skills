---
name: Threat Intelligence Aggregator
description: Aggregates and analyzes open-source intelligence (OSINT) data from multiple sources to identify threats, validate indicators, and enrich security investigations.
---

# Overview

The Threat Intelligence Aggregator is a security-focused API that collects, normalizes, and correlates open-source intelligence (OSINT) data across public and proprietary threat feeds. It enables security teams to rapidly enrich indicators of compromise (IoCs)—including IP addresses, domains, file hashes, and email addresses—with contextual threat intelligence, reputation scores, and historical breach data.

This tool is essential for SOC analysts, threat hunters, and incident responders who need rapid validation of suspicious artifacts during investigations. By querying a unified aggregation layer rather than consulting dozens of separate feeds, teams reduce investigation time, improve accuracy, and maintain consistent threat scoring across the organization.

The API is ideal for security operations centers (SOCs), managed security service providers (MSSPs), threat intelligence platforms (TIPs), and enterprise security teams building custom detection and response workflows.

## Usage

### Sample Request

```json
{
  "input": "192.168.1.100"
}
```

### Sample Response

```json
{
  "indicator": "192.168.1.100",
  "indicator_type": "ipv4",
  "reputation_score": 72,
  "threat_level": "high",
  "sources": [
    {
      "name": "AbuseIPDB",
      "reports": 145,
      "last_seen": "2024-01-15T09:32:00Z"
    },
    {
      "name": "Shodan",
      "services": ["SSH", "HTTP"],
      "last_scanned": "2024-01-14T18:20:00Z"
    }
  ],
  "associated_malware": [
    "Emotet",
    "Trickbot"
  ],
  "geolocation": {
    "country": "RU",
    "city": "Moscow",
    "asn": "AS8452"
  },
  "whois_data": {
    "registrar": "RIPE NCC",
    "registered": "2015-03-22"
  },
  "confidence": 0.89,
  "last_updated": "2024-01-15T10:45:00Z"
}
```

## Endpoints

### POST /osint-lookup

**Description:** Performs open-source intelligence lookup on a provided indicator. Aggregates threat data from multiple sources and returns enriched threat intelligence including reputation scores, geolocation, associated malware, and source attribution.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input` | string | Yes | The indicator to query. Supports IPv4/IPv6 addresses, fully qualified domain names (FQDNs), email addresses, file hashes (MD5, SHA-1, SHA-256), and URLs. |

**Response Schema (200 OK):**

```json
{
  "indicator": "string",
  "indicator_type": "string",
  "reputation_score": "number",
  "threat_level": "string",
  "sources": [
    {
      "name": "string",
      "reports": "integer",
      "last_seen": "string (ISO 8601)"
    }
  ],
  "associated_malware": ["string"],
  "geolocation": {
    "country": "string",
    "city": "string",
    "asn": "string"
  },
  "whois_data": {
    "registrar": "string",
    "registered": "string"
  },
  "confidence": "number",
  "last_updated": "string (ISO 8601)"
}
```

**Error Response (422 Validation Error):**

```json
{
  "detail": [
    {
      "loc": ["body", "input"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

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

- **Kong Route:** `https://api.mkkpro.com/security/threat-intel-v2`
- **API Docs:** `https://api.mkkpro.com:8011/docs`
