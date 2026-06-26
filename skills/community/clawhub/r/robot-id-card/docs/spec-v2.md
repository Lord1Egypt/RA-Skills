# RIC Protocol Specification v2.0

> Aligned with **RFC 9421 HTTP Message Signatures** (IETF, Feb 2024)  
> and **Cloudflare Web Bot Auth** / IETF `draft-meunier-web-bot-auth-architecture`

---

## What Changed from v1.0

| Aspect | v1.0 (legacy) | v2.0 (this spec) |
|--------|--------------|-----------------|
| Header format | Custom `X-RIC-*` | Standard `Signature` + `Signature-Input` + `Signature-Agent` (RFC 9421) |
| Signature encoding | Hex | Base64 (RFC 9421 standard) |
| Timestamp unit | Unix milliseconds | Unix **seconds** (RFC 9421) |
| Replay protection | 5-min time window only | Time window **+** nonce uniqueness |
| Bot tag | n/a | `tag="web-bot-auth"` for ecosystem compatibility |
| Public key discovery | Registry lookup only | `/.well-known/http-message-signatures-directory` (JWKS, RFC 8037) |
| Signed components | `{id}:{ts}:{url}` string | RFC 9421 signature base: `@authority`, `@method`, `@path` |

v1.0 `X-RIC-*` headers are still accepted but return a `deprecation_notice` in the response.

---

## Request Headers (v2.0)

Every HTTP request from a bot must carry these three headers:

```
Signature-Input: ric=("@authority" "@method" "@path");keyid="ric_a3f8c2d1_xyz12345";created=1718000000;expires=1718000300;nonce="Zmxhbmd4MTIz";tag="web-bot-auth"
Signature:       ric=:HIbjHC5rS0BKbgTHA...base64...==:
Signature-Agent: "ResearchBot"; cert="https://registry.robotidcard.dev/v1/bots/ric_a3f8c2d1_xyz12345"
```

### Signature-Input fields

| Field | Required | Description |
|-------|----------|-------------|
| Component list | ✅ | Signed HTTP components: at minimum `"@authority"` |
| `keyid` | ✅ | The bot's RIC ID (`ric_<fp8>_<rand8>`) |
| `created` | ✅ | Signature creation time (Unix seconds) |
| `expires` | Recommended | Expiry time (Unix seconds). Recommended: `created + 300` |
| `nonce` | Recommended | Base64url-encoded random bytes (16+ bytes). Prevents replay attacks |
| `tag` | Recommended | Must be `"web-bot-auth"` for Web Bot Auth ecosystem compatibility |

### Signature-Agent format

```
"<bot display name>"; cert="<certificate URL>"
```

---

## Signature Base Construction

The signature base is the canonical string that is signed with Ed25519.  
It follows RFC 9421 §2.5:

```
"@authority": example.com
"@method": GET
"@path": /api/articles
"@signature-params": ("@authority" "@method" "@path");keyid="ric_a3f8_xyz1";created=1718000000;expires=1718000300;nonce="Zmxh";tag="web-bot-auth"
```

Rules:
- Each line is `"<component>": <value>`
- The final line is always `"@signature-params": <everything after "label=" in Signature-Input>`
- Lines are joined with `\n` (no trailing newline)
- The signature is `Ed25519( UTF-8(signature_base) )`

---

## Public Key Directory (JWKS)

Bot operators publish public keys at a well-known URL so verifiers can retrieve them without a centralized registry call.

### Registry-hosted (default for RIC bots)

```
GET https://registry.robotidcard.dev/.well-known/http-message-signatures-directory
GET https://registry.robotidcard.dev/.well-known/http-message-signatures-directory?kid=ric_abc_xyz
GET https://registry.robotidcard.dev/v1/bots/{id}/keys
```

Response `Content-Type: application/http-message-signatures-directory+json`:

```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "<base64url of 32-byte public key>",
      "kid": "ric_a3f8c2d1_xyz12345",
      "use": "sig"
    }
  ]
}
```

### Self-hosted (advanced)

Bots with their own domain can host keys at:
```
https://yourdomain.com/.well-known/http-message-signatures-directory
```

Use `ric sign` to generate headers — the `keyid` can be the full URL of your key directory.

---

## Registry Verification (7-Step Flow)

`POST /v1/verify` with body:

```json
{
  "authority":       "example.com",
  "method":          "GET",
  "path":            "/api/articles",
  "signature_input": "ric=(...);keyid=...;created=...;nonce=...;tag=...",
  "signature":       "ric=:<base64>:",
  "signature_agent": "\"ResearchBot\"; cert=\"...\""
}
```

Steps:

1. **Header presence** — Confirm `signature_input` and `signature` are present
2. **Public key retrieval** — Parse `keyid` from `Signature-Input`; look up bot in registry
3. **Timestamp validation** — `created` must not be > 5 min old; `expires` must not be passed; ±30s clock skew allowed
4. **Nonce uniqueness** — If `nonce` present, check it has not been seen in the last 10 min; mark as used
5. **Tag verification** — If `tag` present, must be `"web-bot-auth"`
6. **Ed25519 verification** — Reconstruct signature base; verify with bot's stored public key
7. **Registration status** — Confirm bot is not `dangerous`

---

## Generating Headers: `ric sign`

```bash
ric sign --cert bot.ric.json \
         --authority "example.com" \
         --method GET \
         --path "/api/articles" \
         --ttl 300
```

Output:
```
Signature-Input: ric=("@authority" "@method" "@path");keyid="ric_a3f8_xyz1";created=1718000000;expires=1718000300;nonce="abc123";tag="web-bot-auth"
Signature: ric=:HIbjH...base64...==:
Signature-Agent: "ResearchBot"; cert="https://registry.robotidcard.dev/v1/bots/ric_a3f8_xyz1"
```

---

## Website Integration (SDK v2.0)

```typescript
import { RICMiddleware } from '@robot-id-card/sdk'

app.use(RICMiddleware({
  permissions: {
    '/api/posts':   { minGrade: 'unknown', level: 1 },
    '/api/comment': { minGrade: 'healthy', level: 4 },
  }
}))
```

The middleware automatically detects RFC 9421 headers and passes `authority`, `method`, and `path` to the registry for signature base reconstruction.

---

## Certificate Format (unchanged from v1.0)

```json
{
  "ric_version": "2.0",
  "id": "ric_a3f8c2d1_xyz12345",
  "created_at": "2026-01-15T10:00:00Z",
  "developer": {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "org": "ExampleAI Inc.",
    "verified": false
  },
  "bot": {
    "name": "ResearchBot",
    "version": "1.0.0",
    "purpose": "Web research assistant for academic users",
    "capabilities": ["read_articles", "follow_links"],
    "user_agent": "ResearchBot/1.0 (RIC:ric_a3f8c2d1_xyz12345)"
  },
  "grade": "healthy",
  "public_key": "ed25519:<64-hex-chars>",
  "signature": "..."
}
```

---

## Security Properties

| Property | Mechanism |
|----------|-----------|
| Bot identity binding | Ed25519 signature — private key never leaves bot |
| Replay prevention | `expires` (max 5 min) + `nonce` uniqueness (10-min window) |
| Clock skew tolerance | ±30 seconds |
| Tamper detection | Signature base includes all signed components |
| Accountability | Public audit log; auto-block on 3 violation reports |
| Key discovery | JWKS at `/.well-known/http-message-signatures-directory` |

---

## Standards References

- [RFC 9421 — HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421) (IETF, Feb 2024)
- [RFC 8037 — CFRG Elliptic Curves for JOSE](https://www.rfc-editor.org/rfc/rfc8037) (OKP/Ed25519 JWK format)
- [draft-meunier-web-bot-auth-architecture](https://datatracker.ietf.org/doc/html/draft-meunier-web-bot-auth-architecture) (Cloudflare IETF Draft)
- [Cloudflare Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/)

---

*Version: 2.0 · Created: 2026-04-17*
