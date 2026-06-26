# UI/UX Pro Max (OpenClaw Port)

An OpenClaw-native, zero-dependency skill that provides intelligent UI/UX design reasoning and automatic styling guidelines for agents.

> **Note**: This is a direct, natively-optimized port of the excellent [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) created by [NextLevelBuilder](https://github.com/nextlevelbuilder). 
> The Python reasoning engine and dataset are entirely their work. This package has simply adapted the documentation (`SKILL.md`) to use OpenClaw's robust Local Skill execution model via standard `exec` permissions, bypassing the need for ACP configurations.

## Features
- Provides an AI agent with a 100% offline, local search engine containing 67 UI styles, 96 color palettes, and 57 font pairings.
- Natively forces the agent (via `SKILL.md` constraints) to run the `search.py` evaluator BEFORE blindly outputting generic HTML/CSS.
- Works perfectly with OpenClaw's `messaging` profile when granting explicit `python3` safeBin execution rights.

## Installation

Extract this directory into your OpenClaw agent's workspace `skills/` folder, or directly into the global `~/.openclaw/skills/` directory. 

Ensure your agent's `tools.exec.safeBins` includes `python3` if it is operating under a restricted profile.

## License
MIT License. See the `LICENSE` file for details.
