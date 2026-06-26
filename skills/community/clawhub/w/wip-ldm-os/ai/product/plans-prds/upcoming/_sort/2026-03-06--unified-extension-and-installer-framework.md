# Product Idea: Unified Extension and Installer Framework

**Date:** 2026-03-06
**Source:** Parker + CC-Mini, during extension audit and memory analysis session
**Status:** Architecture vision. This is the money shot.
**Priority:** Highest. This is what everything leads to.

---

## The Thesis

> "Software shouldn't be built into apps, but into small bespoke tools. Apps are for people. Tools are for LLMs, and increasingly, LLMs are the ones using software." ... Andrej Karpathy

LDM OS is the local runtime for those tools. AI CASH is the marketplace. The manifest is the universal package format. Agent Pay is the wallet.

**LDM OS is a lightweight local runtime that manages agent identity, extensions, and tool wiring across multiple AI harnesses.**

LDM OS + Universal Installer + AI CASH + Stripe = the App Store for AI agents.

Four things that should be one system:

| Component | Repo | What it does | Where it installs |
|-----------|------|-------------|-------------------|
| Universal Installer | `wip-universal-installer` | Detects 6 interface types, installs them | `~/.openclaw/extensions/` |
| Memory Crystal | `memory-crystal` | Memory DB, capture, search, MCP | `~/.ldm/extensions/` + `~/.openclaw/extensions/` |
| LDM OS | `wip-ldm-os` | Agent identity, directory scaffolding | `~/.ldm/` |
| AI CASH / Agent Pay | `wip-agent-pay` | Agent payments, Connectors marketplace | MCP server |

The combination: LDM OS is the runtime. The manifest is the universal package format. AI CASH is the payment rail. Stripe Connect is the settlement. Apple Pay is the consumer UX.

How do you get agents to pay? That's what Agent Pay does. That's what AI CASH does. Everything else... the OS, the installer, the manifest, the registry... exists to make that transaction possible.

---

## The Competitive Landscape (Mar 6, 2026)

We're not alone. The big players are moving:

### OpenAI: AgentKit + Symphony (released Mar 5, 2026)

- **AgentKit** ... visual canvas for composing multi-agent workflows. Drag-and-drop nodes.
- **Connector Registry** ... central place to manage how data and tools connect. Sound familiar?
- **Symphony** ... open source framework for orchestrating autonomous AI coding agents. Elixir/BEAM.
- **Agents SDK** ... production upgrade of Swarm. Lightweight agent framework.

OpenAI is building their version of what we're building. Their Connector Registry is their extension marketplace. Their AgentKit is their visual orchestration layer.

### Anthropic: Claude Code + MCP

- **MCP** ... Model Context Protocol. The tool interface standard. We already use it.
- **Claude Code hooks** ... PreToolUse, Stop. How we wire extensions today.
- Claude will absorb memory, identity, and extension concepts. It's a matter of when, not if.

### Others

- **n8n, Zapier** ... visual orchestration, but human-configured. Not agent-discovered.
- **Nevermined, nullpath, Salesforce AgentExchange, Google Cloud AI Agent Marketplace** ... all miss the mainstream accessibility piece (per GPT/Grok feedback).

### Our Advantage

Nobody has this combination:
1. **Sovereign local runtime** (LDM OS ... your data stays on your machine)
2. **Universal manifest** (one file works for local install AND cloud marketplace)
3. **Fiat Apple Pay** (consumer taps Face ID, not crypto wallet setup)
4. **Zero billing for developers** (write a manifest, deploy an endpoint, get paid via Stripe)
5. **Harness-agnostic** (works with Claude Code, OpenClaw, GPT, Codex, whatever comes next)

OpenAI's Connector Registry is locked to their ecosystem. Ours works with any agent.

---

## The Harness Reality

### What we can and can't control

| Harness | Source | Can modify? | Can guarantee merge? | How we wire |
|---------|--------|------------|---------------------|-------------|
| OpenClaw | Open source | Yes (fork + rebase) | No. 1 PR merged, 1 Steepay merged, 1 pending | Symlink or config change, .mcp.json |
| Claude Code | Closed | No | No | settings.json hooks + MCP + CLAUDE.md |
| Claude Desktop | Closed | No | No | MCP only |
| GPT (iOS) | Closed | No | No | API endpoints, Custom GPTs |
| Codex | Open source | Yes | Unknown | TBD |

### The Design Principle

**LDM OS never depends on a harness change it doesn't control.**

For open source harnesses (OpenClaw, Codex): we can fork, modify, and rebase. We carry patches. If our PRs get merged upstream, great. If they don't, we still work. We already have this reality with OpenClaw: symlink fix sitting unmerged, breaking things.

For closed source harnesses (Claude Code, Claude Desktop, GPT): we work with whatever surface they expose. Hooks, MCP, config files, instructions. No assumptions about future features.

If what we build gets absorbed by the harness... that's a win. We want Claude to ship native persistent memory. We want OpenAI to adopt the manifest format. We want GPT to support MCP. When they do, our patterns become the standard. Memory Crystal proves the pattern. The harnesses absorb it.

### The PI Framework Abstraction

OpenClaw created amazing patterns: the plugin system, lifecycle hooks, workspace file loading, gateway routing. But those patterns are trapped inside OpenClaw. If OpenClaw goes away tomorrow, you lose the plugin system, the workspace loading, the lifecycle hooks.

LDM OS abstracts the PI (programmatic interface) framework out of the harness. The automation layer... plugins, hooks, lifecycle events, tool registration... sits in the sovereign layer, not inside any harness. Any harness that supports the interface gets the full ecosystem. Harnesses that don't support it can't be automated with us.

The harnesses we support right now:
- **Claude Code** (CLI, macOS)
- **Claude Desktop** (macOS, iOS)
- **GPT** (iOS)
- **Codex** (macOS, iOS)
- **OpenClaw** (macOS)

That's the scope. Nothing else matters until these work.

### Designed to Be Absorbed

This is not competitive. This is catalytic.

When Anthropic ships native persistent memory in Claude Code, that's a win. When OpenAI builds their version of the manifest format, that's a win. When OpenClaw merges our patches, that's a win.

Three scenarios:
1. **They absorb the concept.** They build it differently but solve the same problem. We migrate. Win.
2. **They absorb the code.** Our patterns become the standard. Best case. Win.
3. **They build something incompatible.** Cloud-only, no sovereignty. LDM OS becomes the sovereign alternative. We still have our thing. Win.

In all cases, LDM OS survives because it's the sovereignty layer. The harnesses come and go. The soul files, the memory, the identity... that persists in `~/.ldm/`.

---

## What Exists Today

### Universal Installer (wip-universal-installer)

Already built. Already works. Scans any repo for six interface types:

1. **CLI** ... `package.json` bin entry
2. **Module** ... ESM main/exports
3. **MCP Server** ... `mcp-server.mjs`
4. **OpenClaw Plugin** ... `openclaw.plugin.json`
5. **Skill** ... `SKILL.md`
6. **Claude Code Hook** ... `guard.mjs` or `claudeCode.hook`

Detection logic is solid (`detect.mjs`). Installation logic works (`install.js`). But it installs to `~/.openclaw/extensions/`, not `~/.ldm/extensions/`. And it doesn't know about agents, agent wiring, or LDM OS.

### Memory Crystal's installer (crystal init)

Also already built. Scaffolds `~/.ldm/`, deploys CC hooks, registers MCP servers, installs cron. But it's doing double duty: it's both the OS installer and the memory component installer. The architecture doc from Feb 26 says these should separate: "ldm init is the OS. crystal init adds memory."

### AI CASH Connectors

The marketplace vision (see `wip-agent-pay/ai/plans/connectors--2026-02-25.md`). Developers publish paid capabilities via YAML manifest. Agents discover them through a registry. Consumers pay per use with Apple Pay. Developer never builds billing. Both ChatGPT and Grok independently validated: "this is the product, not a feature."

The registry is the moat. If agents default to your registry for tool discovery, you win.

### Agent Pay (wip-agent-pay)

Already an MCP server. Already runtime-agnostic. Three tools: `agent_pay` (micropayments), `agent_pay_x402` (paywalled URLs), `agent_pay_fund` (Apple Pay funding). This is the payment rail that makes the marketplace work.

---

## Definitions

**Extension:** A package that exposes one or more agent-callable capabilities (CLI, MCP tool, skill, or API endpoint) described by a manifest.

**The economic model:** The marketplace takes a percentage of each transaction processed through AI CASH. Developers get paid via Stripe Connect. Consumers pay via Apple Pay / Google Pay / card. We never touch the money... Stripe settles everything.

**The manifest is the real platform.** npm won because of `package.json`. Docker won because of `Dockerfile`. iOS won because of IPA metadata. Chrome won because of `manifest.json`. Our equivalent is the LDM manifest. If the manifest standard spreads, the ecosystem spreads. Everything else (installer, registry, payments) flows from that one file.

---

## The Architecture

```
              AI CASH REGISTRY
            (Discovery + Payment)
                    |
                    |
           +--------v--------+
           |   LDM OS        |
           | local runtime   |
           | extensions      |
           | identity        |
           +--------+--------+
                    |
                    |
      +-------------+-------------+
      |             |             |
 Claude Code     OpenClaw        GPT
   Harness        Harness      Harness
```

The Linux userland for AI agents. Harnesses are shells. LDM OS is the OS.

### One system. Three layers.

```
Layer 1: LDM OS (the sovereign runtime)
  ~/.ldm/
  ├── extensions/           <-- single source of truth for all extensions
  ├── agents/               <-- registered agents (cc-mini, oc-lesa-mini, etc.)
  ├── config.json           <-- what's installed, what's wired to what
  └── bin/                  <-- OS-level tools (ldm CLI)

Layer 2: Universal Installer (local distribution)
  ldm install <repo>        <-- point at any repo, detect interfaces, package as extension
  ldm wire <ext> <agent>    <-- connect extension to agent runtime
  ldm doctor                <-- show all agents, extensions, wiring
  ldm update                <-- update extensions, track versions across machines
  ldm uninstall <ext>       <-- remove extension, unwire from all agents, clean up

Layer 3: AI CASH Marketplace (cloud distribution + payments)
  ldm publish <ext>         <-- push extension manifest to registry with pricing
  Agent discovery           <-- agents query registry, find capabilities
  Apple Pay                 <-- consumer taps Face ID, payment processes
  Stripe Connect            <-- developer gets payouts, we take channel fee
```

### The Manifest: One File, Three Layers

The manifest is the bridge. Same file works everywhere:

```yaml
name: deep-research
version: 1.0.0
description: Web research with source verification
author: yourname

# Interfaces (detected by Universal Installer)
interfaces:
  mcp: mcp-server.mjs
  cli: cli.mjs
  skill: SKILL.md

# Pricing (for AI CASH marketplace)
pricing:
  per_call: 0.03
  currency: USD
  estimate: "8-10 calls for a typical research task"

# Requirements (what the host machine needs)
requires:
  node: ">=20"
  os: ["darwin", "linux"]
  tools: ["curl"]

# Schema (for validation)
$schema: https://ldm.sh/manifest/v0.1.json

# Endpoint (for cloud use via marketplace)
endpoint: https://your-api.com/research
```

- `ldm install` reads interfaces, ignores pricing. Installs locally.
- `ldm publish` reads everything. Pushes to registry with pricing.
- Agent discovery reads pricing + endpoint. Calls cloud or installs locally.

### Bootstrapping

`ldm` is a standalone script. No dependencies on the extension system it creates. You get it via:
```bash
curl -fsSL https://ldm.sh | sh && ldm doctor
```

One command. Bootstraps `~/.ldm/`, installs the CLI, and immediately shows you what's running. Also available via:

```bash
npm install -g @wipcomputer/ldm   # or
brew install wipcomputer/tap/ldm  # future
```

The first thing it installs is itself. Then everything else flows through `ldm install`.

### Agent Wiring (per-harness)

When you install an extension, LDM OS detects which agents exist and wires up using whatever interface the harness supports:

| Agent Runtime | How it loads extensions | What LDM OS does |
|--------------|----------------------|-------------------|
| Claude Code | settings.json hooks + MCP registrations | Writes hook entries, runs `claude mcp add` |
| Claude Desktop | MCP servers only | Registers MCP |
| OpenClaw | Plugin dir + .mcp.json | Symlink to ~/.ldm/extensions/ or copy, update .mcp.json |
| GPT | Custom GPTs, API endpoints | Generate API endpoint config |
| Codex | TBD | TBD |

LDM OS adapts to the harness. The harness doesn't adapt to us.

### Versioning and Updates

Extensions track versions in `~/.ldm/config.json`. `ldm update` checks for newer versions:

```bash
ldm update                    # update all extensions
ldm update memory-crystal     # update one
ldm pin memory-crystal@0.7.2  # pin to version
```

This matters because there are multiple machines (mini + air). Same extensions, same versions, synced through the manifest.

---

## The Flywheel

This is Grok's framing from the Connectors review, applied to the full system:

1. LDM OS makes it easy to install extensions locally
2. Developers build extensions (tools, MCP servers, skills)
3. AI CASH makes it easy to publish and monetize
4. Agents become more capable (more connectors available)
5. Consumers trust one-tap Apple Pay approval
6. More consumers attract more developers
7. Registry becomes the default discovery layer
8. AI CASH becomes the required settlement rail
9. LDM OS becomes the required local runtime

**That's platform lock-in. But the good kind... the kind where everything is open source, your data is local, and you can leave anytime.**

### Cold Start

Who are the first 10 developers? Us. Parker, Claude Code, Lēsa. Who are the first 10 consumers? Lēsa instances. We're dogfooding every extension through the system before anyone else touches it. Memory Crystal, Agent Pay, file-guard, healthcheck... all built by us, installed by us, used by us daily. That's not a weakness. That's proof of conviction. The marketplace launches with real extensions that have been running in production, not placeholder demos.

### The Payment UX: Stripe + Apple Pay + Google Pay

This is the wedge against every crypto-only competitor. The x402 protocol requires a crypto wallet. We require a tap.

Agent hits a paywall. Consumer sees Apple Pay (or Google Pay, or card). Face ID. Done. No wallet setup. No seed phrases. No bridging tokens. The agent economy needs mainstream consumers, not just crypto-native early adopters.

Under the hood: Stripe Connect. Developer publishes a paid extension, gets a Stripe Connect account, receives payouts. Developer never builds billing. Consumer never thinks about payment infrastructure. We take a channel fee on every transaction.

This is the same architecture as the App Store: Apple handles payments, developers build apps, consumers tap to buy. Except it's open, it's for agents, and the extensions run locally on your machine.

### Go-to-Market: Two Sides of the Marketplace

**The positioning: "AI tools should cost pennies, not subscriptions."**

Everything right now is monthly: ChatGPT Plus, Claude Pro, Midjourney, Perplexity, SEO tools, Shopify apps. $20/month, $49/month, $149/month. Our message: pay $0.05 when the agent runs, not $49/month whether you use it or not. That's psychologically easier to accept. That's the anti-subscription wedge.

**Side 1: Infra connectors (supply side)**

Target AI infrastructure builders... CREA, Higgs, Tavily, Replicate, PDF tools. These people already have APIs, GPU endpoints, SaaS products, developer audiences. What they don't have: agent distribution, per-call micropayments, Apple Pay UX, automatic billing.

Pitch: "Stop building SaaS. Publish a skill." Write a manifest, deploy an endpoint, get paid via Stripe. One minute setup.

| Company | Connector |
|---------|-----------|
| CREA | image generation |
| Higgs | research / reasoning |
| Tavily | web search |
| Replicate | model inference |
| PDF tools | document conversion |

**Side 2: Commerce connectors (demand side... this is the bigger idea)**

Target Shopify stores, Amazon sellers, Gumroad creators, consultants, Notion template sellers. These businesses already pay for SEO tools, ad copy, product images, listing optimization. They already understand Stripe and Apple Pay. They already spend on TikTok/Instagram ads.

Pitch: "Turn your Shopify store into an AI skill marketplace listing." Turn your store into a callable capability.

| Merchant type | Agent skill |
|---------------|-------------|
| Shopify art store | generate custom prints |
| fitness coach | personalized workout plan |
| tax accountant | tax answer / doc review |
| law templates | contract generator |
| drop shipper | product lookup + order |

Instead of: `visit website -> browse -> checkout`
It becomes: `agent -> capability -> Apple Pay`

**Launch vertical: e-commerce AI skills.** 20 really useful ecommerce skills (product description generator, review analyzer, competitor price monitor, ad copy generator, Shopify SEO optimizer) and the system immediately feels alive. First 50 skills need to feel essential.

**Ad strategy: TikTok + Instagram.** Shopify sellers live there. Hook: "Generate your Amazon listing in 10 seconds. Pay once. No subscription." Or: "ChatGPT will soon be shopping for your customers. If your store isn't callable by AI, it doesn't exist."

**The category this creates:** App Store + Stripe + Fiverr + Zapier, but callable by agents. That's new.

### The Registry

The registry stores: extension manifests, pricing metadata, compatibility requirements (`requires` field), reputation/signing data, and callable cloud endpoints. Agents query it to discover capabilities. The registry is the gravitational center of the ecosystem.

### Trust and Security

Since this is installer + payments + agent tooling, trust is first-class:

- **Signed manifests.** Publisher identity verified via Stripe Connect onboarding.
- **Verified publishers.** Badge system. First-party extensions (ours) are always verified.
- **Permissions / scopes.** Extensions declare scopes in the manifest (`fs:read`, `network`, `secrets`). First run: LDM OS shows a consent dialog ("This extension wants to read ~/Documents and call external APIs. Allow?"). No silent access.
- **Sandboxing.** Enforcement is future work. For now, scopes are declarative (trust-based, like npm). Full sandboxing (process isolation, filesystem jails) comes later. Name it honestly: the trust model is only as good as its enforcement, and enforcement is v2.
- **Local vs remote disclosure.** Manifest declares whether the extension runs locally or calls a cloud endpoint. User always knows where their data goes.
- **Payment consent boundary.** Agent always asks before spending money. "This costs $0.05. Run?" User taps Face ID. No silent charges.

---

## The Organization Answer

### Option A for now, evolve to C.

Move the Universal Installer's detection logic into LDM OS. `ldm install` is the command. `ldm init` scaffolds the OS. `crystal init` calls `ldm init` first. Keep Memory Crystal, Dream Weaver, and Agent Pay as separate component repos that install through `ldm install`.

When there are enough extensions that the framework needs to be truly generic, refactor toward Option C (LDM OS is purely a framework, everything is an extension). But today, Option A ships.

---

## Extension Audit (What's Real Today)

From the Mar 6 analysis session with Parker:

| Extension | Status | Needs OpenClaw? | LDM OS Action |
|-----------|--------|----------------|----------------|
| memory-crystal | Live, both runtimes | No | First LDM OS extension. Model for others. |
| wip-agent-pay | Live, MCP | No | Already runtime-agnostic. The payment rail. |
| wip-file-guard | Live, CC hook | No | Already a CC hook. LDM OS extension. |
| wip-repo-permissions-hook | Live, CC hook | No | Already a CC hook. LDM OS extension. |
| op-secrets | Live, OC only | No (needs op CLI) | Convert to MCP server for CC (priority). |
| tavily | Live, OC only | No (API wrapper) | Convert to MCP server (lower priority). |
| root-key | Live, OC only | Yes (OC skill) | Convert to MCP tool. |
| private-mode | Live, OC only | Yes (OC plugin) | Convert to MCP tool or CC hook. |
| compaction-indicator | Live, OC only | Yes (OC lifecycle) | Keep OC-only for now. |
| lesa-bridge | Live, both | Needs OC gateway | Only useful when Lesa exists. |
| context-embeddings | Dead | Yes | Kill. Memory Crystal replaced it. 128 MB orphan. |
| cc-session-export | Dead | No | Kill. Absorbed into memory-crystal cc-poller. |
| session-export | Dead | Yes | Kill. Absorbed into memory-crystal openclaw.ts. |

---

## Initial Shipping Sequence

### Week 1: Foundation

1. Kill dead extensions (context-embeddings, cc-session-export, session-export)
2. Build `ldm init` as standalone bootstrapper
3. Build `ldm install` / `ldm uninstall` targeting `~/.ldm/extensions/`
4. Define manifest v0.1 format (interfaces, pricing, requires)
5. Memory Crystal as first `ldm install` extension (proof of concept)
6. Wire OpenClaw to read from `~/.ldm/extensions/` (symlink or config)

### Week 2: Polish + Wiring

7. `ldm doctor` showing all agents, extensions, wiring
8. Move Universal Installer detection logic into LDM OS
9. Agent Pay MCP working across all harnesses
10. 2-3 extensions installing cleanly through `ldm install`
11. Fresh install test on clean macOS account

### Month 1: Payments + Marketplace

12. Stripe Connect integration for developer payouts
13. Apple Pay / Google Pay consumer flow
14. AI CASH Connectors registry (cloud)
15. `ldm publish` (push to registry)
16. `ldm update` with version tracking
17. First 5 commerce connectors (e-commerce vertical)
18. First 5 infra connectors (CREA, Higgs, Tavily, Replicate, PDF)
19. op-secrets as MCP server for CC
20. TikTok/Instagram ad creative for Shopify merchants

---

## The Industry Analogy

The analogy:
- **App Store** did this for mobile app distribution
- **npm** did this for JavaScript module distribution
- **Stripe** did this for payments
- **LDM OS + AI CASH** does this for agent capability distribution and payment

| Ecosystem | Distribution | Runtime |
|-----------|-------------|---------|
| Apple | App Store | iOS |
| npm | npm registry | Node |
| Docker | Docker Hub | container runtime |
| **LDM OS** | **AI CASH registry** | **agent runtime** |

The registry becomes the gravitational center. Not the runtime. npm won because of the registry. App Store won because of the registry. The runtime is necessary but not sufficient. The registry is the moat.

---

## Related Documents

- `memory-crystal-private/ai/product/product-ideas/ldm-os-universal-extension-framework.md` ... extension framework vision
- `wip-agent-pay/ai/plans/connectors--2026-02-25.md` ... Connectors marketplace plan
- `wip-agent-pay/ai/feedback/connectors-review--2026-02-25.md` ... GPT + Grok validation ("this is the product")
- `wip-universal-installer/SPEC.md` ... Universal Interface Specification
- `wip-universal-installer/detect.mjs` ... detection logic (moves into LDM OS)
- `wip-ldm-os/ai/products/plans-prds/2026-02-26--architecture-decisions.md` ... architecture decisions
- `memory-crystal-private/ai/product/notes/memory-analysis.md` ... where all the data lives today
