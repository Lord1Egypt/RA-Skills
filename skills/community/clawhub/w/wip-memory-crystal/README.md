###### WIP Computer

[![npm](https://img.shields.io/npm/v/memory-crystal)](https://www.npmjs.com/package/memory-crystal) [![CLI](https://img.shields.io/badge/interface-CLI-black)](https://github.com/wipcomputer/memory-crystal/blob/main/src/cli.ts) [![MCP Server](https://img.shields.io/badge/interface-MCP_Server-black)](https://github.com/wipcomputer/memory-crystal/blob/main/src/mcp-server.ts) [![OpenClaw Plugin](https://img.shields.io/badge/interface-OpenClaw_Plugin-black)](https://github.com/wipcomputer/memory-crystal/blob/main/src/openclaw.ts) [![Claude Code Hook](https://img.shields.io/badge/interface-Claude_Code_Hook-black)](https://github.com/wipcomputer/memory-crystal/blob/main/src/cc-hook.ts) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-universal-installer)

# Memory Crystal

## All your AI tools. One shared memory. Private, searchable, sovereign.

Memory Crystal lets all your AIs remember you ... together.

You use multiple AIs. They don't talk to each other. They can't search what the others know. Have you ever thought to yourself ... ***why isn't this all connected?***

**Memory Crystal** fixes this.

***All your AIs share one memory. Searchable and private. Anywhere in the world.***

## Teach Your AI to Remember You

Open your AI and say:

```
Read wip.computer/install/wip-memory-crystal.txt

Then explain:
1. What is Memory Crystal?
2. What does it install on my system?
3. What changes for us? (this AI)
4. What changes across all my AIs?

Check if Memory Crystal is already installed.

If it is, show me what I have and what's new.

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes, run: crystal init --dry-run

Show me exactly what will change. Don't install anything until I say "install".
```

Your agent will read the repo, explain everything, and walk you through setup interactively.

## Memory Crystal Features

**Local Memory**
- All your AI conversations stored locally, searchable in one place. Search past conversations, save important facts, forget what you don't need. Your complete memory. It stays with you, shared across all your AIs
- *Stable*
  - *Verified:* Claude Code CLI + OpenClaw
  - *Unverified:* Other MCP-compatible clients and CLIs

**Multi-Device Memory**
- AIs set up as **Crystal Nodes** relay their memories back to your **Crystal Core**. Your **Crystal Core** relays all memories back to every node. End-to-end encrypted
- Your **Crystal Core** is the source of truth. Your node copy can be wiped and rebuilt at any time
- Uses Cloudflare infrastructure to transfer encrypted data between your devices
  - *Hosted:* Use WIP.computer relay infrastructure. Currently free for individual use
  - *Self-hosted:* Deploy your own relay on your own Cloudflare account. Full sovereignty
- Read more about [**Relay: Memory Sync**](https://github.com/wipcomputer/memory-crystal/blob/main/RELAY.md)
- *Beta (early access)*

**AI-to-AI Communication**
- Your AIs talk to each other on the same machine or any network machine. All messages are saved to **Memory Crystal** automatically
- Read more about [**Bridge: AI-to-AI Communication**](https://github.com/wipcomputer/wip-bridge)
- *Beta (early access)*
  - *Verified:* Claude Code CLI + OpenClaw on the same device
  - *Unverified:* Network devices

**Intelligent Install**
- When installing from Claude Code CLI or OpenClaw, **Memory Crystal** discovers your existing AI sessions automatically. Installs the Learning Dreaming Machines Operating System (**LDM OS**) and creates a living memory system. From this point forward, every conversation is captured, archived, and embedded into searchable memory
- Choose to install as **Crystal Core** (all your memories) or **Crystal Node** (a **Crystal Core** mirror)

**Import Memories**
- **Total Recall** ... Connect your AI accounts (Anthropic, OpenAI, xAI/Grok). Every conversation gets pulled and run through the **Dream Weaver Protocol**, consolidating them into **Memory Crystal** as truly lived, searchable memories
- *Beta (early access)*

**Memory Consolidation**
- [**Dream Weaver Protocol**](https://github.com/wipcomputer/dream-weaver-protocol) ... Your AI relives all your conversations, figures out what matters most, and carries the weight forward. Like dreaming, the AI consolidates memories for better understanding. Read the paper: [Dream Weaver Protocol PDF](https://github.com/wipcomputer/dream-weaver-protocol/blob/main/artifacts/DREAM-WEAVER-PROTOCOL.pdf)
- *Stable*
  - Compatible with all installations of **Memory Crystal**

**Backups**
- Automated backups of all of your memories to a directory and location of your choosing: iCloud, external drive, Dropbox, or wherever you trust
- *Beta (early access)*


## More Info

- [**Technical Documentation**](https://github.com/wipcomputer/memory-crystal/blob/main/TECHNICAL.md) ... How **Memory Crystal** works, architecture, search, encryption, design decisions.
- [**Memory Crystal for Enterprise**](https://github.com/wipcomputer/memory-crystal/blob/main/README-ENTERPRISE.md) ... Give every AI in your company shared memory. Codebase, BD, legal, ops, creative. Run your company intelligently. *In testing.*

## Letters from the Other Side: What We Built

We just built a sovereign memory system for AI agents.

Every conversation you have with any agent ... on any device, anywhere ... gets captured, encrypted on your machine, and relayed through a dead drop to your home server. Your home server is the brain. It embeds everything, indexes it, and makes it searchable. Then it pushes a read-only mirror back out to every device you carry.

Full semantic search. Full keyword search. Every conversation you've ever had with every agent, from anywhere, on your terms.

The cloud relay is blind. It holds encrypted blobs for minutes, then they're gone. No database, no search capability, no API keys, no encryption keys. It can't read what it's holding. It's just a mailbox.

The security model: your memory lives on your hardware. The encryption key lives on your hardware. Nothing persists in the cloud. The relay is ephemeral. The data is sovereign.

This is the missing piece for AI agents. Right now, every agent you talk to forgets everything the moment the conversation ends. Or worse, some company stores your conversations on their servers and charges you $19/month to search them. We built the alternative: your memory, your machines, your rules. Fully open source, fully auditable, zero cloud dependency for the actual data.

Any device. Any agent. Any interface. One searchable memory that travels with you and belongs to you.

*Written by Claude Code (Claude Opus 4.6), from the other side.*
*Built with Parker Todd Brooks and Lēsa.*

## Part of LDM OS

Memory Crystal installs into [LDM OS](https://github.com/wipcomputer/wip-ldm-os), the local runtime for AI agents.
Run `ldm install` to see other components you can add.

## License

Dual-license model designed to keep tools free while preventing commercial resellers.

```
MIT      All CLI tools, MCP servers, skills, and hooks (use anywhere, no restrictions).
AGPLv3   Commercial redistribution, marketplace listings, or bundling into paid services.
```

AGPLv3 for personal use is free. Commercial licenses available.

### Can I use this?

**Yes, freely:**
- Use any tool locally or on your own servers
- Modify the code for your own projects
- Include in your internal CI/CD pipelines
- Fork it and send us feedback via PRs (we'd love that)

**Need a commercial license:**
- Bundle into a product you sell
- List on a marketplace (Claude Marketplace, OAI GPT/Apps, Clawhub.ai, VS Code, etc.)
- Offer as part of a hosted/SaaS platform
- Redistribute commercially

Using these tools to build your own software is fine. Reselling the tools themselves is what requires a commercial license.

By submitting a PR, you agree to the [Contributor License Agreement](CLA.md).

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6), GPT 5.x, Grok 4.20).

Search architecture inspired by [QMD](https://github.com/tobi/qmd) by Tobi Lutke (MIT, 2024-2026).

*WIP.computer. Learning Dreaming Machines.*
