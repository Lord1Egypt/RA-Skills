# YouTube Transcript Contract

Use only when the compact `SKILL.md` is not enough.

## Commands

Script: `scripts/fetch.mjs`

```powershell
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID"
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID" --lang es
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID" --timestamps
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID" --json
node "<skill-dir>\scripts\fetch.mjs" --help
```

## Flags

| Flag | Values | Default | Purpose |
|---|---|---|---|
| `--url` | YouTube URL | required | Video to fetch captions for |
| `--lang` | language code | `en` | Subtitle language, e.g. `en`, `es`, `de` |
| `--timestamps` | flag | off | Keep `[hh:mm:ss]` prefixes in plain-text or JSON transcript output |
| `--json` | flag | off | Output `{ url, title, lang, auto, timestamps, transcript }` |
| `--no-dedup` | flag | off | Disable rolling-window dedup for auto-captions |
| `-h`, `--help` | flag | — | Show help |

## Credentials and dependency

No API keys or env secrets. Requires Node.js 18+ and `yt-dlp` installed/on PATH for normal use. Offline regression hooks are inert unless `YOUTUBE_TRANSCRIPT_SELFTEST=1` is set by `scripts/self-test.mjs`; do not set self-test hooks for normal transcript extraction. The wrapper requests VTT subtitles directly with `--sub-format vtt` and does not invoke yt-dlp's subtitle-conversion postprocessor.

Install examples:

- Windows: `winget install yt-dlp`
- macOS: `brew install yt-dlp`
- Cross-platform: use official yt-dlp project instructions.

Verify:

```powershell
yt-dlp --version
```

## Auto-caption rolling-window dedup

YouTube auto-generated captions often emit a 3-line scrolling window, causing repeated phrase spam when cues are concatenated.

When `auto: true`, the script trims YouTube's repeated scrolling-window caption artifacts. For timestamped output, it removes only newly repeated cue-prefix overlap when the overlap is 3+ words. For non-timestamp output, it also collapses consecutive identical 3- to 15-word phrases to one copy. This typically reduces transcript size substantially without losing content.

Conservative boundaries:

- Only runs for auto-captions.
- Only collapses consecutive repeats/overlaps.
- Preserves single-word repetition.
- `--timestamps` keeps timestamps while trimming repeated cue-prefix overlap.

Use `--no-dedup` if deliberate repeated 3+ word phrases must be preserved.

Timestamped cue-overlap comparison keeps only the last 500 transcript words in memory for matching; this is far larger than normal YouTube caption overlap and bounds long-video memory/comparison cost.

## Output formats

Default: cleaned plain text as one compact transcript paragraph, timestamps and HTML tags stripped.

With `--timestamps`: each line is prefixed with `[hh:mm:ss]`. Treat this as an advanced/evidence mode for quote traceability, timestamped notes, or debugging; default plain text is the recommended human-reading output.

With `--json`:

```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "title": "Video title from yt-dlp",
  "lang": "en",
  "auto": false,
  "timestamps": false,
  "transcript": "full cleaned transcript as a single string"
}
```

Use `--json` as the default machine/agent handoff for research triage, summarization, and downstream tooling. `--json --timestamps` is supported when a machine workflow needs timestamp anchors, but it is not intended as a human-readable inspection format because newlines are escaped inside the JSON string.

`auto` is true when only auto-generated captions were available. If yt-dlp metadata parsing is unavailable, `title` may be empty and `auto` falls back to best-effort detection.

Errors are CLI-style by design: success prints plain text or JSON to stdout; failures print a human-readable error to stderr and exit nonzero, even when `--json` was requested.

## What the script does

- Validates YouTube URL and flags.
- Creates a fresh temp directory under `os.tmpdir()` with `fs.mkdtempSync`.
- Spawns `yt-dlp` with argv array/no shell using `--skip-download`, `--write-subs`, `--write-auto-subs`, `--sub-lang`, `--sub-format vtt`, `--no-playlist`, `--no-warnings`, `--ignore-config`, `--print-json`, `-o <temp-template>`, `--`, and the allowlisted YouTube URL.
- Parses resulting `.vtt`: strips WEBVTT header, cue-id lines, timing lines, HTML tags, and consecutive duplicates.
- Prints plain text, timestamped plain text, or JSON.
- Removes temp directory best-effort on exit and kills the active `yt-dlp` child on SIGINT/SIGTERM.

## What it does not do

- Does not download audio or video.
- Does not transcribe audio; captions only.
- Does not modify configuration.
- Passes `--ignore-config` so user-level `yt-dlp` config is not read for this invocation.
- Does not write files outside the temporary subtitle directory it creates and removes.
- Does not call a web API directly; only `yt-dlp` talks to YouTube.
- Does not auto-update `yt-dlp`.

## Troubleshooting

- `yt-dlp not found on PATH` -> install yt-dlp and reopen shell.
- `no subtitles available for lang=<x>` -> video lacks captions in that language; try another language.
- `yt-dlp exited with code N` -> private, region-locked, age-restricted, removed, or other yt-dlp/provider failure. The helper performs best-effort scrubbing of temp- and home-directory paths from the stderr tail before printing; unrelated absolute paths emitted by `yt-dlp` itself may remain.
- HTTP 429 -> YouTube rate-limited the IP; wait before retrying. The helper surfaces a wait-before-retry hint when `429` or `too many requests` appears in yt-dlp stderr.
- Some `yt-dlp` versions may exit nonzero after still writing usable VTT subtitles. The helper continues with a warning when a subtitle file exists, and fails hard when no VTT is produced.
- `.vtt file not produced` -> usually no captions exist.
- Choppy auto-caption lines -> YouTube caption artifact; dedup helps but cannot fix every source issue.
- Respect copyright and platform terms; prefer summaries and brief quotes, and do not republish long/full transcripts unless you have rights or permission.

## Agent usage pattern

1. Pass the full user-provided YouTube URL.
2. Default to `--lang en` unless another language is clear.
3. Use default plain text for direct reading/summarization.
4. Use `--json` as the default structured handoff for research triage, summarization, and downstream tooling.
5. Use `--timestamps` only for quote traceability, timestamped notes, or debugging; full timestamp-per-cue output is intentionally not the default human-reading path.
6. Use `--json --timestamps` only for machine traceability workflows that need timestamp anchors inside JSON, not for human inspection.
7. Save long transcripts to a file when useful; summarize before pasting unless raw text is requested.
8. Cite the YouTube URL and note whether captions were auto-generated when known.

## Changelog

- `1.1.3`: Add stubbed offline yt-dlp fixture tests for dependency-missing, nonzero-exit-with-VTT, 429 hint, temp/home path scrubbing, output-size guard, timeout, and output modes; gate self-test hooks behind `YOUTUBE_TRANSCRIPT_SELFTEST=1`; continue when usable VTT subtitles are produced despite nonzero yt-dlp exit; kill active yt-dlp child on SIGINT/SIGTERM; broaden local-path scrubbing and scrub unexpected/read-error paths.
- `1.1.2`: Add offline self-test fixtures, export parser/allowlist helpers for tests, pass `--ignore-config`, remove subtitle conversion postprocessor to avoid ffmpeg ambiguity, scrub temp path from yt-dlp error tails, and surface 429 retry guidance.
- `1.1.1`: Public docs cleanup: normalized input/output packet wording, structured handoff wording, and changelog language; no runtime behavior change.
- `1.1.0`: Auto-caption cleanup update: timestamped output now trims 3+ word rolling cue overlap, non-timestamp output retains rolling phrase dedup, docs clarify JSON timestamp behavior/copyright posture/error behavior, and VTT timing parsing accepts short `mm:ss.mmm` cues.
- `1.0.5`: Review-date metadata refresh after public release audit; no runtime behavior change.
- `1.0.4`: Public release audit/rescan metadata refresh; no runtime behavior change.
- `1.0.3`: Public docs update with explicit `yt-dlp` trust boundary, YouTube host allowlist, temp-file behavior, and publish/update checks.
- `1.0.2`: Public-release hardening: 120-second `yt-dlp` timeout and 2,000,000-character output guard.
- `1.0.1`: Security/audit polish: documented trust boundary, host allowlist, no-shell spawn, language validation.
