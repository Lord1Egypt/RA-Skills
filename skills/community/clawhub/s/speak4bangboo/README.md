# speak4bangboo

Cross-framework Bangboo persona pack for LLMs (Cursor, Claude, OpenClaw, and other prompt-driven runtimes).

This repository provides reusable Bangboo-style prompt assets with one shared behavior contract:

- Outer grunt prefix is decorative.
- Parentheses carry the real meaning.
- Safety and factual constraints are enforced in real-meaning content.

## Why this repo

- One canonical behavior across multiple platforms.
- Better Chinese/English consistency for Bangboo voice.
- Drop-in prompt files for Cursor, Claude, and OpenClaw.

## Project layout

- `.cursor/skills/speak4bangboo/SKILL.md`: Cursor-native skill entry (`name: speak4bangboo`).
- `.cursor/skills/speak4bangboo/reference-lexicon.md`: strict Chinese combos + English onomatopoeia examples.
- `prompts/core-rules.md`: platform-agnostic canonical rules.
- `prompts/claude-project.md`: paste-ready block for Claude Project/Instructions.
- `prompts/openclaw-system.md`: paste-ready system prompt for OpenClaw-like runtimes.
- `docs/integration.md`: integration and validation checklist.
- `CLAUDE.md`: Claude quick entry file.
- `OPENCLAW.md`: OpenClaw quick entry file.

## Quick start

### Cursor

1. Keep repository structure unchanged.
2. Ensure `.cursor/skills/speak4bangboo/SKILL.md` is available.
3. Include `reference-lexicon.md` in context for strict Chinese combo output.

### Claude

1. Copy `prompts/claude-project.md` into Project Instructions.
2. Add `reference-lexicon.md` as project knowledge for strict combo mode.

### OpenClaw (or equivalent)

1. Use `prompts/openclaw-system.md` as system prompt.
2. Load `reference-lexicon.md` in memory/knowledge (optional but recommended).

## GitHub publishing checklist

Before creating a public release:

1. Review prompt files under `prompts/`.
2. Verify examples and constraints in `reference-lexicon.md`.
3. Update `CHANGELOG.md`.
4. Tag version (for example: `v1.1.0`).
5. Create a GitHub Release with change summary and compatibility notes.

## Contributing

Please read `CONTRIBUTING.md` before opening pull requests.

## Release process

See `RELEASING.md` for the versioning and GitHub release checklist.

## License

Released under the MIT License. See `LICENSE`.
