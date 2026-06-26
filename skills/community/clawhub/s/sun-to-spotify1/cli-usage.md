# Sun CLI Usage

Reference for the `sun` CLI: install, authentication, commands, flags, JSON mode, error handling, and common end-to-end workflows. The CLI generates audio experiences — podcasts, audiobooks, or audio courses — from a prompt.

The CLI is the recommended path. For HTTP-only flows see [http-api.md](http-api.md).

## Installation

The `sun` CLI is self-contained — it ships and works independently of the monorepo. PyPI package name is `sun-cli`; the installed binary is `sun`. Once installed, `sun` is available on `PATH` from any directory.

### Curl installer (recommended)

```bash
curl -fsSL https://sunapp-ai.github.io/sun-to-spotify/install.sh | bash
```

The installer picks the first available Python package manager — `uv` (preferred), then `pipx`, then `pip --user` — and installs `sun-cli` from PyPI. If none of those is on `PATH`, the script prints install instructions and exits 1; install one and re-run.

### uv tool install

If the user already has [uv](https://docs.astral.sh/uv/):

```bash
uv tool install 'sun-cli>=0.2.1'
```

This places `sun` on `PATH` (`~/.local/bin` by default) without requiring a project venv. Update with `uv tool upgrade sun-cli`.

### pip / pipx

Standard Python install:

```bash
pip install 'sun-cli>=0.2.1'
# or, isolated:
pipx install 'sun-cli>=0.2.1'
```

Python 3.10+ required. Only two runtime deps: `httpx` and `typer`.

### Verify

```bash
sun --help
sun --version     # prints "sun-cli <version>"
```

macOS and Linux are first-class. Windows works for the HTTP calls but the credentials file relies on user-directory ACL, not `chmod 0600`.

### Monorepo dev install (internal contributors only)

For working on the CLI itself from inside the `sun-monorepo` checkout:

```bash
uv sync                    # install project dependencies into the venv
uv run sun --help          # invoke the dev build
```

External users do **not** need this; they should use one of the install methods above and run `sun ...` directly. The `uv run sun ...` form only applies inside the monorepo.

If `sun --help` fails after a fresh install, the most common causes are:
- The install dir isn't on `PATH` — check `echo $PATH` and re-source the shell rc.
- The install partially failed — re-run the installer.
- A previous version is shadowing the new one — `which -a sun` to find duplicates.

## Authentication

### Two auth flows

| Endpoint family | Auth | Header |
| --- | --- | --- |
| Token management (`POST/GET/DELETE /v1/public/tokens*`) | Supabase JWT | `Authorization: Bearer <jwt>` |
| Everything else (`/v1/public/courses*`, `/v1/public/whoami`) | Personal API token | `Authorization: Bearer sk_live_...` |

Token-management endpoints reject API-token auth on purpose: a leaked API token cannot mint replacements.

> The underlying HTTP path is still `/v1/public/courses/*` — only the CLI subcommand was renamed to `audio`.

### `sun login` — Supabase login

```bash
sun login                                # opens browser, loopback POST handoff
sun logout                               # forget cached session + saved tokens
sun whoami                               # prints email, user_id, active token name
```

`sun login` opens the user's browser to `https://sunapp.ai/login`, where they can sign in with email + password, create a new account, or reset a forgotten password via the **"Forgot your password?"** link. The webapp posts the resulting Supabase session to a loopback listener the CLI binds; tokens never appear in any URL.

For new accounts, the user signs up with email + password, then clicks the confirmation link Supabase emails them. The link must be opened on the same machine where `sun login` is still running — the original loopback completes the handoff automatically and the CLI logs in. No second `sun login` invocation is needed. The same applies to the password-reset flow: clicking the reset link on the same machine and setting a new password completes the loopback automatically.

The browser flow is the only supported way to log in. There is no `--email`/`--password` or `--no-browser` fallback; headless and CI environments need to authenticate on a machine with a browser first, then carry the resulting credentials file or `SUN_TOKEN` over.

The CLI fetches the Supabase URL and anon key automatically from the public `auth-config` endpoint. The refresh token is persisted at `~/.config/sun/credentials.json` with mode `0600` on Unix.

> Verify the exact env-var names with `sun --help`. The CLI is the source of truth — older docs may use different names.

### `sun tokens` — personal API tokens

```bash
sun tokens create NAME             # prints secret to stdout, saves as active
sun tokens create NAME --no-save   # prints, does not save (CI: capture into a var)
sun tokens list
sun tokens revoke NAME|ID
```

Token shape: `sk_live_<22-char-base32>_<32-char-base32>`. The full secret is shown **once** at creation. `NAME` must match `^[a-z0-9-]+$`, 1-64 chars, unique per user.

Revoke is idempotent — revoking the same token twice still returns `204`. Soft-revoked tokens stay visible in `tokens list` (audit trail) but cannot authenticate.

## Generating audio (podcast / audiobook / audio course)

> `sun courses ...` still works as a hidden alias for backwards compatibility — it prints a one-line deprecation warning on stderr and runs the same command. Use `sun audio` in all new scripts.

### `sun audio create`

```bash
sun audio create \
  --prompt "A 30-minute course on the French Revolution" \
  --duration-minutes 30
# Prints the job_id to stdout.

# Or read the prompt from a file / stdin:
sun audio create --input ./prompt.txt
cat ./prompt.txt | sun audio create

# Block until done and print the result:
sun audio create --prompt "..." --wait
# stderr: status updates (PENDING → PROCESSING → SUCCESS)
# stdout: human summary, or full JSON with --json

# Pick a specific voice:
sun audio create --prompt "..." --voice-id <uuid>

# Register a webhook fired as each episode finishes:
sun audio create --prompt "..." --callback-url https://your.handler/hook
```

Flags:

| Flag | Purpose |
| --- | --- |
| `--prompt TEXT` | Audio prompt — the topic for the podcast / audiobook / audio course. 1-4000 chars. Mutually exclusive with `--input`/stdin. |
| `--input PATH` | Read prompt from a file. |
| `--duration-minutes N` | 5-120. Default 30. |
| `--voice-id UUID` | Optional voice override. |
| `--callback-url URL` | Optional HTTPS URL the server will POST to as each episode finishes. Body: `{event, job_id, episode_id, episode_number, title, audio_url}`. Fire-and-forget — treat as a hint and re-fetch the manifest for truth. |
| `--wait` | Block until SUCCESS / ERROR. Polls with exponential back-off (2s → 30s cap, total 30 min). |
| `--json` | Emit machine-readable JSON to stdout. |

Exactly one prompt source must be provided (`--prompt`, `--input`, or stdin when stdin is not a TTY). Otherwise the CLI errors out.

`--wait` exit codes:
- `0` on `SUCCESS`
- non-zero on `ERROR` or 30-min timeout

### `sun audio status`

```bash
sun audio status <JOB_ID>
sun audio status <JOB_ID> --json
```

Returns the lightweight status payload. Always `200`, even when the job is in `ERROR` (the error sits inside the body, not the status code).

Recommended manual cadence when not using `--wait`: first poll at 5s, then exponential back-off capped at 30s. Typical 30-min generation completes in **60-300s**.

### `sun audio get`

```bash
sun audio get <JOB_ID>                    # JSON manifest to stdout
sun audio get <JOB_ID> --json             # same; explicit
sun audio get <JOB_ID> --out ./my-audio   # download manifest + audio + images
sun audio get <JOB_ID> --partial --out ./my-audio   # works mid-generation
```

`--out DIR` writes:

```
DIR/overview.json                                  # the manifest
DIR/cover.<ext>                                    # top-level cover image
DIR/episodes/001-<slug>.mp3                        # first episode audio
DIR/episodes/001-<slug>.<ext>                      # first episode artwork (optional)
DIR/episodes/002-<slug>.mp3
DIR/episodes/002-<slug>.<ext>
...
```

Filename format: `NNN-<slug>.mp3` where `NNN` is the zero-padded episode number (`001`, `002`, …). The slug is the episode title slugified by the CLI. Slugs are lowercase ASCII with hyphens, max 60 chars, falling back to `"untitled"`. Example: `001-from-manya-to-governess-early-years-and-formative-struggles.mp3` — the `001` prefix marks it as the first episode; sequential ordering is preserved.

Episodes whose `audio_url` is `null` (still uploading, or you used `--partial` and they haven't finished generating) are skipped with a stderr warning. **Re-run the same command** to fetch fresh signed URLs and pick up missing files. The result endpoint re-signs URLs on every read.

`--partial` lets you fetch while the job is still PENDING/PROCESSING. Without it, `audio get` returns `409 not_ready` until the job reaches `SUCCESS`. With it:
- ERROR jobs still 409 — read `sun audio status` for error details.
- Course-level fields (cover URL, description) may be null mid-generation.
- Per-episode `audio_url` and `image_url` are null until each one finishes; the CLI silently skips them.

Re-run `sun audio get --partial --out DIR` on a loop to pick up new episodes as they arrive.

## JSON mode

For agents, always pass `--json`:

```bash
sun --json audio status <JOB_ID>
sun audio create --prompt "..." --json
```

Note: some commands accept `--json` as a global flag (before the subcommand), others as a subcommand flag. Both work in current builds — when in doubt, run `sun --help` or `sun audio create --help`.

In JSON mode:
- All structured output is JSON on stdout.
- Errors emit the bare error envelope: `{"error": {"code": "...", "message": "...", ...}}` and exit non-zero.
- Status updates and progress hints go to stderr (suppressible by redirecting `2>/dev/null`).

## Configuration / env vars

| Variable | Purpose |
| --- | --- |
| `SUN_TOKEN` | Use this API token instead of the credentials file (CI mode). Takes precedence over `~/.config/sun/credentials.json`. |
| `SUN_API_BASE_URL` | Override the default API base URL (e.g. for staging or local dev). |

Confirm the exact names against `sun --help` if the CLI has been rebuilt — env-var names are the most likely thing to drift.

## Error codes

| HTTP | `error.code` | Meaning | Action |
| --- | --- | --- | --- |
| 401 | `unauthorized` | Missing / malformed / unknown / revoked token | `tokens list`, mint a new one, or `login` again |
| 403 | `forbidden` | Anonymous Supabase user trying to mint a token | `login` with email + password |
| 404 | `not_found` | Resource doesn't exist OR is owned by another user | Verify the job/token id |
| 409 | `conflict` | Duplicate token name on `tokens create` | Pick a different name |
| 409 | `not_ready` | `audio get` while job not yet `SUCCESS` (and `--partial` not used, or job is in ERROR) | Poll status; retry, or pass `--partial` |
| 422 | `validation_error` | Body failed schema validation | Read `error.details`; fix the request |
| 429 | `rate_limit_exceeded` | Per-user 24h cap reached | Read `Retry-After`; ask user before waiting |
| 500 | `internal_error` | Server-side failure | Safe to retry with back-off |

Both `409 conflict` and `409 not_ready` share the HTTP status — always read `error.code`, not just the status.


## Common workflows

### Mint token + generate + download (fresh user)

```bash
sun login
sun tokens create laptop
sun audio create \
  --prompt "A 30-minute course on the French Revolution" \
  --duration-minutes 30 \
  --wait
# read JOB_ID from the --wait output, or from --json
sun audio get <JOB_ID> --out ./french-revolution
```

### Stream episodes as they finish (recommended for sun-to-spotify)

```bash
JOB_ID=$(sun audio create --prompt "..." --duration-minutes 30 --json | jq -r .job_id)
OUT="./audio-${JOB_ID:0:8}"

while true; do
  STATUS=$(sun audio status "$JOB_ID" --json | jq -r .status)
  sun audio get "$JOB_ID" --partial --out "$OUT" >/dev/null 2>&1 || true

  # ...do something with newly-arrived episodes in $OUT/episodes/...

  case "$STATUS" in
    SUCCESS) break ;;
    ERROR)   sun audio status "$JOB_ID" --json | jq -r .error; exit 1 ;;
  esac
  sleep 10
done
```

### Generate-and-download (existing token, headless)

```bash
export SUN_TOKEN="sk_live_..._..."

JOB=$(sun audio create --prompt "..." --json | jq -r .job_id)

while true; do
  S=$(sun audio status "$JOB" --json | jq -r .status)
  case "$S" in
    SUCCESS) break ;;
    ERROR)   sun audio status "$JOB" --json | jq -r .error; exit 1 ;;
    *)       sleep 10 ;;
  esac
done

sun audio get "$JOB" --out ./out
```


## Troubleshooting

### `Logged in as ...` but `tokens list` returns 401

Supabase session expired. Run `sun login` again. If the credentials file was edited or the password changed, the refresh path may fail.

### `401 unauthorized` with an API token that worked yesterday

The token may have been revoked. Run `sun tokens list` — revoked tokens show as `[REVOKED]`. Mint a new one.

### `429` even though I haven't hit my limit

Window is rolling 24h, not calendar day. A request at 23:00 yesterday still counts until 23:00 today. `X-RateLimit-Reset` and `Retry-After` are authoritative. Web-app and voice-agent generations do **not** count toward the public-API quota — only public-API requests do.

### Job stuck in `PENDING` for >60s

Worker saturation. Public-API requests share concurrency with the rest of the platform. The job will pick up when a slot frees; this isn't a 503. Keep polling.

### `409 not_ready` even though status shows `SUCCESS`

Briefly possible during the worker's commit window. Wait 1-2 seconds and retry the result endpoint. Alternatively, pass `--partial` to `sun audio get` — it returns 200 mid-generation and won't 409 on the commit-window race.

### `audio_url` is `null` after `SUCCESS`

The episode audio file hasn't propagated to storage yet, or there's a transient storage error for that episode. Re-fetch the result endpoint to refresh signed URLs and try again. `sun audio get --out` already does this — re-run the same command.

### `login` prints "wrong email or password"

Run `login` again with the correct credentials. If the password is forgotten, run `sun login` (browser flow) and click **"Forgot your password?"** on the /login page to send a reset email; click the link on the same machine where `sun login` is still running and set a new password — the loopback completes automatically.

### `login` prints "the server's auth config is invalid"

Server-side misconfiguration, not the user's password. Surface the error to the user; don't retry.

### CLI hangs / connection times out

Check `SUN_API_BASE_URL`. For local dev set it to `http://127.0.0.1:8000`. For staging vs. production, confirm the deployment URL with the user.

### `--json` gives unexpected shape

Some subcommands accept `--json` globally (`sun --json audio status ...`), others as a flag on the subcommand (`sun audio status --json ...`). Both forms exist in current builds; if one doesn't parse, try the other. `sun audio create --help` shows the supported placement.
