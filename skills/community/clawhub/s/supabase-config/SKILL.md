---
name: supabase-config
description: 'Change hosted Supabase Auth settings safely: read, diff, PATCH only named keys (writes remote config). Use when config push or a redirect broke magic links. Trigger on "magic link goes to localhost".'
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["python3"],"env":["SUPABASE_ACCESS_TOKEN"]},"homepage":"https://supabase.com/docs/reference/api/introduction"}}
---

# Supabase Config — Change One Auth Setting, Not Twenty

`supabase config push` does not push "your changes". It builds a **complete** Auth config from `config.toml` plus the CLI's built-in template and sends it, so every scalar you did not declare goes out at its local-dev default: `site_url = http://127.0.0.1:3000`, email confirmations off, 6-character passwords. The Management API has a partial `PATCH` instead. This skill reads, diffs, patches only the keys you name, then re-reads and fails if anything else moved.

Sources: CLI source at tag `v2.116.0` (`pkg/config/auth.go`, `updater.go`, `templates/config.toml`, the `config push` side-effects doc), Auth server source (`internal/utilities/request.go`), official docs checked 2026-09-30. Facts marked *observed* come from one production migration (CLI 2.116.0, Sept 2026). Re-check them after a CLI upgrade.

## When to Use

| Trigger | Go to |
|---|---|
| "after `config push` magic links go to localhost / signup is open / confirmations stopped" | §1 then §4 |
| "change one Auth setting on the hosted project" | §2 |
| "magic link lands on the homepage instead of `/auth/callback`" | §4 |
| "add the staging / preview URL to redirects" | §4 `add-redirect` |
| "turn on leaked-password protection", a setting missing from `config.toml` | §5 |
| "`db reset --linked`", "run psql against prod", "tests fail with `Name has no usable address`" | §6 |
| "local lint is clean but the remote advisor complains" | §6 advisors |

## Access and data

| Item | What this skill needs |
|---|---|
| Credentials | `SUPABASE_ACCESS_TOKEN`: a personal access token (`sbp_…`) from the dashboard, or a fine-grained token with `auth_config_write` + `project_admin_write`. Env var only. The script sends it in a header, in-process: never in argv, never printed, never written to disk. |
| Network out | `https://api.supabase.com` only. `--api-base` accepts nothing else except an `http://` loopback address (test servers). |
| Writes | **Remote Auth configuration** via `PATCH /v1/projects/<ref>/config/auth`, only with `--apply`. Without it, every write command is a dry run. Nothing else is written, locally or remotely. |
| Data persisted | None. `show` prints to stdout with secret-looking string fields (`*secret*`, `smtp_pass`, `*_key`, `*auth_token*`) replaced by `<redacted>`. |

The script is `scripts/authcfg.py` (stdlib, Python 3.9+). Before first use, edit its `PINNED_REF` line to your project ref (§3).

## 1. What `config push` actually sends

For each service the CLI does GET → diff → print the diff → prompt `[Y/n]` → write. The Auth write body is not the diff: it is `ToUpdateAuthConfigBody()` over the whole local config, and the local config is the embedded template merged under your `config.toml`. **An undeclared key is not "unchanged", it is "template default".**

| Undeclared in `config.toml` | Value pushed | Effect on a hosted project |
|---|---|---|
| `auth.site_url` | `http://127.0.0.1:3000` | Every magic link that fails the allow-list lands on localhost (§4) |
| `auth.additional_redirect_urls` | `["https://127.0.0.1:3000"]` → `uri_allow_list` | Your real callback URLs are gone |
| `auth.email.enable_confirmations` | `false` → `mailer_autoconfirm: true` | Sign-ups are confirmed without email proof |
| `auth.enable_signup` | `true` → `disable_signup: false` | Public sign-up reopens on an invite-only app |
| `auth.minimum_password_length` / `password_requirements` | `6` / `""` | Password policy weakened |
| `auth.jwt_expiry`, `email.otp_expiry` | `3600` | Custom session and OTP lifetimes reset |
| `auth.rate_limit.*` | template values (`sign_in_sign_ups = 30`, …) | Tuned rate limits reset |
| `[auth.external.apple]` | `enabled = false` (it is in the template) | Apple sign-in configured in the dashboard is switched off |

Sent **only when declared** (nil-pointer sections, the CLI assumes platform defaults should not change): email templates and subjects, `[auth.email.smtp]`, `[auth.captcha]`, hooks, and every external provider other than Apple. Settings with no `config.toml` key at all (§5) are never sent.

Traps around the prompt:

- `--yes` and `--output-format json` / `stream-json` auto-confirm.
- Declining the prompt exits **0**, like a successful push. The exit code does not tell you whether anything was written.
- The ref resolves `--project-ref` → `SUPABASE_PROJECT_ID` → `supabase/.temp/project-ref`. A stale env var wins over the link.
- A `[remotes.<name>]` block whose `project_id` equals the target is merged over the base before the push.
- `[db.settings]` has no gate: it is diffed and written (`PUT …/config/database/postgres`) on every push.

If you must use `config push`: declare **every** Auth scalar you care about, copying values from `authcfg.py show`, run it interactively, read the diff, and answer `n` the first time.

## 2. The partial PATCH

`PATCH /v1/projects/{ref}/config/auth` is partial (every body field is optional; only fields sent change). The script adds what the endpoint doesn't: a read-before, a typed diff, a dry run, and a read-after that proves nothing else moved.

```bash
export SUPABASE_ACCESS_TOKEN=...          # from a secret store, not a file in the repo
S=scripts/authcfg.py; REF=<your-20-letter-ref>

python3 $S show --ref $REF --keys site_url,uri_allow_list,disable_signup,mailer_autoconfirm
# Output: {"site_url": "https://app.example.com", "uri_allow_list": "https://app.example.com/auth/callback", ...}

python3 $S patch --ref $REF --set jwt_exp=7200 --set disable_signup=true
# Output: Project <ref> — auth config diff:
# Output:   disable_signup: false -> true
# Output:   jwt_exp: 3600 -> 7200
# Output: DRY RUN. Nothing sent. Re-run with --apply to PATCH.

python3 $S patch --ref $REF --set jwt_exp=7200 --set disable_signup=true --apply
# Output: VERIFIED: 2 field(s) changed, nothing else moved.
```

| Rule enforced | Why |
|---|---|
| The key must exist in the GET response | A typo (`jwt_expiry` is the TOML name, `jwt_exp` the API name) would otherwise be silently ignored or rejected |
| Value typed like the remote field: `true`/`false` for booleans, numbers for numerics, literal text for strings (`smtp_port=2525` stays `"2525"`) | `disable_signup=yes` must not become a truthy string |
| Unchanged keys are dropped from the body; an all-unchanged request sends nothing | The body contains the change and only the change |
| `--body file.json` requires `--keys a,b` listing exactly its keys | A generated body cannot smuggle an extra field |
| After `--apply`: re-GET, every requested key must hold its new value, every other key must equal its before-value | Exit **3** otherwise, with the list. A server-side side effect is caught, not assumed away |

Exit codes: `0` ok · `1` advisors at or above `--fail-on`, or a redirect that falls back · `2` refused, nothing sent · `3` written but verification failed: read the list and fix by hand · `4` API or network error.

API names differ from TOML names: `jwt_exp` (TOML `jwt_expiry`), `uri_allow_list` (TOML `additional_redirect_urls`, a list; API is one comma-separated string), `disable_signup` (negated `enable_signup`), `mailer_autoconfirm` (negated `enable_confirmations`). `show` gives the authoritative list.

## 3. The ref guard lives in code, not in the environment

A guard that reads its allowed target from `.env` validates whatever `.env` points to: it checks the target against itself. `PINNED_REF` is a constant in the script; `--ref` must equal it. Changing project means editing one line, which shows up in a diff and a review.

| Input | Result |
|---|---|
| `PINNED_REF` still the placeholder, empty, or not 20 lowercase letters | Refused before any request |
| `--ref` absent, malformed, or different from `PINNED_REF` | Refused before any request |
| `SUPABASE_ACCESS_TOKEN` absent, blank, or containing whitespace | Refused |
| `--api-base` not `https://api.supabase.com` and not `http://` loopback (lookalike hosts included) | Refused: the token never leaves for another host |
| GET returns `{}`, `[]`, or non-JSON | Refused or API error: no diff against nothing |

Apply the same pinning to CLI commands that write (§6).

## 4. Magic links: `site_url` and `uri_allow_list`

The Auth server decides where a link lands with this chain (`GetReferrer`): `redirect_to` if valid, else the `Referer` header if valid, else **`site_url`**. No error, no log line on the client: a rejected redirect looks like "the link opens the homepage".

| Rule (Auth server source) | Consequence |
|---|---|
| Same scheme + host as `site_url`, same port (any port on localhost/loopback) → allowed without any allow-list entry | Only other hosts need entries |
| An IP-literal host is allowed only if loopback; a decimal-only host is always rejected | `http://127.0.0.1:5173` always passes; a LAN IP never does |
| Allow-list entries are globs with separators `.` and `/`: `*` stops at `.` and `/`, `**` matches anything, `?` one non-separator char | `https://*.example.com` does not match `a.b.example.com`; `…/callback` does not match `…/callback/` |
| Matched against the full URL minus `#fragment`, **query string included** | Exact entry `https://x.example.com/cb` rejects `…/cb?next=/dash`. Use `…/cb**` (`?` is a one-character wildcard, not a literal) |
| `uri_allow_list` is one string; a PATCH replaces it whole | Sending "the new URL" deletes every other entry |

```bash
python3 $S check-redirect "https://staging.example.com/auth/callback?next=/x" --ref $REF
# Output: FALLBACK: no allow-list entry matches (query string included). The link will land on site_url (https://app.example.com), silently.
python3 $S check-redirect "https://x.example.com/cb" --site-url https://app.example.com --allow-list "https://x.example.com/cb**"   # offline
# Output: ACCEPTED: matches allow-list entry https://x.example.com/cb**
python3 $S add-redirect "https://staging.example.com/auth/callback**" --ref $REF --apply
# Output: VERIFIED: 1 field(s) changed, nothing else moved.
```

`add-redirect` appends and keeps every existing entry. `patch --set uri_allow_list=…` refuses to drop an existing entry unless you pass `--allow-remove`. Entries with commas or whitespace are refused (they would split the list). The checker models `*`, `**`, `?` only; a pattern with `[…]`, `{…}` or `\` is refused: test those against the real server.

Production: `site_url` = the page that handles the session (not a marketing homepage), exact callback paths in the list, `**` only on preview domains you own.

## 5. Settings `config.toml` cannot express

Some Auth fields exist in the API and have no key in the CLI config schema. Example: `password_hibp_enabled` (leaked-password protection). Zero occurrences in the v2.116.0 config template, the Go config and the TS port. *Observed:* the API rejects it on the Free plan with an explicit message; it works on Pro.

```bash
python3 $S patch --ref $REF --set password_hibp_enabled=true --apply
```

How to spot one: the key appears in `show` but `grep -ri <key> supabase/config.toml` and the CLI template find nothing. Such a field is set only through the API or dashboard, and `config push` never resets it. Note it where the team documents config, or the next person will look for it in `config.toml`.

## 6. Remote database work

| Command / situation | What to know |
|---|---|
| `supabase db reset --linked` | Docs: "a SQL script is executed to identify and drop all user created entities in the remote database", then migrations and seed. A seed with test users and known passwords becomes live on a reachable project. Human-run only, after the pin check below |
| `db.<ref>.supabase.co` (direct host) | *Observed:* IPv6-only (no A record). Host tools reach it; containers the CLI starts (`pg_prove` in `supabase test db`, `pg_dump` in `supabase db dump`) fail with `Name has no usable address` and `Tests: 0`: DNS, not your tests. Use the pooler with `--db-url` |
| Pooler hostname | Take it from `supabase/.temp/pooler-url` after `supabase link`. *Observed:* guessing the `aws-0-<region>` prefix hit a dead name; the project was on `aws-1-` |
| Docker on a "cloud-only" machine | `pg_dump` and `pg_prove` still run in containers: a Docker engine must be up, the local stack need not be |
| DSN in argv | Visible in `ps` to every local user. One `psql` entry point, password in the child's env |
| Remote advisors | Differ from local: plan-level settings (leaked-password protection) and grants only exist remotely. Gate on `supabase db advisors --linked --fail-on warn` or `authcfg.py advisors --fail-on WARN` |
| Shared remote DB for tests | Storage objects persist across `db reset` (the local container started empty). Append-only audit tables grow with every run: an assertion `count = N` becomes `count >= N` |

```bash
# Pin check before any --linked write. Pinned here, compared to both ref sources the CLI reads.
PINNED=<your-20-letter-ref>
linked=$(cat supabase/.temp/project-ref 2>/dev/null)
[ -n "$linked" ] && [ "$linked" = "$PINNED" ] || { echo "REFUSE: linked ref is '${linked:-none}'"; exit 2; }
[ -z "${SUPABASE_PROJECT_ID:-}" ] || [ "$SUPABASE_PROJECT_ID" = "$PINNED" ] || { echo "REFUSE: SUPABASE_PROJECT_ID overrides the link"; exit 2; }

# Single psql entry point: password via env of the child only, never in argv.
psql_remote() {
  : "${SUPABASE_DB_PASSWORD:?}" "${POOLER_HOST:?from supabase/.temp/pooler-url}"
  PGPASSWORD="$SUPABASE_DB_PASSWORD" psql \
    "host=$POOLER_HOST port=${POOLER_PORT:-5432} dbname=postgres user=postgres.$PINNED sslmode=require" \
    -v ON_ERROR_STOP=1 "$@"
}

python3 $S advisors --ref $REF --fail-on WARN
# Output: [security] 2 finding(s)
# Output:   WARN  auth_leaked_password_protection — Leaked Password Protection Disabled
```

When code (tests, scripts) and the CLI link can point at different projects, check both against the pin in one preflight. Otherwise a verification can pass green after testing two different databases.

## 7. Selftest

```bash
python3 scripts/authcfg.py --selftest
# Output: 57/57 passed
```

It starts a mock Management API on `127.0.0.1`, never a real project. Hostile fixtures: placeholder, empty and `None` pin; absent, malformed and foreign ref; absent and blank token; foreign and lookalike API hosts; GET returning `{}`, `[]`, HTML; unknown key; wrong types; empty and relative `site_url`; allow-list shrink; `--body` with an extra key, `{}`, `null`; a server that resets another field on PATCH; a server that ignores the PATCH; secrets and token absent from all output. Each guard was removed once (ref match, host check, post-verify both ways, allow-list shrink, body keys, redaction, empty GET, type check). The selftest failed every time. Run it again after any edit.

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `REFUSED: PINNED_REF is not set` | First use | Edit the constant, commit the one-line diff |
| `unknown field(s) jwt_expiry` | TOML name used | API name from `show` (`jwt_exp`) |
| `HTTP 401` | Token missing scope, revoked, or not a PAT | New PAT from the dashboard; fine-grained tokens need `auth_config_write` + `project_admin_write` |
| API error naming the plan | Feature gated by plan (§5) | Upgrade or leave it off; nothing was written |
| Exit 3, `changed without being requested` | Server-side coupling or a concurrent edit | Read the listed fields, restore with one `patch`, find who else writes |
| Link lands on homepage | Redirect rejected, fallback to `site_url` | `check-redirect` with the exact URL the app sends |
| Link lands on `127.0.0.1:3000` | A `config push` with undeclared `site_url` | `patch --set site_url=…`, then §1 before the next push |

## Scope

This skill ONLY: reads a hosted project's Auth config; PATCHes keys you name, after a dry-run diff and with `--apply`; re-reads to verify; predicts redirect acceptance; reads remote advisors; documents which CLI commands write remotely and how to pin them.

This skill NEVER: runs `config push`, `db push --linked` or `db reset --linked` itself; sends a key you did not request; sends the token to a host other than the official API or loopback; prints or stores the token or secret fields; reads its target ref from the environment or a `.env` file.

*Alexandre Bloch · ClawHub @alexbloch-ia*
