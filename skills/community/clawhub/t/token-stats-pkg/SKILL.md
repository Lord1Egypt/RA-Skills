---
name: agent-usage-stats
description: "选择要监控的 AI 助手 → 查看 token 消耗。支持 Hermes / Claude Code / CodeX / OpenClaw，每次都让你选"
version: 2.0.9
author: zhouhaoyong
license: MIT
source: https://github.com/zhouhaoyong/token-stats
clawhub: https://clawhub.ai/zhouhaoyong/agent-usage-stats
tags:
  - token
  - usage
  - monitoring
  - cross-agent
  - interactive
---

# token-stats — 选个 Agent 看它的消耗

## 核心原则

1. **每次运行都弹菜单** — 你想看哪个 Agent 就选哪个，不预设
2. **数据来自本地** — 不联网，纯读你的 Agent 本地数据文件
3. **零依赖** — 纯 Python 标准库，装完即用

## 前置条件

- Python 3.8+
- 至少一种 Agent 有使用记录：Hermes / Claude Code / CodeX / OpenClaw
- 安装方式：`clawhub install agent-usage-stats`，然后 `python3 ~/skills/agent-usage-stats/token-stats.py setup`

## 用法速查

```bash
# 交互式菜单（默认）
token-stats

# 跳过菜单直接看
token-stats -b hermes
token-stats -b claude-code
token-stats -b codex

# 实时监控
token-stats --watch
token-stats -b hermes --watch

# 查看本机装了哪些 Agent
token-stats --list-backends

# 查看版本
token-stats --version
```

## Hermes 集成

Hermes 的 SKILL.md 里可以这样用：

```yaml
run: token-stats -b hermes
```

这样每次任务结束会自动输出 Hermes 的 token 消耗，不弹菜单。

## 数据源说明

| Agent | 数据读哪里 |
|-------|-----------|
| Hermes | `~/.hermes/state.db` → sessions 表 |
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| CodeX | `~/.codex/state_*.sqlite` → threads 表 |
| OpenClaw | `~/ai-testing-lab/openclaw/data/.../sessions.json` |
