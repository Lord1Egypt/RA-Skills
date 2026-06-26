# zsxq-digest

## What it is

`zsxq-digest` is an OpenClaw skill that turns recent Knowledge Planet updates into either:
- a short daily triage digest
- or a richer per-circle stream digest

It helps answer:
- what changed
- which posts are worth opening first
- what each circle has been discussing recently

It is designed for **private membership content**. The public skill contains workflow + scripts, but **never** includes your personal token, cookies, or planet data.

## MVP direction

First-run authorization:
- **guided auth bootstrap**

Primary steady-state mode:
- **local private session / token**

Secondary mode:
- **browser relay recovery / verification**

Experimental only:
- plain fetch fallback

## Why token-first

Many OpenClaw users run agents on a VPS, Mac mini, or other remote host, while logging in to Knowledge Planet from a different device. A local gitignored token file is often more practical than requiring a live browser relay all the time.

That said, a usable product needs a smoother **first-run authorization** experience. This repo therefore distinguishes between:
- **bootstrap**: how the host gets an initial reusable session/token
- **steady state**: how later digest runs work after that token already exists

## Security warning

Do not commit or publish:
- `state/session.token.json`
- raw cookies
- copied request headers containing private auth material
- private planet exports

Recommended rule:
- keep all runtime state under gitignored `state/`

## Local token file

Recommended file:
- `state/session.token.json`

Recommended schema:

```json
{
  "kind": "cookie",
  "cookie_name": "zsxq_access_token",
  "cookie_value": "<private>",
  "domain": ".zsxq.com",
  "source": "browser-devtools-copy",
  "captured_at": "2026-03-08T14:30:00+08:00",
  "user_agent": "optional",
  "note": "stored locally only; do not commit"
}
```

## Quick start

### 1. List joined groups

```bash
python3 scripts/collect_from_session.py \
  --token-file state/session.token.json \
  --mode groups
```

### 2. Fetch one group's recent topics

```bash
python3 scripts/collect_from_session.py \
  --token-file state/session.token.json \
  --mode group-topics \
  --group-id 123456789 \
  --count 20 \
  --output /tmp/zsxq-items.json
```

### 3. Build a tracked groups config first

A practical daily workflow is to export a starter `state/groups.json` from the live token, then locally disable planets you do not want in the digest.

```bash
python3 scripts/export_groups_config.py \
  --token-file state/session.token.json \
  --output state/groups.json
```

You can also pre-disable known expired or ignored planets while exporting:

```bash
python3 scripts/export_groups_config.py \
  --token-file state/session.token.json \
  --output state/groups.json \
  --disable-group-id 28885882511511
```

### 4. Fetch multiple groups in one run

```bash
python3 scripts/collect_from_session.py \
  --token-file state/session.token.json \
  --mode multi-group-topics \
  --group-id 123456789 \
  --group-id 987654321 \
  --exclude-group-id 555555555 \
  --output /tmp/zsxq-multi.json
```

You can also drive this from a groups file so expired or disabled planets are skipped before collection:

```json
[
  {"group_id": 28888122422841, "name": "学不完根本学不完", "enabled": true},
  {"group_id": 28885882511511, "name": "老蒋的靠谱书屋", "enabled": false, "status": "expired"}
]
```

```bash
python3 scripts/collect_from_session.py \
  --token-file state/session.token.json \
  --mode multi-group-topics \
  --groups-file state/groups.json \
  --output /tmp/zsxq-multi.json
```

### 4. Deduplicate against bounded cursor state

```bash
python3 scripts/dedupe_and_state.py \
  /tmp/zsxq-multi.json \
  --cursor state/cursor.json \
  --access-mode token \
  --write-new-items /tmp/zsxq-new.json
```

### 5. Render a simple legacy digest

```bash
python3 scripts/digest_updates.py /tmp/zsxq-new.json
```

### 6. Render the new stream digest (recommended)

First enrich the normalized items for per-circle scoring and layout:

```bash
python3 scripts/enrich_stream_items.py \
  /tmp/zsxq-new.json \
  --output /tmp/zsxq-stream.json
```

Then render the stream digest markdown:

```bash
python3 scripts/render_stream_digest.py \
  /tmp/zsxq-stream.json
```

### 7. Or run the full legacy pipeline in one command

```bash
python3 scripts/run_digest_pipeline.py \
  --source token \
  --token-file state/session.token.json \
  --group-id 123456789 \
  --group-id 987654321 \
  --cursor state/cursor.json \
  --print-digest
```

### 8. Or run the full stream pipeline in one command (recommended)

```bash
python3 scripts/run_stream_pipeline.py \
  --source token \
  --token-file state/session.token.json \
  --groups-file state/groups.json \
  --cursor state/cursor.json \
  --print-digest
```

### 8.1 Private enhancement mode for news-list circles

For circles that often post grouped news/link lists (for example an editor-style circle), you can enable a **private enhancement mode** that keeps the public default untouched but renders those news-list entries as cleaned copied lines instead of forcing a second summarization layer.

```bash
python3 scripts/run_stream_pipeline.py \
  --source token \
  --token-file state/session.token.json \
  --group-id 88888851184282 \
  --cursor state/cursor.json \
  --private-news-list-mode \
  --print-digest
```

Design intent:
- public default remains neutral and generic
- private mode can be tuned for specific circles without changing the public product contract

### 9. Browser fallback from a captured JSON snapshot

```bash
python3 scripts/collect_from_browser.py browser-capture.json --output /tmp/zsxq-browser.json
```

### 10. Browser-tool recovery path

When token mode fails:
1. use OpenClaw browser tooling to open a logged-in Knowledge Planet page
2. confirm the visible feed with `browser.snapshot`
3. use the starter function in `scripts/browser_capture_starter.js` with `browser.act(... evaluate ... )`
4. save the returned JSON as `browser-capture.json`
5. run the normal browser-file pipeline

```bash
python3 scripts/run_stream_pipeline.py \
  --source browser-file \
  --browser-input browser-capture.json \
  --cursor state/cursor.json \
  --print-digest
```

### 11. Unified browser bootstrap workflow

Use the single workflow entrypoint for first-run browser-assisted authorization.

Step 1: prepare / probe QR state and update `state/auth-bootstrap.json`:

```bash
python3 scripts/run_browser_bootstrap.py run \
  --zsxq-ws-url ws://127.0.0.1:18800/devtools/page/ZSXQ \
  --wechat-ws-url ws://127.0.0.1:18800/devtools/page/WECHAT
```

Typical result at this stage:
- `QR_READY` → send the QR to the user
- `AUTH_WAITING_CONFIRMATION` → user scanned, wait for confirmation
- `QR_EXPIRED` → refresh and resend
- `AUTH_CAPTURE_UNVERIFIED` → QR flow is gone; try cookie capture next

Step 2: after scan/confirmation, reuse the same entrypoint and let it capture cookies, finalize `state/session.token.json`, and verify token mode:

```bash
python3 scripts/run_browser_bootstrap.py run \
  --zsxq-ws-url ws://127.0.0.1:18800/devtools/page/ZSXQ \
  --wechat-ws-url ws://127.0.0.1:18800/devtools/page/WECHAT \
  --capture-ws-url ws://127.0.0.1:18800/devtools/page/LOGGED_IN_ZSXQ \
  --auto-finalize
```

Default outputs:
- `state/auth-bootstrap.json`
- `state/captured-cookies.json`
- `state/session.token.json`
- `state/groups.probe.json`

If token capture succeeds but the immediate verification query hits a transient API-side failure, the workflow still returns `status: ok` and preserves a `verification_warning` field instead of silently pretending verification passed.

If you want to run the phases separately, these lower-level helpers still exist:
- `scripts/auth_bootstrap.py`
- `scripts/sync_auth_bootstrap.py`
- `scripts/capture_browser_cookies.js`
- `scripts/prepare_zsxq_qr_bootstrap.js`
- `scripts/probe_wechat_qr_state.js`

## Known limitations

- token-mode HTTP may still hit anti-bot or WAF behavior
- some response shapes may differ across clients or versions
- MVP keeps previews lightweight and does not aggressively expand long posts
- browser relay is still the main recovery path when token-mode fails
- current browser script is a normalization layer for captured JSON, not a full browser controller by itself
- joined-group listings may include planets you no longer want in the digest; prefer `--groups-file` or `--exclude-group-id` to keep the tracked scope explicit
- token mode may hit intermittent API-side failures such as `code=1059: 内部错误`; current collector retries transient failures before treating the run as failed
- private news-list rendering is intentionally **not** the public default; it is a local/private enhancement for circles whose posts are already condensed link/news bundles

## Expected error statuses

- `TOKEN_MISSING`
- `TOKEN_INVALID`
- `TOKEN_EXPIRED`
- `ACCESS_DENIED`
- `EMPTY_RESULT`
- `QUERY_FAILED`
- `PARTIAL_CAPTURE` (for example: some requested groups were skipped, but other groups were collected)

## Auth bootstrap and browser recovery

See:
- `references/auth-bootstrap.md`
- `references/browser-recovery.md`
- `references/browser-workflow.md`

The current public MVP does **not** claim a fully proven OAuth-style remote binding flow.
Instead it uses this decision model:
- if a reusable token already exists, use token mode
- if not, try a guided browser bootstrap / recovery path
- if the environment cannot recover a reusable token automatically, fall back to manual token import

The current public MVP also keeps browser mode intentionally lightweight:
- browser tooling captures visible feed cards
- a local JSON snapshot is produced
- `scripts/collect_from_browser.py` normalizes that snapshot
- the normal digest pipeline continues from there

## Public default vs private enhancement

### Public default
The public/reusable default should stay conservative:
- neutral stream digest
- light organization
- minimal visible metadata
- one-sentence summaries for normal discussion / Q&A posts
- no circle-specific custom editorial logic baked into the public contract

### Private enhancement
For your own local workflow, you may enable custom rendering rules for specific circles.
Current example:
- `--private-news-list-mode`
- if a post is already a compact news/link bundle, keep the cleaned copied lines directly instead of forcing another summary layer

This keeps the public skill publishable while still allowing higher-fit local use.

## Suggested repo boundary

If you publish this skill to GitHub, use **this folder itself** as the repo root or copy it as-is into a dedicated repo.

Recommended repo contents:
- `SKILL.md`
- `README.md`
- `scripts/`
- `references/`
- `.gitignore`

Do not publish:
- `state/`
- personal token/session files
- private captures or exports
- personal planet names unless you intentionally want a private fork

## Publishing note

For the final public repo:
- keep the skill package lean
- keep private runtime state out of the package and out of git
- keep public-facing docs inside this folder so the repo stays self-contained

If you have local `state/` files under the skill folder, do **not** package directly from the live working tree with the raw packager. Use the sanitized helper instead:

```bash
python3 scripts/package_public_release.py --output-dir ./dist
```

It stages a clean copy, strips `state/`, cache files, and `.bak-*`, then verifies the final `.skill` does not contain private runtime files.
