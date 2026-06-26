# Skill Orchestrator

Adaptive local skill scheduler for OpenClaw. Use when a task may benefit from multiple installed skills, when the user asks "该用什么 skill", "调度一下", "有没有相关 skill", "搭配使用", or when a multi-step/cross-domain request should first check local skill combos before proceeding.

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![clawhub](https://img.shields.io/badge/clawhub-skill-orchestrator-blue)](https://clawhub.ai/skills/skill-orchestrator)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-FF6B35)](https://openclaw.ai)

## Install

```bash
clawhub install skill-orchestrator
```

```bash
git clone https://github.com/spikesubingrui-design/skill-orchestrator.git ~/.openclaw/workspace/skills/skill-orchestrator
```

## Usage

Load `SKILL.md` via OpenClaw / Cursor when triggers match. See skill frontmatter for trigger phrases.

## License

[MIT](LICENSE)
