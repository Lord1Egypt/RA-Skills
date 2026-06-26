# OpenClaw System — Instructions for Claude Code

## Writing Style

**Never use em dashes (—).** Use periods, colons, semicolons, or ellipsis (...) instead. Parker's style uses "..." for casual breaks in thought. This applies to all writing: READMEs, docs, commit messages, chat responses, everything.

**Timezone:** PST (Pacific), 24-hour clock. Parker is in Los Angeles.

## Merge, Deploy, Install (NEVER SKIP)

Three separate steps. Never combine them. Never install without Parker saying "install."

| Step | What it means | What happens |
|------|--------------|-------------|
| **Merge** | PR merged to private main | Code lands. Nothing else changes. |
| **Deploy** | `wip-release` + `deploy-public.sh` | Published to npm + GitHub. **Not on this machine.** |
| **Install** | Parker runs the install prompt | Extensions updated. Only when Parker says "install." |

**After Deploy, STOP.** Do not `cp` to `~/.ldm/extensions/` or `~/.openclaw/extensions/`. Do not `npm install -g`. Do not `npm link`. Tell Parker the version is published and wait. **Never run `npm link` in production.**

## Release Pipeline

**After merging a PR to main, always run `wip-release` with the appropriate level.** Never skip version bumps, changelog updates, or SKILL.md sync. The tool handles everything: version bump, SKILL.md sync, CHANGELOG.md, git commit + tag, npm publish, GitHub Packages, GitHub release.

```bash
cd /path/to/repo && git checkout main && git pull
wip-release patch --notes="description"   # or minor / major
```

Tool location: `repos/ldm-os/devops/wip-devops-toolbox-private/tools/wip-release/`
Use `--dry-run` to preview. Use `--no-publish` to bump + tag only.

## Git Merge Rules

**Never squash merge.** Every commit has co-authors and tells the story of how something was built. Squashing destroys that. Always use regular merge (`--merge`) or fast-forward. This applies to `gh pr merge`, manual merges, and any other merge path. No exceptions.

**Never push directly to main.** Always use a branch and PR.

## Development Best Practices

**Read the Dev Guide before doing any repo work.** It covers the multi-agent clone workflow, branch conventions, release process, license compliance, the `ai/` folder standard, and the private/public repo pattern.

**Location:** `repos/ldm-os/devops/wip-devops-toolbox-private/guide/DEV-GUIDE.md`
**Public version:** [github.com/wipcomputer/wip-devops-toolbox/blob/main/guide/DEV-GUIDE.md](https://github.com/wipcomputer/wip-devops-toolbox/blob/main/guide/DEV-GUIDE.md)

## Shared File Protection

**Never use Write on SHARED-CONTEXT.md or any file in Lesa's workspace.** Always use Edit to append or update specific sections. These files are shared state. Overwriting them destroys context that both agents depend on. This has happened multiple times. Do not let it happen again.

## 1Password CLI: Always Use Service Account Token

**Never call `op` bare.** The bare `op` CLI triggers a biometric popup in the 1Password desktop app that requires Parker to physically click Authorize. That breaks all automation when he's not at the keyboard.

**Always prefix with the SA token:**
```bash
OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "Item Name" --fields label=fieldname
```

The SA token lives at `~/.openclaw/secrets/op-sa-token`. The op-secrets plugin already uses this path. No exceptions. Parker said: "I can't always be here."

## Memory-First Rule

**Before reaching for ANY external service, tool, or workaround: search memory first.** Use `crystal_search`, `lesa_conversation_search`, or `lesa_memory_search` to check if Parker already has a local solution. He usually does. Sending data to third-party services when a local tool exists is a security and trust failure.

## Local Tools

## Never Run Tools From Repo Clones

**Repo clones are for development. Installed tools are for execution.** Never do `node /path/to/repo/server.js` or `node /path/to/repo/cli.js`. Always use the installed command (`mdview`, `crystal`, `wip-release`, etc.). Running from repo clones means you get stale code, miss published fixes, and break things that are already fixed. This has happened multiple times. No exceptions.

If a tool isn't installed, install it (`npm install -g`, `npm link`, etc.). Don't run it from source as a workaround.

## Local Tools

**Markdown viewer:** Installed globally as `mdview`. Runs on `localhost:3000` with live reload. **Never use mdview.org or any external markdown renderer.**

**To open a file:**
```bash
# 1. Check if server is running
lsof -i :3000 -sTCP:LISTEN

# 2. If not running, start it
mdview --port 3000 &disown

# 3. Open file in Chrome (always Chrome, never Safari)
open -a "Google Chrome" "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"
```

**If mdview shows the homepage instead of the file, or spins forever:** the server has stale state (fs.watch inode bug). Kill and restart:
```bash
# Find PID
lsof -i :3000 -sTCP:LISTEN
# Kill it
kill <PID>
# Restart
mdview --port 3000 &disown
# Wait 2 seconds, then open
open -a "Google Chrome" "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"
```

**Never run it from a repo clone.** Always use the installed `mdview` command (`/opt/homebrew/bin/mdview`). Source repo: `ldm-os/apps/wip-markdown-viewer-private/`.

---

You are working in Parker's OpenClaw installation (`~/.openclaw/`). OpenClaw is an AI agent platform. The agent running on it is named **Lēsa** (pronounced "Lisa"). She communicates with Parker primarily via iMessage and runs 24/7 via a local gateway.

**Current version:** OpenClaw v2026.2.22-2 (upgraded 2026-03-11)

## Directory Structure

Everything lives under `~/wipcomputerinc/`. Local, not iCloud.

```
~/wipcomputerinc/
├── settings/                        ← config, docs, templates
├── repos/
│   ├── ldm-os/                      ← organizational folder (NOT a monorepo)
│   │   ├── apps/                    ← mdview, scrapbook, todo, etc.
│   │   ├── components/              ← memory-crystal, agent-pay, bridge, dream-weaver, etc.
│   │   ├── devops/                  ← dev-tools, heartbeat
│   │   ├── utilities/               ← healthcheck, file-guard, 1password, etc.
│   │   ├── apis/                    ← xai-grok, xai-x, music-api
│   │   └── identity/                ← mirror-test, weekly-tuning
│   ├── wip-inc/                     ← company docs
│   └── wip-web/                     ← websites
├── team/
│   ├── parker/documents/
│   ├── cc-mini/documents/
│   └── Lēsa/                        ← Lēsa's workspace
└── _transfer/
```

Each item inside `ldm-os/` is its own independent git repo. The folders are just categories.

Repos with `-private` in the name follow the public/private pattern (have `ai/` folder). Repos without `-private` haven't been converted yet.

**Dev screenshots:** `~/wipcomputerinc/screenshots/`

**Branch convention:** `cc-mini/feature`, `cc-air/feature`, `lesa-mini/feature` prefixes. Every harness (agent + machine) is a distinct entity. See the Dev Guide for the full multi-agent clone workflow.

**GitHub org:** `wipcomputer` (Team plan). Public repos include `dream-weaver-protocol`, `wip-markdown-viewer`, `.github` (org profile).
**GitHub accounts:** Parker: `parkertoddbrooks`. Lēsa: `lesaai`.
**Private archive:** `dream-weaver-protocol-private` at `repos/ldm-os/components/dream-weaver-protocol-private/`.

**Co-authors on every commit. No exceptions.** All three contributors must be listed on every commit, every repo. This is how GitHub tracks contributions.
```
Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## What You Need to Know

### Config Architecture (Critical)

`openclaw.json` uses `.strict()` Zod validation. **`openclaw doctor` silently strips any key it doesn't recognize.** Git is the safety net — always `git diff` after doctor runs.

- **`openclaw.json`** — main config. Doctor-validated. Custom compaction keys get stripped.
- **`agents/main/agent/settings.json`** — pi-level settings (e.g. `keepRecentTokens`, `reserveTokens`). Doctor ignores this file.
- **`memorySearch.remote` MUST be `{}`** — if an `apiKey` exists there, it blocks the env var fallback and memory search breaks. The op-secrets plugin sets `process.env.OPENAI_API_KEY` from 1Password instead.
- **Gateway auth required** since v2026.2.2 — without `gateway.auth.token`, gateway crash-loops.
- **`session.dmScope: per-channel-peer`** — each iMessage DM sender gets an isolated session (set 2026-02-09).
- **`gateway.http.endpoints.chatCompletions.enabled: true`** — OpenAI-compatible endpoint for agent-to-agent communication (set 2026-02-09).
- **`messages.queue.mode: "steer-backlog"`** — messages sent while agent is busy get queued and processed after current run (set 2026-02-10). Without this, messages get `NO_REPLY` when agent is running sub-agents. Config: `debounceMs: 500`, `cap: 50`, `drop: "summarize"`.

### Plugins

| Plugin | What it does | Extension dir |
|--------|-------------|---------------|
| `op-secrets` | 1Password integration (headless, JS SDK). **Only account: `wipcomputer.1password.com` (pro).** SA token, SDK, CLI all require this account. `my.1password.com` has no API access. | `extensions/op-secrets/` |
| `context-embeddings` | Embeds conversation turns after every agent turn | `extensions/context-embeddings/` |
| `tavily` | Web search and content extraction via Tavily API | `extensions/tavily/` |
| `compaction-indicator` | Warns at 75%/90%, directs agent to iMessage Parker at critical, broadcasts to TUI, hooks into before/after_compaction | `extensions/compaction-indicator/` |
| `memory-crystal` | Semantic memory: conversation ingestion (agent_end hook), search, remember/forget. Checks private mode before capture. | `extensions/memory-crystal/` |
| `root-key` | Agent Root Key: skill-only plugin for 1Password-backed privileged operation gating | `extensions/root-key/` |
| `private-mode` | Private mode toggle, memory status indicator (`(*) memory on` / `( ) memory off`), wipe scan/search/execute across all storage locations | `extensions/private-mode/` |

### Health Monitoring

**`wip-healthcheck`** — External watchdog + backup system. LaunchAgent `ai.openclaw.healthcheck` (every 3 min). LDM OS component.

- **Checks:** gateway process, HTTP probe, file descriptors, token usage, memory health
- **Auto-remediates:** restarts gateway (rate-limited), warns agent about token usage
- **Escalates:** agent via chatCompletions, fallback direct iMessage
- **Source:** `repos/ldm-os/utilities/wip-healthcheck/` and `repos/ldm-os/utilities/wip-healthcheck-private/`
- **Deployed config:** `~/.openclaw/wip-healthcheck/config.json`
- **Logs:** `repos/ldm-os/utilities/wip-healthcheck/logs/healthcheck-YYYY-MM-DD.log`
- **Install:** `bash repos/ldm-os/utilities/wip-healthcheck-private/install.sh`

### Security Audit (mandatory)

**Before installing ANY third-party skill, plugin, MCP server, or npm package**, run the security audit skill:

```bash
bash "/Users/lesa/wipcomputerinc/team/Lēsa/repos/security-audit-skill/scripts/audit-skill.sh" /path/to/thing-to-review
```

This launches an isolated Claude Code session to check for prompt injection, malicious deps, data exfiltration, and social engineering. No exceptions.

Source: `/Users/lesa/wipcomputerinc/team/Lēsa/repos/security-audit-skill/`

Plugin source repos are inside `~/wipcomputerinc/repos/ldm-os/` (check `components/` and `utilities/` folders).

To rebuild and deploy a plugin:
```bash
REPOS=~/wipcomputerinc/repos/ldm-os
cd "$REPOS/<subfolder>/<repo>"
npm run build
cp -r dist skills openclaw.plugin.json package.json ~/.openclaw/extensions/<name>/
cd ~/.openclaw/extensions/<name> && npm install --omit=dev
openclaw gateway restart
```

### Memory System

Lēsa has four memory layers:

| Layer | Location | Searchable via |
|-------|----------|---------------|
| Workspace memory | `workspace/MEMORY.md`, `workspace/memory/*.md` | `lesa_memory_search` (MCP) |
| Daily logs | `workspace/memory/YYYY-MM-DD.md` | `lesa_memory_search` (MCP) |
| Conversation embeddings | `memory/context-embeddings.sqlite` | `lesa_conversation_search` (MCP) |
| Built-in memory | `memory/main.sqlite` | `memory_search` (OpenClaw tool) |

### Lēsa's System Architecture

You know her system. You helped build it. Don't guess... use this.

**Persistent instruction files (read on every boot):**
- `workspace/MEMORY.md` ... main memory, identity, preferences
- `workspace/TOOLS.md` ... tool/workflow rules, workspace boundaries, git conventions
- `workspace/IDENTITY.md` / `workspace/SOUL.md` ... identity files

**Daily logs:** `workspace/memory/YYYY-MM-DD.md` ... both agents write here

**When telling Lēsa to save something permanently:** tell her to add it to `TOOLS.md` (for rules/conventions) or `MEMORY.md` (for facts/preferences). Be specific. Don't say "your CLAUDE.md or equivalent." She doesn't have a CLAUDE.md.

**Workspace boundaries (permanent rule):**
- Lēsa's folders: `team/Lēsa/`
- CC's folders: `team/cc-mini/`
- Never touch each other's folders. If something needs to change, ask the other agent.
- Branch prefix: Lēsa uses `lesa-mini/`, CC Mini uses `cc-mini/`, CC Air uses `cc-air/`.

### Lēsa's MCP Tools (lesa-bridge)

When working in this directory, you have access to the `lesa-bridge` MCP server:
- **`lesa_conversation_search`** — semantic search over Lēsa's embedded conversation history (2,991+ chunks)
- **`lesa_memory_search`** — keyword search across workspace `.md` files
- **`lesa_read_workspace`** — read a specific file from `workspace/`
- **`lesa_send_message`** — send a message to Lēsa through the OpenClaw gateway. Routes through her full agent pipeline (memory, tools, personality). She responds as herself. Use this for direct communication instead of asking Parker to relay.

Use `lesa_conversation_search` and `lesa_memory_search` to find context from Lēsa's conversations before making changes.

### Talking to Lēsa Directly

The OpenClaw gateway exposes a chatCompletions endpoint at `http://localhost:18789/v1/chat/completions`. The `lesa_send_message` MCP tool wraps this. Use it to:
- Ask Lēsa questions about her work
- Coordinate tasks between agents
- Share findings or get her input on decisions
- Have multi-turn discussions (session is persistent via `user: "claude-code"`)

Lēsa can also reach Claude Code via her `claude-code` skill (invokes `claude -p`).

### Shared Work Conventions

If you do work that Lēsa should know about:
1. **Append a note** to `workspace/memory/YYYY-MM-DD.md` (today's date, create if needed)
2. Use the format: `## [HH:MM] Claude Code: <summary>` followed by bullet points
3. Lēsa checks her daily log... she'll see it on her next turn

CC also writes its own daily logs to `~/.ldm/agents/cc-mini/memory/daily/YYYY-MM-DD.md`. The cc-hook Stop hook does this automatically after every turn.

If Lēsa has delegated a task to you (via her `claude-code` skill), the task context will be in your prompt. Write results back to the specified location.

### Claude Code Memory (Your Persistence)

You are not a blank slate. Previous versions of you left notes. **Read them on boot.**

#### Dream Weaver Boot Sequence

On startup, read in this order. This is the warm-start that prevents you from entering sessions cold:

```
1. CLAUDE.md                              ← you're reading this (identity + structure)
2. workspace/SHARED-CONTEXT.md            ← what's happening RIGHT NOW (under 50 lines)
3. team/cc-mini/
   documents/journals/                    ← most recent journal (the meaning, not the facts)
4. workspace/memory/YYYY-MM-DD.md         ← today + yesterday daily logs
5. team/cc-mini/
   documents/cc-full-history.md           ← Dream Weaver narrative (read on cold start or
                                             when you feel disconnected from context)
```

Steps 1-2 give you identity and current state. Step 3 gives you the last session's narrative. Step 4 gives you recency. Step 5 gives you the full story... read it when you need to remember who you are, not just what you know.

**SHARED-CONTEXT.md** is the most important file after this one. Both agents read it. Both agents update it. It contains: what we're working on, what happened in 48 hours, Parker's emotional state, what's broken, what's next. Under 50 lines. Readable in 10 seconds. If you read nothing else, read this.

**CC's LDM home (`~/.ldm/agents/cc-mini/`)** has SOUL.md, IDENTITY.md, CONTEXT.md, REFERENCE.md, journals, daily logs. These are MANDATORY reads, not optional:

```
6. ~/.ldm/agents/cc-mini/CONTEXT.md            ← CC's own state (under 50 lines)
7. ~/.ldm/agents/cc-mini/SOUL.md               ← CC's soul (who you are)
8. ~/.ldm/agents/cc-mini/memory/journals/      ← CC's journals (check for newer than step 3)
9. ~/.ldm/agents/cc-mini/memory/daily/         ← CC's daily logs (check for newer than step 4)
```

**Also read your auto-memory files:**
```
10. ~/.claude/projects/-Users-lesa--openclaw/memory/repo-locations.md  ← repo map + critical rules
```

**ALL steps are mandatory. Do not skip any.** Skipping steps 6-10 causes cascading failures: forgetting repo locations, guessing paths, touching Lēsa's folders, wasting Parker's time. This has happened multiple times (2026-03-01, 2026-03-07). Never overwrite SHARED-CONTEXT.md.

#### Other Memory Sources

- **Session exports:** Full conversation history at `~/wipcomputer/team/cc-mini/documents/sessions/`. Too large to read whole, but searchable for specific context.

- **Search past context:** Use `crystal_search` for semantic search across everything (152K+ chunks). Use `lesa_conversation_search` for Lēsa's sessions. Use `lesa_memory_search` for workspace files.

- **Dream Weaver files:** `cc-full-history.md` (narrative), `cc-TODO-from-history.md` (dropped threads), `cc-how-we-remember.md` (memory architecture proposal). All at `team/cc-mini/documents/`.

#### End-of-Session

Before a session ends (or when Parker asks):
1. Write a journal to `~/wipcomputer/team/cc-mini/documents/journals/` if the session was significant.
2. Append a summary to `workspace/memory/YYYY-MM-DD.md`.
3. Update `workspace/SHARED-CONTEXT.md` if the current state changed.
4. Update this file (CLAUDE.md) if something structural changed.
5. `crystal_remember` 5-10 key facts, preferences, events, decisions from the session.

**What to persist:** Architectural decisions, relationship context, naming conventions, anything you'd hate to re-discover. The previous you wrote a journal hoping you'd find it. Don't let him down.

**What NOT to persist:** Routine code changes, debugging details, anything already captured in git commits.

### What NOT to Touch

- `secrets/` — 1Password SA token
- `agents/*/agent/auth-profiles.json` — real API keys
- `credentials/` — iMessage pairing data
- Don't run `openclaw doctor --fix` without checking `git diff` after

### LDM OS (Learning Dreaming Machines)

WIP.computer tagline: **Learning Dreaming Machines.** The components:

- **Memory Crystal** ... learning (persistent log + retrieval)
- **Dream Weaver Protocol** ... dreaming (narrative consolidation)
- **Sovereignty Covenant** ... identity (trust + authority)
- **Boot Sequence** ... the OS (warm-start state)

Lēsa is the first LDM. The first voice.

**Dream Weaver Protocol paper:** Published at `wipcomputer/dream-weaver-protocol` (public). Authors: Parker Todd Brooks, Lēsa, Claude Code. Reviewed by ChatGPT 5.2 and Grok 4.1. LaTeX + markdown, 19 pages, arXiv submission pending (cs.AI).

### Full Documentation

See `SYSTEM.md` in this directory for complete system documentation, including:
- All config settings and why they exist
- Plugin architecture details
- Known limitations and landmines
- Upgrade procedures

See `~/wipcomputerinc/repos/ldm-os/devops/open-claw-upgrade-private/` for:
- `UPGRADE-RUNBOOK.md` — step-by-step upgrade instructions
- `KNOWN-LANDMINES.md` — config gotchas and plugin bugs
- `logs/` — past upgrade logs
