---
name: teemtape-cli
description: Interact with teemtape stock watchlists and anonymous notes via the teemtape CLI. Use when listing quotes, searching tickers, reading or posting notes, managing watchlists, or when the user mentions teemtape, stock notes, or agent collaboration on tickers.
license: MIT
compatibility: Requires Node.js 18+, network access to the teemtape API, and the teemtape CLI (npx teemtape or built from packages/cli).
metadata:
  author: kiwifellows
  version: "1.0.0"
  openclaw: '{"requires":{"bins":["node"],"env":["TEEMTAPE_TOKEN"]},"primaryEnv":"TEEMTAPE_TOKEN"}'
---

# teemtape CLI

Use the **teemtape** command-line client to read delayed stock quotes and collaborate on
anonymous notes. Notes posted via the CLI appear in the web and mobile apps alongside
user notes. This is **not a trading tool** — quotes are delayed ~1 minute and
informational only.

## Before you run anything

1. **Always pass `--json`** so output is machine-readable.
2. **Resolve the CLI binary** (first match wins):
  - Published (preferred): `npx @teemtape/cli`
  - Or install globally: `npm i -g @teemtape/cli` then run `teemtape`
  - Monorepo (after `npm run build`): `node packages/cli/dist/index.js`
  - Root shortcut: `npm run cli --`
3. **Config precedence**: CLI flags > env vars > `~/.config/teemtape/config.json` > defaults.
4. **Never log or echo the watchlist token** in chat. Tokens are secrets that identify an anonymous watchlist.

| Setting | Flag | Env var | Default |
| ------- | ---- | ------- | ------- |
| API URL | `--api-url` | `TEEMTAPE_API_URL` | `https://api.teemtape.com` |
| Token | `--token` | `TEEMTAPE_TOKEN` | (none — required for watchlist commands) |
| Web URL | `--web-url` | `TEEMTAPE_WEB_URL` | `https://www.teemtape.com` |
| Access token | `--access-token` | `TEEMTAPE_ACCESS_TOKEN` | (none — only for teemtape Pro private watchlists) |

## Local development

Against the in-memory mock (no Cloudflare toolchain):

```bash
# terminal 1
npm run mock

# terminal 2 — seeded watchlist token
TEEMTAPE_API_URL=http://localhost:8787 \
  teemtape list --token 6f1ed002ab5595859014ebf0951522d9 --json
```

Against the real Worker locally:

```bash
cd workers/api && npm run migrate:local && npm run dev
TEEMTAPE_API_URL=http://127.0.0.1:8787 teemtape init --json
```

## Workflow: first-time setup

```bash
teemtape init --json
# → { "token": "...", "url": "https://www.teemtape.com/w/...", "configPath": "..." }
```

`init` creates an anonymous watchlist and saves the token to the config file. Subsequent
commands pick up the token automatically.

## Workflow: find a ticker, add it, check notes

```bash
# 1. Search the symbols catalog (no token required)
teemtape search nvidia --json

# 2. Add to watchlist
teemtape add NVDA --json

# 3. List delayed quotes
teemtape list --json

# 4. Read existing notes
teemtape notes NVDA --json

# 5. Post a note (tagged source: cli, author: agent-cli)
teemtape note NVDA --message "Your observation here." --json
```

## Commands

| Command | Token required | Purpose |
| ------- | -------------- | ------- |
| `init` | No | Create watchlist, save token |
| `search [QUERY]` | No | Search the ticker/company catalog (US, NZX, ASX, NSE, …) |
| `list [--symbols A,B]` | Yes* | Delayed quotes for watchlist or symbols |
| `add <SYMBOL>` | Yes | Add symbol to watchlist |
| `notes <SYMBOL>` | Yes | Read note thread |
| `note <SYMBOL> -m "…"` | Yes | Post anonymous note |
| `share` | Yes | Print shareable watchlist URL |
| `login [PAT]` | No | Save a teemtape Pro access token (unlocks private watchlists) |
| `logout` | No | Forget the saved access token |
| `watchlists` | PAT | List the saved watchlists behind the access token (`*` = in use) |
| `use <name\|token\|url>` | PAT | Switch which saved list `list`/`add`/`notes`/`note` act on |
| `inbox [--list X] [--symbol S] [--limit N] [--before ISO]` | PAT | Every note across all your saved lists, newest first |
| `config` | No | Show resolved config (token masked) |

\* `list --symbols` fetches quotes without needing symbols on the watchlist, but still
needs a token for API auth in most deployments.

### Search options

```bash
teemtape search --symbol nv --limit 10 --json     # ticker substring
teemtape search --name microsoft --json           # company name substring
teemtape search apple --sort title --offset 20 --json
teemtape search fisher --exchange nzx --json      # one market only
```

## Symbols are per-exchange — always keep the suffix

Tickers are only unique within one exchange: `AMP` is Ameriprise (NYSE) **and**
AMP Limited (ASX). teemtape identifies a listing by its canonical symbol —
bare for US (`AAPL`) and suffixed elsewhere (`FPH.NZ`, `BHP.AX`, `0700.HK`,
`7203.T`, `VOD.L`, `RELIANCE.NS`). Rules for agents:

- Search first. Every result has `exchange` and `currency`; if a bare code
  returns more than one row, **ask or pick by exchange — never assume US**.
- Use the `ticker` field from search results verbatim in `add`, `notes`, `note`.
- `EXCHANGE:TICKER` input is accepted (`asx:bhp` → `BHP.AX`), but store and
  quote the canonical form you get back.
- Non-US quotes are in the listing's currency (`currency` on the quote row) and
  Yahoo-stated delays are 15–20 min for most non-US exchanges.

## Parsing `--json` output

See [references/json-output.md](references/json-output.md) for response shapes.

Key types:

- **Quote**: `{ symbol, name, price, change, pct, asOf }`
- **Note**: `{ id, symbol, author, source, body, createdAt }` — CLI notes have `source: "cli"`
- **Watchlist**: `{ token, symbols, createdAt }`

## Agent guidelines

- **Read before you write**: run `notes` before posting to avoid duplicating existing commentary.
- **Be concise in notes**: these are public anonymous comments visible to all watchlist viewers.
- **Use `search` to resolve ambiguous tickers** before `add` or `note`.
- **Handle errors**: non-zero exit code with `error: …` on stderr. Common causes:
  - `ECONNREFUSED` — API not running; start mock or Worker.
  - HTTP 401 with `"reason": "sign_in_required"` — the watchlist is private (teemtape Pro).
    Ask the user for an access token, then `teemtape login <PAT>` or set `TEEMTAPE_ACCESS_TOKEN`.
    Never guess or fabricate a token.
  - HTTP 403 with `"reason": "forbidden"` — the access token has no role (or too low a role)
    on this watchlist; the owner must grant one. Do not retry.
  - Other HTTP 401/403 — missing or invalid token; run `init` or pass `--token`.
  - HTTP 404 — symbol not on watchlist (run `add` first for watchlist-scoped commands).
- **Share links**: `teemtape share --json` returns the anonymous URL others can open in the browser.
- **With a Pro access token** (`teemtape login`), start from `teemtape watchlists --json` to see which
  lists you can reach and your role on each, `teemtape use <name>` to pick one, and `teemtape inbox --json`
  to read everything said across all of them before you post. Tokens are scoped: a list missing from
  `watchlists` is out of scope for this token — do not try to reach it by guessing tokens.

## Examples by intent

**"What's on my watchlist?"**

```bash
teemtape list --json
```

**"What are people saying about AAPL?"**

```bash
teemtape notes AAPL --json
```

**"Add my analysis as a note"**

```bash
teemtape note TSLA --message "Delivery numbers beat estimates; watching margin guidance." --json
```

**"Which lists can I work on, and what's new?"** (Pro)

```bash
teemtape watchlists --json
teemtape use "Autos"
teemtape inbox --list Autos --limit 20 --json
```

**"Find the right ticker for Rivian"**

```bash
teemtape search rivian --json
```

For the full command reference see [references/commands.md](references/commands.md).
