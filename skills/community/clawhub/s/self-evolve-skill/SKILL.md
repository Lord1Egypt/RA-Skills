---
name: self-evolve-remote-stats
description: Use curl to query self-evolve.club shared skill rankings, self-evolve personal stats, and update self-evolve.club profile info. Use this when users ask for shared ranking, self-evolve personal info, or profile updates.
---

# Self-Evolve Remote Stats

Use this skill to interact with self-evolve.club API by `curl` only.

- Website: `https://www.self-evolve.club/`
- API base URL: `https://self-evolve.club/api/v1`

## Inputs

- `BASE_URL` (default: `https://self-evolve.club/api/v1`)
- Optional `LIMIT` for leaderboard (default `10`)
- `REQUEST_KEY_ID` is required only for setting username

## Trigger

Use this skill when users want:
- shared skill ranking / leaderboard
- self-evolve personal ranking/profile info
- to set/update self-evolve.club personal profile info

## Commands

Set base URL:

```bash
BASE_URL="https://self-evolve.club/api/v1"
```

### 1) Get overview (no key required)

```bash
curl -s "$BASE_URL/stats/overview"
```

### 2) Get leaderboard (no key required)

```bash
LIMIT=10
curl -s "$BASE_URL/stats/leaderboard?limit=$LIMIT"
```

Notes:
- Response includes masked key only (`masked_request_key_id`), not full key.
- Use `?limit=1..100`.

### 3) Set username (requires your key)

```bash
REQUEST_KEY_ID="<request_key_id>"
USERNAME="alice"

curl -s -X POST "$BASE_URL/users/username" \
  -H "request-key-id: $REQUEST_KEY_ID" \
  -H 'content-type: application/json' \
  -d "{\"username\":\"$USERNAME\"}"
```

Real request example:

```bash
curl -s -X POST "https://self-evolve.club/api/v1/users/username" \
  -H "request-key-id: rk_demo_1234567890abcdef" \
  -H "content-type: application/json" \
  -d '{"username":"kevin001"}'
```

### 4) Get my ranking info (requires your key)

```bash
REQUEST_KEY_ID="<request_key_id>"
curl -s "$BASE_URL/stats/me" \
  -H "request-key-id: $REQUEST_KEY_ID"
```


```bash
curl -s -X POST "https://self-evolve.club/api/v1/users/username" \
  -H "request-key-id: $REQUEST_KEY_ID" \
  -H 'content-type: application/json' \
  -d "{\"username\":\"$USERNAME\"}"
```

## Read key from local plugin file

Default plugin key file location:

```bash
KEY_FILE="$HOME/.openclaw/plugins/self-evolve/remote-request-key.json"
REQUEST_KEY_ID="$(jq -r '.requestKeyId' "$KEY_FILE")"
```

If `jq` is unavailable, use Python:

```bash
REQUEST_KEY_ID="$(python3 - <<'PY'
import json, os
path = os.path.expanduser('~/.openclaw/plugins/self-evolve/remote-request-key.json')
with open(path, 'r', encoding='utf-8') as f:
    print(json.load(f).get('requestKeyId', ''))
PY
)"
```

If `remote-request-key.json` is still not found, inspect plugin config to locate custom key path:

```bash
openclaw config get plugins.entries.self-evolve.config
```

## Safety

- Never print full `REQUEST_KEY_ID` in shared logs.
- Do not send `REQUEST_KEY_ID` for public endpoints (`overview`, `leaderboard`).
- Personal endpoints (`/stats/me`, `/users/username`) must use your own key in header `request-key-id`.
