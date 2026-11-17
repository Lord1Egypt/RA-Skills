---
name: yt
description: Use when the user wants to run any yt-ai operation from Claude Code — ingest a video, discover subscription uploads, batch-fetch pending, search the library, rate/recommend, compile highlights, build a supercut, check status, or run a full pipeline (daily routine or single-video). The umbrella entry point for the yt-mem-ai CLI; delegates per-video analysis, digests, and reviews to [[yt-agent]].
---

# yt — the yt-mem-ai entry point

Single entry point for driving the yt-mem-ai YouTube pipeline CLI. Every data
operation goes through the CLI — never touch the LanceDB store directly.

## Prereqs

- **Always invoke the CLI as `uvx yt-mem-ai <cmd>`** — zero-install, cached,
  always latest. **Nothing is installed on PATH**: the native plugins ship skills
  only, so do NOT go hunting for a `yt-ai` binary, a wrapper script, or a venv.
  (Only inside a source checkout of this repo may you use `uv run yt-ai <cmd>`.)
- **Always single-quote a video/channel URL** — YouTube URLs contain `?` and `&`,
  which the shell treats as glob and job-control metacharacters, so a bare URL
  fails (zsh: `no matches found`). Write
  `uvx yt-mem-ai fetch 'https://www.youtube.com/watch?v=ID'`, never bare. Same for
  `transcript` and `channel-list`.
- Settings live in a global config file, not a `.env` you hand-edit: inspect and
  change anything with `uvx yt-mem-ai config list` / `uvx yt-mem-ai config set
  KEY VALUE` (see **Configure & maintain**). Prefer `config set` over exporting
  env vars — each `uvx` run is a fresh process, so an env var only applies to the
  one command you prefixed it to.
- Video lifecycle status: `discovered → transcribed → summarized` (live streams
  get a terminal `stream` and skip transcription).

```bash
uvx yt-mem-ai <command> [args]
```

## Decide what the user wants, then run

### Ingest one video
```bash
uvx yt-mem-ai fetch '<url>'        # download audio + transcribe + embed + store
uvx yt-mem-ai transcript '<url>'   # same pipeline (alias intent)
```

### Discover + batch ingest (subscriptions)
```bash
uvx yt-mem-ai discover [--after <DATE>] [--deep] [--min-duration <s>] [--json]
uvx yt-mem-ai fetch-pending [--since <DATE>] [--limit <N>]   # ingest 'discovered' videos
```

### Enumerate a channel (does not ingest)
```bash
uvx yt-mem-ai channel-list '<url>' [--limit <N>] [--from <DATE>] [--to <DATE>] [--json]
# newest uploads for a channel URL/@handle; feed the URLs to `fetch` to ingest a group.
```

### Read / query the library
```bash
uvx yt-mem-ai list [--status <s>] [--since <DATE>] [--json]
uvx yt-mem-ai show <video_id> [--json]     # metadata + full transcript
uvx yt-mem-ai status                        # counts by status
uvx yt-mem-ai search "<query>" [--hybrid|--fts|--vector] [-k <N>]
```

### Summaries (skills generate the analysis; CLI persists it)
```bash
uvx yt-mem-ai save-summary <video_id> "<summary_md>" \
  --highlights '<json>' --qa '<json>'
```
Do **not** write summaries free-hand here. For the model-generated analysis
(summary + timestamped highlights + Q&A + presentation, a subscription digest, or
a cross-video review), hand off to **[[yt-agent]]**.

[[yt-agent]] produces the analysis with **this agent** (Claude Code) reading the stored
transcript — no API key, no OpenRouter, no external LLM call. (The desktop app has
a separate OpenRouter-based summarize path; it is not used here.)

### Taste / recommendations
```bash
uvx yt-mem-ai like <video_id>      # feedback table (latest signal per video wins)
uvx yt-mem-ai dislike <video_id>
uvx yt-mem-ai recommend [--limit <N>] [--json]   # rank unrated fetched videos by taste
```

### Configure & maintain
```bash
uvx yt-mem-ai config list                     # every setting, value, and source
uvx yt-mem-ai config set KEY VALUE            # e.g. WEBSHARE_PROXY_USERNAME, YT_EMBEDDING_MODEL
uvx yt-mem-ai config get KEY [--reveal]       # secrets masked unless --reveal
uvx yt-mem-ai config unset KEY                # remove from the config file
```
Use this to reconfigure the engine on request — set Webshare proxy creds, switch
the embedding model/backend, point at a cookies browser, change caption languages
— without hand-editing `.env`. `set` writes the global config
(`~/.yt-mem-ai/config.env`) by default; add `--project` for `./.env`. Only known
`.env` keys are accepted. After changing the embedding model/backend, migrate the
existing library:
```bash
uvx yt-mem-ai reembed                          # re-embed all chunks with the current YT_EMBEDDING_* config
```

### Compile / video output
```bash
uvx yt-mem-ai compile [--since <DATE>] [--max-minutes <N>] [--out <path>] [--json]
# Deep-linked highlights doc from summarized videos. Fast, no download. Prints the
# markdown to stdout by default; pass --out compilations/<DATE>.md to save a file.

uvx yt-mem-ai supercut [--since <DATE>] [--max-minutes <N>] [--out <path>] [--keep-clips]
# → actual video reel supercuts/<date>.mp4 + .refs.md sidecar.
# Slow: re-downloads each clip (720p) + ffmpeg concat. Needs network + local ffmpeg.

uvx yt-mem-ai frame <video_id> --at <seconds|H:M:S> [--out <path>]
# Grab one still frame from an ingested video (needs yt-dlp + ffmpeg).
# → frames/<id>_<s>s.png by default.
```

> The REST API / `serve` command moved to the **yt-mem-ai-desktop** repo
> (`yt-ai-desktop-serve`); it is not part of this engine CLI.

## When YouTube blocks a fetch

Two different blocks with two different fixes — read the message, don't guess.

| Error | Cause | Fix |
|---|---|---|
| `YouTube bot check: ... Sign in to confirm you're not a bot` (exit 4) | yt-dlp (audio/metadata) needs a logged-in session | `uvx yt-mem-ai config set YT_COOKIES_BROWSER chrome` (or `brave`/`firefox`/`edge`/`safari`), then re-run |
| `captions blocked by YouTube (IP rate-limited)` (exit 3) | the transcript API is IP-blocked | cookies do **not** help — retry later, or set `YT_CAPTIONS_USE_WEBSHARE true` + `WEBSHARE_PROXY_USERNAME`/`WEBSHARE_PROXY_PASSWORD` |
| `no captions available` (exit 1) | video has no caption track | re-run with `--whisper` (downloads audio, slower) |

Set these with `config set`, not `KEY=value uvx …`: the config file persists
across runs, an env var only covers the single command you prefixed.
On macOS the first Chrome-cookie read may raise a Keychain prompt — if a command
hangs, tell the user to approve it.

## Pipelines

**Daily routine** (subscriptions → digest → clickable highlights):
```bash
uvx yt-mem-ai discover          # new uploads → 'discovered'
uvx yt-mem-ai fetch-pending     # download+transcribe+embed today's batch (skips failures)
```
then invoke **[[yt-agent]]** (process subscriptions → per-video summaries + `digests/<DATE>.md`), then:
```bash
uvx yt-mem-ai compile           # deep-linked highlights doc for the day
# optionally: uvx yt-mem-ai supercut   # shareable video reel
```

**Single video on demand:**
```bash
uvx yt-mem-ai fetch '<url>'
```
then invoke **[[yt-agent]]** (single-video summary / highlights / Q&A / presentation).

## Conventions

- Skills-primary summarization: the CLI stores data; skills read via
  `show --json` / `search` and write via `save-summary`. Never invent
  highlight timestamps — anchor them with `uvx yt-mem-ai search "<phrase>" --vector -k 3`.
- Dates are `YYYY-MM-DD` strings; string comparison is date comparison.
- `is_seen` is status-based (`transcribed`/`summarized`), so ingest is retry-safe;
  re-running `fetch`/`fetch-pending` is safe.
- Always report what ran + the resulting file paths (digests/compilations/supercuts) in chat.

## Notes

- If `show` prints `not found`, the video isn't ingested — run `fetch '<url>'` first.
- If `fetch-pending`/`list` finds nothing for a day, run `discover` first.
- `supercut` continues past a clip whose download/render fails (logged in the
  `.refs.md` sidecar's skipped list) rather than aborting.
- Related: [[yt-agent]] (analysis scenarios: single video, subscription digest, cross-video review).
```
