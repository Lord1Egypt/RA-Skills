# AGENTS.md

Guidance for coding agents working on this repository.

## What this repo is

A standalone OpenClaw **skill**: `SKILL.md` (instructions the agent follows) + `scripts/`
(the actual runner and installer) + a local `.venv` built by `scripts/install.sh`.

## Commands

```bash
bash scripts/install.sh            # build/rebuild the venv and install deps
bash -n scripts/yt-transcribe.sh   # syntax check the runner
bash scripts/yt-transcribe.sh --help
```

## Rules

- Never commit secrets. `.env*` is gitignored except `.env.template`; real tokens live in a secrets
  store outside the repo, never in a tracked file.
- Never commit `.venv/` or downloaded media.
- Keep `SKILL.md`'s `description` accurate and keep script paths relative (`{baseDir}` in `SKILL.md`,
  `$SCRIPT_DIR` in scripts).
- The runner must stay self-contained: resolve `yt-dlp`/`whisper` from the venv first, then PATH.
- Keep the summary/research-plan procedures in `SKILL.md` in sync with actual behaviour.
