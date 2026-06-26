# Current System Map

This file lists the current repo surfaces that are already useful for a third-party agent bridge.

## Auth
- `GET /api/auth/captcha/generate`
  - returns CAPTCHA image data for email-code login
- `GET /api/auth/login`
  - starts Google OAuth
- `POST /api/auth/callback`
  - exchanges Google code for local VibeVideo token
- `GET /api/auth/wechat/login-config`
  - gets WeChat QR login configuration
- `POST /api/auth/wechat/callback`
  - completes WeChat login
- `GET /api/auth/captcha/generate`
  - returns CAPTCHA challenge
- `POST /api/auth/captcha/verify`
  - verifies CAPTCHA and can send email-link login
- `POST /api/auth/email-code/send`
  - sends one-time email verification code
- `POST /api/auth/email-code/verify`
  - verifies code and issues local session
- `GET /api/auth/email-verify`
  - magic-link verification redirect
- `POST /api/auth/email-token-setup`
  - writes cookies from a local access token
- `PUT /api/access/tokens/{token_id}`
  - can expire the current saved session token during logout

## Identity
- `GET /api/users/me`
  - returns current user profile, permissions, credits, and plan state

## Access Control
- `GET /api/access/overview`
- `GET /api/access/sub-users`
- `POST /api/access/sub-users`
- `PUT /api/access/sub-users/{sub_user_id}`
- `DELETE /api/access/sub-users/{sub_user_id}`
- `GET /api/access/tokens`
- `PUT /api/access/tokens/{token_id}`

These routes are important because a provider bridge should inherit owner / sub-user semantics rather than building a second permission system.

## Studio Projects
- `GET /api/projects`
  - lists Studio projects for the current user

The OpenClaw runtime uses this endpoint to let the user pick a target project and to build direct project-page links.

## Studio Script Drafts
- `POST /api/scripts/create_async`
  - creates a single Studio episode draft from script text
- `GET /api/scripts/task_status?video_id=...&step=create_script`
  - polls until the Studio draft is ready to open

## Tools
- `POST /api/tools/generate_async`
  - image / video generation task creation
- `GET /api/tools/task_status`
  - polling entry
- `GET /api/tools/fetch_result`
  - fetches generated result payloads

## Service Flags
- `GET /api/service/get-sora2-not-stable`
- `POST /api/service/set-sora2-not-stable`

Useful as an example of small scoped capabilities behind auth.

## Recommended Missing Layer
Planned but not yet present:
- `POST /api/agent-bridge/providers/{provider_id}/session`
- `GET|POST /api/agent-bridge/providers/{provider_id}/callback`

That bridge layer should:
- mint short-lived handoff grants
- constrain provider capability set
- log audit trail
- normalize mixed auth response shapes for external agents
