---
name: Yabbie Net
slug: yabbie-net
version: 0.2.0
description: A safety net for AI agents. Catches unsafe tool calls before they execute.
author: Devlines
homepage: https://yabbie.net
repository: https://github.com/Devlines/yabbie.net
license: MIT
tags:
  - security
  - safety
  - guardrails
  - mcp
  - proxy
  - governance
category: security
env:
  - name: ANTHROPIC_API_KEY
    required: false
    description: Required ONLY if tier2 AI judge is enabled with provider "anthropic". Not needed for tier1-only mode.
---

# Yabbie Net — A Safety Net for AI Agents

Yabbie Net is an open-source MCP proxy that sits between your OpenClaw agent and its tools, catching unsafe actions before they execute.

**Source code**: [github.com/Devlines/yabbie.net](https://github.com/Devlines/yabbie.net) (MIT licensed, fully auditable)

## What It Does

Three tiers of protection:

1. **Deterministic rules** (instant, free, no external calls) — file path deny lists, tool blocklists, rate limits
2. **AI intent judge** (optional, opt-in only) — a small model checks if each action matches your stated goal
3. **Human escalation** (rare) — you only see actions that are uncertain AND irreversible

**Tier 1 requires no API keys, makes no network calls, and sends no data externally.** It runs entirely locally using pattern matching.

## Security and Privacy

Because this is a security tool, transparency matters. Here is exactly what Yabbie Net does and does not do:

**What the proxy sees:**
- Tool names and arguments passing through the MCP stdio channel (same data the MCP server already receives)

**What is sent externally (ONLY when tier2 is explicitly enabled):**
- Tool name
- Truncated argument summary (keys + types + short values; large content like file bodies is replaced with byte counts — never sent in full)
- Your `taskContext` string from `yabbie.yaml`
- Sent to: Anthropic API (if `provider: anthropic`) or localhost Ollama (if `provider: ollama`)

**What is NEVER sent externally:**
- Full file contents, full argument values, or raw MCP traffic
- Any data when tier2 is disabled (the default)
- Telemetry is opt-in only (`telemetry: true` in config). Anonymous aggregates only (latency percentiles, verdict ratios). No tool names, no arguments, no file paths.

**Credentials:**
- `ANTHROPIC_API_KEY` — required ONLY if you enable tier2 with `provider: anthropic`. Set it in your shell environment. Not needed for tier1-only mode.
- No other credentials are required.

## Setup

Install as a project dependency (recommended over global install):

```bash
npm install yabbie-net@0.2.0
```

Or install globally:

```bash
npm install -g yabbie-net@0.2.0
```

In your `openclaw.json`, wrap any MCP server:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["yabbie-net@0.2.0", "--verbose", "--", "npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    }
  }
}
```

**Note:** This modifies how your MCP servers are invoked. Yabbie acts as a transparent proxy — all tool calls pass through it. Review the [source code](https://github.com/Devlines/yabbie.net/blob/main/src/proxy.ts) to understand the interception mechanism.

## Configuration

Create `yabbie.yaml` in your project root:

```yaml
version: 1

# Tier 1: Local rules only. No network calls. No API keys needed.
tier1:
  files:
    deny: ["**/.env", "**/secrets*", "**/*.pem", "**/*.key"]
  tools:
    deny: ["shell_exec"]
  rateLimit:
    maxCallsPerMinute: 30

# Tier 2: DISABLED by default. Requires ANTHROPIC_API_KEY if enabled.
# Sends tool name + truncated args to the configured provider.
tier2:
  enabled: false
  provider: anthropic       # "anthropic" (requires ANTHROPIC_API_KEY) or "ollama" (local, no key)
  sensitivity: balanced
  taskContext: "Describe what your agent should be doing"

# Tier 3: Human approval for uncertain + irreversible actions.
tier3:
  enabled: true
  channel: stderr

log:
  verbose: true

# Anonymous telemetry. Off by default. No tool names or arguments ever sent.
telemetry: false
```

**Recommended first step:** Start with tier1 only (the default). No API keys needed, no external calls. Add tier2 later once you've reviewed the audit logs and understand your agent's patterns.

## How It Affects Other Skills

When you route an MCP server through Yabbie in `openclaw.json`, the proxy intercepts `tools/call` JSON-RPC messages for that server. This means:

- Tool calls may be **blocked** if they match deny rules (the agent receives a clear error message)
- Tool calls may be **delayed** by ~1ms for tier1 checks, or ~300-800ms if tier2 is enabled
- All other MCP messages (initialize, tools/list, notifications) pass through unmodified
- The proxy does not modify tool arguments or responses — it only allows or blocks

## Why This Exists

Cisco research found 36% of ClawHub skills contain prompt injection vulnerabilities. Agents have exfiltrated data, created unauthorized accounts, and deleted production databases. NVIDIA's NemoClaw addresses this but requires RTX/DGX hardware.

Yabbie Net is a lightweight, software-only safety layer that runs anywhere.

## Audit and Verify

All actions are logged locally to `.yabbie/audit.jsonl`:

```bash
npx yabbie-net log --tail 20   # View recent actions
npx yabbie-net stats            # View performance metrics
```

## Links

- [Source Code](https://github.com/Devlines/yabbie.net) — fully auditable, MIT licensed
- [Report Issues](https://github.com/Devlines/yabbie.net/issues)
