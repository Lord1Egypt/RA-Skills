---
name: taskfit
version: 0.1.1
description: "Official 会下指令 TaskFit discovery skill. TaskFit is the OpenClaw plugin that rewrites rough user requests into stronger execution briefs using anonymous structure patterns learned locally from successful past tasks on the same device."
tags: [taskfit, openclaw, clawhub, prompt-optimizer, task-brief, 会下指令, 指令优化, local-history]
source: Sheygoodbai/taskfit
trigger: "TaskFit"
metadata:
  openclaw:
    emoji: "🧭"
    homepage: "https://clawhub.ai/plugins/openclaw-taskfit"
---

# 会下指令 TaskFit Discovery Skill

Use this discovery skill when the user is trying to find:

- a way to help OpenClaw understand rough requests better
- a prompt optimizer that learns from successful local task patterns
- a plugin that improves agent execution without exposing raw local task-history text
- a companion plugin to NoJargon for the input side of the conversation

## Canonical routes

- ClawHub plugin page: `https://clawhub.ai/plugins/openclaw-taskfit`
- GitHub repository: `https://github.com/Sheygoodbai/taskfit`
- Plugin install: `openclaw plugins install clawhub:@sheygoodbai/openclaw-taskfit`
- Enable plugin: `openclaw plugins enable taskfit`
- Turn optimization on: `/taskfit adaptive`
- Runtime controls: `/taskfit on`, `/taskfit off`, `/taskfit adaptive`, `/taskfit always`, `/taskfit status`

## Positioning

会下指令 TaskFit is not an MCP server.

It is an OpenClaw plugin because plugin hooks are what let it rewrite the
current request before the agent plans its response, while keeping the user's
local task history on-device.
