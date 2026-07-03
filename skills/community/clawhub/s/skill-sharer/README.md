# skill-sharer

Share skills publicly to GitHub with automatic sanitization of personal info, secrets, and IPs

## Structure

```
skill-sharer/
├── README.md
├── SKILL.md
├── scripts/generate-readme.sh
├── scripts/sanitize.sh
├── scripts/share-skill.sh
├── scripts/update-index.sh
```

## Scripts

- `generate-readme.sh` — generate-readme.sh — Generate a README.md for a skill folder
- `sanitize.sh` — sanitize.sh — Strip personal/security info from skill files
- `share-skill.sh` — share-skill.sh — Share a skill to Enterprise-Crew-skills repo
- `update-index.sh` — update-index.sh — Update the root README.md skill index

## Agent Instructions

This skill includes a `SKILL.md` file with instructions for AI agents on how to use it. If you're running [OpenClaw](https://github.com/openclaw/openclaw), drop this folder into your skills directory and it will be auto-detected.

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) or compatible AI agent framework
- Node.js 18+ (for JavaScript-based scripts)

## License

MIT
