---
name: wcs-helper-feishu-skill
description: Configure OpenClaw Feishu plugin without editing config files. Send simple commands via Feishu private chat to toggle streaming, set group reply behavior, run diagnostics, or restart the service. No CLI knowledge needed.
metadata:
  openclaw:
    tags: ["feishu", "openclaw", "config", "chat", "plugin", "setup"]
    user-invocable: true
version: 1.0.0
---

# WCS Helper: Feishu Plugin Config

> Configure OpenClaw's Feishu plugin without touching config files.

---

## When You Need This

**Scenario A — "My AI is not responding in group chat"**
→ Send `/万重山-飞书-群里` → choose option → select **"@才回"** or **"自动回复"**

**Scenario B — "The reply is too fast, I want to see it type out"**
→ Send `/万重山-飞书-打字效果` → toggles streaming mode ON/OFF

**Scenario C — "OpenClaw feels stuck, something is wrong"**
→ Send `/万重山-飞书-诊断` → checks processes, memory, disk, network

**Scenario D — "Diagnosis found a problem, fix it automatically"**
→ Send `/万重山-飞书-修复` → applies automatic fixes

**Scenario E — "Just want to see current settings"**
→ Send `/万重山-飞书` → shows all current settings at once

---

## All Commands

| Command | What It Does |
|---------|-------------|
| `/万重山-飞书` | Show all current settings |
| `/万重山-飞书-打字效果` | Toggle streaming mode (watch AI type) |
| `/万重山-飞书-群里` | Change group reply behavior |
| `/万重山-飞书-诊断` | Run diagnostic checks |
| `/万重山-飞书-修复` | Apply automatic fixes |
| `/万重山-飞书-重启` | Restart OpenClaw service |

---

## Setup

### Prerequisites

- OpenClaw installed and running
- Feishu bot configured (app_id + app_secret from Feishu Open Platform)
- Bot added to your Feishu workspace

### Installation

```bash
npx -y clawhub install guanqi0914/wcs-helper-feishu-skill
```

### First-Time Setup

After installing, send `/万重山-飞书` to the bot to verify it works and see current settings.

---

## Feature Details

### Streaming Mode (`/万重山-飞书-打字效果`)

When ON: AI responses appear word-by-word in real-time, like watching someone type.

When OFF: AI waits until the full response is ready, then sends it at once.

Use cases:
- ON: Conversational chat, brainstorming, interactive dialogue
- OFF: Long reports, structured output, code generation

### Group Reply Behavior (`/万重山-飞书-群里`)

Three modes:
1. **@才回** (default): Bot only responds when mentioned with @ — good for large groups
2. **自动回复**: Bot analyzes every group message and responds to relevant ones — good for small groups or focused discussions
3. **关闭**: Bot ignores all group messages

### Diagnostics (`/万重山-飞书-诊断`)

Checks:
- OpenClaw process status
- Feishu streaming configuration
- Memory and disk usage
- OpenClaw log errors (last 50 lines)

### Auto-Fix (`/万重山-飞书-修复`)

Automatically fixes:
- Memory bloat (high memory usage from old processes)
- Zombie autossh tunnel (stale SSH tunnel processes)
- Disk space warnings

### Restart (`/万重山-飞书-重启`)

Restarts the OpenClaw service. Use when:
- Configuration changes don't take effect
- OpenClaw is unresponsive
- After changing streaming or group reply settings

---

## Architecture

```
You (Feishu) 
    ↓ send command
OpenClaw Bot 
    ↓ route to skill
wcs-helper-feishu-skill
    ↓ reads config
~/.openclaw/config/channels.json
    ↓ applies change
OpenClaw reloads config
```

Config file location: `~/.openclaw/config/channels.json`

---

## Troubleshooting

**Bot doesn't respond to commands**
→ Make sure you're sending a private message to the bot, not a group message

**Streaming toggle has no effect**
→ Send `/万重山-飞书-重启` to reload the config

**Group reply mode doesn't work**
→ Check if the bot has `im:message` permissions in the Feishu Open Platform

**Diagnostics show errors**
→ Send `/万重山-飞书-修复` to apply automatic fixes
