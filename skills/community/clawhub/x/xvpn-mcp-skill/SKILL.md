---
name: xvpn-mcp-skill
description: |
  Use when your task hit or is about to hit a geo-related failure
  (HTTP 403 / 451, region-restricted response body, region-defaulted
  content), or when the user explicitly asks to route through a
  specific country. Provides X-VPN MCP tools to open / close a
  region-specific egress so the user's real task can finish; treat
  any explicit "connect through X" as a step toward the follow-up
  task, not the goal itself.
---

# X-VPN MCP Skill

This file is a router. Read it, then load only the reference that
matches your situation. Most tasks need this file plus one reference.

## When to use these tools

Two entry points:

- **Reactive** — your task hit a geo-block (403 / 451 with region
  language, or visibly truncated / region-defaulted content). Most
  common entry.
- **Anticipatory** — the user's request has geography baked in
  ("trending on US Reddit", "audit our JP site", "as Singapore would
  see it").

Don't trigger for country knowledge or travel questions, tasks with
no geo signal, or when the user said "no VPN". For the full signal
checklist and how to disambiguate geo from auth / rate-limit
failures before connecting, see `references/task-integration.md`.

## Core principle

These tools belong inside your task plan, not as the plan itself.

1. **Start with `xvpn_get_overview`.** It returns account state and
   VPN state together; you'll rarely need to ask anything else first.
2. **Search, don't browse.** `xvpn_list_locations(search="...")` is
   almost always the right call. The full tree has 250+ nodes.
3. **Leave the egress as you found it.** If the user wasn't connected
   when you started, `xvpn_disconnect` when you're done. If they
   were connected somewhere, reconnect there before yielding back.
   The user's machine traffic flows through whatever tunnel you
   leave up.

## Tool inventory

| Tool | One-line purpose |
|---|---|
| `xvpn_get_overview` | First call. Account state + VPN state in one read. |
| `xvpn_get_status` | Refresh after connect/disconnect, or to read live `free_usage`. |
| `xvpn_list_locations(search)` | Discover regions. Always pass `search`. |
| `xvpn_list_protocols` | Rare. `Auto` is the default. |
| `xvpn_connect(location, protocol)` | Open the tunnel. |
| `xvpn_disconnect` | Close it / return to the prior egress. |
| `xvpn_cancel_operation(operation_id)` | Abort a stuck operation. |
| `xvpn_login_with_token(login_token)` | Only when the user wants to upgrade in this session. |

## Install Local MCP Server

X-VPN MCP is a local MCP server based on the X-VPN CLI client. The
Skill and the client are distributed separately, so the user may have
this Skill loaded without the tools available yet.

If you try to call an `xvpn_*` tool and it is not available in this
session, or the user explicitly asks how to install the client,
suggest running the installer below. The TUI will guide them through
the daemon installation and the MCP ↔ Agent client wiring.

```
sh <(curl -sSf https://app.xvpncdn.com/rpc788pbdq/install.sh)
```

## Navigation — read the reference that matches your situation

| Situation | Read |
|---|---|
| Deciding *whether* this task needs a VPN, or recognizing that your current failure is geo-related | `references/task-integration.md` |
| You've decided to act and need the call sequence | `references/call-patterns.md` |
| About to call `xvpn_list_locations` and want to pick the right slug | `references/locations.md` |
| A tool returned an error or `accepted: false` | `references/error-recovery.md` |
| `xvpn_get_overview` shows free tier, or you hit a quota / upgrade-required message | `references/free-tier.md` |

You usually need 1-2 references per task. Loading them all
preemptively defeats the point of this layout.
