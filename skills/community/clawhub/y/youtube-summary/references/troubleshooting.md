# Troubleshooting

Use `--json` when possible to get structured errors.

## Quick checks

- Node.js 18+ installed
- `youtube2md` installed on PATH (recommended pinned install: `npm i -g youtube2md@1.0.2`)
- `python3` available (required for `prepare.py` transcript text output)
- URL is a valid YouTube link
- `OPENAI_API_KEY` set for full mode
- Full-mode default model is `gpt-5.4-mini` unless the fifth runner argument or `YOUTUBE2MD_DEFAULT_MODEL` overrides it
- If captions/audio require signed-in YouTube access, set one of:
  - `YOUTUBE_COOKIES_PATH`
  - `YOUTUBE_COOKIE_HEADER`
- Legacy env override is not set:
  - `YOUTUBE2MD_BIN`

## Common failures and fixes

### 1) `youtube2md` not found

Fix:
- Install pinned binary:
  - `npm i -g youtube2md@1.0.2`
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

### 3) `python3` not found (simple/transcript mode text prep)

Symptom:
- Extract JSON is created but `.txt` transcript is missing

Fix:
- Install Python 3
- Verify with `python3 --version`
- Re-run simple or transcript mode so `prepare.py` can generate `.txt`

### 4) Full mode without API key

Symptom:
- OpenAI auth error / missing key

Fix:
- Default runner behavior auto-falls back to simple mode when key is missing.
- To force hard-fail behavior instead, set:
  - `YOUTUBE2MD_ALLOW_EXTRACT_FALLBACK=0`
- If you want full summary output, set `OPENAI_API_KEY` and rerun full mode.

### 5) Change the default full-mode model

Fix:
- Per run, pass the fifth runner argument:
  - `scripts/run_youtube2md.sh <url> full ./summaries/video.md Korean gpt-5.4-mini`
- Or set the runner default env var:
  - `YOUTUBE2MD_DEFAULT_MODEL=gpt-5.4-mini scripts/run_youtube2md.sh <url> full`

### 6) Transcript unavailable or YouTube blocks anonymous access

Symptom:
- Captions are missing/blocked, audio fallback is unavailable, or `E_TRANSCRIPT_UNAVAILABLE` is returned

Fix:
- Retry later / try another video
- If the video is available only to a signed-in session, provide a YouTube cookie source:
  - `YOUTUBE_COOKIES_PATH=./cookies.youtube.json scripts/run_youtube2md.sh <url> extract`
  - `YOUTUBE_COOKIE_HEADER='VISITOR_INFO1_LIVE=...; ...' scripts/run_youtube2md.sh <url> extract`
- For Whisper fallback paths, ensure `OPENAI_API_KEY` is set.

### 7) OpenAI rate limit

Fix:
- Retry after backoff
- Optionally use a different model with the fifth runner argument or `YOUTUBE2MD_DEFAULT_MODEL`.

### 8) Output file missing / write failure

Fix:
- Provide explicit writable path:
  - Full: `scripts/run_youtube2md.sh <url> full ./summaries/custom.md`
  - Extract: `scripts/run_youtube2md.sh <url> extract ./summaries/custom.json`
- Or provide an output directory:
  - `YOUTUBE2MD_OUT_DIR=./output scripts/run_youtube2md.sh <url> extract`

### 9) Package trust / version policy

Symptom:
- Security policy blocks unreviewed package installs

Fix:
- Use pinned install: `npm i -g youtube2md@1.0.2`
- Prefer vetted internal mirrors or vendored artifacts in strict environments.
- See `references/security.md` for installation-time risk decisions.

## Structured error codes (`--json`)

- `E_TRANSCRIPT_UNAVAILABLE`
- `E_OPENAI_AUTH`
- `E_OPENAI_RATE_LIMIT`
- `E_WHISPER_FAILED`
- `E_NETWORK`
- `E_WRITE_FAILED`

## Recovery response pattern

1. State what failed in one line.
2. Give one concrete retry/fix command.
3. Ask whether to retry automatically.
