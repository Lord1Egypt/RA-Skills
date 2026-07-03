# Security and installation considerations

Review this before installing or enabling the skill.

## 1) Runtime dependencies are mandatory

The runner relies on:

- Node.js 18+
- preinstalled `youtube2md` executable on PATH
- `python3` (for transcript text preparation via `prepare.py`)

## 2) Command execution hardening

The runner executes only a resolved local executable path from `type -P youtube2md`.

Hardening behavior:

- no runtime npm execution (`npx`) path exists
- legacy env-based command overrides are blocked:
  - `YOUTUBE2MD_BIN`
  - `YOUTUBE2MD_ALLOW_RUNTIME_NPX`

This removes both arbitrary command override vectors and runtime npm execution at run time.

## 3) Installation-time supply-chain boundary

Even without runtime `npx`, trust still depends on how `youtube2md` is installed.

Recommended baseline:

- install pinned version: `npm i -g youtube2md@1.0.2`
- in stricter environments: use a vetted internal mirror or vendored reviewed package
- re-audit dependencies before any future version bump

## 4) OPENAI_API_KEY data exposure boundary

Providing `OPENAI_API_KEY` enables full summarization mode in youtube2md workflows.

Practical implication:

- transcript text and/or audio-derived content may be sent to OpenAI APIs.

If content is sensitive, do not set `OPENAI_API_KEY`; use extract-only mode when captions are available and summarize locally from prepared transcript text.

## 5) YouTube cookie boundary

`YOUTUBE_COOKIES_PATH` and `YOUTUBE_COOKIE_HEADER` can allow youtube2md to access captions or audio that anonymous requests cannot reach.

Practical implications:

- cookie files/headers are credentials and should not be logged, committed, or shared
- cookie-backed requests may expose signed-in YouTube session context to the local tool runtime
- use short-lived exports when possible and delete them after use in sensitive environments

## 6) Upstream trust and review

`prepare.py` and the local shell runner are simple and readable, but the highest trust boundary is still the upstream `youtube2md` package and its dependencies.

Before production use in sensitive environments:

- review upstream source and release history for `youtube2md@1.0.2`
- verify dependency tree and lock strategy
- define an update cadence and re-audit process

## Recommended maintainer actions

1. Keep runtime dependencies explicit in skill docs (`Node.js/python3`, plus `youtube2md` executable requirement).
2. Keep runtime command behavior fail-closed (no env-based command override execution).
3. Keep package target fixed at `youtube2md@1.0.2` until the next explicit reviewed version bump.
4. Document `OPENAI_API_KEY` behavior as an explicit data-sharing choice.
5. Treat YouTube cookie env vars as sensitive credentials.
6. Re-audit upstream package versions before bumping pins.
7. Exclude generated `summaries/*` outputs from release packages.
