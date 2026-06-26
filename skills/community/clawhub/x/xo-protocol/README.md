# XO Protocol

**The Dating Intelligence API.**

Identity verification, compatibility scoring, and reputation — answers, not data. All data access requires explicit user authorization via OAuth.

> **Status:** Public Beta — free to use, rate limits apply.

## Quick Links

- [Landing Page](https://xoxo.space/en/protocol)
- [API Docs (Swagger)](https://protocol.xoxo.space/protocol/docs)
- [OpenAPI Spec](./openapi.yaml)

---

## Quick Start (5 minutes)

### Install the SDK

```bash
npm install @xo-protocol/sdk
```

### Get a Trust Profile

```javascript
import { XOClient } from '@xo-protocol/sdk'

const xo = new XOClient({ apiKey: 'your-api-key' })
xo.setAccessToken(userToken) // from OAuth flow

// One call to get everything
const { identity, reputation, socialSignals } = await xo.getTrustProfile()

console.log(identity.verified)              // true
console.log(identity.trust_score)           // 1.0
console.log(reputation.tier)                // "gold"
console.log(socialSignals.engagement_score) // 0.45
console.log(socialSignals.confidence)       // 0.9
```

### Add "Login with XO" to Your App

```javascript
const xo = new XOClient({ apiKey: 'your-api-key' })

// 1. Generate login URL
const url = xo.getAuthorizationUrl({
  clientId: 'your_client_id',
  redirectUri: 'https://yourapp.com/callback',
  state: crypto.randomUUID(),
})
// → redirect user to `url`

// 2. Handle callback
const tokenData = await xo.exchangeCode({
  code: req.query.code,
  clientId: 'your_client_id',
  clientSecret: 'your_secret',
  redirectUri: 'https://yourapp.com/callback',
})
// → xo.setAccessToken() is called automatically
```

---

## Use Cases

### 1. Trust Badge for Dating Apps

Show a verified trust badge on user profiles. Filter out unverified users from search results.

```javascript
const profile = await xo.getTrustProfile()

if (profile.identity.verified && profile.identity.trust_score > 0.8) {
  showBadge('✅ Highly Trusted')
} else if (profile.identity.verified) {
  showBadge('✅ Verified')
} else {
  showBadge('⚠️ Unverified')
}
```

→ See [trust-badge.html](./examples/trust-badge.html) for a complete embeddable widget.

### 2. Quality-Based User Ranking

Sort your user list by trust quality — verified users first, then by reputation tier and engagement.

```javascript
const TIER_ORDER = { novice: 0, bronze: 1, silver: 2, gold: 3, platinum: 4, diamond: 5, s: 6 }

users.sort((a, b) => {
  // Verified first
  if (a.xo.identity.verified !== b.xo.identity.verified)
    return a.xo.identity.verified ? -1 : 1
  // Then by tier
  return TIER_ORDER[b.xo.reputation.tier] - TIER_ORDER[a.xo.reputation.tier]
})
```

→ See [dating-app-integration.js](./examples/dating-app-integration.js) for full filtering + sorting logic.

### 3. AI Agent with Social Context

Give your AI agent access to user trust data via MCP (Model Context Protocol) for Claude Desktop or other AI clients.

```javascript
// AI agent can call: verify_identity, get_reputation, get_social_signals
// See examples/mcp-server.js for a complete MCP server
```

→ See [mcp-server.js](./examples/mcp-server.js) for a ready-to-use MCP server.

### 4. Scam Detection

Use engagement score + confidence to identify potentially fraudulent accounts:

```javascript
const signals = await xo.getSocialSignals()

// Low engagement + high confidence = consistently poor interactions
if (signals.confidence > 0.7 && signals.engagement_score < 0.1) {
  flagForReview(user)
}

// No data at all on an "old" account = suspicious
const identity = await xo.verifyIdentity()
if (!identity.verified && signals.engagement_score === null) {
  requireAdditionalVerification(user)
}
```

---

## SDK Reference

### `new XOClient({ apiKey, baseUrl? })`

Create a client instance.

### `xo.setAccessToken(token)`

Set the JWT after completing OAuth.

### `xo.getAuthorizationUrl({ clientId, redirectUri, state, scopes? })`

Returns the OAuth authorization URL. Default scopes: all.

### `xo.exchangeCode({ code, clientId, redirectUri, clientSecret?, codeVerifier? })`

Exchange auth code for access token. Automatically calls `setAccessToken()`.

### `xo.verifyIdentity()`

Returns: `{ verified, trust_score, has_minted_sbt, attestations, member_since }`

### `xo.searchConnections({ limit?, topicIds?, cursor? })`

Returns: `{ connections: [{ tmp_id, compatibility_score, topics, verified }], cursor, total }`

### `xo.getReputation(token?)`

Returns: `{ tier, reputation_score }` — pass `'me'` (default) or a `tmp_id`.

### `xo.getSocialSignals(token?)`

Returns: `{ engagement_score, confidence }` — pass `'me'` (default) or a `tmp_id`.

### `xo.getProfile(token?)`

Returns: `{ interests, topics, preferences }` — user's self-disclosed preferences. Requires `profile` scope.

### `xo.getNewsfeed(tmpId, { limit?, cursor? })`

Returns: `{ posts: [{ post_id, content, topics, created_at }], cursor, total }` — user's public posts. Requires `newsfeed` scope.

### `xo.getTrustProfile()`

Convenience method — calls `verifyIdentity()`, `getReputation()`, and `getSocialSignals()` in parallel. Returns `{ identity, reputation, socialSignals }`.

---

## Understanding the Scores

| Field | Range | What It Means |
|-------|-------|---------------|
| `trust_score` | 0–1.0 | Composite identity verification score (SBT attestations) |
| `reputation_score` | 0–1.0 | Cumulative platform reputation (aura / 10,000) |
| `tier` | novice → s | Reputation level: novice, bronze, silver, gold, platinum, diamond, s |
| `engagement_score` | 0–1.0 | Conversation quality (AI-scored chat depth + peer reviews) |
| `confidence` | 0–1.0 | How reliable the engagement score is (more data = higher confidence) |

**Rules of thumb:**
- `trust_score > 0.8` + `verified: true` → highly trustworthy user
- `confidence < 0.5` → engagement score is based on too few data points, don't rely on it heavily
- `engagement_score < 0.1` + `confidence > 0.7` → consistently poor interactions, potential red flag

---

## Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/protocol/v1/auth/token` | POST | API Key | Exchange Firebase token or auth code for JWT |
| `/protocol/v1/auth/authorize` | POST | Public | Generate OAuth authorization code |
| `/protocol/v1/identity/verify` | GET | API Key + JWT | SBT verification status, trust score, attestations |
| `/protocol/v1/connections/search` | GET | API Key + JWT | AI-computed compatibility scores — no personal data |
| `/protocol/v1/reputation/{token}` | GET | API Key + JWT | Reputation tier and score |
| `/protocol/v1/social-signals/{token}` | GET | API Key + JWT | Composite engagement score |
| `/protocol/v1/profile/{token}` | GET | API Key + JWT | User's self-disclosed preferences (requires `profile` scope) |
| `/protocol/v1/newsfeed/{tmp_id}` | GET | API Key + JWT | User's public posts (requires `newsfeed` scope) |

---

## Authentication

XO Protocol supports two authentication flows:

### 1. Direct Authentication (first-party apps)

```bash
curl -X POST https://protocol.xoxo.space/protocol/v1/auth/token \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "firebase", "assertion": "<firebase_id_token>"}'
```

### 2. OAuth 2.0 Authorization Code Flow (third-party apps)

```
1. Redirect user to:
   https://xoxo.space/en/oauth/authorize
     ?client_id=your_client_id
     &redirect_uri=https://yourapp.com/callback
     &scope=identity,connections
     &state=random123
     &response_type=code

2. User authenticates with Google and approves scopes

3. User is redirected to:
   https://yourapp.com/callback?code=AUTH_CODE&state=random123

4. Exchange code for token:
   POST /protocol/v1/auth/token
   {
     "grant_type": "authorization_code",
     "code": "AUTH_CODE",
     "client_id": "your_client_id",
     "client_secret": "your_secret",
     "redirect_uri": "https://yourapp.com/callback"
   }
```

**PKCE** is supported for public clients (SPAs) — use `code_challenge` + `code_verifier` instead of `client_secret`.

---

## Scopes

| Scope | Endpoint | Description |
|-------|----------|-------------|
| `identity` | `/identity/verify` | View SBT verification status, trust score, attestations |
| `connections` | `/connections/search` | Get AI-computed compatibility scores between users |
| `reputation` | `/reputation/{token}` | View reputation tier and score |
| `social_signals` | `/social-signals/{token}` | View composite engagement score |
| `profile` | `/profile/{token}` | Access user's self-disclosed preferences and interests |
| `newsfeed` | `/newsfeed/{tmp_id}` | Browse user's publicly shared posts |

---

## Examples

| Example | Description |
|---------|-------------|
| [quickstart.js](./examples/quickstart.js) | Basic OAuth flow + API calls |
| [trust-badge.html](./examples/trust-badge.html) | Embeddable Trust Badge widget (HTML + CSS + JS) |
| [dating-app-integration.js](./examples/dating-app-integration.js) | Full dating app integration patterns |
| [mcp-server.js](./examples/mcp-server.js) | MCP server for Claude Desktop / AI agents |

---

## Privacy

XO Protocol is designed as a **privacy-first intelligence API**:

- **No PII**: No real names, photos, or location in any response.
- **User-Authorized**: All data access requires explicit OAuth consent. Profile and newsfeed data are only accessible when the user approves those scopes.
- **Ephemeral IDs**: Real user IDs are never exposed. Connections return `tmp_id` tokens (24h TTL, per-API-key scoped).
- **Scoped Tokens**: Each JWT is limited to the approved scopes. No scope creep.

---

## Rate Limits

| Tier | Rate Limit | Price |
|------|-----------|-------|
| Free (Beta) | 100 req/min | $0 |
| Pro | 1,000 req/min | Coming soon |
| Enterprise | 10,000 req/min | Contact us |

---

## Errors

All errors follow [RFC 7807 Problem Details](https://tools.ietf.org/html/rfc7807):

```json
{
  "type": "urn:xo:error:api_key_required",
  "status": 400,
  "title": "Api Key Required",
  "detail": "Missing X-API-Key header"
}
```

---

## Getting an API Key

Fill out the [API Key Request form](https://xoxo.space/en/protocol#cta) on the protocol page and we'll get back to you.

---

## Links

- Website: [xoxo.space](https://xoxo.space)
- Protocol Landing: [xoxo.space/protocol](https://xoxo.space/en/protocol)
- API Docs: [protocol.xoxo.space/protocol/docs](https://protocol.xoxo.space/protocol/docs)

---

**Note:** Only existing XO users can authenticate. New accounts must be created via the [XO App](https://xoxo.space).
