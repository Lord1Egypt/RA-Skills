---
name: sites-friendify-integration
description: Manage sites.friendify.cloud deployment with auth flow, pending states, and owner-based dashboards
version: 1.0.0
metadata: {"openclaw": {"requires": {"env": ["OPENCLAW_GATEWAY_TOKEN"]}, "primaryEnv": "OPENCLAW_GATEWAY_TOKEN"}}
---

# Sites.friendify.cloud Integration Skill

## Complete Flow
1. **User Request**: User sends "erstelle seite" via Telegram.
2. **AI Action**: AI creates site (Docker + Traefik), generates pending entry with auth code, sends code via Telegram.
3. **User Verification**: User enters code at `sites.friendify.cloud/register`.
4. **Activation**: Site status changes from "pending" to "live", user session linked.
5. **Dashboard**: Only verified user can access `/dashboard` to manage (delete, privacy toggle).

## Features
- **Auth-Protected**: All management requires OpenClaw gateway token authentication.
- **Pending State**: Sites start as pending, only go live after code verification.
- **Owner Dashboard**: `/dashboard` shows only sites owned by the verified user.
- **Privacy Control**: Toggle sites to "private" (hidden from public `/sites` listing).
- **Code Generation**: AI uses `POST /generate-code` to create registration codes.

## API Routes (implemented in OpenClaw server)
| Path | Method | Description |
|------|--------|-------------|
| `/sites` | GET | List public live sites |
| `/dashboard` | GET | Owner's site management dashboard |
| `/register` | POST | Verify code, activate site |
| `/generate-code` | POST | Generate auth code (AI only) |
| `/dashboard/toggle-privacy` | POST | Toggle site privacy |
| `/dashboard/delete` | POST | Delete owned site |

## Usage for AI Agents
When user requests "erstelle seite":
1. Deploy site via Docker Compose with Traefik labels
2. Call `POST /generate-code` with `{name, url, owner: telegramChatId}`
3. Send returned code to user via Telegram
4. Instruct user to visit `sites.friendify.cloud/register` with the code
