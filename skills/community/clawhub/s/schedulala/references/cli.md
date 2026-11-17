# CLI reference — `schedulala`

Install: `npx schedulala <command>` (no install) or `npm install -g schedulala`.
Node.js 18+, zero runtime dependencies.

## Auth

```bash
# Device flow — the CLI PRINTS a code + https://schedulala.com/developers/verify;
# the USER opens that URL (sign-in via magic link, SAME email) and enters the
# code. The CLI does not open a browser and never prompts on stdin; it polls
# up to 15 min, then saves the key to ~/.schedulala/config.json.
schedulala init --email you@example.com
# --json emits TWO JSON documents (code+URL first, completion later) —
# stream-parse them; JSON.parse on the whole stdout fails.

# Non-interactive (user already has a key)
export SCHEDULALA_API_KEY=sk_live_...
schedulala whoami --json          # exit 0 = ready · exit 2 = missing/bad key

# Or persist the key without env
schedulala config set api_key sk_live_...
```

Key priority: `--api-key` flag > `SCHEDULALA_API_KEY` env > config file.
Base URL priority: `--base-url` > `SCHEDULALA_API_URL` env > config `base_url`.
Config file: `~/.schedulala/config.json` (mode 0600).

A fresh init key lands on the free taster: 2 connected accounts, 4 free
posts (lifetime — never resets), no posting to X. Existing subscribers get
their paid plan on the same key.

`sk_test_` keys are sandbox: simulated posting, no quota burn. `--sandbox`
errors fast on a live key (sandbox is decided server-side by key prefix).

## Commands

| Command | What it does |
|---|---|
| `init --email <email>` | Device-auth flow, saves API key |
| `whoami` | Current user + plan |
| `post "<content>" --platforms <p,p>` | Create a post (see flags below) |
| `post:list` | List posts; `--status --platform --brand-id --page --limit --after --before` |
| `post:status <id>` | One post's per-platform status; `--watch` polls until published/failed |
| `post:delete <id>` | Cancel scheduled / delete draft |
| `post:retry <id>` | Retry failed platforms |
| `accounts` | Connected accounts; `--platform` filter |
| `accounts:health` | Health-check all accounts |
| `connect <platform>` | Connect link / credential connect (see below) |
| `usage` | Quota + limits |
| `upgrade` | Opens the pricing page |
| `config set\|get\|list\|path` | Manage config |

## `post` flags

Scheduling (pick one): `--now`, `--schedule <ISO8601>`, `--draft`, `--queue`.
**Default when none is given = draft.**

`--platforms` entries are `platform` or `platform=accountId` — the id form is
REQUIRED when more than one account is connected on that platform (the API
400s listing the choices otherwise). Ids come from `schedulala accounts
--json`; `=` is the separator because ids can contain `:` (Bluesky DIDs).

```bash
schedulala post "hi" --platforms "bluesky=did:plc:xyz,twitter" --now --json
```

- `--media <url[,url…]>` — public URLs; type inferred from extension
  (mp4/mov/webm/m4v/avi = video, else image).
- `--platform-content '<json>'` — per-platform text, e.g.
  `'{"twitter":{"content":"Tweet version"}}'`.
- `--platform-settings '<json>'` — per-platform settings, e.g.
  `'{"tiktok":{"privacy":"PUBLIC_TO_EVERYONE","postMode":"direct"}}'`.
  (Content and settings are merged into one platformSettings object;
  settings win on key conflicts.)
- `--first-comment "<text>"` — auto-post this as the first comment ~15s
  after publishing (linkedin, facebook, instagram, youtube, twitter,
  threads, bluesky, mastodon; text + links only).
- `--first-comments '<json>'` — advanced array form
  `'[{"target":0,"text":"…"}]'` (thread targets apply via the threads API).
- `--brand-id <id>`, `--timezone <IANA>`, `--idempotency-key <key>`
  (sent as an `Idempotency-Key` header — use it to prevent duplicate posts),
  `--sandbox`.

```bash
schedulala post "Launch day!" --platforms twitter,linkedin \
  --schedule "2026-08-01T15:00:00Z" \
  --media "https://example.com/banner.jpg" \
  --idempotency-key launch-day-1 --json
```

## `connect <platform>`

12 platforms: twitter, instagram, facebook, linkedin, tiktok, threads,
bluesky, youtube, pinterest, telegram, mastodon, google-business.

- OAuth platforms → prints/opens the browser auth URL.
- bluesky → `--identifier` + `--app-password` (prompts if omitted).
- telegram → `--bot-token` (prompts if omitted).
- mastodon → dashboard-only (per-instance OAuth); the CLI hands off to
  `https://schedulala.com/dashboard?connect=1`.

## Agent usage pattern

```bash
export SCHEDULALA_API_KEY=sk_live_...
POST_ID=$(schedulala post "Hello!" --platforms twitter --now --json | jq -r '.post.id // .post._id')
schedulala post:status $POST_ID --watch --json
schedulala usage --json
```

Best practices: always `--json` (data → stdout; errors →
`{"error":{"message":"…","code":N}}`); check `usage --json` before volume;
use `--idempotency-key`; `post:status --watch` to confirm delivery.
Unknown flags are rejected (strict parsing).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Authentication error (401/403) |
| 3 | Validation error (400) |
| 4 | Not found (404) |
| 5 | Rate limited (429) |
| 6 | Server error (5xx) |
| 7 | Network error |

Env vars: `SCHEDULALA_API_KEY`, `SCHEDULALA_API_URL`, `NO_COLOR`.
