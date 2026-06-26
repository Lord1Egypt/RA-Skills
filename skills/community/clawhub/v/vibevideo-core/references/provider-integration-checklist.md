# Provider Integration Checklist

Use this checklist before binding OpenClaw or another third-party agent.

## 1. Pick The Smallest Useful Capability Set
Start with:
- `identity.current_user`
- `tools.generate_async`
- `tools.task_status.read`
- `tools.result.read`

Only add more after the first provider flow is stable.

## 2. Choose Transport
- `redirect`: best default for OpenClaw-style external agent UI
- `embedded`: only if CSP, cookies, and iframe restrictions are understood
- `popup`: okay for admin or operator tools
- `server_proxy`: use when the external provider should never touch browser auth state

For the current Studio bridge runtime:
- default site selection to `bollo.video`
- let users switch explicitly to `vibevideo.io`
- store the issued access token in a local OpenClaw session file instead of relying on browser cookies

## 3. Choose Auth Strategy
- prefer `session_handoff`
- use `email_code` as fallback
- keep `internal_service` for backend-only automation

## 4. Preserve Existing Repo Contracts
- send locale via `x-request-locale`
- preserve `{error_code, data?, error_message?}` when exposing normalized APIs
- preserve owner / sub-user context

## 5. Security Review
- do not expose the primary auth cookie to the provider
- set a short bridge token TTL
- whitelist provider origins
- log session issuance and exchange events
- keep provider scopes explicit and revocable

## 6. OpenClaw-Specific Recommendation
For the first OpenClaw version:
- use `redirect`
- use backend-issued short-lived bridge sessions
- enable auth fallback through `email_code`
- expose tool generation only after successful identity lookup
- postpone project mutation and upload-write scopes

## 7. Rollout Gate
Do not widen capability scope until:
- audit events are visible
- token revocation is tested
- sub-user behavior is verified
- callback replay protection exists
