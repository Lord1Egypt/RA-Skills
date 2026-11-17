---
name: reachowl-auth
description: "Connect and verify a ReachOwl account in the ReachOwl MCP server using the user's ReachOwl API token. Use when setting up ReachOwl, when any ReachOwl tool reports a missing or invalid token, when the user pastes a ReachOwl token, wants to log in with email and password, switch accounts, or log out."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, authentication, mcp, setup
---

# ReachOwl Auth

Every other ReachOwl skill needs a verified token on the MCP session. Run this flow first.

Tool names below are the bare MCP names; your client may prefix them (for example `mcp__reachowl__get_user`).

## The token

- A ReachOwl API token looks like `123|abcDEF…` (digits, a pipe, then a random string).
- Users get it in the ReachOwl web app under **ReachOwl MCP Tool**, or from `POST https://reachowl.com/api/v1/authenticate`.
- Being "connected" in Claude, Cursor, or Smithery is **not** a ReachOwl login. The token is what identifies the account.

## MCP tools

| Tool | Purpose |
|------|---------|
| `auth_status` | Is a token stored on this session? (`has_token`; does not call the API) |
| `set_token` | Store a token on this session: `{ token }` |
| `get_user` | Validate the token; returns the user, default `team_id`, and `teams` |
| `authenticate` | Fallback only: `{ email, password }` mints and stores a token |
| `clear_token` | Remove the token from this session |

## Workflow

1. Call `auth_status`.
2. If `has_token` is true (the token came from the connector header), go to step 4.
3. If false, ask the user for their ReachOwl API token and call `set_token { token }`.
   Only if they have no token, offer `authenticate { email, password }`.
4. Call `get_user`. On success, tell the user which account and team are connected and keep `team_id` for later create calls.
5. If `get_user` returns 401, the token is wrong or revoked: ask for a new one and repeat from step 3.
6. To switch accounts or log out: `clear_token`, then start again.

## Rules

- Never echo the full token back in chat; refer to it as `123|…`.
- Reject values that are not `digits|…` (OAuth or JWT strings will not work).
- Prefer `set_token` over `authenticate`; do not ask for a password if the user can provide a token.

## Example

```
User: Connect my ReachOwl account. My token is 12|abc…
→ set_token { token: "12|abc…" }
→ auth_status            // has_token: true
→ get_user               // user + team_id
→ "Connected as ali@example.com (team 7715)."
```
