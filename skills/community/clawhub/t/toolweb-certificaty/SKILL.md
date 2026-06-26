---
name: Certificaty
description: Generate, manage, and download SSL/TLS certificates with token-based verification and multi-domain support.
---

# Overview

Certificaty is a certificate management API that streamlines the provisioning and lifecycle management of SSL/TLS certificates for web domains. Built for DevOps teams, security engineers, and automation platforms, it provides a secure, token-based workflow for generating certificates, verifying domain ownership, and downloading certificate files.

The API supports single and multi-domain certificate types, integrates with email-based verification flows, and maintains an audit trail of all certificate operations. It is ideal for organizations managing multiple domains, automated infrastructure deployments, and enterprises requiring compliance-ready certificate management.

Key capabilities include token generation for certificate orders, domain verification, certificate generation with configurable types, and direct file downloads for deployment across infrastructure.

# Usage

## Generate a Token for Certificate Order

```json
{
  "email": "admin@example.com",
  "domain": "example.com",
  "cert_type": "single"
}
```

**Response:**

```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "message": "Token generated successfully for domain verification"
}
```

## Generate a Certificate

```json
{
  "domain": "example.com",
  "order_id": "ORD-20240115-001",
  "cert_type": "single"
}
```

**Response:**

```json
{
  "status": "success",
  "certificate_id": "CERT-20240115-001",
  "domain": "example.com",
  "issued_at": "2024-01-15T10:30:00Z",
  "expires_at": "2025-01-15T10:30:00Z",
  "download_url": "/download/example.com/certificate.crt",
  "message": "Certificate generated successfully"
}
```

# Endpoints

## GET /

**Summary:** Root

**Description:** Returns API metadata and service information.

**Parameters:** None

**Response:** JSON object with API details.

---

## GET /status

**Summary:** Status

**Description:** Returns the operational status of the Certificaty service.

**Parameters:** None

**Response:** JSON object indicating service health and availability.

---

## GET /certificates

**Summary:** Certificates

**Description:** Retrieves a list of all certificates managed by the service.

**Parameters:** None

**Response:** JSON array of certificate objects with metadata.

---

## POST /generate-token

**Summary:** Generate Token

**Description:** Creates a verification token for initiating a certificate order. Required before certificate generation.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| email | string (email) | ✓ | Email address for certificate order notifications and verification |
| domain | string | ✗ | Single domain for certificate (use for single-domain certificates) |
| domains | array of strings | ✗ | Multiple domains for certificate (use for multi-domain or wildcard certificates) |
| cert_type | string | ✗ | Certificate type: `single` (default), `multi`, or `wildcard` |

**Request Body:**

```json
{
  "email": "admin@example.com",
  "domain": "example.com",
  "cert_type": "single"
}
```

**Response (200):**

```json
{
  "token": "string",
  "expires_in": "integer",
  "status": "success"
}
```

**Response (422):** Validation error with field-level details.

---

## POST /generate-certificate

**Summary:** Generate Certificate

**Description:** Generates an SSL/TLS certificate for a verified domain using a valid order ID.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| domain | string | ✓ | Domain name for which to generate the certificate |
| order_id | string | ✓ | Unique order identifier returned from token generation or order system |
| cert_type | string | ✗ | Certificate type: `single` (default), `multi`, or `wildcard` |

**Request Body:**

```json
{
  "domain": "example.com",
  "order_id": "ORD-20240115-001",
  "cert_type": "single"
}
```

**Response (200):**

```json
{
  "certificate_id": "string",
  "domain": "string",
  "issued_at": "string (ISO 8601)",
  "expires_at": "string (ISO 8601)",
  "status": "success"
}
```

**Response (422):** Validation error with field-level details.

---

## GET /download/{domain}/{filename}

**Summary:** Download Certificate

**Description:** Downloads a generated certificate file in PEM, CRT, or KEY format.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| domain | string | ✓ | Domain name associated with the certificate |
| filename | string | ✓ | Name of the file to download (e.g., `certificate.crt`, `private.key`) |

**Response (200):** Binary file download (certificate or key file).

**Response (422):** Validation error with field-level details.

---

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

- **Kong Route:** https://api.toolweb.in/tools/certificaty
- **API Docs:** https://api.toolweb.in:8164/docs
