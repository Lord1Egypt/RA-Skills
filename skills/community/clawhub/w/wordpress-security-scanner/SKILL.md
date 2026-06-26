---
name: WordPress Security Scanner
description: Scan WordPress sites for security vulnerabilities, misconfigurations, and potential threats.
---

# Overview

The WordPress Security Scanner is a specialized security assessment tool designed to identify vulnerabilities, weak configurations, and security risks in WordPress installations. It performs automated scanning of WordPress sites to detect common security issues including outdated plugins, insecure themes, missing security headers, and other critical weaknesses that could expose sites to attack.

This tool is ideal for WordPress site owners, security professionals, penetration testers, and hosting providers who need to maintain visibility into the security posture of their WordPress deployments. Whether you're performing routine security audits, pre-deployment assessments, or continuous monitoring, the WordPress Security Scanner provides actionable intelligence to strengthen your WordPress security.

The scanner analyzes multiple security dimensions of your WordPress installation and returns detailed findings that enable you to prioritize remediation efforts and implement security hardening measures.

## Usage

**Example Request:**

```json
{
  "url": "https://example-wordpress.com"
}
```

**Example Response:**

```json
{
  "scan_id": "scan_1234567890",
  "url": "https://example-wordpress.com",
  "status": "completed",
  "timestamp": "2024-01-15T10:30:45Z",
  "findings": {
    "critical": [
      {
        "type": "outdated_wordpress",
        "severity": "critical",
        "description": "WordPress version 5.8.2 detected. Current version is 6.4.2.",
        "remediation": "Update WordPress to the latest stable version immediately."
      }
    ],
    "high": [
      {
        "type": "exposed_wordpress_version",
        "severity": "high",
        "description": "WordPress version is publicly exposed in HTML source.",
        "remediation": "Remove version information from header and implement version hiding."
      }
    ],
    "medium": [
      {
        "type": "missing_security_headers",
        "severity": "medium",
        "description": "Missing X-Frame-Options header detected.",
        "remediation": "Add security headers: X-Frame-Options, X-Content-Type-Options, etc."
      }
    ]
  },
  "summary": {
    "total_issues": 3,
    "critical_count": 1,
    "high_count": 1,
    "medium_count": 1,
    "low_count": 0
  }
}
```

## Endpoints

### POST /scan

**Description:** Scan a WordPress site for security vulnerabilities and misconfigurations.

**Method:** `POST`

**Path:** `/scan`

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | The full URL of the WordPress site to scan (e.g., `https://example.com`). Must be a valid, publicly accessible WordPress installation. |

**Response (200 OK):**

The response contains a comprehensive security assessment including:

- `scan_id` (string): Unique identifier for the scan
- `url` (string): The scanned WordPress URL
- `status` (string): Scan status ("completed", "in_progress", or "failed")
- `timestamp` (string): ISO 8601 formatted scan timestamp
- `findings` (object): Categorized security findings organized by severity level
  - `critical` (array): Critical security issues requiring immediate action
  - `high` (array): High-severity vulnerabilities
  - `medium` (array): Medium-severity issues
  - `low` (array): Low-severity findings
- `summary` (object): Aggregated counts of issues by severity

Each finding includes:
- `type` (string): Classification of the vulnerability
- `severity` (string): Severity level
- `description` (string): Detailed explanation of the issue
- `remediation` (string): Recommended corrective action

**Response (422 Validation Error):**

Returns validation errors if the request is malformed:

```json
{
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| detail | array | Array of validation error objects |
| loc | array | Location path to the invalid field |
| msg | string | Error message |
| type | string | Error type classification |

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

- **Kong Route:** https://api.mkkpro.com/security/wordpress-security-scanner
- **API Docs:** https://api.mkkpro.com:8031/docs
