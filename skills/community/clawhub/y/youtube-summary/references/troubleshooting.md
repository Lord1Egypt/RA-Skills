# Troubleshooting

Use `--json` (`YOUTUBE2MD_JSON=1`) when possible to get a structured result envelope with `ok`, `code`, and `outputPath`.

## Quick checks

- Node.js 20.18.1+ installed
- `youtube2md` installed on PATH (recommended pinned install: `npm i -g youtube2md@1.2.0`)
- URL is a valid YouTube link (watch, youtu.be, Shorts, Live, Embed, Music, youtube-nocookie embed)
- URLs containing `&` are quoted in the shell
- A summarization provider is available for full mode:
  - Codex ChatGPT login (`codex login status`), or
  - `OPENAI_API_KEY`
- If captions/audio require signed-in YouTube access, set one of:
  - `YOUTUBE_COOKIES_PATH`
  - `YOUTUBE_COOKIE_HEADER`
- Legacy env override is not set:
  - `YOUTUBE2MD_BIN`

> **Secret handling:** `OPENAI_API_KEY`, `YOUTUBE_COOKIES_PATH`, and `YOUTUBE_COOKIE_HEADER` are credentials. Never paste them into chat or command output, and never commit them. Supply them through secure secret storage or a local `.env`/env file rather than inline in a prompt. Prefer a file-based cookie export (`YOUTUBE_COOKIES_PATH`) over a raw `YOUTUBE_COOKIE_HEADER` string, redact these values from any logs you share, and remember that enabling a provider or Whisper fallback sends transcript/audio-derived content to a third party (OpenAI). See `references/security.md`.

## Common failures and fixes

### 1) `youtube2md` not found

Fix:
- Install pinned binary:
  - `npm i -g youtube2md@1.2.0`
- Verify with:
  - `youtube2md --version`
  - `youtube2md --help`

### 2) Legacy override env rejected

Symptom:
- Runner exits with an error about `YOUTUBE2MD_BIN`.

Fix:
- Unset the env var and rerun:
  - `unset YOUTUBE2MD_BIN`
- Keep using local installed `youtube2md` binary on PATH.

### 3) Full mode without a summarization provider

Symptom:
- Runner warns "no summarization provider available" and switches to simple mode, or `E_SUMMARIZER_UNAVAILABLE` is returned.

Fix:
- Default runner behavior auto-falls back to simple mode; a summary is still produced from the transcript.
- To force hard-fail behavior instead, set:
  - `YOUTUBE2MD_ALLOW_EXTRACT_FALLBACK=0`
- For full mode output, either:
  - log in to Codex with ChatGPT: `codex login` then `codex login status`, **plus** install the peer: `npm i -g @openai/codex-sdk`, or
  - set `OPENAI_API_KEY`.
- A Codex session authenticated with an API key does not count as the keyless Codex path.

### 3a) Codex looks logged in but full mode still refuses it

Symptom:
- `codex login status` prints "Logged in using ChatGPT", yet the runner reports `Codex provider unavailable: Optional @openai/codex-sdk provider is not installed.` — or, before this check existed, youtube2md failed with `E_SUMMARIZER_UNAVAILABLE` right after the runner claimed a provider was available.

Cause:
- The Codex path needs two things: the CLI session **and** the ESM-only `@openai/codex-sdk` peer. `@openai/codex` (the CLI) does not provide it.

Fix:
- `npm i -g @openai/codex-sdk`
- On Homebrew Node, `node_modules/@openai` is often root-owned, so this fails with `EACCES` (`syscall mkdir`). Ask the user to run `sudo npm i -g @openai/codex-sdk` themselves — never escalate privileges from the skill.
- Verify: the runner's pre-check now mirrors youtube2md's own `detectCodexChatGptLogin()`, so once it stops warning, full mode will really use Codex.
- Watch for `INFO: Codex (ChatGPT login) unavailable; full mode will use the billed OPENAI_API_KEY path` — that means an `auto` run is spending API credits, not the ChatGPT subscription.

### 4) Force a specific provider

Fix:
- `YOUTUBE2MD_PROVIDER=codex scripts/run_youtube2md.sh <url> full`
- `YOUTUBE2MD_PROVIDER=openai scripts/run_youtube2md.sh <url> full`
- Default `auto` tries Codex ChatGPT login first, then the OpenAI API.

### 5) Adjust summary detail density

Fix:
- `YOUTUBE2MD_DETAIL=exhaustive scripts/run_youtube2md.sh <url> full` (densest chapter notes, ≈ one bullet per ~300 transcript tokens)
- `YOUTUBE2MD_DETAIL=concise scripts/run_youtube2md.sh <url> full` (quick overview, ≈ one bullet per ~750 tokens)
- Upstream default is `balanced` (≈ ~450); invalid values fail with `E_INVALID_INPUT` (CLI) or runner exit code 9.
- `--detail` moves chapter-bullet density only. It does not lengthen the `## Summary` section, and it changes chapter counts only for short or sparse sections (a full-size chunk always hits the 9-chapter cap).
- Requires `youtube2md@1.1.0+` (`--detail` is unknown to older versions).

### 6) `## Summary` section looks too short

Symptom:
- Full-mode output opens with only a few sentences of summary, and raising `--detail` does not lengthen it.

Explanation and options:
- Expected since youtube2md 1.2.0: the Summary is an orientation capped at 8 sentences (with a paired word ceiling), and the detail deliberately lives in `## Chapters`. Pass the output through as-is instead of expanding it.
- If the user wants more substance, the lever is chapter density: `YOUTUBE2MD_DETAIL=exhaustive`.
- If the user specifically wants a longer narrative overview, write it separately from the transcript; do not present it as youtube2md output.

### 7) Change the full-mode model

Fix:
- Per run, pass the fifth runner argument:
  - `scripts/run_youtube2md.sh <url> full ./summaries/video.md Korean gpt-5.6-luna`
- Or set the runner default env var:
  - `YOUTUBE2MD_DEFAULT_MODEL=<model> scripts/run_youtube2md.sh <url> full`
- Per provider (when `--model` is not passed): `CODEX_MODEL` for the Codex path, `OPENAI_MODEL` for the OpenAI API path.
- If the Codex backend rejects the default model (its catalog changes independently of the OpenAI API), set a supported `CODEX_MODEL`.

### 7a) Transcript or summary comes back in the wrong language

Symptom:
- An English video produces an Arabic (or Chinese, Russian, ...) transcript/summary. `YOUTUBE2MD_JSON=1` shows something like `"actualLanguage": "ar"` with `"autoGeneratedCaptions": false`.

Cause:
- Without `--caption-lang`, youtube2md has no language to rank tracks by, so every manually-authored track ties and YouTube's list order wins. Videos with community translations often list a translation first (`Found caption tracks: ar, zh, en, en, fr, ...`).

Fix:
- Pin the language and re-run:
  - `YOUTUBE2MD_CAPTION_LANG=en scripts/run_youtube2md.sh <url> full`
- Verify with `YOUTUBE2MD_JSON=1` that `actualLanguage` is what you expect.
- The runner warns whenever `YOUTUBE2MD_CAPTION_LANG` is unset; treat it as a cue to check the output language.
- Upstream fix worth making in youtube2md: rank the video's original track first (InnerTube marks it — `vssId` beginning with `.`, or the default audio track's caption index) instead of leaving unranked ties to list order.

### 8) Transcript unavailable or YouTube blocks anonymous access

Symptom:
- Captions are missing/blocked or `E_TRANSCRIPT_UNAVAILABLE` is returned

Fix:
- Prefer a specific caption track first: `YOUTUBE2MD_CAPTION_LANG=<code>` (e.g. `en`, `ko`).
- Retry later / try another video.
- If the video is available only to a signed-in session, provide a YouTube cookie source (treat these as secrets — keep them out of chat, logs, and version control; a file export is safer than an inline header):
  - `YOUTUBE_COOKIES_PATH=./cookies.youtube.json scripts/run_youtube2md.sh <url> extract`
  - `YOUTUBE_COOKIE_HEADER='VISITOR_INFO1_LIVE=...; ...' scripts/run_youtube2md.sh <url> extract`
- For captionless videos, allow the Whisper STT fallback (sends audio to OpenAI; requires `OPENAI_API_KEY`; audio under 24 MB):
  - `YOUTUBE2MD_CAPTIONS_ONLY=0 scripts/run_youtube2md.sh <url> extract`

### 8a) Only part of the summary reaches the user

Symptom:
- The reader receives a message starting with `(1/2)` or `(1/3)` and nothing after it. Re-running produces the same complete `.md` on disk, so the summarization itself is fine.

Cause — **not** the channel's message cap:
- The agent hand-split the summary and sent part 1 through openclaw's `message` tool. Under the codex-app-server backend that call is turn-terminal: on a successful send with nothing else in flight, openclaw records `turn.dynamic_tool_terminal_release`, interrupts the model turn, and ends it (`assistantTexts: []`). Parts 2..n are never attempted.
- Verified 2026-07-25 in `~/.openclaw/agents/main/sessions/*.trajectory.jsonl`: two runs each show `CALL message` → `turn.dynamic_tool_terminal_release` → `session.ended` ~1-3 s later, with no second send.

Fix:
- Send the whole summary in **one** call. openclaw chunks outbound Telegram text at `textChunkLimit` (default 4,000) and loops over the chunks, so nothing is lost — the 11,352-character 3h07m summary splits into 5 messages on its own (`markdownToTelegramChunks(text, 4000)` → `[3470, 516, 3582, 410, 2426]`).
- Never emit `(1/n)` parts as separate sends; that is what causes this symptom.
- Do not respond by shortening the summary, attaching a file, or linking to the output path.
- Raise or lower `channels.telegram.textChunkLimit` in `openclaw.json` if the per-message size needs tuning; the cap itself is the transport's, not the skill's.

### 9) Video unavailable

Symptom:
- `E_VIDEO_UNAVAILABLE` (private, deleted, age-restricted) or `E_UNSUPPORTED_URL`

Fix:
- Verify the URL opens in a browser.
- For age-restricted or membership content, provide YouTube cookies (see above).

### 10) OpenAI rate limit

Fix:
- youtube2md retries transient failures with exponential backoff internally; retry the run after a pause if it still fails.
- Optionally use a different model with the fifth runner argument or `YOUTUBE2MD_DEFAULT_MODEL`.

### 11) Output file missing / write failure

Fix:
- Provide explicit writable path:
  - Full: `scripts/run_youtube2md.sh <url> full ./summaries/custom.md`
  - Extract: `scripts/run_youtube2md.sh <url> extract ./summaries/custom.txt`
- Or provide an output directory:
  - `YOUTUBE2MD_OUT_DIR=./output scripts/run_youtube2md.sh <url> extract`
- With `YOUTUBE2MD_JSON=1`, read the exact written path from the envelope's `outputPath`.

### 12) Package trust / version policy

Symptom:
- Security policy blocks unreviewed package installs

Fix:
- Use pinned install: `npm i -g youtube2md@1.2.0`
- Prefer vetted internal mirrors or vendored artifacts in strict environments.
- See `references/security.md` for installation-time risk decisions.

## Structured error codes (`--json`)

Error envelopes are versioned: `{ "schemaVersion": 1, "ok": false, "mode": "...", "code": "...", "message": "..." }`.

- `E_INVALID_INPUT` — missing or invalid CLI argument
- `E_UNSUPPORTED_URL` — unsupported YouTube URL shape or invalid video ID
- `E_VIDEO_UNAVAILABLE` — video is private, deleted, age-restricted, or otherwise unavailable
- `E_TRANSCRIPT_UNAVAILABLE` — no caption track and no usable Whisper path
- `E_SUMMARIZER_UNAVAILABLE` — neither Codex SDK nor the OpenAI API fallback could summarize
- `E_OPENAI_AUTH` — the configured `OPENAI_API_KEY` fallback is invalid
- `E_OPENAI_RATE_LIMIT`
- `E_WHISPER_FAILED`
- `E_NETWORK`
- `E_WRITE_FAILED`
- `E_UNKNOWN` — unexpected unclassified failure

## Recovery response pattern

1. State what failed in one line.
2. Give one concrete retry/fix command.
3. Ask whether to retry automatically.
