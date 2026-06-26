---
name: Suspicious File Scanner
description: Analyzes uploaded files to detect suspicious characteristics and potential security threats.
---

# Overview

The Suspicious File Scanner is a security-focused API that analyzes files to identify potentially malicious or suspicious characteristics. By leveraging advanced threat detection techniques, this tool helps organizations screen files before they enter their systems, reducing the risk of malware infections, ransomware, and other file-based attacks.

This API is ideal for security teams, developers building defense-in-depth solutions, and organizations that need automated file validation as part of their security workflows. Whether you're protecting email gateways, web upload portals, or endpoint systems, the Suspicious File Scanner provides rapid threat assessment to complement your existing security infrastructure.

The tool processes files through multiple detection heuristics and returns comprehensive analysis results, enabling you to make informed decisions about file acceptance or quarantine. Integration is straightforward via multipart file uploads, making it easy to embed file scanning into existing applications.

## Usage

**Scan a file for suspicious characteristics:**

```json
POST /scan-file
Content-Type: multipart/form-data

file: [binary file data]
```

**Sample Request:**

Upload a file using multipart form data. Most HTTP clients handle this automatically:

```bash
curl -X POST \
  -F "file=@/path/to/sample.exe" \
  https://api.mkkpro.com/security/suspicious-file-scanner/scan-file
```

**Sample Response:**

```json
{
  "filename": "sample.exe",
  "file_size": 245760,
  "file_type": "application/x-msdownload",
  "scan_timestamp": "2024-01-15T10:32:45Z",
  "threat_detected": true,
  "threat_level": "high",
  "threat_indicators": [
    {
      "indicator": "executable_packed",
      "description": "File appears to be packed or obfuscated",
      "confidence": 0.95
    },
    {
      "indicator": "suspicious_imports",
      "description": "Contains suspicious Windows API imports",
      "confidence": 0.87
    }
  ],
  "recommendation": "quarantine"
}
```

## Endpoints

### POST /scan-file

**Description:** Scans an uploaded file for suspicious characteristics and potential threats.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | binary | Yes | The file to scan. Accepts any file type. Submit as multipart form-data. |

**Response Schema (200 OK):**

The response contains detailed analysis results for the scanned file:

```json
{
  "filename": "string",
  "file_size": "integer",
  "file_type": "string",
  "scan_timestamp": "string (ISO 8601)",
  "threat_detected": "boolean",
  "threat_level": "string (low, medium, high, critical)",
  "threat_indicators": [
    {
      "indicator": "string",
      "description": "string",
      "confidence": "number (0.0-1.0)"
    }
  ],
  "recommendation": "string (allow, review, quarantine)"
}
```

**Error Response (422 Validation Error):**

```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "Field required",
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

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/security/suspicious-file-scanner
- **API Docs:** https://api.mkkpro.com:8013/docs
