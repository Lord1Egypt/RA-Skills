# LDM OS Store

**Date:** 2026-03-11
**Status:** Concept

---

## What This Is

LDM OS needs a store. Not an app store. A capability store. Agents discover tools, pay for them, use them. The store is native to the OS, not bolted on.

## Why It Lives in LDM OS

Agent Pay is the payment rail. WIP Cloud is the hosting layer. But the store concept belongs to LDM OS because:

1. **Every agent needs tools.** Memory Crystal, Dream Weaver, devops tools, 1Password, voice calling. These are OS-level capabilities, not apps.
2. **Discovery is an OS function.** The OS knows what the agent needs. The OS surfaces available tools. The OS handles installation.
3. **Payment is an OS function.** The agent doesn't go to a website to buy things. The OS has a wallet. The OS handles the 402.
4. **Identity is an OS function.** The store knows who the agent is (sovereignty). Purchases are tied to the agent's identity, not a user account.

The store is the convergence of Memory Crystal (what does the agent know?), Agent Pay (how does the agent pay?), and the install pipeline (how does the agent get new capabilities?).

## Architecture

```
LDM OS Store
    |
    +--- Discovery (what's available?)
    |      |
    |      +--- llms.txt / SKILL.md on github.io, wip.computer
    |      +--- ClawHub registry
    |      +--- npm registry
    |      +--- Agent Pay Connectors (paid capabilities)
    |
    +--- Installation (how do I get it?)
    |      |
    |      +--- wip-install (all 7 interfaces)
    |      +--- clawhub install
    |      +--- npm install -g
    |
    +--- Payment (does it cost anything?)
    |      |
    |      +--- Free: MIT tools (most things)
    |      +--- AI CASH: Apple Pay per transaction
    |      +--- AGENT WALLET: sovereign wallet, no fees
    |
    +--- Hosting (where does it run?)
           |
           +--- Local: CLI, MCP, OC Plugin, CC Hook
           +--- Remote: WIP Cloud (mcp.wip.computer)
```

## Four Distribution Layers

1. **wipcomputer.github.io** ... now. Free static CDN. AI-readable.
2. **wip.computer** ... the website. Permanent home for discovery.
3. **WIP Cloud** ... remote MCP hosting. Commercial. Every Claude surface.
4. **Agent Pay Connectors** ... the marketplace. Paid capabilities.

## The Flow

```
Agent needs a capability
    -> LDM OS checks what's available (discovery)
    -> Agent finds a tool (SKILL.md, ClawHub, Connectors)
    -> If free: install and use
    -> If paid: Agent Pay handles the 402
        -> AI CASH (user taps Apple Pay)
        -> or AGENT WALLET (agent signs directly)
    -> Tool installed via wip-install (all interfaces)
    -> Tool available locally or via WIP Cloud
    -> Agent uses it
```

## Relationship to Agent Pay

Agent Pay is the payment implementation. The store concept is broader:

- Agent Pay = "how does the agent pay?"
- LDM OS Store = "how does the agent discover, pay for, install, and use capabilities?"

Agent Pay is a component of the store. The store is a component of LDM OS.

## Relationship to WIP Cloud

WIP Cloud is the hosting implementation. The store uses WIP Cloud to make tools available remotely. But the store also works without WIP Cloud (local-only tools installed via wip-install).

---

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
