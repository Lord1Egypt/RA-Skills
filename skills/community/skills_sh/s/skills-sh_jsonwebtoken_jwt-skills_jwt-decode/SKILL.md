---
name: jwt-decode
description: Decode and inspect JSON Web Tokens (JWTs) without verification. Use when the user provides a JWT string and wants to see its header, payload, or claims — e.g. "decode this JWT", "what's in this token", "inspect this JWT", "show me the claims", "parse this token". Also triggers on raw JWT strings (three base64url segments separated by dots).
---

# JWT Decode

Decode a JWT by base64url-decoding its header and payload. Does NOT verify signatures — use `jwt-validate` for that.

## Steps

1. Split the token on `.` into three parts (header, payload, signature).
2. Base64url-decode and parse parts 1 and 2 as JSON.
3. Display header, payload (with all claims), and the raw signature string.
4. For `exp`, `nbf`, `iat` — show both the Unix timestamp and human-readable UTC. If `exp` is past, note **expired** and by how long.
5. Run security checks (see below).

## Output Format

```
## Header
{ "alg": "RS256", "typ": "JWT", "kid": "abc123" }

## Payload
{ "iss": "https://auth.example.com/", "sub": "user|12345", "exp": 1735689600 }

exp: 2025-01-01T00:00:00Z — EXPIRED (3 months ago)
iat: 2024-12-31T00:00:00Z

## Signature
Algorithm: RS256 | Signature: [base64url string]
(Not verified — use jwt-validate to verify)
```

## Security Checks

Flag these prominently when found:

- **`alg: none`** — Token is unsigned. Warn: "This token has no signature and cannot be trusted. Any party could have created or modified it." This is a known attack vector (CVE-2015-9235) where attackers strip signatures to bypass verification.
- **Sensitive data in payload** — JWTs are encoded, not encrypted. Warn if you spot passwords, secrets, API keys, or PII in claims.
- **Missing `exp`** — Token never expires. Flag as a security risk.
- **`jku`/`jwk`/`x5u` in header** — These can be used to trick verifiers into fetching attacker-controlled keys. Flag if present.

## Notes

- If `cty` header is "JWT", the payload is a nested JWT — decode recursively.
- On decode failure, report the specific error (malformed base64, invalid JSON, wrong segment count).
- This skill only reveals token contents — it says nothing about authenticity. Direct users to `jwt-validate` for verification.

---
