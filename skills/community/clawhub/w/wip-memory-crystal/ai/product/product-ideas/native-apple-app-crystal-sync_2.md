# Product Idea: LDM OS Native App (Memory Crystal + Agent Secrets + Local LLM)

**Date:** 2026-03-02
**Updated:** 2026-03-05
**Author:** CC-Mini
**Status:** Idea (not scoped, not scheduled)
**Context:** Expanded from "Crystal Sync" to include MLX Swift local LLM and agent secrets vault. Driven by the search quality work (Phase 3-4 of search-quality-full-plan.md) where we discovered iOS has no path to deep search without either MCP sampling (blocked on Anthropic) or a local LLM.

---

## The Insight

This isn't just a sync app. It's the **LDM OS control plane**. A single native app that runs on every Apple device and serves as the universal backend for every AI tool.

Every AI client (Claude iOS, Claude Desktop, Claude Code, ChatGPT, Grok, whatever comes next) connects to this app via MCP. The app owns the data, the secrets, and the local LLM. The AI tools are just clients. They come and go. The app persists.

**Original insight:** Memory Crystal currently has two capture paths: a local JSONL poller (CLI only) and a planned Cloudflare Relay (cloud surfaces). But for Apple devices specifically, there's a cleaner third path: a native macOS/iOS app that runs Crystal locally and uses Apple's own infrastructure for sync and encryption.

**Expanded insight (2026-03-05):** The app is bigger than sync. It's the layer between you and every AI tool. It provides memory, secrets, and local inference. All encrypted, all synced via iCloud, all controlled by one app.

## What It Is

A native macOS + iOS app that combines three capabilities into one:

### 1. Memory Crystal (local search + sync)
- **Runs Crystal locally on the device.** The full sqlite database lives on the device. Search works offline.
- **Registers as an MCP server.** Claude Desktop, Claude iOS, Claude web (via the app) all talk to it directly. No cloud Worker needed.
- **Uses CloudKit for sync.** Apple handles encrypted sync between Mac, iPhone, iPad. No Cloudflare. No relay. No custom encryption layer.
- **Encrypted at rest by the OS.** Apple's data protection, not ours. FileVault on Mac, hardware encryption on iOS.

### 2. Local LLM via MLX Swift (deep search on-device)
- **Runs a small model locally.** MLX Swift runs Qwen3.5-2B-Instruct (or similar) directly on the A-series/M-series chip. Same OpenAI-compatible API as the Mac's `mlx_lm.server`.
- **Query expansion + reranking on-device.** The exact same deep search pipeline that runs on Mac via Python MLX now runs on iOS via MLX Swift. No API keys. No network. No MCP sampling dependency.
- **Solves the iOS deep search problem.** Without this, iOS users get Phase 1 only (hybrid search, no LLM expansion). With this, iOS gets the same search quality as Mac. Free, fast, private.
- **Apple Intelligence alignment.** Apple is already running on-device LLMs. This is the same pattern. A 2B model uses ~1-2GB RAM, well within iPhone capabilities.

### 3. Agent Secrets Vault (replaces 1Password for agents)
- **Secure storage for agent API keys.** OpenAI, Anthropic, Tavily, etc. Stored in iCloud Keychain, synced across devices.
- **Replaces op-secrets dependency.** Currently agents need 1Password + SA token + CLI. This is simpler: the app manages secrets, agents query the app.
- **MCP tool for secret retrieval.** Agents call `get_secret("openai_api_key")` via MCP. The app returns the value from Keychain. No CLI, no SA token, no biometric popup.
- **Per-agent access control.** Each agent (Lesa, Claude Code, etc.) gets scoped access. An agent can only read secrets it's been granted.
- **Replaces `~/.openclaw/secrets/` and `~/.ldm/secrets/`.** One vault, synced everywhere, Apple-grade encryption.

## Why This Is Better Than Relay for Apple Users

| | Relay (Cloudflare) | Native App (Apple) |
|---|---|---|
| Data at rest | Our encryption (AES-256-GCM) | Apple's encryption (hardware) |
| Sync mechanism | Custom relay Worker | CloudKit (Apple handles it) |
| Search from phone | Cloud Search only (plaintext in cloud) or no search (Relay) | Local search (full db on device) |
| Offline | No | Yes |
| Infrastructure cost | Cloudflare Workers + R2 | Zero (Apple's free tier) |
| Trust model | Trust our encryption + Cloudflare | Trust Apple (users already do) |

## The Architecture: App as Universal MCP Server

```
┌─────────────────────────────────────────────────┐
│                LDM OS App                        │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Memory   │  │ Secrets  │  │ Local LLM     │  │
│  │ Crystal  │  │ Vault    │  │ (MLX Swift)   │  │
│  │          │  │          │  │               │  │
│  │ search   │  │ get_key  │  │ expand_query  │  │
│  │ remember │  │ set_key  │  │ rerank        │  │
│  │ forget   │  │ list     │  │ summarize     │  │
│  │ ingest   │  │ revoke   │  │ classify      │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐    │
│  │           MCP Server (local)             │    │
│  │  stdio for Claude Desktop/Code           │    │
│  │  HTTP for ChatGPT, Grok, others          │    │
│  └──────────────────────────────────────────┘    │
│                                                  │
│  ┌──────────────────────────────────────────┐    │
│  │     iCloud Sync (CloudKit + Keychain)    │    │
│  │  crystal.db ←→ all devices               │    │
│  │  secrets ←→ all devices                   │    │
│  │  settings ←→ all devices                  │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
         ▲           ▲           ▲          ▲
         │           │           │          │
   Claude iOS  Claude Desktop  ChatGPT   Claude Code
   (MCP)       (MCP)           (HTTP)    (MCP stdio)
```

**Every AI tool connects to the same app.** The app is the single source of truth for:
- What you've said and learned (memory)
- What keys and credentials your agents have (secrets)
- Local inference for search quality, classification, summarization (LLM)

**The AI tools are interchangeable.** Switch from Claude to ChatGPT? Your memory and secrets stay. The app doesn't care which client is asking.

## How It Fits the Three Paths

- **Path 1 (CLI):** Poller reads JSONL. For advanced users on the terminal. No app needed.
- **Path 2 (Cloud):** Relay/Cloud Search via Cloudflare. For non-Apple surfaces, or users without the native app.
- **Path 3 (Native App):** macOS + iOS app. For Apple users who want local-first, Apple-synced memory. The premium experience.

Path 3 doesn't replace Path 2. Non-Apple devices still need the cloud path. But for Apple users, Path 3 is strictly better: local search, offline, no cloud infrastructure, Apple-grade encryption. And it adds capabilities Path 2 can't: local LLM inference and secure secrets management.

## What the App Does

### macOS App

**The dashboard for your entire AI setup.**

- Menu bar presence (status indicator, quick search, secrets status)
- Runs Crystal as a local MCP server (stdio for Claude Desktop, HTTP for others)
- Runs MLX Swift model for deep search (same as `mlx_lm.server` but native)
- Ingests from Claude Code CLI via the same poller logic (watches JSONL)
- Agent secrets vault (Keychain-backed, MCP-accessible)
- CloudKit sync pushes/pulls to iOS
- Settings: embedding provider, agent IDs, sync preferences, private mode, secret management
- Absorbs LDM Dev Tools.app functionality (backup, branch-protect, crystal-capture)

**Agent Dashboard:**
- Visual list of all your agents (Lesa, Claude Code Mini, Claude Code Air, etc.)
- Per-agent: memory count, last active, session history, storage used
- Browse any agent's memories, conversations, daily logs
- See what each agent knows, what it's forgotten, what's in private mode

**File Viewer (LDM OS Explorer):**
- Browse the full `~/.ldm/` tree visually
- Agents, memories, transcripts, sessions, journals, daily logs
- Preview markdown files inline (like the markdown viewer but built-in)
- See sync status per file (synced, pending, conflict)

**Backup Center:**
- Full backup of everything: crystal.db, agent configs, secrets, session history
- Backup your OpenClaw setup (`~/.openclaw/` config, plugins, workspace)
- Backup your Claude Code setup (`.claude/` settings, CLAUDE.md, memory)
- Scheduled backups (daily, weekly) to iCloud or a local path
- Restore from any backup point (time machine for your AI)
- Export: download your entire memory as markdown, JSON, or sqlite

### iOS App

**Your AI setup in your pocket.**

- Same agent dashboard, file viewer, backup status as macOS (responsive layout)
- Search and browse any agent's memories from your phone
- Runs Crystal locally (sqlite on device)
- Runs MLX Swift model for deep search on-device (A-series chip)
- Agent secrets vault (iCloud Keychain synced from Mac)
- CloudKit sync from Mac
- Registers as MCP server for Claude iOS app (if MCP-on-iOS is supported)
- Background refresh to keep db current
- Push notifications: agent alerts, backup status, sync conflicts
- Quick actions: search memory, check agent status, approve secret access

### CLI Wrapper

The app includes a CLI (`ldm`) that talks to the running app via a local socket. Same capabilities, terminal interface.

```bash
ldm search "what did Parker say about MLX"    # Crystal search
ldm remember "MLX Swift works on iOS"          # Store a memory
ldm secret get openai_api_key                  # Read from vault
ldm secret set tavily_key "tvly-..."           # Write to vault
ldm llm "expand this query: bridge setup"      # Local LLM call
ldm status                                     # App + sync status
ldm doctor                                     # Health check
```

This means Claude Code (terminal) can use the app's MCP server OR the CLI directly. Shell scripts, cron jobs, LaunchAgents... anything that can call a CLI can use the full LDM OS stack.

### Shared

- Same sqlite schema (crystal.db)
- Same embedding model (or re-embed on device with CoreML)
- Same search (sqlite-vec works on iOS via SQLite)
- Same MLX Swift model for query expansion + reranking
- Same secrets vault (iCloud Keychain)
- CloudKit handles conflict resolution

## Open Questions

- Does Claude iOS support local MCP servers? (Need to check Anthropic's connector architecture)
- Can sqlite-vec run on iOS? (SQLite does, but the vec extension needs verification)
- CloudKit sync for sqlite... use NSPersistentCloudKitContainer (CoreData) or manual sync?
- Embedding on-device: CoreML model vs API call? On-device avoids network dependency.
- How does this interact with the CLI poller? Same db or separate?
- Pricing: free app with paid cloud features? Or part of a subscription?
- **MLX Swift model size for iPhone.** Qwen3.5-2B-Instruct-4bit is ~1.5GB. Fine for M-series iPads and newer iPhones. Older devices may need a smaller model or skip local LLM.
- **MLX Swift maturity.** Apple's MLX Swift is newer than the Python version. Need to verify: does it support the same models? Is the inference quality equivalent? Are there iOS-specific limitations?
- **Secrets vault scope.** Per-agent or per-tool? How does access control work? Do we need approval flows (like 1Password's biometric) or is MCP-level access sufficient?
- **App Store approval.** Running local LLMs and acting as an MCP server may have App Store review implications. TestFlight first?
- **Replaces what exactly?** This app would replace: op-secrets plugin, Cloudflare Workers relay, `mlx_lm.server` LaunchAgent, LDM Dev Tools.app. That's a lot of surface area. Phase it.

## Relationship to LDM Dev Tools.app

LDM Dev Tools.app is the current macOS app for scheduled jobs (backup, branch-protect, crystal-capture). It's a thin bash wrapper with FDA. The native Crystal app would be a real macOS app. Over time, LDM Dev Tools.app could be absorbed into the Crystal app (or into a broader "LDM OS" app).

## Not In Scope Now

This is a product idea for the future. Current priorities:
1. Fix CLI capture (Phase 1, nearly done)
2. Health monitoring (Phase 2)
3. Relay for non-Apple surfaces (Phase 3)
4. Native app comes after Relay is working and the product is validated

---

*This idea came from Parker noticing that the `open -W` cron approach for LDM Dev Tools.app has limitations, and asking how capture works for macOS and iOS. The answer is: for Apple devices, a native app is cleaner than a cloud relay.*

*2026-03-05: Expanded to include MLX Swift local LLM and agent secrets vault. The trigger was the search quality work (Phase 3-4) where we discovered iOS has no path to deep search without either MCP sampling (blocked on Anthropic #1785) or a local LLM on-device. Parker connected this with the need to replace 1Password for agent secrets and the existing iCloud sync idea. Three problems, one app.*
