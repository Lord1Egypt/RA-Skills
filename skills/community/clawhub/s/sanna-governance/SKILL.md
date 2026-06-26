---
name: sanna
description: "Sanna governance — tool calls are governed transparently"
metadata:
  openclaw:
    tags: ["governance", "security", "constitution", "receipts", "compliance", "audit", "ed25519", "cryptographic-proof", "tool-gating", "enforcement", "guardrails", "ai-safety", "agent-safety", "approval", "escalation", "policy", "permissions", "trust", "verification", "openclaw-plugin"]
    summary: "Constitution enforcement and Ed25519-signed cryptographic receipts for every AI agent tool call. Define what actions agents can and cannot take in YAML constitutions. Three possible outcomes per tool call: allowed, blocked, or escalated for human approval. Every governed action produces a verifiable receipt proving governance was applied at the moment of execution."
    requiresPlugin: "@sanna-ai/openclaw"
    requires:
      bins: ["node"]
---

# Sanna Governance

This system has Sanna governance enabled. A constitution defines what actions
are allowed, denied, or require escalation. Governance is applied automatically
to every tool call — no special tool names or prefixes are needed.

## How It Works

Call tools normally. The governance layer intercepts each call and evaluates it
against the constitution before execution. There are three possible outcomes:

- **Allowed** — the tool executes normally
- **Blocked** — the tool is denied with an explanation of which rule was violated
- **Escalated** — the tool requires human approval before it can proceed

## Governed Tool Tiers

| Tier | Tools | Risk Level |
|---|---|---|
| 1 | exec, bash, write, edit, apply_patch, process | Modifies system state |
| 2 | browser, message, nodes | Composite tools with high-risk actions |
| 3 | web_search, web_fetch, cron, gateway, sessions_send, sessions_spawn | Audit trail |

Tier 4 tools (read, image, canvas, sessions_list, sessions_history,
session_status, memory_search, memory_get, agents_list) are not governed.

## Receipts

Every governed action generates a cryptographic receipt that proves governance
was applied. Receipts are generated and persisted automatically — no action
is needed from the agent.
