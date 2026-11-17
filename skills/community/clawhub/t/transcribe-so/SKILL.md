---
name: transcribe-so
description: Transcribe audio and video with the transcribe.so CLI. Turns YouTube videos, podcasts (Apple Podcasts, Spotify, SoundCloud, Vimeo, Twitch, Loom), direct media URLs, and local audio or video files into speaker-labelled transcripts with timestamped segments, chapters, sections, cited Q&A, and subtitle files (SRT, VTT, karaoke VTT). Use when the user wants a transcript, show notes, chapters, subtitles, quotes, or answers grounded in a recording. 52 languages and dialects.
homepage: https://transcribe.so/agent
metadata: {"openclaw":{"emoji":"🎙️","requires":{"bins":["transcribe-so"],"env":["TRANSCRIBE_API_KEY"]}}}
---

## Install transcribe-so if it doesn't exist

```bash
npm install -g transcribe-so
# or
pnpm install -g transcribe-so
```

npm package: https://www.npmjs.com/package/transcribe-so
github: https://github.com/shsunmoonlee/transcribe-agent
official website: https://transcribe.so

---

| Property | Value |
|----------|-------|
| **name** | transcribe-so |
| **description** | Speech-to-text CLI: media in, speaker-labelled transcript + chapters + cited Q&A out |
| **allowed-tools** | Bash(transcribe-so:*) |

---

## Hard Rules (Read First)

**Rule 1 - Quote before create.** `quote` is free; `create` charges the wallet. Show the user the price for anything non-trivial. The quote's `transcription_id` is NOT the job id - never pass it to `wait` or `result`. Only the id in the `create` (or `run`) 202 response is the job.

**Rule 2 - Local files go through `upload` first.** `create` never accepts a filesystem path. Run `transcribe-so upload <file>`, then pass the returned `upload_id` plus `--duration` with `--source upload`. URL sources (`youtube`, `platform_url`, `external_url`) must be publicly fetchable without auth.

**Rule 3 - `status: "queued"` on create is SUCCESS, not an error.** It means the account's concurrency cap is reached and the job waits FIFO for a slot. Never re-submit a queued job. A GET showing `quoted` is different: that row is a quote that was never started (see Rule 1) and will never progress. Exception: `source=upload` is REJECTED at the cap with a fair-use error instead of being queued - wait for a running job to finish; do not hammer retry.

**Rule 4 - Never hand-roll polling.** Use `wait <id>` or `run`; they drive the server's long-poll endpoint in capped windows. A `waiting for a concurrency slot` line on stderr is normal.

**Rule 5 - stdout is pure JSON, except `subtitles`.** `subtitles <id>` prints the raw SRT/VTT body so it can be piped to a file; every other command prints one JSON document. All progress and chatter goes to stderr, so `| jq .` always works.

**Rule 6 - `delete` and `retry` require `--yes`.** Deletion is irreversible (row, derived data, stored media). Retry re-charges from scratch; the original failed charge is not refunded.

**Rule 7 - Know which budget you hit.** Transcription bills per minute from the wallet; `ask` uses a daily Q&A allowance (never the wallet); `me` shows the balance. Exit 4 means the account needs funds (top up or raise the key's spend cap). Exit 6 means the CLI's own `--max-usd` refused - raise `--max-usd`, do NOT top up.

---

## Authentication

```bash
export TRANSCRIBE_API_KEY=tsk_live_...   # https://transcribe.so/settings/api-keys
transcribe-so auth:status
```

New accounts start with free credit. The CLI refuses to send the key to a non-default or non-https `TRANSCRIBE_API_URL` unless `--allow-custom-host` is passed.

## Exit codes

| Code | Meaning | What to do |
|------|---------|------------|
| 0 | success | parse stdout |
| 1 | API or generic error (including `not_ready`, `qna_quota_exceeded`) | read `error.code`; `not_ready` means run `wait <id>` first; a used-up Q&A allowance frees on a rolling 24h window |
| 2 | usage error / custom-host refusal | fix the flags |
| 3 | auth (401, `scope_forbidden`, missing key) | check TRANSCRIBE_API_KEY and its scopes |
| 4 | payment (`insufficient_funds`, `spend_cap_exceeded`) | top up or raise the key's cap |
| 5 | transient (rate limit, wait timeout, 5xx) | retry later; per-minute rate limits are already auto-retried with Retry-After |
| 6 | local budget refusal (`max_usd_exceeded`) | raise `--max-usd`; do not top up |

Non-2xx API responses print the API's JSON error envelope verbatim on stdout: `{"error": {"code", "message", "request_id", "doc_url"}}`.

## Core Workflow

```bash
# 1. Check auth and balance
transcribe-so me | jq '{email, wallet_balance_usd}'

# 2. Price it (free)
transcribe-so quote --source youtube --url "https://www.youtube.com/watch?v=..." | jq .retail_usd

# 3. One command end to end (quote -> budget gate -> create -> wait -> result)
transcribe-so run --source youtube --url "https://www.youtube.com/watch?v=..." --max-usd 2

# Or step by step:
ID=$(transcribe-so create --source youtube --url "https://..." | jq -r .id)
transcribe-so wait "$ID"
transcribe-so result "$ID" | jq '.chapters[] | {title, start_seconds, url}'
```

`run` requires an explicit `--max-usd` budget; there is no default. The request body the CLI sends for a YouTube job looks like [examples/youtube.json](examples/youtube.json).

## Essential Commands

```bash
transcribe-so auth:status                      # is the key valid?
transcribe-so me                               # account, wallet, limits, key scopes
transcribe-so pipelines                        # per-minute pricing + supported languages
transcribe-so quote --source ... --url ...     # free price preview
transcribe-so create --source ... --url ...    # submit (202: {id, retail_usd, ...})
transcribe-so wait <id> [--timeout 1800]       # long-poll to terminal state
transcribe-so result <id> [--include all]      # chapters,sections,qna by default
transcribe-so run --source ... --max-usd <n>   # the whole flow, budget-gated
transcribe-so list [--limit 50] [--api-only]   # newest first, cursor-paginated
transcribe-so get <id>                         # status/stage/progress snapshot
transcribe-so upload <file> [--duration <s>]   # presigned PUT; prints upload_id
transcribe-so subtitles <id> [--format srt]    # RAW body to stdout (pipe to file)
transcribe-so ask <id> -q "..."                # cited Q&A (daily allowance)
transcribe-so delete <id> --yes                # irreversible
transcribe-so retry <id> --yes                 # re-charges from scratch
```

Sources: `--source youtube|platform_url|external_url|upload`. `youtube` for any youtube.com or youtu.be URL; `platform_url` for hosted pages (Apple Podcasts, Spotify episodes, SoundCloud, Vimeo, Twitch VODs, Loom); `external_url` for direct public media URLs; `upload` for files sent with `upload` (needs `--upload-id` and `--duration`).

## Common Patterns

**Local file, start to finish** - full walk-through in [examples/upload-flow.md](examples/upload-flow.md):

```bash
UP=$(transcribe-so upload ./interview.mp3)   # duration probed with ffprobe if installed
transcribe-so run --source upload \
  --upload-id "$(echo "$UP" | jq -r .upload_id)" \
  --duration  "$(echo "$UP" | jq -r .duration_seconds)" \
  --max-usd 5
```

**Batch a folder** - see [examples/batch-transcribe.sh](examples/batch-transcribe.sh). Submit sequentially and let the server queue at the concurrency cap; remember Rule 3's upload exception.

**Podcast to chapters/show notes:**

```bash
transcribe-so run --source platform_url --url "https://podcasts.apple.com/..." --max-usd 3 \
  | jq -r '.chapters[] | "\(.start_seconds | floor)s  \(.title)"'
```

**Watch-folder heartbeat (OpenClaw)** - [examples/heartbeat-openclaw.json](examples/heartbeat-openclaw.json) runs the batch script on a schedule so anything dropped into a folder gets transcribed.

**Subtitles for vertical video:**

```bash
transcribe-so subtitles "$ID" --format vtt --preset tiktok-shorts > clip.vtt
```

**Fire-and-forget with a webhook** - pass `--callback-url https://your-endpoint` to `create`; the 202's `callback.secret` is the HMAC key for the signed `transcription.completed` / `transcription.failed` POST. No polling needed.

## Gotchas

- The quote's `transcription_id` is not the job id (Rule 1). `run` handles this for you.
- `create` responses are slim 202 acks; `billed_minutes` and `retail_usd` appear there but NOT on later GETs.
- `result` has no single full-text field: join `segments[].text` (pass `--include segments` or `all`).
- `--include segments` can be large; the default `chapters,sections,qna` is usually what you want.
- Chapters, sections, and citations carry a pre-computed `url` deep link - use it VERBATIM; never rebuild timestamp URLs yourself.
- `ask` needs `status=completed` (409 `not_ready` otherwise) and consumes the daily allowance; cached pairs via `result --include qna` are free - read those first.
- Uploads over 50 MB warn (single-shot presigned PUT, 900s expiry); over 500 MB the CLI refuses and points at the resumable tus flow or the web app.
- Rate limit is 60 requests/min per key, shared with the MCP server. Per-minute limits auto-retry; fair-use and allowance exhaustion never do.
- `--idempotency-key` makes create/retry retries safe; the CLI always sends one (auto-generated UUID by default).

## Quick Reference

| Task | Command |
|------|---------|
| Price a video | `quote --source youtube --url <u>` |
| Transcribe under budget | `run --source youtube --url <u> --max-usd 2` |
| Full text | `result <id> --include segments \| jq -r '.segments[].text'` |
| Chapter list | `result <id> \| jq '.chapters[] \| {title, start_seconds}'` |
| SRT file | `subtitles <id> > out.srt` |
| Cited answer | `ask <id> -q "..."` |
| Local file | `upload <file>` then `run --source upload --upload-id ... --duration ...` |

Also available as a remote MCP server (https://transcribe.so/mcp) and a Claude Code plugin (`/plugin marketplace add shsunmoonlee/transcribe-agent`, then `/plugin install transcribe-so@transcribe-agent`). REST reference: https://transcribe.so/openapi.json and https://transcribe.so/developers/docs.
