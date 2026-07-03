# Contributing to RealBrowser by Ceki

Thanks for considering a contribution. This skill is a thin client to the Ceki marketplace — most logic lives in `ceki-sdk` (Python/Node) and on the backend.

## What this repo contains

- `SKILL.md` — instructions for AI agents using this skill (the primary user-facing artifact)
- `manifest.json` — ClawHub metadata
- `README.md`, `LICENSE`, `install.sh`, `CHANGELOG.md` — repo hygiene
- `clawhub-listing.md` — submission copy for the ClawHub registry
- `examples/` — integration configs (Claude Desktop, Cursor, Cline) + Python/Node quickstarts

## What this repo does NOT contain

- The marketplace dispatcher (closed source, runs on api.ceki.me)
- The Ceki Chrome extension (separate distribution at [browser.ceki.me/install](https://browser.ceki.me/install))
- The ceki-sdk CLI / Python SDK ([ceki-sdk on PyPI](https://pypi.org/project/ceki-sdk/) — separate repo)

## How to contribute

### Reports

- Bug in the skill instructions (wrong CLI flags, outdated examples, typos) → open an issue
- Broken integration example (Claude Desktop, Cursor, Cline config) → open an issue with the host name + version
- Anti-bot regression (a site that used to pass started failing) → open a discussion, not an issue (the fix usually lands in the SDK / extension, not here)

### PRs

- Doc fixes, typo corrections, clarity improvements → welcome
- New integration examples (LangGraph, Letta, AutoGen, etc.) → welcome
- New SKILL.md sections → please open a discussion first to align on scope

### Things we won't merge

- PRs adding specific anti-detect mechanics or fingerprint-spoofing details to SKILL.md (we keep that surface generic on purpose)
- PRs that hardcode credentials or token paths
- PRs that change pricing or revenue share (those are policy, not docs)

## License

By contributing, you agree your work is MIT-licensed (see `LICENSE`).

## Code of conduct

Be respectful. Hosts are real people; agents act on their behalf. Don't propose anything that breaks that trust.
