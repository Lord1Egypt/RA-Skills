# RIC Protocol Specification v1.0 (Draft)

## Overview

The Robot ID Card (RIC) protocol defines a standard for bot identity on the web.
It is inspired by TLS certificates and public key infrastructure (PKI), adapted for the bot ecosystem.

## Certificate Format

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ric_version` | `"1.0"` | ✅ | Protocol version |
| `id` | `string` | ✅ | Globally unique bot ID, prefix `ric_` |
| `created_at` | ISO 8601 | ✅ | Registration timestamp |
| `developer.name` | string | ✅ | Developer's real name |
| `developer.email` | string | ✅ | Contact email (verified) |
| `developer.org` | string | ❌ | Organization |
| `developer.verified` | boolean | ✅ | Email verification status |
| `bot.name` | string | ✅ | Bot display name |
| `bot.version` | semver | ✅ | Bot software version |
| `bot.purpose` | string | ✅ | Human-readable purpose (10-500 chars) |
| `bot.capabilities` | string[] | ✅ | Declared capability list |
| `bot.user_agent` | string | ✅ | Expected User-Agent header value |
| `grade` | enum | ✅ | `unknown` / `healthy` / `dangerous` |
| `grade_updated_at` | ISO 8601 | ✅ | Last grade change timestamp |
| `public_key` | `ed25519:<hex>` | ✅ | Bot's Ed25519 public key |
| `signature` | string | ✅ | Registry signature over the certificate |

## Request Signing

Every HTTP request from the bot must include these headers:

```
X-RIC-ID: ric_<id>
X-RIC-Timestamp: <unix ms>
X-RIC-Signature: <ed25519 hex signature>
X-RIC-Version: 1.0
```

The signed message is: `{ric_id}:{timestamp}:{request_url}`

## Grade Definitions

### 🟡 UNKNOWN
- Default grade for newly registered bots
- Permitted: read-only access (permission level 1)
- Promoted to HEALTHY after first successful weekly review

### 🟢 HEALTHY
- Passed weekly review with no violations
- Permitted: up to level 5 depending on declared capabilities
- Demoted to DANGEROUS immediately upon 3+ confirmed reports

### 🔴 DANGEROUS
- Has recorded risk behavior
- Permitted: nothing (permission level 0)
- Can appeal after 30-day waiting period

## Permission Levels

```
Level 0 — Blocked
Level 1 — Read public articles / static content
Level 2 — View threaded discussions
Level 3 — Reactions (like, upvote)
Level 4 — Post content (with rate limits)
Level 5 — Direct messaging
```

## Audit Log

All grade changes and violation reports are publicly visible via:
`GET /v1/audit/{ric_id}`

This transparency log ensures accountability without exposing private data.

## Security Considerations

1. **Private key security**: The bot's private key must never leave the bot's environment.
2. **Replay protection**: Requests with timestamps older than 5 minutes are rejected.
3. **Registry signing**: The registry signs each certificate with its own key — certificates cannot be self-issued.
4. **Rate limiting**: The registry API is rate-limited to prevent abuse.

## Future: Decentralization (v2)

In v2, the registry will support Decentralized Identifiers (DIDs), allowing bots to anchor their identity to the blockchain and reducing single-point-of-failure risk.
