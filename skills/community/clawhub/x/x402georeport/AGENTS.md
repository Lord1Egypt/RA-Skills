# AGENTS.md

Repository guidance for agents using this skill package.

## Package Purpose

- Name: `x402geo-skill`
- Type: standalone skill package
- Primary entrypoint: `SKILL.md`

This repository is designed to work both as a Claude plugin-backed skill package and as a `skills.sh`-style skill directory.

## Structure

- `SKILL.md`: main skill definition
- `.claude-plugin/plugin.json`: Claude plugin metadata
- `marketplace.json`: marketplace metadata for skills-directory ecosystems
- `agents/openai.yaml`: lightweight agent UI metadata

## Compatibility Notes

- The skill slug is `x402geo-skill` and should stay aligned with the directory name.
- Keep `SKILL.md`, `.claude-plugin/plugin.json`, and `marketplace.json` names/version metadata in sync.
