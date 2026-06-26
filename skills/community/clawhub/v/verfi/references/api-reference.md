# Verfi API Reference

Base URL: `https://api.verfi.io/tenant/v1`

All requests require: `Authorization: Bearer sk_YOUR_SECRET_KEY`

## GET /sessions

List claimed sessions (paginated).

**Query Parameters:**
- `page` (int, default 1)
- `limit` (int, 1-100, default 20)
- `status` (string): `claimed`, `unclaimed`, `recorded`, `expired`

**Response:**
```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "verfiID": "VF-a1b2c3d4",
        "status": "claimed",
        "createdAt": "2026-01-15T10:30:00Z",
        "claimedAt": "2026-01-15T12:00:00Z",
        "expirationDate": "2029-01-15T12:00:00Z",
        "piiDetected": true
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalCount": 92,
      "limit": 20,
      "hasNextPage": true,
      "hasPrevPage": false
    }
  }
}
```

## GET /sessions/{verfiID}

Look up a session. Cross-tenant (any tenant can search any session). Requires `sessions:search` scope.

**Path:** `verfiID` — format `VF-xxxxxxxx` or full proof URL

**Query Parameters:**
- `email` (string): SHA-256 hash of email to verify
- `phone` (string): SHA-256 hash of phone to verify

**Response:**
```json
{
  "success": true,
  "data": {
    "verfiID": "VF-a1b2c3d4",
    "found": true,
    "status": "claimed",
    "originatingTenantId": "...",
    "claimingTenantId": "...",
    "createdAt": "2026-01-15T10:30:00Z",
    "claimedAt": "2026-01-15T12:00:00Z",
    "expirationDate": "2029-01-15T12:00:00Z",
    "piiDetected": true,
    "verification": {
      "consentRules": true,
      "emailMatch": true,
      "phoneMatch": null
    }
  }
}
```

## GET /sessions/{verfiID}/proof

Machine-readable proof. Requires `sessions:proof` scope. All PII is SHA-256 hashed.

**Response:**
```json
{
  "success": true,
  "data": {
    "verfiID": "VF-a1b2c3d4",
    "status": "claimed",
    "consent": {
      "given": true,
      "language": "By submitting this form, I consent to...",
      "tcpa_compliant": true,
      "one_to_one": true
    },
    "session": {
      "created_at": "2026-01-15T10:30:00Z",
      "duration_ms": 45200,
      "page_url": "https://example.com/quote",
      "referrer": "https://google.com"
    },
    "interactions": {
      "total_events": 234,
      "mouse_movements": 89,
      "clicks": 12,
      "scroll_events": 8,
      "form_interactions": 15,
      "keystroke_count": 142,
      "time_to_first_interaction_ms": 1200,
      "time_to_submit_ms": 45200
    },
    "form_data": {
      "fields_filled": ["email", "phone", "name", "zip"],
      "checkboxes_checked": 1,
      "consent_checkbox_interacted": true
    },
    "device": {
      "ip_hash": "037312f1...",
      "user_agent": "Mozilla/5.0 ...",
      "screen_resolution": "1920x1080",
      "platform": "Win32",
      "timezone": "America/New_York"
    },
    "pii_binding": {
      "method": "hash",
      "fields_bound": ["email", "phone"],
      "hash": "acc09418..."
    },
    "proof_url": "https://proof.verfi.io/VF-a1b2c3d4?token=...",
    "verification": {
      "integrity": "f9872e02...",
      "tamper_detected": false
    }
  }
}
```

## POST /sessions/{verfiID}/claim

Claim a session. Requires `sessions:claim` scope.

**Request Body (optional):**
```json
{
  "expirationDate": "2028-06-15T00:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "verfiID": "VF-a1b2c3d4",
    "status": "claimed",
    "claimingTenantId": "...",
    "claimedAt": "2026-01-15T12:00:00Z",
    "expirationDate": "2029-01-15T12:00:00Z"
  }
}
```

**Errors:** 404 (not found), 409 (already claimed or not in "recorded" status), 403 (free tier limit)

## POST /sessions/{verfiID}/unclaim

Release a claimed session. Only the claiming tenant can unclaim. Requires `sessions:unclaim` scope.

**Response:**
```json
{
  "success": true,
  "data": {
    "verfiID": "VF-a1b2c3d4",
    "status": "unclaimed",
    "unclaimedAt": "2026-02-01T09:00:00Z"
  }
}
```

**Errors:** 403 (not your session), 409 (not claimed)

## PUT /sessions/{verfiID}/expiration

Update expiration. Must be 30+ days from now, max 5 years from claim. Rate limited: 3/month per session, 24h cooldown. Requires `sessions:expiration` scope.

**Request Body:**
```json
{
  "expirationDate": "2028-06-15T00:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "verfiID": "VF-a1b2c3d4",
  "expirationDate": "2028-06-15T00:00:00Z",
  "rateLimitInfo": {
    "updatesRemaining": 2,
    "nextUpdateAllowed": "2026-01-16T12:00:00Z",
    "monthlyResetDate": "2026-02-01T00:00:00Z"
  }
}
```

**Errors:** 400 (too soon / exceeds max), 429 (rate limited)

## Error Format

All errors return:
```json
{
  "error": "Short error name",
  "details": "Human-readable explanation"
}
```
