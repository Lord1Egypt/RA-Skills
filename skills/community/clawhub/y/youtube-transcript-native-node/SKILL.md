---
name: youtube-transcript-native-node
description: Extract a clean plain-text transcript from existing YouTube captions - native Node.js, zero npm dependencies. Use when the user asks to summarize, quote, or extract captions/transcript text from a YouTube URL. Wraps the `yt-dlp` binary on PATH; writes subtitles to a temp dir, parses .vtt captions, strips timestamps/HTML tags, and prints clean text or JSON. No API keys required.
version: 1.1.4
risk_class: external-binary-youtube-network-third-party-content
---

# YouTube Transcript (Native Node)

Version: 1.1.4 / publishable utility.

Minimal YouTube caption extractor. Native Node.js, zero npm dependencies, wraps the external `yt-dlp` binary.

## Risk / invocation class

Risk class: **external binary wrapper / YouTube network access / third-party content**.

Use deliberately. This skill does not call a web API directly, but `yt-dlp` talks to YouTube and the local environment owns the `yt-dlp` PATH/binary supply-chain trust boundary.

## Input packet

Required:

- `url`: full YouTube URL from the user.
- `goal`: raw transcript, summary input, quote extraction, timestamped notes, or JSON handoff.
- `privacy_sensitivity`: normal, private/client, or unknown.
- `language`: default `en` unless another language is requested.

Optional:

- `timestamps`: needed or not.
- `json`: needed for downstream tool use.
- `dedup_preference`: default auto-caption rolling-window dedup, or `--no-dedup` to preserve rolling-window/repeated-phrase artifacts as much as possible. Exact consecutive duplicate cue text may still be collapsed during VTT parsing.
- `output_destination`: chat summary, saved file, downstream summarizer, etc.

Stop or ask before use if the video/context is private or client-sensitive and sending access to YouTube via `yt-dlp` is not appropriate.

## Output packet

Return compactly:

- source YouTube URL
- language requested and whether timestamps/JSON were used
- transcript status: success, no captions, dependency missing, private/blocked/rate-limited, or failed
- whether captions appear auto-generated when known
- saved path if the transcript was separately written to a file
- concise transcript summary or excerpt, unless the user requested raw text
- caveats and next safe step

## Security behavior

- Accepts only `http(s)` YouTube URLs on `youtube.com`, `www.youtube.com`, `m.youtube.com`, or `youtu.be`.
- Validates `--lang` as a simple subtitle language code before invoking `yt-dlp`.
- Spawns `yt-dlp` with an argv array and no shell; it does not execute user-provided commands.
- Bounds the subprocess with a 120-second timeout.
- Creates and removes a temporary subtitle directory under the OS temp path.
- Refuses to print transcripts larger than 2,000,000 characters.
- Reads no API keys, env secrets, or credential/config files. Offline regression hooks are inert unless `YOUTUBE_TRANSCRIPT_SELFTEST=1` is set by `scripts/self-test.mjs`; do not set self-test hooks for normal transcript extraction.
- Passes `--ignore-config` so user-level `yt-dlp` config does not silently alter wrapper behavior.
- Static-analysis `child_process` warnings are expected because this skill intentionally wraps trusted `yt-dlp`.

## When to use

Use this when:

- the user provides a YouTube URL and wants spoken text/captions;
- clean plain text is needed for summarization, search, or quoting;
- the video has creator-uploaded subtitles or auto-generated captions.

Do not use this when:

- the user expects actual audio transcription; this extracts existing captions only;
- the platform is not YouTube;
- the video is a live stream that has not ended;
- the video/content is privacy-sensitive and should not be accessed via YouTube/yt-dlp;
- `yt-dlp` is not installed/on PATH and installing it has not been approved.

## Commands

Script: `scripts/fetch.mjs`

```powershell
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID"
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID" --lang es
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID" --timestamps
node "<skill-dir>\scripts\fetch.mjs" --url "https://www.youtube.com/watch?v=VIDEO_ID" --json
node "<skill-dir>\scripts\fetch.mjs" --help
```

For all flags, dedup details, output formats, dependency notes, and troubleshooting, load `references/youtube-transcript-contract.md`.

## Operating guidance

- Pass the full user-provided YouTube URL; do not invent/transform URL forms unnecessarily.
- Default to `--lang en` unless another language is clear.
- Use default plain text for direct human reading and summaries.
- Use `--json` as the default structured handoff for research triage, summarization, and downstream tooling.
- Use `--timestamps` only when timestamped notes, quote traceability, or debugging are needed; it is an advanced/evidence mode, not the recommended default for reading.
- Use `--json --timestamps` only for machine traceability workflows that need timestamp anchors inside JSON; it is not intended as a human-readable inspection format.
- Save long transcripts to a file when useful; do not paste giant transcripts unless requested.
- Summarize first and quote sparingly by default.
- Respect copyright and platform terms; do not republish long/full transcripts unless the user has rights or permission.
- Note that captions may be auto-generated and imperfect.

## Required checks before publishing/updating

Minimum no-video/no-network checks:

```powershell
node --check skills\youtube-transcript-native-node\scripts\fetch.mjs
node skills\youtube-transcript-native-node\scripts\self-test.mjs
node skills\youtube-transcript-native-node\scripts\fetch.mjs --help
node skills\youtube-transcript-native-node\scripts\fetch.mjs --url "https://example.com/watch?v=not-youtube" --json
```

The invalid-host smoke should fail before invoking `yt-dlp`.

Optional environment check:

```powershell
yt-dlp --version
```

Do not install/update `yt-dlp` as part of this skill without explicit approval.

## Public registry exposure

Classification: **publishable utility with external binary + YouTube access**.

Before public update, run sanitizer/static checks and ensure docs clearly disclose:

- `yt-dlp` dependency and PATH/binary trust boundary;
- YouTube-only URL allowlist;
- no API keys/env secrets/config reads;
- temp-directory behavior and stderr temp-path scrubbing;
- no audio/video download and no audio transcription;
- expected `child_process` static-analysis warning.
- best-effort scrub of temp- and home-directory paths from the last lines of `yt-dlp` stderr; unrelated absolute paths emitted by `yt-dlp` itself may remain.

Respect copyright and platform terms in examples, docs, and outputs: prefer summaries and brief quotes; do not publish long/full third-party transcripts unless rights or permission are clear.

Do not include private/internal/client strategy, operator-specific operational notes, or full third-party transcript samples in a public release.

## Changelog

- `1.1.4`: ClawHub publication/version refresh after public-readiness review; no runtime behavior change.
- `1.1.3`: Add stubbed offline yt-dlp fixture tests for dependency-missing, nonzero-exit-with-VTT, 429 hint, temp/home path scrubbing, output-size guard, timeout, and output modes; gate self-test hooks behind `YOUTUBE_TRANSCRIPT_SELFTEST=1`; continue when usable VTT subtitles are produced despite nonzero yt-dlp exit; kill active yt-dlp child on SIGINT/SIGTERM; broaden local-path scrubbing and scrub unexpected/read-error paths.
- `1.1.2`: Add offline self-test fixtures, export parser/allowlist helpers for tests, pass `--ignore-config`, remove subtitle conversion postprocessor to avoid ffmpeg ambiguity, scrub temp path from yt-dlp error tails, and surface 429 retry guidance.
- `1.1.1`: Public docs cleanup: normalized input/output packet wording, structured handoff wording, and changelog language; no runtime behavior change.

