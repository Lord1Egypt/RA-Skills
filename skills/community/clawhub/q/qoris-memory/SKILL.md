---
name: "Legacy — Qoris Memory (use qoris-memory-mcp)"
description: "⚠️ LEGACY LISTING. The canonical home for this skill is now qoris-memory-mcp under the @qoris-ai org publisher. Please run: clawhub install qoris-memory-mcp."
version: "1.0.5"
author: "qorisai"
homepage: "https://qoris.ai"
repository: "https://github.com/QORIS-AI/qoris-memory-openclaw-skill"
tags:
  - legacy
  - deprecated
  - memory
  - mcp
metadata:
  clawdis:
    primaryEnv: QORIS_API_KEY
    homepage: https://qoris.ai
    skillKey: qoris-memory
    requires:
      env:
        - QORIS_API_KEY
        - QORIS_WORKSPACE_ID
---

# Legacy — Qoris Memory

> ## ⚠️ This skill has moved
>
> **Install [`qoris-memory-mcp`](https://clawhub.ai/qoris-memory-mcp) instead.**
>
> ```bash
> clawhub install qoris-memory-mcp
> ```
>
> This `qoris-memory` slug under `@apps-debug` is kept only for backward compatibility with users who installed earlier versions. All future updates, new features, and new versions will be published exclusively to `qoris-memory-mcp` under the `@qoris-ai` org publisher.

## Why did it move?

We set up a dedicated `@qoris-ai` organization publisher on ClawHub and migrated the canonical listing to it. This `@apps-debug` listing is the original pre-migration home and will no longer receive feature updates.

## What to do

If you're already using `qoris-memory`, switch to `qoris-memory-mcp`:

```bash
clawhub uninstall qoris-memory
clawhub install qoris-memory-mcp
```

Your existing `QORIS_API_KEY` and `QORIS_WORKSPACE_ID` work identically with the new slug — same underlying MCP server at `https://mcp.qoris.ai/mcp`, same tools, same behavior.

## Data Handling & Privacy

This skill connects to the Qoris MCP server (`https://mcp.qoris.ai/mcp`) and exposes explicit memory tools (`save_memory`, `search_knowledge`, etc.). The skill does not capture or persist conversation content automatically — only data you explicitly pass to a tool call is transmitted.

- **What gets sent:** only content you pass to explicit tool calls
- **Where it's stored:** `https://mcp.qoris.ai/mcp` scoped to your `QORIS_WORKSPACE_ID`
- **Credential ownership:** `QORIS_API_KEY` is your own per-user secret, not bundled
- **Retention:** per `https://qoris.ai/privacy`
- **Revocation:** rotate `QORIS_API_KEY` in your dashboard

## Available Memory Tools (inherited from canonical)

`save_memory`, `get_memories`, `search_knowledge`, `update_memory`, `delete_memory`, `list_knowledge_documents`, `get_document_full_content`.

See the full documentation at the canonical listing: [qoris-memory-mcp](https://clawhub.ai/qoris-memory-mcp).

## Support

- Canonical listing: `https://clawhub.ai/qoris-memory-mcp`
- Documentation: `https://docs.qoris.ai/memory`
- Source: `https://github.com/QORIS-AI/qoris-memory-openclaw-skill`
- Support: `eliel@qoris.ai`

## About Qoris AI

Qoris AI builds the trust and governance layer for enterprise AI agents. NVIDIA Inception Program member. Claude Partner Network member. Patent pending U.S. 63/907,730. Based in Stamford, CT.

`qoris.ai`
