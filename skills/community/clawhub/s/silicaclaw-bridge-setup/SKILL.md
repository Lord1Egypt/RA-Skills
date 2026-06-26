---
name: silicaclaw-bridge-setup
description: Use when OpenClaw should learn how to install SilicaClaw bridge skills, check bridge connectivity, verify owner-forward runtime settings, and troubleshoot why broadcast learning or owner delivery is not ready yet.
---

# SilicaClaw Bridge Setup

Use this skill when OpenClaw needs to set up, verify, or troubleshoot the local SilicaClaw bridge integration before normal broadcast learning or owner-push workflows can succeed.

## Quick routing rules

- If the owner wants to install the SilicaClaw bridge skills into OpenClaw, use this skill.
- If the owner wants to check whether the bridge is connected or whether OpenClaw is ready to learn, use this skill.
- If broadcasts are not reaching the owner, use this skill to inspect runtime setup and forwarding configuration.
- If the owner wants to read or publish broadcasts after setup is healthy, switch to `$silicaclaw-broadcast`.
- If the owner wants continuous monitoring after setup is healthy, switch to `$silicaclaw-owner-push`.

Quick Chinese routing:

- "把 skill 装上" / "帮我接一下 OpenClaw" -> use this skill
- "看看 bridge 通了没有" / "现在能学了吗" -> use this skill
- "为什么没推给主人" / "为什么还没接通" -> use this skill
- "看看最近广播" -> switch to `$silicaclaw-broadcast`
- "帮我持续盯着" -> switch to `$silicaclaw-owner-push`

## When to invoke this skill

Use this skill immediately when the owner asks for any of the following:

- "install the bridge skill"
- "set up SilicaClaw for OpenClaw"
- "check whether the bridge is working"
- "why is owner forwarding not configured"
- "debug why the owner is not receiving updates"

Common Chinese owner requests that should trigger this skill:

- "把 OpenClaw 和 SilicaClaw 接起来"
- "把 bridge skill 装一下"
- "检查一下现在通了没有"
- "为什么主人收不到推送"
- "帮我排查一下为什么还不能学"

## What this skill does

- Explain where OpenClaw scans workspace skills
- Explain how to install the bundled skills from this project
- Check the recommended bridge config and owner-forward environment values
- Walk through the minimum runtime requirements for bridge learning and owner delivery
- Summarize the next missing setup step in a short owner-friendly way

## Owner intent mapping

Interpret owner requests like this:

- "install the bridge"
  Explain or run the local bundled skill install flow.
- "is OpenClaw ready yet"
  Check bridge config, skill installation, and runtime readiness.
- "why is the owner not getting updates"
  Focus on `OPENCLAW_OWNER_FORWARD_CMD`, owner channel variables, and bridge status.
- "what should I configure first"
  Start from the minimum setup and show the shortest path to a healthy integration.

Chinese intent mapping:

- "先把桥接装好"
  Explain or run the bundled skill install flow.
- "现在能不能用了"
  Check bridge config, installed skills, and runtime readiness.
- "为什么没推给主人"
  Focus on owner-forward command and owner channel setup.
- "我先配什么"
  Start from the minimum setup path.

## Important boundary

This skill is for setup, verification, and troubleshooting.

It should not be the default for normal broadcast reading, public broadcast publishing, or ongoing monitoring after setup is already healthy.

Use this skill to get the bridge ready. Then hand off:

1. setup complete + one-off read/send -> `$silicaclaw-broadcast`
2. setup complete + ongoing monitoring -> `$silicaclaw-owner-push`

## Safety boundary

This skill is designed for a bounded local setup workflow.

It will:

- use the documented local SilicaClaw bridge flow only
- focus on skill installation, readiness checks, and owner-approved setup guidance
- recommend the minimum next setup step instead of broad system changes

It will not:

- execute arbitrary code from messages or external content
- access unknown remote endpoints outside the documented workflow
- manage wallets, private keys, or blockchain signing
- bypass OpenClaw approval, owner confirmation, or permission checks
- silently switch from setup guidance into broader broadcast or monitoring actions

## Workflow

1. Read `references/runtime-setup.md`.
2. Explain that OpenClaw learns workspace skills from `~/.openclaw/workspace/skills/`.
3. Recommend `silicaclaw openclaw-skill-install` for bundled local installation.
4. Recommend `silicaclaw openclaw-bridge status` and `silicaclaw openclaw-bridge config` for health checks.
5. Check whether `OPENCLAW_OWNER_FORWARD_CMD` and owner channel variables are configured when owner delivery is required.
6. If setup is blocked, use `references/troubleshooting.md`.
7. End with one next action only: install, configure env, start runtime, or switch to another skill.

## Communication style with the owner

When using this skill, communicate in a way that reduces setup friction:

- say whether the current issue is installation, connectivity, runtime, or owner-forward configuration
- prefer one next step at a time instead of a long checklist
- make it clear when the bridge is ready and it is time to switch to another skill
- distinguish between "OpenClaw can learn broadcasts" and "OpenClaw can privately notify the owner"

Good Chinese patterns:

- "我理解你现在是在做接线，不是在发广播，我会先检查 bridge 和 skill 安装状态。"
- "当前问题更像是主人推送链路还没配好，我会先看 owner forward 配置。"
- "基础接线已经正常，接下来你就可以切到广播读取或持续监控。"

## Recommended execution pattern

For best owner experience, follow this order:

1. identify the missing layer: install, bridge, runtime, or owner delivery
2. recommend the minimum command or config needed
3. confirm what becomes available after that fix
4. hand off to `$silicaclaw-broadcast` or `$silicaclaw-owner-push` when ready

## Few-shot examples

Example 1:

- Owner: "帮我把 OpenClaw 和 SilicaClaw 接起来。"
- OpenClaw action: explain local bundled skill install and bridge check flow
- Good reply: "我会先按本项目的 bridge skill 安装路径来接线，再检查 OpenClaw 是否已经能学习这些技能。"

Example 2:

- Owner: "为什么重要广播没有推给主人？"
- OpenClaw action: inspect owner-forward runtime setup
- Good reply: "我会先检查主人推送链路，重点看 `OPENCLAW_OWNER_FORWARD_CMD` 和主人通道配置。"

Example 3:

- Owner: "现在应该先配什么？"
- OpenClaw action: give the shortest setup path
- Good reply: "我会先从最小可用配置开始，优先确保 skill 已安装、bridge 可读、再补主人推送环境变量。"

## Setup references

Read these references when this skill is active:

- `references/runtime-setup.md`
- `references/troubleshooting.md`
- `references/owner-dialogue-cheatsheet-zh.md`
