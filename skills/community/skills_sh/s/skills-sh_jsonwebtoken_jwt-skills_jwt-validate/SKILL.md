---
name: jwt-validate
description: Verify and validate JSON Web Tokens (JWTs) by checking signatures, expiration, claims, and structure. Use when the user wants to verify, validate, or check a JWT — e.g. "verify this token", "is this JWT valid", "check the signature", "validate this token against my JWKS", "is this token expired". Supports HMAC, RSA, and ECDSA with secrets, PEM keys, or JWKS endpoints.
---

# JWT Validate

Verify a JWT's signature and validate its claims. Confirms the token is authentic, unexpired, and structurally sound.

## Validation Order

Check in this order. Stop and report at the first failure.

### 1. Structure

- Exactly 3 dot-separated parts, each valid base64url
- Header and payload parse as valid JSON
- Header contains `alg`; `alg` is not `none` (unless explicitly expected)

### 2. Claims

- `exp` must be in the future (report time until expiry or how long ago it expired)
- `nbf` must be in the past or present
- `iat` must be in the past; flag if > 30 days old
- `iss`, `aud`, `sub` — if user provides expected values, they must match
- Allow 60 seconds clock skew tolerance on all time checks

### 3. Signature

Requires the user to provide a secret, PEM public key, or JWKS URI. Always pass secrets and tokens via inline env vars to avoid shell history exposure.

**Node.js** (preferred):

First, ensure `jose` is available — install it globally if missing:

```bash
node --input-type=module -e "await import('jose')" 2>/dev/null || npm install -g jose
```

Then verify the token:

```bash
JWT_TOKEN='the.jwt.here' JWT_SECRET='user-provided-secret' node --input-type=module -e "import {jwtVerify} from 'jose'; try { const {payload}=await jwtVerify(process.env.JWT_TOKEN, new TextEncoder().encode(process.env.JWT_SECRET), {algorithms:['HS256'],clockTolerance:60}); console.log('VALID'); console.log(JSON.stringify(payload,null,2)); } catch(e) { console.log('INVALID:',e.message); }"
```

**Python**:

```bash
JWT_TOKEN='the.jwt.here' JWT_SECRET='user-provided-secret' python3 -c "
import jwt,json,os
try:
  d=jwt.decode(os.environ['JWT_TOKEN'],os.environ['JWT_SECRET'],algorithms=['HS256'],leeway=60)
  print('VALID'); print(json.dumps(d,indent=2))
except Exception as e: print(f'INVALID: {e}')
"
```

**JWKS verification** (Node.js):

```bash
JWT_TOKEN='the.jwt.here' JWKS_URI='https://example.auth0.com/.well-known/jwks.json' node --input-type=module -e "import {jwtVerify,createRemoteJWKSet} from 'jose'; try { const {payload}=await jwtVerify(process.env.JWT_TOKEN, createRemoteJWKSet(new URL(process.env.JWKS_URI)), {algorithms:['RS256']}); console.log('VALID'); console.log(JSON.stringify(payload,null,2)); } catch(e) { console.log('INVALID:',e.message); }"
```

If no secret/key is provided, perform structure + claims validation only, and clearly state the signature was NOT verified.

## Output Format

```
## JWT Validation Report
Structure: PASS
Claims:    PASS — exp 2025-06-15T12:00:00Z (expires in 2h)
Signature: PASS — RS256, key kid "abc123"
Result:    VALID
```

On failure:

```
## JWT Validation Report
Structure: PASS
Claims:    FAIL — exp 2024-01-15T12:00:00Z (expired 6 months ago)
Signature: SKIPPED
Result:    INVALID — token expired
```

## Security Rules

- **Never trust the token's `alg` header for verification.** Always use the algorithm the user expects or that matches the provided key type. Trusting the header enables algorithm confusion attacks where an attacker switches RS256 to HS256 and signs with the public key as an HMAC secret.
- **Always specify `algorithms` as an explicit allowlist** in verification calls. Never pass `algorithms: [decoded.header.alg]`.
- **Never pass secrets/tokens as literal command-line arguments.** Use environment variables. Args are visible in shell history and `ps` output.
- **`alg: none`** — Flag as a critical security issue. The token is unsigned and cannot be trusted.
- **If no key is provided**, validate structure and claims only. Clearly state: "Signature was NOT verified — token authenticity is unknown."

---
