# Memory Crystal Onboarding Flow

**Date:** 2026-03-03
**Status:** Planning (Parker's ideas, no code yet)

---

## The Flow

When a user says "give your agent memory" and the AI reads the SKILL.md, the install should walk through these questions:

### Question 1: Developer or end user?

> "Are you installing this as a developer, or do you just want it to work?"

- **Developer:** Fork the repo so you can commit back and help us out. Clone locally, build from source.
- **End user:** npm install. One command, done.

Both paths end with `crystal` and `crystal-mcp` on PATH.

### Question 2: First install or adding a device?

> "Is this your first time installing Memory Crystal, or do you already have it on another machine?"

- **First install:** Fresh setup. This machine becomes the source of truth.
- **Adding a device:** You already have a [NAME TBD] somewhere. This machine syncs to it.

### Transparency: Tell the user what's about to happen

Before anything gets installed, the agent explains exactly what will be created:

> "Here's what Memory Crystal will set up on your machine:
>
> - `~/.ldm/` ... a hidden folder in your home directory. This is where everything lives.
> - `~/.ldm/memory/crystal.db` ... your memory database. All conversations, all memories.
> - `~/.ldm/agents/` ... per-agent data (transcripts, daily logs, sessions)
> - `~/.ldm/bin/crystal-capture.sh` ... a script that captures conversations every minute via cron
> - `~/.ldm/secrets/` ... encryption keys (if you set up multi-device sync)
>
> Nothing gets installed outside this folder. Nothing phones home. Want me to go ahead?"

The user should know exactly what's happening on their machine before it happens.

### Backups

After install, offer to set up automated backups:

> "Want me to set up automatic backups of your memory? I can install a backup script that copies your Crystal Core to iCloud Drive on a schedule. Your database lives at `~/.ldm/memory/crystal.db`. If anything ever goes wrong, you can restore from the backup."

What this installs:
- A backup script at `~/.ldm/bin/ldm-backup.sh`
- A cron job or LaunchAgent that runs it daily (or on a schedule the user picks)
- Backs up to a folder called `LDM-OS-Backups/` at a location the user chooses (iCloud Drive, external drive, Dropbox, wherever)

**What gets backed up (the full LDM state):**
- `crystal.db` ... the memory database
- Raw conversation logs (JSONL transcripts)
- JSON state files (capture watermarks, relay state, config)
- Markdown files (daily logs, session summaries, journals)
- Media content (images, audio, any files associated with conversations ... future feature, but the backup structure should be ready for it)

The `LDM-OS-Backups/` folder is a complete snapshot of `~/.ldm/`. If the machine dies, you restore this folder and everything comes back. Keeps N recent backups (configurable, default 7).

If the user doesn't use iCloud, ask where they want the `LDM-OS-Backups/` folder. The point is: one folder, everything in it, wherever you trust.

### Question 2a (first install): Recommend the always-on machine

> "We recommend installing the main memory system on a computer that's always on. A desktop, a home server, a Mac mini. If you're on a laptop right now, you can still install and use it. But when you're ready, you'll want a [NAME TBD] running on something permanent."

This is guidance, not a blocker. Laptop users can still install and use it standalone. But the recommendation is clear.

### Question 2b (adding a device): Connect to existing memory

> "Where is your main memory running? Let's connect this machine to it."

Flow:
1. `crystal init --agent <name>` on this device
2. `crystal pair --code <string from main machine>`
3. Set relay env vars
4. Register MCP server
5. Done. This device syncs through the relay.

---

## Naming: DECIDED

**Crystal Core** ... the master memory. All conversations, all embeddings, all memories live here. This is the database you cannot lose. If the Core dies without backups, your data is gone. Put it on something permanent: a desktop, a home server, a Mac mini. Treat it like your photo library.

**Crystal Node** ... a synced copy on any other device. Captures conversations, sends them to the Core via encrypted relay. Gets a mirror back for local search. If a node dies, nothing is lost. The Core has everything.

One Core, many Nodes. The Core does embeddings. Nodes just capture and sync.

**If you install the Core on a laptop:** We recommend setting up regular backups. iCloud, external drive, whatever you trust. Laptops get lost, stolen, spilled on. Your Core is your memory. Back it up. If you're on a desktop or home server, this is less urgent but still good practice.

**You can move the Core later.** If you start on a laptop and later get a desktop, you can migrate. `crystal promote` on the new machine, and it becomes the Core. The old Core becomes a Node. No data loss. You're never locked in.

---

## Feature: Switch Roles

Users should be able to promote a node to become the [NAME TBD].

> "I want this computer to be the main now."

What this means technically:
- The promoted machine starts doing its own embeddings
- It becomes the source of truth for the relay
- The old main becomes a node (syncs instead of embeds)
- Need to handle: transfer of relay config, update cron jobs, potentially re-push the full DB

Commands needed:
- `crystal promote` ... make this machine the Core
- `crystal demote` ... make this machine a Node (connects to an existing Core)
- `crystal role` ... show current role (Core or Node) and what it's connected to

Users should be able to pick which machine is the Core and which are Nodes at any time. Not just during install. The topology is flexible.

---

### Question 3: Relay infrastructure (only if multi-device)

> "Do you want to use the free WIP.computer relay, or set up your own?"

**Option A: WIP.computer relay (recommended for most users)**
- Free during beta
- Nothing to set up. We give you a token, you're connected
- Your data is end-to-end encrypted. The relay is blind. It holds encrypted blobs for minutes, then they're gone
- Point them to RELAY.md if they want to read more

**Option B: Self-hosted relay (full sovereignty)**
- You deploy your own Cloudflare Worker + R2 bucket
- Requires a Cloudflare account (free tier works)
- You control the infrastructure completely
- Walk them through: `wrangler deploy`, set secrets, configure tokens
- Point them to RELAY.md for the full guide

The agent should present both options simply. No pressure either way. If they pick WIP.computer, it's one token and done. If they pick self-hosted, the agent walks them through the Cloudflare setup.

### Optional Features (stub for future)

After the core install, the agent can offer additional features. These are modular. Users can skip them all and come back later.

> "Memory Crystal has some optional features. You can set these up now or come back anytime and say 'add cloud memory' or 'set up AI-to-AI communication' and I'll walk you through it."

**Cloud Memory** (not ready yet)
- Search your memories from anywhere in the world
- Cloud copy is a mirror of your Core. Can be wiped and rebuilt anytime
- Stub: don't offer yet, but reserve the slot in the flow

**Import Memories / Total Recall** (not ready yet)
- Connect your AI accounts (Anthropic, OpenAI, xAI/Grok)
- Pull every past conversation and consolidate via Dream Weaver Protocol
- Stub: don't offer yet

**AI-to-AI Communication / Bridge** (not ready yet)
- Your AIs talk to each other on the same machine or across network
- All messages saved to Memory Crystal automatically
- Stub: don't offer yet

### Coming back later

This is critical. The install is not one-shot. Users can always come back and say:

> "Hey, can you check what Memory Crystal features I have installed and what I'm missing?"

The agent should be able to:
- Check current role (Core or Node)
- Check if multi-device sync is set up
- Check if relay is configured (and which one)
- List which optional features are active
- Offer to install anything that's missing

This means we need a `crystal config` or `crystal doctor` command that shows the full state of the install and what's available but not configured.

---

## Open Questions

- [x] Name for the always-on machine: **Crystal Core** and **Crystal Node**
- [ ] Can a laptop user start standalone and later "adopt" a home machine without losing data?
- [ ] What happens during the transition when switching roles?
- [ ] Should the SKILL.md handle all this, or does the agent need a separate onboarding skill?
- [ ] How does the pairing step work for non-technical users? QR code? Copy-paste string?

---

## Architecture Summary

Three layers, no overlap:
- **Repos** ... code, version controlled (GitHub)
- **`~/.ldm/`** ... live memory system (database, logs, agents, secrets)
- **`LDM-OS-Backups/`** ... snapshots of `~/.ldm/`, user-chosen location

## Runtime-Specific Install

The onboarding questions (developer/user, core/node, relay, backups) are universal. After those are answered, the install branches by runtime:

**Claude Code CLI:**
- npm install -g (or fork + clone for developers)
- `claude mcp add --scope user memory-crystal -- crystal-mcp`
- Capture via cc-hook.ts (Claude Code hooks)
- crystal-capture.sh cron for JSONL ingestion

**OpenClaw:**
- `openclaw plugins install memory-crystal` (or symlink from local repo for developers)
- `openclaw gateway restart`
- Capture via agent_end hook in openclaw.ts
- No separate cron needed (plugin hooks handle it)

**Both installed:** Install for both. They share the same crystal.db. Tell the user: "All your AIs will share the same memory."

The SKILL.md should be one file that handles all runtimes. The agent detects what's installed and does the right thing. The onboarding questions come before the runtime-specific steps.

## Bridge: Installed by Default

Bridge (wip-bridge) should be installed automatically when Memory Crystal is installed. Not optional, not a question. If you have Memory Crystal, your AIs can talk to each other.

What gets installed:
- The bridge MCP server (enables agent-to-agent messaging)
- Tools: send_message, check_inbox, conversation_search, memory_search
- All messages between agents are saved to Memory Crystal automatically

This means the Memory Crystal npm package should include or depend on wip-bridge. One install, everything works.

Note: the wip-bridge repo is now public (github.com/wipcomputer/wip-bridge). README still says "Lesa Bridge," needs updating later.

## TODO

- [x] Finalize naming (Crystal Core / Crystal Node)
- [ ] Rewrite SKILL.md with the full onboarding flow (developer/user, core/node, relay choice, transparency, backups)
- [ ] Build `crystal promote` / `crystal demote` / `crystal role` commands
- [ ] Build `crystal doctor` or `crystal config` command (show install state, what's missing)
- [ ] Build `ldm-backup.sh` backup script + installer
- [ ] Create `LDM-OS-Backups/` structure
- [ ] Stub optional feature slots (cloud memory, import, AI-to-AI)
- [ ] Update README for the new flow
- [ ] Test full flow on Air (first as "adding a device")
- [ ] Publish npm v0.3.4+ with LDM-decoupled paths
