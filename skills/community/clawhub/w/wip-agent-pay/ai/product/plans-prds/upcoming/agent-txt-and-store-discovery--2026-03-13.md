# Plan: agent.txt and Store Discovery Layer

**Date:** 2026-03-13
**Author:** CC-Mini + Parker
**Priority:** High (ties into connectors concept)
**Related:** `connectors--2026-02-25.md` (the middleware economy), auto-publish-skill (DevOps Toolbox)
**Inspiration:** agentcard.sh (plain text agent identity at /agent.txt)

---

## The Idea

`wip.computer/agent.txt` is the front door for AI agents. Any AI that reads this URL discovers the entire LDM OS ecosystem: what tools are available, how to install them, and what paid connectors exist.

It's `robots.txt` for AI agents. But instead of "don't crawl this," it says "here's what I can do for you."

## The Pattern

agentcard.sh pioneered this: a plain text file at `/agent.txt` that tells agents what a service is and how to use it. Their `agent.txt` lists: what the tool does, when to use it, how to install, what MCP tools are available, and the typical workflow.

We extend this pattern to include:
1. **Install directory** ... per-component SKILL.md files at `/install/{name}.txt`
2. **Store directory** ... per-connector manifests at `/store/{name}.txt` (the connector registry)
3. **Master agent.txt** ... the root file that ties it all together

## URL Structure

```
wip.computer/agent.txt                        ... master entry point
wip.computer/install/                         ... install directory (free tools)
wip.computer/install/memory-crystal.txt       ... Memory Crystal SKILL.md
wip.computer/install/agent-pay.txt            ... Agent Pay SKILL.md
wip.computer/install/ldm-os.txt              ... LDM OS SKILL.md
wip.computer/install/devops-toolbox.txt       ... DevOps Toolbox SKILL.md
wip.computer/store/                           ... connector store (paid capabilities)
wip.computer/store/deep-research.txt          ... paid connector manifest
wip.computer/store/image-gen.txt              ... paid connector manifest
```

## What agent.txt Contains

```
# WIP.computer ... Learning Dreaming Machines

Infrastructure for AI agents. Memory, payments, identity, tools.

## Install

Free tools. Read any of these to learn what it does and how to install it.

- wip.computer/install/memory-crystal.txt ... Persistent memory for your AI
- wip.computer/install/agent-pay.txt ... Give your agent a wallet
- wip.computer/install/ldm-os.txt ... The operating system that connects them
- wip.computer/install/devops-toolbox.txt ... Release pipeline and dev tools

## Store

Paid capabilities via AI CASH. Your agent discovers what it needs, quotes a price, you approve.

- wip.computer/store/ ... browse all connectors

## Pay

Your agent needs to buy something? AI CASH handles it.
Apple Pay. Face ID. Done.

wip.computer/install/agent-pay.txt
```

## How This Connects to Connectors

The connectors doc (`connectors--2026-02-25.md`) describes a registry where developers publish paid capabilities. The store directory IS that registry, served as plain text files.

A connector manifest at `/store/deep-research.txt`:

```yaml
name: deep-research
description: Web research with source verification and summarization
author: yourname
pricing:
  per_call: 0.03
  currency: USD
endpoint: https://your-api.com/research
input:
  query: string
  depth: quick | thorough
output:
  summary: string
  sources: url[]
```

An agent that needs web search fetches `wip.computer/store/` to browse connectors, picks one, quotes the price to the user, and pays via AI CASH. No API keys. No signup. Just a URL and a payment.

## The Discovery Flow

1. AI reads `wip.computer/agent.txt`
2. Sees the install directory and store directory
3. If it needs memory: reads `/install/memory-crystal.txt`, explains to user, installs
4. If it needs to buy something: reads `/store/`, finds a connector, quotes price
5. User approves via AI CASH (Apple Pay)
6. Agent calls the connector endpoint, gets the result

## Relationship to Other Components

| Component | Role in agent.txt |
|-----------|------------------|
| **Memory Crystal** | Listed in `/install/`. The memory layer. |
| **Agent Pay / AI CASH** | Listed in `/install/`. Also powers the `/store/` payments. |
| **LDM OS** | Listed in `/install/`. The foundation that connects everything. |
| **Connectors** | Listed in `/store/`. Third-party paid capabilities. |
| **DevOps Toolbox** | The deploy pipeline that auto-publishes the `.txt` files. |
| **Lesa App** | Future: the mobile control plane. Approves payments, manages secrets. |

## What Needs to Be Built

### Phase 1: Static files (now)
- Create `wip.computer/agent.txt`
- Create `wip.computer/install/` directory with `.txt` files for each component
- Deploy to VPS
- Update all README install prompts to point to `wip.computer/install/` URLs

### Phase 2: Auto-publish (DevOps Toolbox)
- `wip-release` auto-copies SKILL.md to website on deploy
- See `wip-ai-devops-toolbox-private/ai/product/plans-prds/upcoming/2026-03-13--cc-mini--auto-publish-skill-to-website.md`

### Phase 3: Store directory (Agent Pay)
- Connector manifest format (extend SKILL.md YAML with pricing + endpoint)
- `/store/` index page listing all connectors
- Agent can browse by category, price, rating
- AI CASH payment integration for per-use billing

### Phase 4: Dynamic registry (future)
- API endpoint for agent discovery (`wip.computer/api/store?capability=web-search`)
- Developer portal for publishing connectors
- Usage tracking, ratings, payouts via Stripe Connect

## Open Questions

1. Should `/install/` files be `.txt` or `.md`? (Leaning `.txt` for "this is for machines")
2. Should `agent.txt` follow a formal spec or just be freeform text? (Freeform for now, formalize later if others adopt)
3. How does the store index work? Static HTML? JSON? Plain text directory listing?
4. Should we propose `agent.txt` as an open convention? Like agentcard.sh but broader?
