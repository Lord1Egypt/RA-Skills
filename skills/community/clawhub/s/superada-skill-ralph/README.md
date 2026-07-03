# ralph

Autonomous AI coding loop (Ralph) - runs Codex/Claude Code repeatedly until all PRD items are complete

## Structure

```
ralph/
├── README.md
├── SKILL.md
├── scripts/convert-prd.sh
├── scripts/create-prd.sh
├── scripts/run-ralph.sh
├── scripts/status.sh
```

## Scripts

- `convert-prd.sh` — Convert a PRD markdown file to prd.json for Ralph
- `create-prd.sh` — Create a PRD (Product Requirements Document) for a feature
- `run-ralph.sh` — Run Ralph loop on a project
- `status.sh` — Check Ralph loop status for a project

## Agent Instructions

This skill includes a `SKILL.md` file with instructions for AI agents on how to use it. If you're running [OpenClaw](https://github.com/openclaw/openclaw), drop this folder into your skills directory and it will be auto-detected.

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) or compatible AI agent framework
- Node.js 18+ (for JavaScript-based scripts)

## License

MIT
