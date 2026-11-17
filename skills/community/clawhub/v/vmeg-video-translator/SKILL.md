---
name: vmeg-media-translation
description: >-
  Use when the user needs video/audio/subtitle translation, material and task management,
  script editing, or export via VMEG in an AI coding assistant or OpenClaw agent.
  Requires VMEG Remote MCP (OAuth or vmeg_sk API Key). Tool usage follows MCP server instructions.
version: 1.0.0
category: media
platforms:
  - claude-code
  - cursor
  - windsurf
  - codex
  - gemini-cli
  - antigravity
  - qoderwork
  - workbuddy
  - openclaw
metadata:
  openclaw:
    homepage: https://www.vmeg.ai
    requires:
      network: true
---

# VMEG Media Translation

Call `vmeg_*` tools via VMEG Remote MCP (`https://www.vmeg.ai/api/mcp`).

## Authentication

Choose one (see [references/oauth.md](references/oauth.md)):

- **OAuth** — browser login and project selection in the client (recommended for individuals)
- **API Key** — `Authorization: Bearer vmeg_sk_xxx` (recommended for scripts/automation)

## Instruction priority

1. **MCP server instructions (highest)** — injected automatically after connecting. **Follow strictly; do not override with this Skill.**
2. **This Skill** — when to enable, connection prerequisites, platform doc routing, install/troubleshooting entry points.
3. **references/tools.md** — read only when the user asks what tools exist or what they do (quick reference, no parameter details).
4. **install / setup / oauth / README** — read only when the user asks about install, OAuth, API Key, or MCP connection failures.

## Platform detection and doc routing (Agent must read)

1. **Detect current platform** from the runtime (e.g. Cursor → `cursor`; Claude Code → `claude-code`; OpenClaw → `openclaw`). If unclear, **ask the user**; do not guess.
2. **Read only one setup file**: `references/setup-{platform}.md` (see table below). **Do not** read all `setup-*.md` files.
3. **MCP UI operations** — do **not** rely on hardcoded shortcuts or menu paths in this Skill. Instead:
   - Search **MCP** or **Model Context Protocol** in the current agent's Command Palette / Settings
   - Or read that platform's **official docs** / built-in help (e.g. cursor-guide in Cursor; OpenClaw Control UI `/settings/mcp`)
   - Optionally read the user's local MCP config (e.g. `~/.cursor/mcp.json`, `~/.openclaw/openclaw.json`) to verify setup
4. **VMEG-specific content** (endpoint, OAuth/API Key, config examples, presigned upload): read the current platform's setup file + [setup-common.md](references/setup-common.md) + [oauth.md](references/oauth.md).

| Current platform | Read |
|------------------|------|
| Cursor | [setup-cursor.md](references/setup-cursor.md) |
| Claude Code | [setup-claude-code.md](references/setup-claude-code.md) |
| Windsurf | [setup-windsurf.md](references/setup-windsurf.md) |
| Codex | [setup-codex.md](references/setup-codex.md) |
| Gemini CLI | [setup-gemini-cli.md](references/setup-gemini-cli.md) |
| Antigravity | [setup-antigravity.md](references/setup-antigravity.md) |
| QoderWork | [setup-qoderwork.md](references/setup-qoderwork.md) |
| WorkBuddy | [setup-workbuddy.md](references/setup-workbuddy.md) |
| OpenClaw | [setup-openclaw.md](references/setup-openclaw.md) |

## Prerequisites

Remote MCP must be configured and tools available. If `vmeg_*` tools are not callable, **do not guess business parameters**; follow routing above, read setup + oauth, and guide the user to connect in the **current platform's MCP settings**.

## Coding Agent supplement (fallback when MCP instructions do not cover)

When the user provides a local video/audio **absolute path** (**OAuth: presigned upload recommended**):

1. Use that path; do not scan the whole filesystem
2. Compute file MD5 (`md5sum` / `certutil -hashfile`)
3. Call `vmeg_initiate_material_upload` (`fileHash` + `extName`)
4. If not deduplicated: `curl -X PUT --upload-file @/path/to/file.ext "<presignedPutUrl>"` (**no** VMEG Bearer)
5. Call `vmeg_complete_material_upload`; use returned `materialId` for create-task tools

**API Key alternative**: one-shot `curl -F` to `/api/mcp/material/upload` (Bearer `vmeg_sk_...`)

## When to read which doc

| Scenario | Action |
|----------|--------|
| Translation, materials, tasks, editing, export | Follow **MCP server instructions** + call MCP tools |
| User asks what tools exist / what VMEG can do | Read [tools.md](references/tools.md); invocation details still from instructions |
| MCP not connected / auth failed / how to install | [install.md](references/install.md) + **platform routing**: matching `setup-*.md` + [setup-common.md](references/setup-common.md) + [oauth.md](references/oauth.md) |
| Day-to-day business | **Do not** read install / setup / oauth / README / tools.md |
