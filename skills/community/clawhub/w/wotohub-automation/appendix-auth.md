# Auth Guide

`WOTOHUB_API_KEY` is the primary credential for authenticated WotoHub operations in this skill.

## Execution rules

### Search
Search does not require login by default.

- without token, search uses `openSearch`
- with token, search uses `clawSearch`

### Authenticated actions
These actions require `WOTOHUB_API_KEY`:
- send
- inbox
- auto-reply
- campaign cycle

Privilege note:
- this credential enables user-state operations, including sending and inbox access
- do not share it casually, and do not treat it as equivalent to anonymous search access

## Default headers

### Search without token
```http
Sourceapp: hub
Content-Type: application/json
```

### Search with token or authenticated endpoints
```http
api-key: YOUR_API_KEY
Sourceapp: hub
Content-Type: application/json
```

Default production base:
```text
https://api.wotohub.com/api-gateway
```

## Preflight

Run auth validation before authenticated actions:

```bash
python3 scripts/preflight.py --token YOUR_API_KEY
```

Equivalent API check:

```bash
curl -s "https://api.wotohub.com/api-gateway/user/individual/selUserInfo" \
  -H "api-key: YOUR_API_KEY" \
  -H "Sourceapp: hub"
```

## Search endpoints

### Open search
```bash
curl -s "https://api.wotohub.com/api-gateway/search/openSearch" \
  -H "Content-Type: application/json" \
  -H "Sourceapp: hub" \
  -d '{"platform":"tiktok","pageNum":1,"pageSize":1}'
```

### Authenticated claw search
```bash
curl -s "https://api.wotohub.com/api-gateway/search/clawSearch" \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR_API_KEY" \
  -H "Sourceapp: hub" \
  -d '{"platform":"tiktok","pageNum":1,"pageSize":1}'
```

## Current endpoint coverage

Enabled:
- `openSearch`
- `clawSearch`
- `writeMultipleEmailClaw`, send email
- `selInboxClaw`, inbox list
- `inboxDetailClaw/{id}`, email detail
- `inboxDialogueClaw`, thread detail
- token preflight check

Not enabled by default:
- direct auto-reply execution without the guarded reply flow

Notes:
- reply assist and reply preview are enabled
- low-risk auto-send is only allowed after valid model analysis and full-thread preview flow
- example env files and sample IDs are fixtures only, not production-ready values
