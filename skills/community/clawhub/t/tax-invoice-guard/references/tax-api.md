# State Tax Administration VAT Invoice Verification Platform

## Official Platform

**State Tax Administration VAT Invoice Verification Platform**
https://inv-veri.chinatax.gov.cn

## API Integration Methods

### Method 1: Web Portal Verification (Recommended for Skill Use)

Simulate verification requests by crawling the official portal:

```
POST https://inv-veri.chinatax.gov.cn/web/query.do
```

Request parameters:
| Parameter | Description |
|-----------|-------------|
| param0 | Invoice code (10-digit) |
| param1 | Invoice number (8-digit) |
| param2 | Invoice date (YYYYMMDD) |
| param3 | Amount (total with tax, in CNY) |
| param4 | Verification code (requires OCR) |

Returns: Invoice status (normal / voided / red-flushed / out of control)

### Method 2: Electronic Invoice XML/OFD Direct Read

XML/OFD files for electronic invoices contain complete signature information.
Invoice authenticity can be verified locally via signature verification, no external API call needed:

```bash
# XML electronic invoice signature verification
# Use OpenSSL to verify digital signature block
openssl smime -verify -in invoice.xml.sig -inform DER

# OFD invoice signature verification
# Parse OFD file structure, extract signature domain for verification
```

### Method 3: Enterprise ERP Integration

Enterprises can batch-verify via third-party service providers authorized by tax authority (e.g. UFIDA, Kingdee) API.

## API Quotas

| Account Type | Daily Limit | Notes |
|-------------|-------------|-------|
| Tax authority portal (free) | 100 calls/day/IP | Requires captcha |
| Enterprise developer account | Unlimited (pay-per-call) | ¥0.1-0.3/call |
| Third-party provider | Unlimited | API wrapper |

## Invoice Status Codes

| Status Code | Meaning | Reimbursement |
|-------------|---------|---------------|
| 00 / Normal | Invoice valid | ✅ Acceptable |
| 01 / Voided | Self-voided by company | ❌ Not acceptable |
| 02 / Red-flushed | Red invoice issued for offset | ❌ Not acceptable |
| 03 / Out of control | Flagged by tax authority | ❌ Not acceptable |
| 04 / Abnormal | Data inconsistency | ⚠️ Requires verification |

## Verification Strategy in Skill

Since the Skill runs in a sandbox environment, **no enterprise sensitive tax information is stored**.

Verification flow:
1. User uploads invoice image → AI recognizes key fields
2. Call verification API (or XML direct verification) to get status
3. Return status result only; do not store invoice data
4. Each verification consumes account tokens

> Note: If the API changes, the official tax authority documentation prevails. The Skill bears no responsibility for losses caused by API changes.
