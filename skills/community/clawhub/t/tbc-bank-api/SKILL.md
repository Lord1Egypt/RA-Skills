---
name: tbc-bank-api
description: Use when the user mentions TBC Bank, tbcbank.ge, Georgian bank APIs, PSD2 integration with TBC, account information services (AIS), payment initiation (PIS) with TBC, TPay gateway, TBC installments, or any work involving TBC Bank developer APIs. Trigger even if they just say "TBC" in a banking context.
license: MIT
---

# TBC Bank API Integration Guide

Full reference for building integrations with TBC Bank's Open Banking, PSD2, and payment APIs.

## Quick Reference

| Topic | Reference File |
|-------|---------------|
| OAuth2 & Authentication | `references/auth.md` |
| Account Information Services (AIS) | `references/ais.md` |
| Payment Initiation Services (PIS) | `references/pis.md` |
| Consents & SCA | `references/consent.md` |
| Online Installments | `references/installments.md` |
| TPay Gateway | `references/tpay.md` |

## Base URLs

| Environment | Base URL |
|-------------|----------|
| Sandbox | `https://test-api.tbcbank.ge` |
| Dev OpenBanking | `https://dev-openbanking.tbcbank.ge` |
| Production | `https://api.tbcbank.ge` |
| OpenBanking | `https://openbanking.tbcbank.ge` |

**API path prefix:** `/0.8/v1/` (PSD2) or `/v1/`, `/v2/` for non-PSD2

## Universal Headers

Every request must include:

```http
Authorization: Bearer {access_token}
Content-Type: application/json
X-Request-ID: {uuid4}          # Unique per request
PSU-IP-Address: {user_ip}      # End-user's IP address
```

For signed requests (TPP operations) also include:
```http
Digest: SHA-256={base64_body_hash}
Signature: keyId="{cert_serial}",algorithm="rsa-sha256",headers="...",signature="..."
```

## Common Error Response

```json
{
  "code": "string",
  "type": "https://...",
  "title": "Error summary",
  "status": 400,
  "detail": "Detailed description",
  "traceId": "abc123"
}
```

## Key Workflows

### 1. Account Data Access (AIS)
1. Create consent → get `consentId`
2. Redirect user for SCA authorization
3. Exchange auth code for token with consent scope
4. Call account/balance/transaction endpoints

→ Read `references/consent.md` then `references/ais.md`

### 2. Payment Initiation (PIS)
1. Initiate payment → get `paymentId` + `_links`
2. Start authorization via redirect or OAuth SCA
3. Poll or use webhook for payment status

→ Read `references/pis.md`

### 3. OAuth2 Setup
→ Read `references/auth.md` first — needed by all other flows

### 4. Installment Loans
→ Read `references/installments.md`

### 5. TPay Gateway
→ Read `references/tpay.md`

## Response Conventions

- All monetary amounts are **strings** (e.g., `"amount": "30.00"`)
- Dates use **ISO 8601** (`2023-07-01`, `2025-03-26T00:00:00`)
- HATEOAS `_links` pattern — always follow links from responses, don't hardcode paths
- `transactionStatus` codes: `RCVD` (received), `ACTC` (accepted technical), `ACSP` (accepted settlement in progress), `ACCC` (accepted credit complete), `RJCT` (rejected)
- `scaStatus` codes: `received`, `psuIdentified`, `psuAuthenticated`, `scaMethodSelected`, `finalised`, `failed`
