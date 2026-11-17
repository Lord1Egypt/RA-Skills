# Security and installation considerations

Review this before installing or enabling the skill.

## 1) Runtime dependencies are mandatory

The runner relies on:

- Node.js 20.18.1+
- preinstalled `youtube2md` executable on PATH (pinned `youtube2md@1.2.0`)

Python is no longer required: youtube2md (since 1.0.3) emits transcript text natively (`--extract-format text|timestamped-text`).

## 2) Command execution hardening

The runner executes only a resolved local executable path from `type -P youtube2md` (plus `codex login status` for read-only provider detection when the `codex` CLI is present).

Hardening behavior:

- no runtime npm execution (`npx`) path exists
- legacy env-based command overrides are blocked:
  - `YOUTUBE2MD_BIN`
  - `YOUTUBE2MD_ALLOW_RUNTIME_NPX`

This removes both arbitrary command override vectors and runtime npm execution at run time.

## 3) Installation-time supply-chain boundary

Even without runtime `npx`, trust still depends on how `youtube2md` is installed.

Recommended baseline:

- install pinned version: `npm i -g youtube2md@1.2.0`
- 1.2.0 vs 1.1.0 diff is limited to `dist/summarizer.*` (prompting, chunk thresholds, section sizing) plus `README.md` and the version field; the dependency set and CLI surface are unchanged, so a 1.1.0 audit carries over except for the summarizer behavior itself
- the optional Codex provider adds a second package: `npm i -g @openai/codex-sdk` (large platform binary; only install if the Codex path is wanted)
- in stricter environments: use a vetted internal mirror or vendored reviewed package
- re-audit dependencies before any future version bump

## 4) Summarization provider data exposure boundary

Full mode sends transcript-derived content to OpenAI systems through whichever provider runs:

- **Codex SDK with ChatGPT login** (preferred by `--provider auto`): uses the ChatGPT session; `OPENAI_API_KEY` is not passed to Codex. Codex runs in a temporary read-only working directory with tool, command, and web use disabled.
- **OpenAI API fallback**: requires `OPENAI_API_KEY`; also enables the Whisper STT audio fallback.

Practical implication:

- transcript text and/or audio-derived content may be sent to OpenAI whenever a provider is available.

If content is sensitive, use extract-only mode. The runner's extract mode passes `--captions-only` by default, so audio is never uploaded to Whisper even when `OPENAI_API_KEY` is set; captions are fetched from YouTube and summarization happens locally from the transcript text. Only set `YOUTUBE2MD_CAPTIONS_ONLY=0` when uploading audio to OpenAI is acceptable.

**Full mode has no such default guard.** It keeps the Whisper fallback available, so a captionless video can have its audio downloaded and uploaded to OpenAI whenever `OPENAI_API_KEY` is set. Set `YOUTUBE2MD_CAPTIONS_ONLY=1` to forbid audio upload in full mode as well — the runner now honors it there (it used to apply the flag in extract mode only, silently ignoring an explicit opt-out in full mode). Captionless videos then fail instead of being transcribed.

## 5) YouTube cookie boundary

`YOUTUBE_COOKIES_PATH` and `YOUTUBE_COOKIE_HEADER` can allow youtube2md to access captions or audio that anonymous requests cannot reach.

Practical implications:

- cookie files/headers are credentials and should not be logged, committed, or shared
- cookie-backed requests may expose signed-in YouTube session context to the local tool runtime
- use short-lived exports when possible and delete them after use in sensitive environments

## 6) Upstream trust and review

The local shell runner is simple and readable, but the highest trust boundary is still the upstream `youtube2md` package and its dependencies (now exact-pinned in the package: `@distube/ytdl-core`, `commander`, `dotenv`, `openai`, `tiktoken`, `youtube-transcript`, plus the optional `@openai/codex-sdk` peer).

Before production use in sensitive environments:

- review upstream source and release history for `youtube2md@1.2.0`
- verify dependency tree and lock strategy
- define an update cadence and re-audit process

## Recommended maintainer actions

1. Keep runtime dependencies explicit in skill docs (Node.js 20.18.1+, `youtube2md` executable, optional `@openai/codex-sdk`).
2. Keep runtime command behavior fail-closed (no env-based command override execution).
3. Keep package target fixed at `youtube2md@1.2.0` until the next explicit reviewed version bump.
4. Document both summarization providers (Codex ChatGPT login and `OPENAI_API_KEY`) as explicit data-sharing choices.
5. Keep extract mode captions-only by default; treat `YOUTUBE2MD_CAPTIONS_ONLY=0` as an explicit audio-upload opt-in.
6. Treat YouTube cookie env vars as sensitive credentials.
7. Re-audit upstream package versions before bumping pins.
8. Exclude generated `summaries/*` outputs from release packages.
