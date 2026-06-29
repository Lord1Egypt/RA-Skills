---
name: skill-hub-query
description: >-
  Query, install, update, and edit AI agent skills on any compatible Skill Hub
  (self-hosted, or any Hub implementing the documented API contract).
  Dual-channel: with a token it uses the authenticated API (full features
  including private skills); without a token it falls back to the unauthenticated
  channel (public skills only). Covers: list newly published skills, search by
  keyword / author / time / source, inspect version history, install or upgrade
  a specific version, and edit a skill's card metadata (display name, summary,
  tags, visibility, applicable position, etc.) via a safety-first GET -> diff ->
  backup -> PUT -> dual-channel verify -> auto-rollback flow. Trigger phrases
  include "what's new on the hub", "search for X skill", "install X",
  "update Y skill", "edit hub card info", "show skill version history",
  "skill-hub-query".
---

# skill-hub-query

- **Version**: 1.1.3
- **License**: MIT
- **Author**: Evan Song (<https://github.com/Songhonglei>)
- **Repository**: <https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-hub-query>
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

> Drive any compatible Skill Hub from the command line with a single,
> predictable interface. Works with self-hosted Hubs that implement the
> [documented API contract](#self-hosted-hub-api-contract).

> **Heads-up**: this tool talks to Hubs that implement the API contract below.
> It does NOT target [clawhub.ai](https://clawhub.ai) — that Hub has its own
> API surface and an official CLI named `clawhub`. Use this tool when you have
> a private or compatible Hub to drive.

---

## Agent workflow

### Dual-channel auto-selection

When the user asks a Hub-related question ("what's on the hub", "install X",
"search for Y"), run `sync.sh` / `query.sh` / `install.sh` directly — the
scripts pick the right channel:

| User state | Channel | Capability |
|------------|---------|------------|
| Token set (env or credentials file) | **OpenAPI** (`<HUB_API_PREFIX>/*` with auth header) | Full features incl. private skills |
| No token | **Legacy fallback** (`<HUB_LEGACY_API_PREFIX>/*` without auth) | Search & install public skills |

When falling back the first time, the script emits a one-shot notice
suggesting the user request a token for long-term stability. After that it
stays silent.

### When to actively suggest the user configure a token

Only when the user explicitly needs to:
- install a **private** skill (search finds it, but download requires auth)
- get **contract-stable, long-term** behavior (legacy fallback may be removed)
- when `doctor.sh` explicitly recommends it

### Setting up the token (after the user provides one)

```bash
# Option A: env var (CI / temporary)
export SKILL_HUB_URL="https://hub.your-company.com"
export SKILL_HUB_TOKEN="<your-token>"

# Option B: credentials file (recommended, cross-skill reusable)
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/skill-hub-query"
cat > "${XDG_CONFIG_HOME:-$HOME/.config}/skill-hub-query/credentials.json" <<EOF
{
  "endpoint":   "https://hub.your-company.com",
  "token":      "<your-token>",
  "authHeader": "Authorization",
  "authScheme": "Bearer "
}
EOF
chmod 600 "${XDG_CONFIG_HOME:-$HOME/.config}/skill-hub-query/credentials.json"
```

Then verify with `bash scripts/doctor.sh`.

> Never echo a full token back to the user, write it outside the credentials
> directory, or commit it to git.

### "What's on the hub for X?"
1. Silently `bash sync.sh` (incremental; zero HTTP if nothing changed)
2. `bash query.sh keyword X`
3. Reply with a user-readable table (**name / author / version / updated / summary**), not raw IDs
4. If ≤5 hits include the summary; if many, list top 10 + total count

### "Install X"
1. `bash sync.sh` then `bash query.sh slug X` to get the latest version and summary
2. **Confirm first**: "Will install **{displayName}** v{latest} (author X). Proceed?"
3. After user approves, run: `bash install.sh X --yes`
4. Without `--yes`, install.sh blocks on stdin for already-installed skills; in non-interactive mode it refuses outright — preventing silent overwrite
5. Show: "installed; will be loaded on the next agent session"

### "Install a batch"
1. Query each slug for version + permission info
2. Show one combined manifest + estimated download size, wait for approval
3. After approval, install **serially** with `install.sh <slug> --yes` (avoid rate limiting); report failures separately

---

## Configuration

> ⚠️ **You MUST configure `SKILL_HUB_URL`** (or `.endpoint` in the credentials
> file) before any network call. There is no baked-in default, because no
> single public Hub is guaranteed to implement this contract. Run
> `bash scripts/doctor.sh` first — it will tell you exactly what's missing.

| Env variable | Default | Purpose |
|---|---|---|
| `SKILL_HUB_PROVIDER` | (unset) | Select a **built-in adapter** for a known public Hub instead of the generic contract. Currently supports `skillhub_cn` (see [Built-in provider: skillhub.cn](#built-in-provider-skillhubcn)). When unset, the generic-contract behavior below applies. |
| `SKILL_HUB_URL` | **(must be set)** | Hub base URL, e.g. `https://hub.your-company.com` (ignored when `SKILL_HUB_PROVIDER` is set) |
| `SKILL_HUB_API_PREFIX` | `/api/v1/skill` | Primary API path |
| `SKILL_HUB_LEGACY_API_PREFIX` | `/api/skill` | Fallback API path |
| `SKILL_HUB_AUTH_HEADER` | `Authorization` | HTTP header name for auth |
| `SKILL_HUB_AUTH_SCHEME` | `Bearer ` | Header value prefix (note trailing space; set to `""` for API-key auth) |
| `SKILL_HUB_TOKEN` | (unset) | API token (takes precedence over credentials file) |
| `SKILL_HUB_TOKEN_FILE` | `${XDG_CONFIG_HOME:-~/.config}/skill-hub-query/credentials.json` | Credentials file |
| `SKILL_HUB_SKILLS_DIR` | (auto-detect) | Where installed skills land |
| `SKILL_HUB_CACHE_DIR` | `${XDG_CACHE_HOME:-~/.cache}/skill-hub-query` | Where the local cache lives |
| `SKILL_HUB_EDIT_PREFIX` | same as `SKILL_HUB_LEGACY_API_PREFIX` | Path prefix for `/edit` and `/detail` (edit.sh only) |
| `SKILL_HUB_DISABLE_EDIT` | `0` | Set to `1` to disable `edit.sh` when your Hub does not implement `/edit` |
| `SKILL_HUB_BACKUP_RETENTION` | `20` | How many recent edit.sh backups to keep per slug (older are pruned) |
| `SKILL_HUB_DOWNLOAD_TIMEOUT` | `120` | curl `--max-time` (seconds) for skill ZIP download in install.sh |
| `SKILL_HUB_OWNER_EMAIL` | (auto: `git config user.email`) | Email used by edit.sh owner pre-check; override if your git identity differs from your Hub identity |

### Skills install directory

Resolved in order: `SKILL_HUB_SKILLS_DIR` -> `~/.claude/skills/` ->
`~/.openclaw/workspace/skills/` -> `~/.config/skills/` (first existing wins).

### Setting up Hub URL + token (one-time)

```bash
echo 'export SKILL_HUB_URL="https://hub.your-company.com"' >> ~/.bashrc
echo 'export SKILL_HUB_TOKEN="<your-token>"' >> ~/.bashrc
source ~/.bashrc
```

Or — for richer per-Hub profiles — use the credentials file:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/skill-hub-query"
cat > "${XDG_CONFIG_HOME:-$HOME/.config}/skill-hub-query/credentials.json" <<EOF
{
  "endpoint":   "https://hub.your-company.com",
  "token":      "<your-token>",
  "authHeader": "Authorization",
  "authScheme": "Bearer "
}
EOF
chmod 600 "${XDG_CONFIG_HOME:-$HOME/.config}/skill-hub-query/credentials.json"
```

> Never commit tokens to git, never hardcode them in scripts, and never
> echo the full token to the user.

---

## Built-in provider: skillhub.cn

[skillhub.cn](https://skillhub.cn) is a China-optimized public skills hub.
Because its API shape differs from the generic contract above, this skill ships
a **built-in adapter** for it. Activate it with:

```bash
export SKILL_HUB_PROVIDER=skillhub_cn        # one-off
# or persist it:
echo 'export SKILL_HUB_PROVIDER=skillhub_cn' >> ~/.bashrc
```

When the provider is active, `SKILL_HUB_URL` / token / API-prefix env vars are
**ignored** — the adapter targets `https://api.skillhub.cn` directly. No token
is needed (all supported operations are public, read-only).

### Capability matrix (skillhub.cn)

| Operation | Command | Supported? |
|---|---|---|
| Search / browse | `query.sh keyword <kw>` · `query.sh today` · `query.sh combo --keyword= --category= --source=` | ✅ live (no local cache) |
| Skill detail | `query.sh slug <slug>` | ✅ |
| Version history | `query.sh versions <slug>` | ✅ |
| Install | `install.sh <slug> [--yes]` | ✅ |
| `sync.sh` | — | ⚪ no-op (live search needs no cache; informational, exit 0) |
| `query.sh author <handle>` | — | ❌ no author-filter param on skillhub.cn (use `keyword`) |
| `edit.sh` (edit card metadata) | — | ❌ not available — see below |

### Why edit is not supported on skillhub.cn

skillhub.cn card metadata (displayName / summary / tags / category) is a
**one-way mirror synced from the upstream source** (clawhub / GitHub). The only
write endpoints the platform exposes are publish / unlist / relist / delete /
claim — **none of which edit card fields**. To change a card, update the
**upstream source** and re-publish/let it re-sync. (This differs from a
generic Hub that implements a `PUT /edit` contract, which `edit.sh` drives.)

### Examples (skillhub.cn)

```bash
export SKILL_HUB_PROVIDER=skillhub_cn
bash scripts/query.sh keyword code           # search
bash scripts/query.sh today                  # browse newest
bash scripts/query.sh slug skill-creator     # detail
bash scripts/query.sh versions skill-creator # versions
bash scripts/install.sh skill-creator --yes  # install
bash scripts/doctor.sh                        # shows the capability matrix
```

---

## Self-check / diagnosis

```bash
bash scripts/doctor.sh
```

`doctor.sh` probes both channels (OpenAPI with token, legacy without) plus
optionally the `/edit` endpoint. If at least one channel works, the skill is
usable.

---

## Cache & performance

All list queries hit a local JSON cache (`${SKILL_HUB_CACHE_DIR}/skill-cache.json`),
parsed with jq (sub-ms).

| Trigger | Sync action |
|---|---|
| Cache missing or corrupt | Full sync |
| User asks "refresh cache" | Forced full sync |
| Routine query | Incremental (records with `updatedAt` newer than cursor) |
| Incremental page 1 entirely new (= 100 records) | Upgrade to full sync |

> Incremental sync does NOT prune removed/withdrawn skills (it only unions
> new records). If you hit a "found in cache but install 404s" case, run
> `bash sync.sh --full`. The full sync log will report "pruned N removed".

---

## Multi-user / shared-host caveat

The legacy channel (no token) identifies callers by **source IP**. On shared
hosts (containers, CI runners), all agents/users share one identity.
`scope=mine` returns the list for that shared identity.

For per-user isolation on shared hosts, configure a per-user `SKILL_HUB_TOKEN`.

---

## Quick reference: scenarios

### Scenario 1: search

| User request | Action |
|---|---|
| "Search for calendar-related skills" | `bash sync.sh && bash query.sh keyword calendar` |
| "What was published this week?" | `bash sync.sh && bash query.sh time this_week` |
| "Anything on 2026-05-20?" | `bash query.sh time 2026-05-20` (single day: 00:00 - 23:59) |
| "Between 5/18 and 5/22?" | `bash query.sh time 2026-05-18:2026-05-22` |
| "Last week by user X?" | `bash sync.sh && bash query.sh combo --since=last_week --author=X` |
| "**Only this account (avoid prefix collisions)**" | `bash query.sh author alice@example.com --exact` |
| "Official skills today?" | `bash sync.sh && bash query.sh combo --since=today --source=official` |
| "Show details of skill XX" | `bash query.sh slug XX` |

### Scenario 2: install / update

| User request | Action |
|---|---|
| "Install calendar" | 1) Check cached version 2) Confirm with user 3) After approval: `bash install.sh calendar --yes` |
| "Update html-go-live to latest" | First `query.sh slug html-go-live` for new version + confirm with user -> after approval `bash install.sh html-go-live --yes` (`--yes` must be user-authorized) |
| "Install html-go-live 2.4.0" | Same confirmation flow -> after approval `bash install.sh html-go-live 2.4.0 --yes` |
| "Search skillhub.cn for X" | `SKILL_HUB_PROVIDER=skillhub_cn bash query.sh keyword X` (no token; see [Built-in provider: skillhub.cn](#built-in-provider-skillhubcn)) |
| "Install X from skillhub.cn" | `SKILL_HUB_PROVIDER=skillhub_cn bash install.sh X --yes` |

> `--yes` is a **user-authorization flag**; an LLM/agent caller **must not add it on its own**.
> The user must explicitly say "yes" / "go ahead" / "install" first; SKILL.md examples in
> automated paths intentionally omit `--yes`.

### Scenario 3: version history

| User request | Action |
|---|---|
| "Version history of html-go-live" | `source scripts/_lib.sh && api_get "${HUB_API_PREFIX}/versions/html-go-live?limit=20" \| jq` |
| "What changed in 2.4.0?" | `api_get "${HUB_API_PREFIX}/versions/html-go-live/2.4.0" \| jq .data.version.changelog` |

### Scenario 4: diagnose / refresh

| User request | Action |
|---|---|
| "skill-hub-query is broken / I can't find anything" | `bash doctor.sh` (probes all channels and reports the precise issue) |
| "Refresh cache / rebuild cache / prune removed skills" | `bash sync.sh --full` |

### Scenario 5: edit a skill's card metadata

Use `edit.sh` to modify the Hub card for a skill you own. **You can only edit
skills you own**; non-owners get 403 from the Hub.

> **Hub compatibility**: This requires your Hub to implement
> `PUT /edit/<slug>` and `GET /detail/<slug>`. If your Hub does not implement
> them, run: `export SKILL_HUB_DISABLE_EDIT=1` and edit.sh will refuse to run
> with an informative message instead of producing confusing errors.

| User request | Action |
|---|---|
| "Show current card info for my-skill" | `bash edit.sh <slug> --show` |
| "Change summary of my-skill to xxx" | First `--show` or `--dry-run` to confirm -> after approval: `bash edit.sh <slug> --summary "xxx" --yes` |
| "Add tags Demo / Test to my-skill" | First `--show` to grab current tags, build the merged list -> after approval `bash edit.sh <slug> --tags "old1,old2,Demo,Test" --yes` |
| "Change visibility of my-skill to public" | High-risk: surface the prompt to the user explicitly (including any Hub-side policy that may silently downgrade) -> after explicit approval add `--yes` |

> **Agent caller rule (same as install.sh)**: `--yes` is a user-authorization
> flag. An agent must NOT add it on its own; the human user must explicitly
> approve. Without `--yes`, `edit.sh` blocks on stdin in a TTY and refuses to
> proceed in non-interactive mode.

> Array fields (tags / scene / business / ...) are **full overwrites**, not
> additive. To append, first `--show` to read the current list, then submit
> the merged list.

> **Supported fields**: see `bash edit.sh --help` for the full list of CLI flags.

> **Safety guarantees (five-stage flow)**:
> 1. **GET** the authoritative current value
> 2. **Owner pre-check** (server-side 403 is the ultimate safety net)
> 3. **Build patch + show diff** (skip PUT if no actual diff)
> 4. **Backup to disk + user confirm** (backups in `${SKILL_HUB_CACHE_DIR}/edit-backups/`, latest 20 per slug)
> 5. **PUT + dual-channel verify with retry + auto-rollback on mismatch**
>    (visibility silent-downgrade is a documented partial-success edge case)

---

## Self-hosted Hub: API contract

Your Hub must implement these endpoints (response envelope
`{code: 200, message: "", data: {...}}`):

```
GET  <endpoint><SKILL_HUB_API_PREFIX>/search?page=N&size=N&orderBy=updatedAt&order=desc
     -> data: {records: [<skill>...], total: <number>}

GET  <endpoint><SKILL_HUB_API_PREFIX>/versions/<slug>?limit=N
     -> data: {items: [{version, changelog, ...}, ...]}

GET  <endpoint><SKILL_HUB_API_PREFIX>/versions/<slug>/<version>
     -> data: {version: {...}}

GET  <endpoint><SKILL_HUB_LEGACY_API_PREFIX>/download/<slug>?version=<v>&track=true
     -> body: zip bytes (Content-Type may be application/octet-stream)
```

Each `<skill>` record minimally contains:

```json
{
  "slug": "string",
  "displayName": "string",
  "summary": "string",
  "owner": {"displayName": "...", "handle": "...", "email": "..."},
  "source": "official|personal|external",
  "updatedAt": <epoch_ms>,
  "latestVersion": {"version": "x.y.z"}
}
```

For `edit.sh` (optional), additionally:

```
PUT  <endpoint><SKILL_HUB_EDIT_PREFIX>/edit/<slug>
     body = JSON patch (any subset of editable fields)
     empty body returns the current snapshot
     -> data: <full skill metadata>

GET  <endpoint><SKILL_HUB_EDIT_PREFIX>/detail/<slug>
     -> data: {skill: <full metadata>}
```

If your Hub uses a different auth scheme, override `SKILL_HUB_AUTH_HEADER` and
`SKILL_HUB_AUTH_SCHEME` (e.g. `SKILL_HUB_AUTH_HEADER=X-API-Key`
`SKILL_HUB_AUTH_SCHEME=""`).

> 📖 **Need the full request/response field reference?** When implementing or
> debugging a self-hosted Hub, read [`references/api.md`](references/api.md) —
> it documents every endpoint's exact parameters, response envelope, and field
> semantics in detail.

---

## File layout

```
skill-hub-query/
├── SKILL.md                          # this file
├── credentials.example.json          # template for the credentials file
├── references/
│   └── api.md                        # detailed API contract reference
└── scripts/
    ├── _lib.sh                       # path discovery + token + curl wrapper (sourced)
    ├── _edit_lib.sh                  # edit.sh internals (sourced)
    ├── doctor.sh                     # one-shot self-check
    ├── sync.sh                       # full / incremental cache sync
    ├── query.sh                      # query the local cache
    ├── install.sh                    # download + safe extract + atomic dir replace
    └── edit.sh                       # five-stage safe metadata editor (optional Hub features)
```

**Cache & credentials (NOT in skill directory, NOT git-tracked):**
```
${SKILL_HUB_CACHE_DIR:-~/.cache/skill-hub-query}/
├── skill-cache.json                  # full skill index (key = slug)
├── skill-cache-meta.json             # sync cursor + metadata
├── skill-versions.json               # locally installed skill versions
└── edit-backups/                     # snapshots before each edit (latest 20 per slug)

${XDG_CONFIG_HOME:-~/.config}/skill-hub-query/credentials.json   (chmod 600)
```

---

## Direct API call pattern (advanced)

```bash
# 1) source the lib (loads token / paths / curl wrapper)
source ./scripts/_lib.sh

# 2) call any API path (api_get auto-routes: token -> OpenAPI; none -> legacy)
api_get "${HUB_API_PREFIX}/search?keyword=calendar&size=20"
api_get "${HUB_API_PREFIX}/versions/html-go-live?limit=10"
api_get "${HUB_API_PREFIX}/versions/html-go-live/2.4.0"

# 3) download a zip (public skills don't need auth; private skills do)
api_download "html-go-live" "2.4.0" "/tmp/x.zip"
```

For direct `curl` calls, pass the auth header when you have a token:
`-H "$(load_auth_header): $(load_auth_scheme)$SKILL_HUB_TOKEN"`.

---

## Error reference

| Error | What to do |
|---|---|
| `[info] No SKILL_HUB_TOKEN configured, falling back to legacy channel` | Normal; consider setting a token for long-term stability |
| `[error] No SKILL_HUB_TOKEN found, and the legacy fallback channel is unavailable` | Both channels are down; run `doctor.sh` to pinpoint |
| `HTTP 401` / token invalid | Token expired or revoked; refresh it or remove it to fall back to legacy |
| `[error] Skill 'X' access denied (HTTP 403, private skill)` | Private skill; configure a token with permission, or ask the owner |
| `[error] Skill 'X' is private (response code=403)` | Same as above (some Hubs return 200 + JSON error) |
| `[error] Skill 'X' not found (HTTP 404)` | Wrong slug / removed; try `query.sh slug X` and possibly `sync.sh --full` |
| `[error] Download failed: X (network error)` | curl-layer failure (network/DNS); check connectivity |
| `zip contains unsafe paths` | Defense against directory traversal; report to Hub maintainer |
| `Extracted content is missing SKILL.md` | Malformed zip; aborted without touching existing install |
| `install failed; rolling back` | Atomic dir replace failed (rare; usually disk full) |
| `X exists and --yes not given` | Agent didn't get user authorization; have the user say "yes" first |
| Cache corruption (jq parse failure) | `sync.sh` rebuilds automatically |
| `edit.sh is disabled because SKILL_HUB_DISABLE_EDIT=1` | Your Hub does not expose `/edit`; unset the var only if it does |

---

## Known limitations

1. The ZIP download endpoint is not part of the formal OpenAPI spec on all Hubs; `install.sh` uses the legacy `/download/<slug>` path (public skills: no auth needed; private: token required).
2. Some legacy fields (`starredAt`, `starred`, `litToday`, etc.) are deprecated and may be missing depending on Hub version.
3. Incremental sync does not prune removed skills (see "Cache" section).
4. The legacy channel is a transition path; for production / long-term use, configure a token.
5. `edit.sh` requires optional `/edit` and `/detail` endpoints; not all Hubs expose them.

---

## Changelog

- **v1.0.1** (2026-06-22): UGLIC patch — all 3 ERR + 4 WARN + 2 INFO fixed.
  - **L1 (ERR)** Fix `require_hub_url` exit-in-cmdsub trap: `endpoint="$(require_hub_url)"` silently dropped the exit because `exit` only kills the subshell. Refactored to `require_hub_url || exit $?; endpoint="$(load_endpoint)"` (api_get / api_download / edit.sh). Adds an explicit doc-comment so callers don't regress.
  - **L2 (ERR)** All curl calls now set `--max-time`: 30s for JSON API (api_get / _edit_lib `PUT`/`GET`) and 120s for ZIP downloads (overridable via `SKILL_HUB_DOWNLOAD_TIMEOUT`). Previously a hung Hub would hang the entire skill indefinitely.
  - **L3 (WARN)** `sync.sh` now validates the first-page response is non-empty JSON before computing `total / pages`, instead of silently reporting "Hub has 0 skill(s)" on failure.
  - **U1 (ERR)** Auto-fixed by L1: misleading legacy-fallback notice no longer appears before the real "no Hub URL" error in sync.sh.
  - **U2 (WARN)** `edit.sh` now calls `require_hub_url` before printing any step output (previously: empty `[edit] Hub URL :` and `[1/5] fetching...` were printed before the actual error).
  - **U3 (INFO)** `load_auth_scheme` now auto-appends a trailing space if non-empty and missing one (so `SKILL_HUB_AUTH_SCHEME="Bearer"` works, not just `"Bearer "`); explicit empty (X-API-Key style) still keeps no space.
  - **I1 (WARN)** Documented previously-undocumented env vars: `SKILL_HUB_BACKUP_RETENTION` (edit.sh backups) and the new `SKILL_HUB_DOWNLOAD_TIMEOUT`.
  - **C1 (WARN)** `sync.sh` and `doctor.sh` now register `trap` EXIT handlers that prune their `mktemp` temp files on any exit path (success / error / Ctrl-C). install.sh already had one.
- **v1.0.0** (2026-06-22): Initial open-source release of `skill-hub-query`.
  Generalized fork of an internal Hub query tool:
  - `SKILL_HUB_URL` / `SKILL_HUB_AUTH_HEADER` / `SKILL_HUB_API_PREFIX` / `SKILL_HUB_LEGACY_API_PREFIX` env-driven configuration (no baked-in default; see Hub compatibility note)
  - XDG-compliant cache and credentials directories
  - Owner pre-check via `git config user.email` (no internal-network-specific paths)
  - `edit.sh` made truly optional via `SKILL_HUB_DISABLE_EDIT=1` for Hubs without `/edit` endpoint
  - Full five-stage safety flow for metadata edits (GET -> diff -> backup -> PUT -> dual-channel verify -> rollback)
  - English-first, no organization-specific identifiers
