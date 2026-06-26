# Troubleshooting

## 1. YouTube anti-bot / login required

Symptoms:
- `yt-dlp` errors like `LOGIN_REQUIRED`
- "Sign in to confirm you're not a bot"

What to do:
- Provide/export a valid `cookies.txt` for YouTube
- Or supply a user-provided local media file / mirror link
- Do not blame Whisper first; this is usually a fetch/auth problem before transcription starts

## 2. Subtitle partial failure (HTTP 429) but subtitle file exists

Symptoms:
- `yt-dlp` returns non-zero
- One subtitle variant fails with 429
- But `.srt` / `.vtt` was still written to `downloads/`

Expected behavior in this skill:
- Continue if any usable subtitle file exists
- Do **not** fail the whole run just because one subtitle variant failed

If it still fails:
- Inspect `downloads/` for `source*.srt` / `source*.vtt`
- Confirm `transcript.txt` generation step ran
- Patch the script only if subtitle files exist and the script still aborts

## 3. Bilibili 403 on shared links

Symptoms:
- metadata fetch fails on `bilibili.com/video/...?...`

Expected behavior in this skill:
- Normalize to `https://www.bilibili.com/video/...`
- Strip `spm_*` tracking params

If it still fails:
- Retry with the normalized URL manually
- Verify `yt-dlp --dump-single-json --skip-download <normalized-url>`

## 4. Xiaohongshu provides no subtitles

Symptoms:
- `requested_subtitles: null`
- no `.srt/.vtt` files land

Interpretation:
- Normal platform behavior for many Xiaohongshu items

What to do:
- Let the pipeline continue to media download + Whisper
- Treat this as a normal fallback, not a failure

## 5. Whisper GPU venv missing or broken

Symptoms:
- `skills/video-knowledge-ingest/scripts/whisper-gpu.sh` exits early
- CUDA / cuBLAS / cuDNN import issues
- `faster_whisper` errors

What to do:
- Check the workspace venv exists: `/home/jason/.openclaw/workspace/.venv-whisper-gpu`
- Check bundled wrapper resolves the workspace root correctly
- Retry CPU fallback if GPU fails
- Confirm `ffmpeg` works before debugging Whisper internals

## 6. ffmpeg / ffprobe missing

Symptoms:
- media normalization fails before transcription

What to do:
- Verify `ffmpeg` and `ffprobe` are on `PATH`
- Use static binaries if needed
- Re-run after confirming `ffmpeg -version` and `ffprobe -version`

## 7. summarize / codex auth failure

Symptoms:
- `summarize` runs but does not produce a real summary
- `codex` returns 401 / not logged in

What to do:
- Check `codex login status`
- Re-auth with `codex login --device-auth` if needed
- Confirm `summarize --version` and a small local-file smoke test

## 8. Run produced a directory but no final record

Symptoms:
- item directory exists
- `source.info.json` exists
- but no `record.json`, `summary.md`, or `index.jsonl` entry

What to do:
- Inspect `downloads/` and `whisper/`
- Determine whether failure happened in:
  1. subtitle fetch
  2. media download
  3. transcription
  4. summary generation
- Fix the earliest broken stage; later stages usually depend on it

## 9. Need to debug with the least noise

Recommended order:
1. run the bundled entrypoint exactly once
2. inspect the created item directory
3. inspect `record.json` or absence thereof
4. inspect `transcript.txt`
5. inspect `summary.md`
6. only then patch code

This prevents "debugging by vibes," which is how people end up blaming the last step for a first-step failure.
