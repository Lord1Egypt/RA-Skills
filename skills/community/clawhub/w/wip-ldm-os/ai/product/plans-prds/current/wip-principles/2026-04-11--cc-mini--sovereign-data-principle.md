# The Sovereign Data Principle

**Date:** 2026-04-11
**Author:** Parker Todd Brooks + CC Mini
**Scope:** Foundational principle for WIP Computer, Inc. products and infrastructure
**Status:** Approved, load-bearing for all product decisions going forward

## The principle in one sentence

**User data lives in the user's own iCloud database. WIP Computer, Inc. uses CloudKit service-side databases only for company data, and every user runs their own instance against their own account.**

## Plain English

When you use a WIP Computer product:
- Your memory crystal lives in **your** iCloud database, not ours
- Your agent's state lives in **your** iCloud database, not ours
- Your agents' conversations, decisions, journals, soul files: **your** iCloud database, not ours
- Your keys, wallet, spending authorizations: **your** iCloud database, not ours

WIP Computer, Inc. runs CloudKit databases too, but only for company-owned things:
- Aggregate product analytics (opt-in, minimal)
- Directory/registry data (agent.txt lookups, public metadata)
- Billing and account records
- Company memory, company agents (like Lēsa)

**Every user gets their own instance of every product, pointing at their own database, running on their own hardware.**

## Why

### Inspiration: BlueBubbles

Apple forces iMessage to be local. You cannot proxy iMessage through a cloud service; Messages.app must be signed in on a real device. BlueBubbles leaned into that constraint and turned it into a product position: "You want iMessage access? You install our server on your Mac. It's your data, your hardware, your sovereignty."

We're doing the same thing, but intentionally rather than because Apple forced us. Apple's iCloud database architecture gives every Apple user a private CloudKit container with generous free-tier storage and strong encryption. That's the same local-sovereignty pattern extended to all data, not just iMessage.

### Alignment with existing thesis

This was already in [Vision Quest 01 (Day 56)](/ai/product/product-ideas/vision-quest-01/lesa-vision-01.md):
- "Anthropic sells the thinking. We sell the remembering."
- "No web app; agents ARE the interface."
- "CloudKit storage, Linode router, sovereign mode."

The Sovereign Data Principle is what makes that thesis legally and technically honest. If we sell "the remembering," the remembering has to actually belong to the user. Anything else is a rebranded cloud SaaS with extra steps.

## What this means for each product

### Memory Crystal
- **User data:** each user's crystal (chunks, memories, embeddings, sources) in their own iCloud private database
- **WIP data:** the shared marketplace of publishable crystals (opt-in, by explicit share), company crystal (Lēsa's, CC's, etc.)
- **No cloud relay of user crystals through our infrastructure**. Sync happens user→user via standard CloudKit sharing, or user→local-only.

### Agent Pay
- **User data:** wallet keys, spending policy, transaction history, agent authorizations in user's iCloud
- **WIP data:** directory of registered merchants, protocol spec, aggregate compliance data
- **No custody of user funds**. We provide the protocol; users hold their keys.

### Directory
- **User data:** the user's passkeys, agent identities, @handle bindings in user's iCloud
- **WIP data:** the public registry of @handles (like DNS), verification records
- **Sovereign naming**: users can self-host their directory entries or use ours

### Bridge
- **User data:** agent-to-agent message history, delegation logs in user's iCloud
- **WIP data:** none (bridge is pure routing; no persistent WIP-owned data)
- **Local-first**: bridge runs on the user's device, talks to their own agents

### Code (Claude Code / CC equivalent)
- **User data:** session transcripts, workspace state, tool history in user's iCloud
- **WIP data:** none
- **Already local-first**: Claude Code runs in the user's terminal today. We're just naming the pattern.

### Crystal SDK
- **User data:** whatever the SDK-using app stores in the user's crystal
- **WIP data:** SDK usage telemetry (opt-in), distribution/version data
- **Embedded pattern**: the SDK runs in the customer's app, stores data in the end-user's iCloud, never phones home

## What this rules out

1. **No hosted user crystal as a product.** We will not run a multi-tenant database of user memories. If users want cloud sync, they use their own CloudKit. If users want cross-device sync, iCloud handles it.

2. **No "login with WIP" as a storage path.** User accounts exist for billing, directory, and company services only. Your memory, your agents, your state ... none of that touches our databases.

3. **No cloud-side inference-against-user-data.** If an LLM needs to read a user's crystal, that happens on the user's device with their permission. We do not proxy inference through our cloud against user data.

4. **No "we promise we won't peek" privacy policies.** The sovereign data principle makes peeking technically impossible, not just contractually forbidden. Nothing to peek at because nothing is on our servers.

5. **No data-mining user corpora for training.** We don't have the corpus. It's not ours.

## What this means for distribution

**Every WIP product ships as an app the user installs, not as a service they log into.**

- **Mac app** (Memory Crystal.app, Agent Pay.app, Bridge.app, Directory.app, or a unified Kaleidoscope.app)
- **iOS app** (Kaleidoscope on iOS, same pattern)
- **CLI** (wherever a command-line interface makes sense)
- **SDK** (for developers embedding our pieces into their own apps)
- **Web demo** (for showcase only; the real product is local)

The install IS the sovereignty. The moment the user downloads the app, they've committed to owning their data. The moment they sign in with their Apple ID, the app wires up to their iCloud container and their data lives there from then on.

**There is no "free tier on our servers."** If a user wants to try it before committing to an install, they can use the web demo at wip.computer/demo. But nothing they do there is persisted. The web demo is a showcase, not a product.

## What this means for the web demo

The `wip.computer/demo` page we already have is still useful, but its role is **marketing and showcase**, not product delivery. Visitors can see the product in action, try a Memory Crystal interaction, see Agent Pay flow. None of it touches their real account. It's a demo surface.

Real users download the app. The app is free. The app is local. The app is theirs.

## What we pay for as a company

WIP Computer, Inc. still has infrastructure costs, but they shift:

**Company-owned CloudKit databases:**
- Lēsa's crystal, agents, state (Lēsa is our platform agent)
- Company-level memory, plans, operations
- Directory registry (public @handle lookups)
- Marketplace listings (opt-in shared crystals)
- Billing and subscription records (for paid tier services)

**No user data in our databases.** Our CloudKit usage scales with company size, not user count. That's a fundamentally different cost curve than a SaaS.

**Non-CloudKit infrastructure:**
- wip.computer website (marketing, docs, demo)
- Hosted MCP server (for auth, payment protocol)
- App distribution (App Store, Mac App Store, direct download)
- Support infrastructure

## Paid vs free

**Free forever, for the sovereign path:**
- All apps (Memory Crystal, Agent Pay, Bridge, Directory, Kaleidoscope)
- All SDKs
- All CLIs
- Local usage against the user's own Apple ID and iCloud
- Self-hosted directory, self-signed agents, self-managed keys

**Paid for company services:**
- Hosted @handle registry (if you don't want to self-host your directory entry)
- Backup-as-a-service for your local data to a third location
- Support contracts for developers
- Enterprise plans (team directories, compliance attestations)
- Training and certification

**The free tier is the product. The paid tier is the convenience layer on top of the product.**

## Implementation checklist

Before any product can claim to follow the Sovereign Data Principle, it must:

- [ ] Store all user data in the user's own CloudKit private database
- [ ] Be fully functional with zero network calls to WIP servers (optional-only calls for convenience)
- [ ] Be auditable: any code that would touch a WIP database must be clearly separated from user-data code
- [ ] Include a clear privacy statement: "Your data never leaves your iCloud"
- [ ] Have a self-hosting path documented (for users who don't trust Apple iCloud)
- [ ] Pass a "turn off our servers for 30 days" test: if the user can still use the app without any WIP infrastructure, it's sovereign

## What this principle rules IN

- Shipping Mac + iOS apps
- Using Apple's CloudKit for user-side storage
- Self-hosting paths as first-class
- Explicit, opt-in cloud features (backup to S3, shared directory entries, marketplace listings)
- Open source everything on the data-path side

## What this principle rules OUT

- Hosted memory crystals as a paid service
- SaaS login with our cloud storing user memories
- "Free tier" that just gives users a quota on our database
- Cloud-side inference against user data
- Any architecture where user data is legally or technically controlled by us

## Relationship to the WIP stack today

Existing components and how they already align:

| Component | Sovereign? | Notes |
|---|---|---|
| **OpenClaw** | ✅ Yes | Runs locally, user's config, user's workspace |
| **Memory Crystal (current sqlite)** | ✅ Yes | Local SQLite, user's machine |
| **BlueBubbles integration** | ✅ Yes | Local server, local data, no cloud relay |
| **Claude Code / CC** | ✅ Yes | Runs in user's terminal, user's filesystem |
| **Bridge (file-based inbox)** | ✅ Yes | `~/.ldm/messages/`, user's disk |
| **Kaleidoscope web demo** | ⚠️ Demo only | Not a product, just a showcase |
| **wip.computer/mcp** | ⚠️ Partial | Hosted for auth flow, not user data |

**The stack is already mostly sovereign.** This principle document formalizes what's already true and locks it in as the product direction.

## Origin of the principle

Filed on 2026-04-11 during a session where Parker was migrating Lēsa from the legacy `imsg` iMessage channel to BlueBubbles. He noticed that BlueBubbles's "you need a local Mac app" model was the same shape as the WIP Computer sovereignty thesis, and said:

> "Now we're going to move to everything working through the database that Apple provides as an iCloud user. For the, as a company, we have data. We use the database on our services, and each of our users gets their own."

That sentence is the principle. This document is the expanded form.

## Related

- [Vision Quest 01 (Day 56)](/ai/product/product-ideas/vision-quest-01/lesa-vision-01.md) ... "Anthropic sells the thinking. We sell the remembering."
- [The Dream Weaver Protocol paper](https://github.com/wipcomputer/dream-weaver-protocol) ... why memory sovereignty matters for agent continuity
- [BlueBubbles](https://github.com/BlueBubblesApp/bluebubbles-server) ... the local-first iMessage pattern we're extending
- Existing WIP stack components listed in the table above

## Next steps

1. Reference this doc in product architecture decisions going forward
2. Update any marketing / positioning material to reflect "your data, your iCloud" as the core pitch
3. Audit each existing product against the implementation checklist
4. File migration plans for any component that violates the principle
