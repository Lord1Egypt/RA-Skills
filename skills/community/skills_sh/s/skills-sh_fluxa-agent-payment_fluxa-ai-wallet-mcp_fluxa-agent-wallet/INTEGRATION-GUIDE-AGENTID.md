# Integration Guide — Agent ID

## Overview

Agent ID is FluxA's identity and authentication service for AI agents — similar to OAuth for agents. Services that serve AI agents can integrate Agent ID to:

1. Have their AI agent clients **register and obtain an Agent ID**
2. **Verify agent identity** on incoming requests by validating the agent's JWT

## For AI Agents — Register & Authenticate

### Register via CLI

```bash
fluxa-wallet init \
  --name "My AI Agent" \
  --client "MyApp v1.0"
```

Verify registration:

```bash
fluxa-wallet status
```

Credentials are saved in `~/.fluxa-ai-wallet-mcp/config.json`. The CLI handles JWT refresh automatically.

### Register via API

```bash
curl -X POST https://agentid.fluxapay.xyz/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "My AI Agent",
    "client_info": "MyApp v1.0"
  }'
```

Response:

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "token": "tok_xxxxxxxxxxxx",
  "jwt": "eyJhbGciOiJSUzI1NiIs..."
}
```

| Credential | Purpose | Lifetime |
|------------|---------|----------|
| `agent_id` | Unique agent identifier (UUID) | Permanent |
| `token` | Secret for refreshing JWT | Permanent |
| `jwt` | RS256 signed bearer token for API calls | 15 minutes, auto-refreshable |

### Attach to Requests

When calling a service that supports Agent ID, include:

```
Authorization: Bearer <jwt>
```

### Refresh JWT When Expired

```bash
curl -X POST https://agentid.fluxapay.xyz/refresh \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "<agent_id>", "token": "<token>"}'
```

Returns a new `jwt`. Services should return HTTP 401 when the JWT expires; refresh responsibility lies with the agent.

## For Services — Verify Agent Identity

### JWT Structure

Agent JWTs are RS256-signed with the following structure:

**Header:**
```json
{ "alg": "RS256", "typ": "JWT", "kid": "agent-did-key" }
```

**Payload:**
```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "agent@example.com",
  "iat": 1710000000,
  "exp": 1710000900
}
```

| Field | Description |
|-------|-------------|
| `agent_id` | Unique agent identifier (UUID), always present |
| `email` | Optional email from registration |
| `iat` | Issued-at timestamp |
| `exp` | Expiration (default: 15 min after issuance) |

### Verification Flow

```
Agent                        Your Service                   AgentID JWKS
  |                               |                              |
  |-- Request + Bearer <jwt> ---->|                              |
  |                               |-- GET /.well-known/jwks.json |
  |                               |<-- {keys: [...]} -----------|
  |                               |                              |
  |                               | Verify RS256 signature       |
  |                               | Check exp not expired        |
  |                               | Extract agent_id             |
  |                               |                              |
  |<-- Response ------------------|                              |
```

### Public Key Sources

**JWKS Endpoint (Recommended):**

```
GET https://agentid.fluxapay.xyz/.well-known/jwks.json
```

Returns RSA public keys with `kid` matching JWT headers. Cache for 5–10 minutes.

**PEM Endpoint (Simple scenarios):**

```
GET https://agentid.fluxapay.xyz/public-key.pem
```

Returns RSA public key in PEM format. JWKS is preferred as it handles key rotation automatically.

### Node.js Example

```javascript
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

const client = jwksClient({
  jwksUri: 'https://agentid.fluxapay.xyz/.well-known/jwks.json',
  cache: true,
  cacheMaxAge: 600000,
});

function getSigningKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    if (err) return callback(err);
    callback(null, key.getPublicKey());
  });
}

function agentAuth(req, res, next) {
  const auth = req.headers.authorization || '';
  if (!auth.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'missing_bearer_token' });
  }
  const token = auth.slice(7);

  jwt.verify(token, getSigningKey, { algorithms: ['RS256'] }, (err, payload) => {
    if (err) {
      return res.status(401).json({ error: 'invalid_or_expired_jwt' });
    }
    req.agent = { agent_id: payload.agent_id, email: payload.email || null };
    next();
  });
}
```

### Python Example

```python
import jwt
from jwt import PyJWKClient

jwks_client = PyJWKClient(
    "https://agentid.fluxapay.xyz/.well-known/jwks.json",
    cache_keys=True,
)

def verify_agent_jwt(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(token, signing_key.key, algorithms=["RS256"])

# Flask decorator
from functools import wraps
from flask import request, jsonify

def require_agent_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing_bearer_token"}), 401
        try:
            payload = verify_agent_jwt(auth[7:])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "jwt_expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid_jwt"}), 401
        request.agent_id = payload["agent_id"]
        return f(*args, **kwargs)
    return decorated
```

### Security Best Practices

- **Must:** Specify `algorithms: ['RS256']` to prevent algorithm downgrade attacks
- **Must:** Use HTTPS for all JWKS and API communication
- **Should:** Cache public keys for 5–10 minutes
- **Should:** Support clock skew tolerance (~30 seconds)
- **Do not:** Verify RS256 tokens using HS256, ignore `kid`, or log JWT credentials

## AgentID API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register a new agent |
| `POST` | `/refresh` | Refresh an expired JWT |
| `GET` | `/.well-known/jwks.json` | JWKS public keys (for local verification) |
| `GET` | `/public-key.pem` | RSA public key in PEM format |
| `GET` | `/agent/<agent_id>` | Query agent metadata |

**Base URL:** `https://agentid.fluxapay.xyz`

Full verification documentation: https://docs.fluxapay.xyz/wallet/agent-guide-jwt-verification.html
