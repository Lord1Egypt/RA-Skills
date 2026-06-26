# Integration Guide

## Goal

Keep one canonical behavior while enabling quick drop-in usage across different frameworks.

## Recommended mapping

- Cursor: `.cursor/skills/speak4bangboo/SKILL.md`
- Claude: `prompts/claude-project.md`
- OpenClaw-like runtimes: `prompts/openclaw-system.md`
- Shared canonical rules: `prompts/core-rules.md`
- Strict combo source: `.cursor/skills/speak4bangboo/reference-lexicon.md`

## Why this structure works

- Framework-specific files reduce prompt-format friction.
- Core rules stay reusable and concise.
- Lexicon remains a strict add-on for Chinese combo fidelity.

## Validation checklist

1. Chinese user input -> outer grunt uses only 嗯/呢/哇/哒; meaning uses `（...）`.
2. English user input -> outer grunt uses Ehn-na style; meaning uses `(...)`.
3. Safety refusal still appears in the real-meaning content.
4. Code response uses one grunt lead line + normal fenced block.
5. If user requests "no roleplay", assistant exits Bangboo style.
