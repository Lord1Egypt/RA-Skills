---
name: rtk-rewrite
version: "0.15.3"
author: "luw2007"
repository: "https://github.com/rtk-ai/rtk"
license: MIT
published: true
tags: rtk, openclaw, plugin, token-saving, rewrite
description: >
  RTK rewrite plugin for OpenClaw. Intercepts exec tool calls and delegates
  rewrites to rtk rewrite to reduce token usage while preserving command intent.
---

# RTK Rewrite OpenClaw Plugin

This plugin hooks into OpenClaw's `before_tool_call` lifecycle:

- Intercepts only `exec` tool calls
- Calls `rtk rewrite "<command>"` to request a rewrite
- Replaces the original command when a rewrite is available
- Supports optional audit logs compatible with Claude Code hook audit format

## Prerequisites

`rtk` must be installed and available in `PATH`.

```bash
brew install rtk-ai/tap/rtk
```

## Install Plugin Files

Copy plugin files to the OpenClaw extensions directory:

```bash
mkdir -p ~/.openclaw/extensions/rtk-rewrite
cp index.ts openclaw.plugin.json ~/.openclaw/extensions/rtk-rewrite/
openclaw config set plugins.entries.rtk-rewrite.enabled true
openclaw gateway restart
```

## Configuration

- `enabled`: Enables rewrite behavior. Default `true`.
- `verbose`: Prints rewrite logs to console. Default `false`.
- `audit`: Writes hook-style audit logs. Default `false`.
- `auditDir`: Optional audit directory. Falls back to `RTK_AUDIT_DIR` or `~/.local/share/rtk`.

## Verification

```bash
rtk rewrite "git status"
rtk hook-audit --since 7 -v
```
