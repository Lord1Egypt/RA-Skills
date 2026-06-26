# Third-Party Agent Bridge Architecture

## Why This Package Exists
The current repo already has several strong building blocks:
- multi-path authentication in `backend/auth/auth_router.py`
- local session issuance in `backend/auth/google_auth.py`
- owner / sub-user permission modeling in `backend/routers/access_router.py`
- async tool execution in `backend/routers/tool_router.py`

What is missing is a **provider-agnostic bridge layer** that lets OpenClaw or another external agent attach to those features without coupling the whole app to one vendor.

## Recommended Design

### 1. Capability-First Instead of Provider-First
Do not start by building `openclaw_login`, `openclaw_tools`, `openclaw_projects`.

Start with:
- a shared capability catalog
- a provider manifest that selects from that catalog
- a bridge service that issues short-lived grants for selected capabilities

This keeps OpenClaw, future custom agents, and internal automation on the same contract surface.

### 2. Session Handoff, Not Cookie Sharing
The existing VibeVideo session cookie should stay inside VibeVideo.

Recommended flow:
1. user logs into VibeVideo normally
2. VibeVideo backend issues a short-lived bridge session for `provider_id`
3. provider exchanges that bridge session for its own local state
4. provider calls back into VibeVideo only through scoped bridge endpoints or existing APIs

Why:
- avoids leaking primary auth cookies to third parties
- makes revocation and audit easier
- lets you map owner/sub-user permissions cleanly

### 3. Auth Strategy Stack
Use auth in layers:

- **Primary**: `session_handoff`
  - best default for OpenClaw and future agent UIs
- **Fallback**: `email_code`
  - useful if the provider needs a user bootstrap path without full OAuth
- **Legacy-compatible helper**: `email-token-setup`
  - good browser-side adapter if the provider receives a VibeVideo-issued local token

### 4. Scope Model
Keep scopes coarse at first:
- `authenticated`
- `owner`
- `sub_user`
- `internal`

Then gate each capability separately.

Example initial OpenClaw rollout:
- allow `identity.current_user`
- allow `tools.generate_async`
- allow `tools.task_status.read`
- allow `tools.result.read`
- optionally allow `auth.email_code.*`
- do **not** allow `projects.write` initially

### 5. Bridge Components To Add Later
This package intentionally stops at the contract layer. The next implementation layer should likely add:

- `backend/routers/agent_bridge_router.py`
  - issue session grants
  - verify provider callback
  - log audit events
- `frontend/.../agents/[provider]`
  - launcher UI
  - callback handling
  - locale-aware redirects
- provider-specific config
  - allowed origins
  - callback URLs
  - enabled capabilities

## Suggested OpenClaw Rollout

### Phase 1
- redirect launcher
- bridge session issuance
- current-user read
- async tools read/write
- audit logs

### Phase 2
- email-code fallback
- access token overview
- provider-side task polling UI

### Phase 3
- project read APIs
- asset upload presign
- limited project writes after audit confidence

## Important Constraints From This Repo
- locale should still come from `x-request-locale`
- backend APIs should prefer `{error_code, data?, error_message?}`
- auth already mixes direct and standard response shapes, so the bridge should normalize them before exposing them externally
- sub-user permissions already exist, so the bridge should preserve owner/sub-user identity instead of flattening everything into a single user role
