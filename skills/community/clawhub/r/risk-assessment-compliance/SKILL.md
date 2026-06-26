---
name: Risk Assessment & Compliance
description: Performs comprehensive security checks and compliance risk assessments on websites and applications.
---

# Overview

Risk Assessment & Compliance is a security-focused API that evaluates web applications and websites for vulnerabilities, compliance violations, and security posture. It provides detailed risk assessments that help organizations identify potential security gaps, regulatory compliance issues, and remediation priorities.

This tool is essential for security teams, compliance officers, and DevOps engineers who need to continuously monitor and validate the security posture of their digital assets. The API performs deep security analysis including vulnerability detection, compliance framework alignment, and risk scoring to support informed security decisions.

Ideal users include security operations centers (SOCs), compliance teams, penetration testers, application security engineers, and organizations undergoing regulatory audits or security certifications.

## Usage

### Sample Request

```json
{
  "url": "https://example.com"
}
```

### Sample Response

```json
{
  "url": "https://example.com",
  "security_score": 78,
  "compliance_status": "PARTIAL",
  "vulnerabilities": [
    {
      "type": "Missing Security Header",
      "severity": "High",
      "header": "Strict-Transport-Security",
      "remediation": "Add HSTS header with max-age of at least 31536000 seconds"
    }
  ],
  "compliance_frameworks": {
    "PCI-DSS": "Non-Compliant",
    "OWASP": "Compliant",
    "GDPR": "Partial"
  },
  "risk_level": "Medium",
  "assessment_timestamp": "2024-01-15T10:30:45Z"
}
```

## Endpoints

### Security Check

**Method:** `POST`

**Path:** `/security-check`

**Description:** Performs a comprehensive security check and compliance risk assessment on a specified URL. Analyzes the target website for common vulnerabilities, security headers, compliance violations, and generates a risk assessment report.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | string | Yes | The complete URL of the website or application to assess (must include protocol, e.g., `https://example.com`) |

**Response (200 - Success):**

Returns a JSON object containing:
- `url`: The assessed URL
- `security_score`: Numeric score (0-100) indicating overall security posture
- `compliance_status`: Status of compliance (Compliant, Partial, Non-Compliant)
- `vulnerabilities`: Array of identified vulnerabilities with severity and remediation guidance
- `compliance_frameworks`: Assessment against industry standards (PCI-DSS, OWASP, GDPR, etc.)
- `risk_level`: Overall risk classification (Low, Medium, High, Critical)
- `assessment_timestamp`: ISO 8601 timestamp of assessment execution

**Response (422 - Validation Error):**

Returns validation error details including:
- `detail`: Array of validation errors with location, message, and error type

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

- **Kong Route:** https://api.mkkpro.com/compliance/risk-assessment
- **API Docs:** https://api.mkkpro.com:8014/docs
