---
name: jwt-encode
description: Create and sign JSON Web Tokens (JWTs) for testing and development. Use when the user wants to generate, create, build, or sign a JWT — e.g. "create a JWT", "generate a test token", "sign this payload", "make a JWT with these claims", "build an access token". Supports HMAC, RSA, and ECDSA algorithms.
---

# JWT Encode

Create and sign JWTs for testing and development.

## Steps

1. **Gather inputs**: claims/payload, algorithm (default: HS256), secret or key, expiration (default: 1 hour).
2. **Build header**: `{"alg": "HS256", "typ": "JWT"}`. Add `kid` if provided.
3. **Build payload**: Always include `iat` and `exp` unless the user opts out. Add user-specified claims.
4. **Sign the token** using the best available method (see below).
5. **Display the result**: the full JWT string and a decoded breakdown of header + payload.

## Signing Methods

Pick the first available. Use the user's claims, secret, and algorithm — the examples below are templates only. Always pass the secret via an inline env var to avoid shell history exposure.

**Node.js** (preferred):

First, ensure `jose` is available — install it globally if missing:

```bash
node --input-type=module -e "await import('jose')" 2>/dev/null || npm install -g jose
```

Then sign the token:

```bash
JWT_SECRET='user-provided-secret' node --input-type=module -e "import {SignJWT} from 'jose'; console.log(await new SignJWT({sub:'1234567890'}).setProtectedHeader({alg:'HS256'}).setIssuedAt().setExpirationTime('1h').sign(new TextEncoder().encode(process.env.JWT_SECRET)))"
```

**Python**:

```bash
JWT_SECRET='user-provided-secret' python3 -c "import jwt,time; print(jwt.encode({'sub':'1234567890','iat':int(time.time()),'exp':int(time.time())+3600}, __import__('os').environ['JWT_SECRET'], algorithm='HS256'))"
```

**Bash** (HMAC-SHA256 only):

```bash
header=$(printf '{"alg":"HS256","typ":"JWT"}' | openssl base64 -e -A | tr '+/' '-_' | tr -d '=')
payload=$(printf '{"sub":"1234567890","iat":1700000000,"exp":1700003600}' | openssl base64 -e -A | tr '+/' '-_' | tr -d '=')
signature=$(printf '%s.%s' "$header" "$payload" | openssl dgst -sha256 -hmac "$JWT_SECRET" -binary | openssl base64 -e -A | tr '+/' '-_' | tr -d '=')
printf '%s.%s.%s\n' "$header" "$payload" "$signature"
```

## Generating Test Keys

Only when the user needs asymmetric keys:

```bash
# RSA
openssl genrsa -out private.pem 2048 && openssl rsa -in private.pem -pubout -out public.pem
# ECDSA P-256
openssl ecparam -genkey -name prime256v1 -noout -out private-ec.pem && openssl ec -in private-ec.pem -pubout -out public-ec.pem
```

## Security Rules

- **Never pass secrets as literal command-line arguments.** Use environment variables (`$JWT_SECRET`) or file input (`--secret-file`). Command args are visible in shell history and `ps` output.
- **Never install packages without user consent.** Do not use `npx -y` or `pip install` silently.
- **If the user doesn't provide a secret**, generate a random one with `openssl rand -base64 32` and clearly label it as a test-only secret.
- **`alg: none`** — If the user requests it, warn that this creates an unsigned token exploitable via CVE-2015-9235. Only create it after explicit confirmation.
- **Generated key files** — Remind the user to delete test keys when done. Never write keys to version-controlled directories.

---
