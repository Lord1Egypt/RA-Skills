# SKILL of Zoom Server-to-Server OAuth REST API

Manage and schedule Zoom meetings REST API directly via Server-to-Server OAuth — no VPS required, no MCP protocol needed.

> EN | [中文](README.zh-cn.md)

## Setup Steps

1. Log in to https://marketplace.zoom.us/
2. From the "Develop" dropdown, select "build app" and create an app of type `Server-to-Server OAuth`
3. Add required OAuth Scopes
4. Get the credentials
5. Activate the app
6. Invoke this SKILL in your AI agent

## Credentials

> ⚠️ **The `ZOOM_CLIENT_SECRET` in `.env` is equivalent to an account-admin password.** Anyone holding the `ACCOUNT_ID + CLIENT_ID + CLIENT_SECRET` triple can mint a 1-hour account-level access token that reads all meeting metadata, cloud recordings, and can delete meetings.
>
> - Never commit `.env` to git. Confirm your IDE, backup tools, and file-sync services (iCloud / Dropbox / OneDrive / Nutstore) are not auto-uploading it.
> - `chmod 600 .env`. The token cache at `~/.zoom-s2s-token.json` is auto-set to `chmod 600` by the script.
> - Use the **minimum scopes** you actually need (see table below). Do not enable `meeting:write:delete`, `cloud_recording:read:*`, or `user:read:list_users` unless required.
> - Create a **dedicated** Server-to-Server App for this skill — do not reuse credentials from other business apps.
> - If leaked: delete the App in Zoom Marketplace → re-create and rotate all four values → `rm -f ~/.zoom-s2s-token.json`.

Edit the `.env` file with your Zoom Server-to-Server OAuth App credentials:

```env
ZOOM_ACCOUNT_ID=yourAccountID
ZOOM_CLIENT_ID=yourClientID
ZOOM_CLIENT_SECRET=yourClientSecret
ZOOM_USER_ID=your_user_email_or_user_id
```


## Required OAuth Scopes

Enable these in your Zoom Marketplace Server-to-Server OAuth App:

| Scope | Purpose |
|-------|---------|
| `meeting:read:list_meetings` | List meetings |
| `meeting:write:create` | Create meetings |
| `meeting:write:delete` | Delete meetings |
| `cloud_recording:read:list_user_recordings` | View cloud recordings |
| `user:read:list_users` | List users |
| `user:read:user` | Get user info |

## Quick Start

```bash
cd ~/.agents/skills/zoom-s2s-oauth/scripts

# List upcoming meetings
python3 zoom-s2s.py list_meetings service@uperform.cn 5 upcoming

# Create a meeting (start_time format: YYYY-MM-DDTHH:MM:SS)
python3 zoom-s2s.py create_meeting "Pancake Discussion" "2026-05-05T10:00:00" 60 Asia/Shanghai

# Get cloud recordings
python3 zoom-s2s.py recordings service@uperform.cn 10
```

## Directory Structure

```
zoom-s2s-oauth/
├── SKILL.md           # AI Agent invocation guide
├── README.md          # This file
├── README.zh-cn.md    # 中文版
├── .env               # Credentials (do NOT commit to git!)
└── scripts/
    └── zoom-s2s.py    # Main script (pure Python3, no external dependencies)
```


## Comparison: MCP vs Server-to-Server REST

| | MCP | Server-to-Server REST |
|---|---|---|
| Requires VPS | ✅ Yes (OAuth callback) | ❌ No |
| Protocol | MCP (JSON-RPC) | Standard REST (pure Python, no deps) |
| Token | User-Managed OAuth | Server-to-Server OAuth |
| Complexity | High (proxy+OAuth) | Low (direct call) |
| Features | Zoom MCP tools | 7 whitelisted CLI actions (list/get/create/delete meeting, get/list user, list recordings) |

If you only need core Zoom meeting/recording features, Server-to-Server REST is simpler.