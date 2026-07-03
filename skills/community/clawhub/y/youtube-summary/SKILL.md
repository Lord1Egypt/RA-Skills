---
name: youtube-summary
description: "Summarize YouTube videos with youtube2md, including bare YouTube URLs with no instructions, chaptered notes, timestamp links, transcript extraction, and key takeaways."
env:
  - name: OPENAI_API_KEY
    required: false
    description: Enables full summarization mode. When set, transcript/audio-derived content may be sent to OpenAI. Omit to use simple or transcript mode when captions are available.
  - name: YOUTUBE2MD_DEFAULT_MODEL
    required: false
    description: Optional runner default model for full mode; this skill defaults to gpt-5.4-mini.
  - name: OPENAI_MODEL
    required: false
    description: Optional youtube2md fallback model when --model is not passed directly. The runner normally passes gpt-5.4-mini explicitly.
  - name: YOUTUBE_COOKIES_PATH
    required: false
    description: Optional EditThisCookie JSON export for youtube.com; used when captions/audio require signed-in YouTube access.
  - name: YOUTUBE_COOKIE_HEADER
    required: false
    description: Optional raw YouTube Cookie header for authenticated metadata, caption, or audio fallback requests.
---

# YouTube Summary (youtube2md)

Use the official `youtube2md` CLI behavior from the package/repository, with this skill's full-mode default model set to `gpt-5.4-mini`.

## Runtime + security prerequisites

- Require **Node.js 18+**.
- Require preinstalled `youtube2md` on PATH.
  - Recommended pinned install: `npm i -g youtube2md@1.0.2`
- Require **python3** for transcript text preparation (`prepare.py`) in simple/transcript modes.
- Default runner uses the local `youtube2md` executable only.
- Runtime npm execution (`npx`) is intentionally not supported by this skill runner.
- The `YOUTUBE2MD_BIN` environment variable override is rejected by the runner.
- `OPENAI_API_KEY` enables full summarization mode; transcript and/or audio-derived content may be sent to OpenAI through youtube2md's workflow.
  - For sensitive content, omit `OPENAI_API_KEY` and use simple or transcript mode when captions are available.
- Full-mode runner default model is `gpt-5.4-mini`.
  - Override per run with the fifth runner argument: `scripts/run_youtube2md.sh <url> full <output_md_path> <language> <model>`.
  - Override by environment with `YOUTUBE2MD_DEFAULT_MODEL=<model>` when the fifth argument is omitted.
- `YOUTUBE_COOKIES_PATH` or `YOUTUBE_COOKIE_HEADER` can be used when YouTube blocks anonymous caption/audio access.
- In sensitive environments, audit upstream `youtube2md@1.0.2` and dependencies before installation or future version bumps.

See `references/security.md` before first-time install/enable.

## Workflow

1. Validate input
   - Accept `youtube.com` and `youtu.be` URLs.
   - If a message contains only YouTube URL(s), treat it as a request to summarize with this skill.
   - If YouTube URL(s) are provided without an explicit task, default to summary output, not transcript-only output.
   - If URLs are missing, ask for one URL per line.

2. Choose mode
   - **Full mode**: generates Markdown with youtube2md's summarization pipeline.
     - If `OPENAI_API_KEY` is visible/available and external API use is acceptable, try full mode first.
     - Defaults to model `gpt-5.4-mini` through the runner.
   - **Simple mode**: uses youtube2md `--extract-only` internally, prepares transcript text (`.txt`), then summarizes from that transcript.
     - Use when API key is unavailable, content is sensitive, external API use is not acceptable, or full mode fails/falls back.
   - **Transcript mode**: uses youtube2md `--extract-only` internally and returns/prepares transcript output without a summary.
     - Use when the user asks for transcript extraction, transcript-only output, raw transcript, or machine-readable transcript JSON.
   - Prefer a **no-error path**: check key first and run simple mode directly when key is missing and the user asked for a summary.

3. Run converter
   - Preferred runner script:
     - `scripts/run_youtube2md.sh <url> full [output_md_path] [language] [model]`
       - If `OPENAI_API_KEY` is missing, runner auto-falls back to the internal extract path; disclose summary output as simple mode.
       - If `[model]` is omitted, runner passes `--model gpt-5.4-mini` unless `YOUTUBE2MD_DEFAULT_MODEL` is set.
     - `scripts/run_youtube2md.sh <url> extract [output_json_path]`
       - `extract` is the runner/CLI mode name.
       - Disclose it as `simple` when summarizing from the prepared `.txt`.
       - Disclose it as `transcript` when returning transcript-only output.
   - Optional machine-readable CLI output:
     - `YOUTUBE2MD_JSON=1 scripts/run_youtube2md.sh <url> full`
     - `YOUTUBE2MD_JSON=1 scripts/run_youtube2md.sh <url> extract`
   - Optional stdout/no-file mode:
     - `YOUTUBE2MD_STDOUT=1 scripts/run_youtube2md.sh <url> extract`
   - Optional output directory:
     - `YOUTUBE2MD_OUT_DIR=./output scripts/run_youtube2md.sh <url> extract`
   - Runtime controls:
     - Use only locally installed `youtube2md` executable.
     - Do not use runtime npm execution (`npx`) for this skill.
   - Direct CLI equivalent:
     - `youtube2md --url <url> [--out <path>] [--out-dir <dir>] [--lang <language>] --model gpt-5.4-mini`
     - Add `--extract-only` for simple/transcript modes.
     - Add `--json` for machine-readable status/errors.
     - Add `--stdout` to write output to stdout instead of a file.

4. Verify output
   - Full mode: Markdown file exists and is non-empty unless `--stdout` is used.
   - Simple mode: JSON file exists and prepared TXT file exists and is non-empty when file output is used.
   - Transcript mode: JSON or TXT transcript output exists and is non-empty, unless `--stdout` is used.
   - If using `--json`, parse `ok: true/false` and handle error `code`.

5. Respond to the user
   - Follow `references/output-format.md` as the default response shape.
   - Follow `references/summarization-behavior.md` for source policy and chapter/takeaway density.
   - Do **not** include generated local file path(s) in normal user-facing replies.
   - Share file paths only when explicitly requested by the user (e.g., debugging/export workflows).
   - **Summary source policy:**
     - Full mode succeeded -> use youtube2md Markdown output as the summary source.
     - Simple mode -> use prepared `.txt` transcript text as the summary source.
     - Transcript mode -> return transcript content or requested transcript artifact details, not a summary.
   - Always append a final mode line after the user-facing result:
     - `Mode: full`
     - `Mode: simple`
     - `Mode: simple (fallback from full; OPENAI_API_KEY unavailable)` when full was requested but the runner fell back and a summary was still produced.
     - `Mode: transcript` when transcript-only output was requested.
   - Keep user-facing flow smooth: if key is missing, use simple output and summarize from `.txt` without surfacing avoidable tool-error noise.

## Multi-video requests

- Process URLs sequentially.
- Return per-video results (omit local file paths unless requested).
- Include the final mode line for each video result.
- If any fail, report successful items first, then failures with fixes.

## Built-in behavior to trust

- Default output paths:
  - Full mode: `./summaries/<video_id>.md`
  - Simple/transcript modes (CLI extract): `./summaries/<video_id>.json`
  - Local runner post-process (simple/transcript modes): `./summaries/<video_id>.txt` via `prepare.py`
- Skill runner default full-mode model: `gpt-5.4-mini` unless the fifth runner argument or `YOUTUBE2MD_DEFAULT_MODEL` overrides it.
- Upstream youtube2md package default model: `gpt-5-mini` when no model is passed directly; this skill normally passes its own default.
- Transcript strategy:
  - YouTube captions via watch-page / InnerTube requests, with YouTube cookies when configured.
  - `youtube-transcript` fallback.
  - Whisper STT fallback when `OPENAI_API_KEY` is available; skipped in simple/transcript modes without an API key.

## Packaging hygiene

- Do not publish generated outputs (e.g., `summaries/*.json`, `summaries/*.txt`) inside the skill folder.
- Keep only source files (`SKILL.md`, `scripts/`, `references/`, helpers) in release artifacts.

## Resources

- CLI runner: `scripts/run_youtube2md.sh`
- Transcript text prep: `prepare.py`
- Output guidance: `references/output-format.md`
- Behavior reference: `references/summarization-behavior.md`
- Security/install notes: `references/security.md`
- Troubleshooting and error codes: `references/troubleshooting.md`
