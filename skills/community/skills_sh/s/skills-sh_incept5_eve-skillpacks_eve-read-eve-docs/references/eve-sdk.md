# Eve SDK

## Use When
- You need to add authentication to an Eve-deployed app (backend, frontend, or fullstack).
- You need to embed an Eve thread-backed agent conversation pane in an app.
- You need to know which SDK packages exist and what they export.
- You need the quick-start install and wiring pattern for a new app.
- You need to understand the token flow between browser, backend, and Eve platform.
- You need to ship branded magic-link login, app-org invites, or domain-based signup on top of Eve SSO.

## Load Next
- `references/auth-sdk.md` for deep auth coverage: middleware behavior, verification strategies, token types, NestJS patterns, session bootstrap sequence, migration guide.
- `references/agents-teams.md` for embedded conversation endpoints, route predicates, and gateway policies.
- `references/gateways.md` for choosing `app`, `api`, or `webchat` provider identity.
- `references/secrets-auth.md` for platform auth model, identity providers, and access control.
- `references/manifest.md` for environment variable interpolation in manifests.

## Ask If Missing
- Confirm whether the app is backend-only, frontend-only, or fullstack.
- Confirm the backend framework (Express or NestJS).
- Confirm whether the app serves browser users, agent jobs, or both.
- For embedded conversations, confirm the Eve project id, `app_id`, and product-level `app_key` convention.

## Overview

The Eve SDK packages eliminate auth and embedded conversation boilerplate in Eve-deployed apps.

| Package | Runtime | Purpose |
|---------|---------|---------|
| `@eve-horizon/auth` | Node.js (Express / NestJS) | Token verification, org membership, route protection |
| `@eve-horizon/auth-react` | Browser (React) | SSO session management, login UI, token cache |
| `@eve-horizon/chat` | Browser / Node.js | Embedded conversation client, bearer fetch, SSE parser, server proxy helper |
| `@eve-horizon/chat-react` | Browser (React) | Conversation provider, hooks, and minimal panes |

## Install

```bash
# Backend
npm install @eve-horizon/auth

# Frontend
npm install @eve-horizon/auth-react

# Embedded conversations
npm install @eve-horizon/chat @eve-horizon/chat-react
```

## Quick-Start: Backend (Express)

```typescript
import { eveAuth, eveIdentityGuard, eveAuthConfig, eveAuthMe } from '@eve-horizon/auth';

app.use(eveAuth());                                         // Parse any Eve token (non-blocking)
app.get('/auth/config', eveAuthConfig());                   // Serve SSO discovery
app.get('/auth/me', eveAuthMe());                           // Full /auth/me for React SDK
app.use('/api', eveIdentityGuard());                        // Protect all API routes
```

Use `eveAuth()` for apps serving both users and agents (most Eve apps). It normalizes both token types into `req.eveIdentity`. See `auth-sdk.md` for the full middleware comparison.

## Quick-Start: Frontend (React)

```tsx
import { EveAuthProvider, EveLoginGate, useEveAuth } from '@eve-horizon/auth-react';

function App() {
  return (
    <EveAuthProvider apiUrl="/api">
      <EveLoginGate>
        <Dashboard />
      </EveLoginGate>
    </EveAuthProvider>
  );
}

function Dashboard() {
  const { user, logout } = useEveAuth();
  return <div>Welcome {user?.email} <button onClick={logout}>Sign out</button></div>;
}
```

## Token Flow

1. User visits app -- `EveAuthProvider` checks `sessionStorage` for a cached token.
2. No cached token -- probes SSO broker `/session` using root-domain cookie.
3. SSO session exists -- receives fresh Eve RS256 token, caches in `sessionStorage`.
4. No SSO session -- shows login form (SSO redirect or token paste).
5. All API requests include `Authorization: Bearer <token>` header.

## Backend Exports

| Export | Type | Description |
|--------|------|-------------|
| `eveAuth(options?)` | Middleware | **Recommended.** Unified auth for user + agent tokens, attach `req.eveIdentity` (non-blocking) |
| `eveIdentityGuard()` | Middleware | Return 401 if `req.eveIdentity` not set |
| `eveUserAuth(options?)` | Middleware | User-only token verification, attach `req.eveUser` (non-blocking) |
| `eveAuthGuard()` | Middleware | Return 401 if `req.eveUser` not set |
| `eveAuthConfig()` | Handler | Serve `{ sso_url, eve_api_url, ... }` from env vars |
| `eveAuthMe(options?)` | Handler | Full `/auth/me` — memberships + project role for React SDK |
| `eveAuthMiddleware(options?)` | Middleware | Agent/job token verification (blocking), attach `req.agent` |
| `verifyEveToken(token, url?)` | Function | JWKS-based local verification (15-min cache) |
| `verifyEveTokenRemote(token, url?)` | Function | HTTP verification via `/auth/token/verify` |

## Frontend Exports

| Export | Type | Description |
|--------|------|-------------|
| `EveAuthProvider` | Component | Context provider, session bootstrap. Props: `apiUrl?`, `projectId?` |
| `useEveAuth()` | Hook | `{ user, loading, orgs, activeOrg, switchOrg, loginWithSso, loginWithToken, logout }` |
| `EveLoginGate` | Component | Render children when authed, login form when not |
| `EveLoginForm` | Component | SSO + token paste login UI |
| `createEveClient(baseUrl?)` | Function | Fetch wrapper with automatic Bearer injection |
| `getStoredToken()` / `storeToken()` / `clearToken()` | Functions | Direct sessionStorage access |

## Chat Exports

| Package | Export | Description |
|---------|--------|-------------|
| `@eve-horizon/chat` | `createConversationClient()` | Browser/Node client for ensure, get, send, messages, and stream |
| `@eve-horizon/chat/server` | `EveConversationsClient` | Server-side helper for backend-proxied turns |
| `@eve-horizon/chat/server` | `forwardTurn()` | Apply enrichment/rejection hooks before forwarding a turn |
| `@eve-horizon/chat` | `conversation.events()` / `conversation.streamEvents()` / `conversation.emitEvent()` | Structured event timeline (typed kinds, replayable cursor) |
| `@eve-horizon/chat` | `conversation.continueByThreadId()` | Continue a routed Eve thread by `thr_*` id, preserving the original dispatch target |
| `@eve-horizon/chat-react` | `EveConversationProvider` | React state provider for one app conversation |
| `@eve-horizon/chat-react` | `useEveConversation()` | Hook exposing conversation state, `ensure`, `send`, `reconnect`, and event stream |
| `@eve-horizon/chat-react` | `EveConversationPane` | Headless render-prop pane |
| `@eve-horizon/chat-react` | `EveConversationDefaultPane` | Minimal styled conversation pane |

## Environment Variables

Auto-injected by the Eve deployer into every deployed app. No manual configuration needed.

| Variable | Used By | Purpose |
|----------|---------|---------|
| `EVE_API_URL` | `@eve-horizon/auth` | JWKS fetch, remote token verification |
| `EVE_ORG_ID` | `@eve-horizon/auth` | Org membership check |
| `EVE_SSO_URL` | Both | Auth config discovery, SSO session probe |
| `EVE_PUBLIC_API_URL` | Both | Public-facing API URL (optional) |

## Common Patterns

### Backend-Only API (Agent Jobs)

For APIs that only serve agent jobs with no browser users:

```typescript
import { eveAuthMiddleware } from '@eve-horizon/auth';

app.use('/api', eveAuthMiddleware({ strategy: 'local' }));

app.get('/api/data', (req, res) => {
  console.log(req.agent.project_id, req.agent.job_id);
});
```

### Fullstack React App

Combine both packages for SSO login with protected API routes:

```typescript
// Backend
app.use(eveUserAuth());
app.get('/auth/config', eveAuthConfig());
app.get('/auth/me', eveAuthMe());
app.use('/api', eveAuthGuard());
```

```tsx
// Frontend
import { EveAuthProvider, EveLoginGate, createEveClient } from '@eve-horizon/auth-react';

const client = createEveClient('/api');
const res = await client.fetch('/data');
```

### Passwordless App Login + Branded Invites

Apps opt into branded SSO and passwordless login by adding `x-eve.branding` and `x-eve.auth` to the manifest — no SDK code change required. `EveAuthProvider` already includes `eve_project_id` in the SSO redirect, and `eveAuthConfig()` exposes it on `/auth/config`.

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"
    primary_color: "#1f6feb"
    email_from_name: "ACME Portal"
  auth:
    login_method: magic_link        # or password_or_magic_link
    self_signup: false
    invite_requires_password: false
```

Both magic-link and invite emails ship app-branded subject, body, logo, and `From:` display name, and ride through an SSO confirmation interstitial (`/m/mlw_<id>`) so corporate mail scanners cannot burn single-use OTPs. Apps that need to invite members from in-product admin pages should use `useEveAppAccess()` + `POST /auth/app-invites`. For multi-tenant projects, declare `x-eve.auth.org_access.domain_signup.domains[]` (v2 rule list) to auto-attach allowlisted email domains to per-rule target orgs without per-user invites. Custom-domain apps must also list their origin in `x-eve.auth.allowed_redirect_origins`.

See `references/auth-sdk.md` and `references/secrets-auth.md` for the full app-scoped magic-link, domain-signup, redirect allowlist, interstitial, and SES suppression coverage.

### Embedded Conversation Pane

Use Eve threads as the durable conversation record for an app-owned object. The SDK calls the project conversations facade and streams snapshot, message, progress, and heartbeat events.

```tsx
import { EveConversationProvider, EveConversationDefaultPane } from '@eve-horizon/chat-react';

function DesignerChat({ projectId, conversationId, token }: {
  projectId: string;
  conversationId: string;
  token: string;
}) {
  return (
    <EveConversationProvider
      baseUrl="/api/eve"
      projectId={projectId}
      appKey={`open-design:${projectId}:${conversationId}`}
      appId="open-design"
      getToken={() => token}
    >
      <EveConversationDefaultPane />
    </EveConversationProvider>
  );
}
```

Backend-proxied apps can use `@eve-horizon/chat/server` with a service token to enrich or reject turns before forwarding them to Eve.

Conversation streams are fetch-based SSE (not native `EventSource`, because bearer auth requires `Authorization` headers). Each `message` or `progress` event carries `eventId` from `thread_messages.id`; pass the last seen id back as `resumeFrom` to replay without gaps:

```typescript
for await (const event of conversation.stream({ resumeFrom: lastEventId })) {
  if (event.eventId) lastEventId = event.eventId;
}
```

### Continuing by Eve Thread Id

When an app already holds an Eve `thread_id` (`thr_*`) — e.g. it surfaced one to the user from a previous session — it can continue the conversation directly without re-supplying the `app_key`:

```typescript
await client.continueByThreadId('thr_ABC', { text: 'follow-up question' });
// hits POST /threads/thr_ABC/chat
```

Continuation reuses the original dispatch target (`route` / `agent` / `team`) stored on the thread, so a later `chat.yaml` change cannot silently re-route an existing conversation. Org-scoped, coordination, and legacy threads without continuation metadata are rejected with `409`.

### Structured Conversation Events

Beyond plain user/assistant messages, every conversation has a normalized event timeline that includes job status changes, tool calls/results, file changes, attachments, errors, and app-emitted events. These are durable, ordered, and replayable.

```typescript
// List events (filter by kind, job, attempt, workflow_step, source)
const { events } = await conversation.events({ kind: ['tool.call', 'tool.result'], limit: 100 });

// Stream events (SSE; resume with `after` cursor or Last-Event-ID)
for await (const event of conversation.streamEvents({ after: lastCursor })) {
  if (event.kind === 'snapshot') continue;
  lastCursor = event.eventId;
}

// Emit an app-defined event (server-side or via authenticated client)
await conversation.emitEvent({
  kind: 'artifact.update',
  text: 'preview updated',
  payload: { artifact_id: 'a_1', version: 2 },
});
```

Event endpoints are also exposed by thread id:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/projects/:project_id/conversations/:app_key/events` | List events for an embedded conversation |
| GET | `/projects/:project_id/conversations/:app_key/events/stream` | SSE stream of events |
| POST | `/projects/:project_id/conversations/:app_key/events` | Emit an app-defined event |
| GET | `/threads/:thread_id/events` | List events by thread id |
| GET | `/threads/:thread_id/events/stream` | SSE stream by thread id |
| POST | `/threads/:thread_id/events` | Emit an app-defined event by thread id |

Standard event kinds: `user.message`, `assistant.message`, `text.delta`, `tool.call`, `tool.result`, `status.changed`, `progress`, `error`, `attachment.added`, `file.change`, `delivery.status`, `final.result`. App-defined kinds must match `^[a-z][a-z0-9_.-]*$` (max 150 chars). Lists default to 100 events; `limit` clamps to 500.

### SSE Authentication

The middleware supports `?token=` query parameter for Server-Sent Events:

```
GET /api/events?token=eyJ...
```

## Deep Auth Reference

For middleware behavior details, verification strategies (`local` vs `remote`), token types (`EveUser` / `EveTokenClaims`), NestJS guard patterns, session bootstrap sequence, token lifecycle and TTLs, `orgs` claim mechanics, and migration from custom auth, see `references/auth-sdk.md`.
