---
name: verfi
description: TCPA consent verification for lead generation. Use when adding consent capture to web forms, verifying lead consent before contact, claiming/managing consent sessions, pulling proof for disputed leads, or integrating with the Verfi API. Covers SDK installation, API authentication, session lifecycle (create → claim → verify → proof), and compliance workflows.
---

# Verfi — Consent Verification for Lead Gen

Verfi captures verifiable proof of consumer consent. Publishers add a script tag to capture sessions; buyers verify consent via API before contacting leads.

## When to Use This Skill

- Adding consent capture to a web form
- Checking if a lead has valid TCPA consent
- Claiming sessions for long-term retention
- Pulling machine-readable proof for disputes
- Integrating Verfi into an existing lead gen pipeline

## Quick Start

### 1. Capture Consent (Publisher)

Add the SDK to any page with a form:

```html
<script src="https://sdk.verfi.io/v1/verfi.js" data-key="pk_YOUR_PUBLIC_KEY" async></script>
```

The SDK auto-detects forms, records interactions (mouse, clicks, keystrokes, scroll), and generates a Verfi ID (`VF-xxxxxxxx`) on form submission.

### 2. Verify Consent (Buyer)

```bash
curl -H "Authorization: Bearer sk_YOUR_SECRET_KEY" \
  https://api.verfi.io/tenant/v1/sessions/VF-a1b2c3d4/proof
```

Returns consent status, interaction metrics, form data, device info, and tamper verification. All PII is SHA-256 hashed.

### 3. Claim Session

```bash
curl -X POST -H "Authorization: Bearer sk_YOUR_SECRET_KEY" \
  https://api.verfi.io/tenant/v1/sessions/VF-a1b2c3d4/claim
```

Starts 3-year retention. Unclaimed sessions expire in 72 hours.

## Authentication

Two key types:

| Key | Format | Use |
|-----|--------|-----|
| Public | `pk_...` | SDK script tag (client-side) |
| Secret | `sk_...` | API calls (server-side, Bearer token) |

Secret keys have scopes: `sessions:claim`, `sessions:unclaim`, `sessions:search`, `sessions:proof`, `sessions:expiration`.

Generate keys in the [Verfi dashboard](https://app.verfi.io) under Integration > API Keys.

## API Endpoints

Base URL: `https://api.verfi.io/tenant/v1`

All endpoints require `Authorization: Bearer sk_...` header.

| Method | Path | Scope | Description |
|--------|------|-------|-------------|
| GET | `/sessions` | — | List claimed sessions (paginated) |
| GET | `/sessions/{verfiID}` | `sessions:search` | Look up session, verify PII hashes |
| GET | `/sessions/{verfiID}/proof` | `sessions:proof` | Machine-readable proof data |
| POST | `/sessions/{verfiID}/claim` | `sessions:claim` | Claim session (3-year retention) |
| POST | `/sessions/{verfiID}/unclaim` | `sessions:unclaim` | Release session (30-day retention) |
| PUT | `/sessions/{verfiID}/expiration` | `sessions:expiration` | Update expiration date |

Full API reference: see [references/api-reference.md](references/api-reference.md)

## Common Workflows

### Publisher: Add Consent Capture to a Form

1. Get a public API key from the Verfi dashboard
2. Add the SDK script tag to the page (before `</body>`)
3. The SDK auto-records sessions — no form modifications needed
4. Each form submission creates a session with a unique Verfi ID
5. Pass the Verfi ID alongside the lead data to buyers

### Buyer: Verify and Claim a Lead

1. Receive lead with Verfi ID from publisher
2. Call `GET /sessions/{verfiID}/proof` to check consent
3. Verify `consent.given === true` and `consent.tcpa_compliant === true`
4. Optionally verify PII binding with `GET /sessions/{verfiID}?email={hash}&phone={hash}`
5. Call `POST /sessions/{verfiID}/claim` to start retention
6. Contact the consumer with documented consent proof

### Dispute: Pull Proof for a Challenged Lead

1. Look up the Verfi ID associated with the disputed lead
2. Call `GET /sessions/{verfiID}/proof` for machine-readable proof
3. Proof includes: consent language, interaction timeline, form data, device info, tamper detection
4. Share the `proof_url` for a human-readable proof page
5. Integrity hash verifies the proof hasn't been tampered with

### Audit: Bulk Verify Consent Across a Lead List

1. Call `GET /sessions` to list all claimed sessions
2. For each session, call `GET /sessions/{verfiID}/proof`
3. Flag sessions where `consent.given === false` or `verification.tamper_detected === true`
4. Unclaim any sessions that don't meet compliance requirements

## MCP Server

For MCP-compatible agents (Claude Desktop, Cursor, Windsurf):

```json
{
  "mcpServers": {
    "verfi": {
      "command": "npx",
      "args": ["-y", "@verfi/mcp-server"],
      "env": { "VERFI_API_KEY": "sk_..." }
    }
  }
}
```

## OpenAPI Spec

Auto-discoverable at: `https://api.verfi.io/.well-known/openapi.json`

Compatible with OpenAI GPT Actions, LangChain, CrewAI, and any framework that generates tools from OpenAPI specs.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| SDK not recording sessions | Check public key is correct, script loads without errors |
| 401 Unauthorized | Verify secret key, check `Authorization: Bearer sk_...` format |
| 403 Insufficient permissions | API key missing required scope — update in dashboard |
| Session not claimable (409) | Session already claimed or status isn't "recorded" |
| Proof shows `consent.given: false` | Form may not have consent language/checkbox detected by SDK |
