# TrendAI Vision One Threat Intelligence API Reference

**Important:** All paths use lowercase `threatintel` (not `threatIntel`).

## Authentication

All requests require a Bearer token in the Authorization header:
```
Authorization: Bearer <VISION_ONE_API_KEY>
Content-Type: application/json;charset=utf-8
```

## Base URLs by Region

| Region | Base URL |
|--------|----------|
| us | https://api.xdr.trendmicro.com |
| eu | https://api.eu.xdr.trendmicro.com |
| jp | https://api.xdr.trendmicro.co.jp |
| sg | https://api.sg.xdr.trendmicro.com |
| au | https://api.au.xdr.trendmicro.com |
| in | https://api.in.xdr.trendmicro.com |
| mea | https://api.mea.xdr.trendmicro.com |

## Endpoints

### GET /v3.0/threatintel/feedIndicators

List threat intelligence feed indicators as STIX 2.1 bundles.

**Query Parameters:**
- `startDateTime` (string, ISO 8601) — Filter start date
- `endDateTime` (string, ISO 8601) — Filter end date
- `top` (integer) — Number of records per page (supported)
- `skipToken` (string) — Pagination continuation token

**Response:** STIX bundle format:
```json
{ "bundle": { "type": "bundle", "objects": [...] }, "nextLink": "..." }
```

**Note:** The `nextLink` URL includes additional required params (`indicatorObjectFormat`, etc.) that must be preserved when paginating.

### GET /v3.0/threatintel/feeds

List intelligence reports as STIX 2.1 report objects.

**Query Parameters:**
- `skipToken` (string) — Pagination token (from nextLink)

**Does NOT support:** `top` parameter (returns 400 if included)

**Response:** STIX bundle format (same as feedIndicators). Each page returns ~100 report objects. The `nextLink` URL includes required params like `topReport`, `responseObjectFormat`, `startDateTime`, `endDateTime`.

### GET /v3.0/threatintel/feeds/filterDefinition

Retrieve allowed filter values for location and industry.

**Response:**
```json
{
  "location": ["Afghanistan", "Albania", ..., "Zimbabwe"],
  "industry": ["Aerospace", "Agriculture", ..., "Utilities"]
}
```

### GET /v3.0/threatintel/suspiciousObjects

List suspicious objects (block/allow list). Uses standard `items[]` format.

**Query Parameters:**
- `top` (integer) — Records per page
- `skipToken` (string) — Pagination token

**Response:**
```json
{ "items": [...], "nextLink": "..." }
```

**Note:** The value field name in each object matches the `type` field (e.g., a `fileSha256` type has a `fileSha256` field containing the hash value, not a generic `value` field).

### POST /v3.0/threatintel/suspiciousObjects

Add objects to the suspicious objects list.

**Request Body:** Array of objects:
```json
[
  {
    "type": "domain",
    "value": "evil.com",
    "scanAction": "block",
    "riskLevel": "high",
    "description": "Optional description",
    "expiredDateTime": "2025-12-31T23:59:59Z"
  }
]
```

**Supported types:** ip, domain, url, fileSha1, fileSha256, senderMailAddress
**Scan actions:** block, log
**Risk levels:** high, medium, low

### POST /v3.0/threatintel/suspiciousObjects/delete

Remove objects from the suspicious objects list.

### GET /v3.0/threatintel/suspiciousObjectExceptions

List exception list items.

### POST /v3.0/threatintel/suspiciousObjectExceptions

Add items to exception list.

## Rate Limits

- Rate limited per 60-second window (exact limits vary by endpoint)
- HTTP 429 response when exceeded
- Maximum request body: 1 MB (HTTP 413 if exceeded)
- Request timeout: 60 seconds (HTTP 504 if exceeded)

## Pagination

Two response formats:
- **STIX endpoints** (feedIndicators, feeds): `bundle.objects[]` with `nextLink` at top level
- **Standard endpoints** (suspiciousObjects): `items[]` with `nextLink` at top level

When following `nextLink`, use ALL query params from the URL (not just skipToken) — the server includes required params like `responseObjectFormat` in the link.
