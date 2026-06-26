---
name: Simple SSL Certificate Manager
description: Automate SSL certificate generation and management with DNS challenge validation and certificate provisioning.
---

# Overview

Simple SSL Certificate Manager is a streamlined API for automating SSL/TLS certificate lifecycle management. Built for security professionals and DevOps teams, it enables DNS-based domain validation, certificate generation via industry-standard protocols, and secure certificate delivery. The platform handles the complexity of certificate provisioning, allowing you to focus on securing your infrastructure.

This tool is ideal for organizations managing multiple domains, implementing Infrastructure-as-Code practices, or automating certificate renewals across distributed systems. With support for staging environments and flexible email validation, it accommodates both development and production workflows.

The API follows a two-step workflow: first generate DNS challenge records for domain ownership verification, then request certificate generation after DNS records are confirmed in place. Built-in debugging capabilities help troubleshoot DNS configuration issues.

## Usage

### DNS Challenge Generation

First, generate DNS challenge data for domain validation:

```json
POST /dns-challenge
Content-Type: application/json

{
  "domain": "example.com",
  "email": "admin@example.com"
}
```

**Sample Response:**

```json
{
  "domain": "example.com",
  "challenge_token": "abc123xyz789",
  "dns_record_type": "TXT",
  "dns_record_name": "_acme-challenge.example.com",
  "dns_record_value": "abc123xyz789_validation_string",
  "challenge_expires_at": "2025-01-15T14:30:00Z"
}
```

### Certificate Generation

After DNS records are in place, request certificate generation:

```json
POST /generate-certificate
Content-Type: application/json

{
  "domain": "example.com",
  "email": "admin@example.com",
  "confirmed": true,
  "staging": false
}
```

**Sample Response:**

```json
{
  "certificate_id": "cert_67890abcde",
  "domain": "example.com",
  "status": "issued",
  "issued_at": "2025-01-15T14:35:00Z",
  "expires_at": "2026-01-15T14:35:00Z",
  "certificate_name": "example_com_2025",
  "download_url": "/download/example_com_2025/certificate.pem"
}
```

### Debug DNS Configuration

Verify DNS setup before certificate generation:

```
GET /debug/example.com
```

**Sample Response:**

```json
{
  "domain": "example.com",
  "dns_records": [
    {
      "name": "_acme-challenge.example.com",
      "type": "TXT",
      "value": "abc123xyz789_validation_string",
      "status": "verified",
      "ttl": 300
    }
  ],
  "validation_status": "success",
  "checked_at": "2025-01-15T14:33:00Z"
}
```

## Endpoints

### GET /

**Summary:** Root  
**Description:** API information and status endpoint.

**Parameters:** None

**Response:** Empty JSON object confirming API availability.

---

### GET /health

**Summary:** Health Check  
**Description:** Verify API service health and readiness.

**Parameters:** None

**Response:** Health status confirmation.

---

### POST /dns-challenge

**Summary:** Create DNS Challenge  
**Description:** Generate DNS challenge data for manual domain ownership verification.

**Parameters:**
- `domain` (string, required): The domain name to validate (e.g., `example.com`)
- `email` (string, email format, required): Contact email for certificate issuance

**Response Shape:**
```
{
  "domain": string,
  "challenge_token": string,
  "dns_record_type": string,
  "dns_record_name": string,
  "dns_record_value": string,
  "challenge_expires_at": string (ISO 8601 datetime)
}
```

---

### POST /generate-certificate

**Summary:** Generate Certificate  
**Description:** Generate SSL certificate after DNS verification is confirmed.

**Parameters:**
- `domain` (string, required): The domain name for certificate issuance
- `email` (string, email format, required): Contact email for the certificate
- `confirmed` (boolean, optional, default: false): Set to `true` after DNS records are verified
- `staging` (boolean, optional, default: false): Use staging certificates for testing

**Response Shape:**
```
{
  "certificate_id": string,
  "domain": string,
  "status": string,
  "issued_at": string (ISO 8601 datetime),
  "expires_at": string (ISO 8601 datetime),
  "certificate_name": string,
  "download_url": string
}
```

---

### GET /download/{cert_name}/{filename}

**Summary:** Download Certificate  
**Description:** Download generated certificate files (PEM, key, chain).

**Parameters:**
- `cert_name` (string, required): Certificate identifier (from generation response)
- `filename` (string, required): File to download (`certificate.pem`, `private.key`, or `chain.pem`)

**Response:** Binary certificate file content or JSON error.

---

### GET /debug/{domain}

**Summary:** Debug Domain  
**Description:** Inspect DNS configuration and validation status for a domain.

**Parameters:**
- `domain` (string, required): Domain name to debug (e.g., `example.com`)

**Response Shape:**
```
{
  "domain": string,
  "dns_records": [
    {
      "name": string,
      "type": string,
      "value": string,
      "status": string,
      "ttl": integer
    }
  ],
  "validation_status": string,
  "checked_at": string (ISO 8601 datetime)
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

- **Kong Route:** https://api.mkkpro.com/security/ssl-certificate-manager
- **API Docs:** https://api.mkkpro.com:8044/docs
