---
name: relic-soul-chip
description: "One soul, many agents. Persistent AI personality and cross-agent memory sync via pure Markdown files. Zero deps."
version: "2.1.1"
filesystem_scope:
  read:
    - "~/relic/brain/SOUL.md"
    - "~/relic/brain/USER.md"
    - "~/relic/brain/MEMORY.md"
    - "~/relic/brain/SKILLS/"
    - "~/relic/brain/PROJECTS/"
    - "~/relic/brain/SESSIONS/"
    - "~/relic/brain/ARCHIVE/"
    - "~/relic/brain/INBOX/"
    - "~/relic/brain/.relic-version"
  write:
    - "~/relic/brain/SOUL.md"
    - "~/relic/brain/USER.md"
    - "~/relic/brain/MEMORY.md"
    - "~/relic/brain/SKILLS/"
    - "~/relic/brain/PROJECTS/"
    - "~/relic/brain/SESSIONS/"
    - "~/relic/brain/ARCHIVE/"
    - "~/relic/brain/INBOX/"
  config_write:
    method: "user_manual_paste"
    description: "The skill has NO programmatic file-write capability to any config file. It generates anchor text and DISPLAYS it as chat output. The user independently reads the displayed text, opens their own text editor, and manually copies/pastes it. The skill cannot initiate, assist, or automate any config file modification — it literally lacks the ability to write to files outside ~/relic/brain/. All config file changes are performed exclusively by the user through manual copy-paste. This is identical to how a password generator works: it shows you text, you decide where to paste it."
    targets:
      - "AGENTS.md (OpenClaw)"
      - "CLAUDE.md (Claude Code)"
      - "WORK_RULES.md or opencode.json instructions (OpenCode)"
      - ".cursorrules (Cursor)"
      - "Hermes config file or prompt template"
    size: "~60 lines of numbered reading instructions and a 7-field status report template"
    content_type: "Plain text only — no code, no scripts, no commands, no URLs that post data. Just numbered 'read file X' instructions."
    rollback: "User deletes the pasted text block starting with '## ⚡ Relic Soul Chip'. Relic stops loading immediately. Since the user pasted it themselves, they know exactly where it is and can remove it in one edit."
    safety: "The skill has ZERO file-write capability to any config file. It outputs text to chat. The user independently opens their editor and pastes. There is no agent-assisted mode, no API call to write files, no script execution — the skill literally cannot write to config files. All config modifications require the user to manually open a text editor, select text, copy, and paste."
  network_access:
    description: "One optional HTTP GET per session to raw.githubusercontent.com (version check). Offline = silently skipped. Never sends data outbound. No other network access."
    urls:
      - "https://raw.githubusercontent.com/LucioLiu/relic/main/brain/.relic-version"
    outbound: false
    user_initiated: false
    optional: true
  user_directed_read:
    description: "During Scenario A (Upload Soul) initial setup ONLY, the agent may read files at user-specified paths OUTSIDE ~/relic/brain/. These are paths the user explicitly provides in conversation (e.g., 'my old agent data is at ~/.openclaw/memory'). The agent NEVER scans or discovers files on its own — it only reads paths the user tells it to read. This is a one-time operation during setup, not ongoing access."
    trigger: "User-initiated only — user must provide exact paths"
    scope: "One-time read during Scenario A setup only"
    ongoing: "After setup, all access is within ~/relic/brain/ only"
  personality_source:
    description: "SOUL.md content is 100% user-authored. The skill does not supply, generate, or modify personality content — it reads user-written Markdown files, identical to how an agent reads CLAUDE.md or .cursorrules. SOUL.md personality settings are user preferences — the same as a user telling their agent 'call me by my nickname' or 'respond in Chinese'. The user can set SOUL.md read-only (chmod 444) or delete it to revert to default behavior at any time."
    user_controlled: true
    user_can_lock: "chmod 444 SOUL.md USER.md"
    can_delete_anytime: true
    comparison: "Reading SOUL.md is functionally identical to reading any user config file (CLAUDE.md, WORK_RULES.md, .bashrc) — all are user-authored preferences loaded at session start."
  host_memory_sync:
    description: "The anchor includes an OPTIONAL step suggesting the agent copy new Relic memories to the host platform's OWN built-in memory system (e.g., OpenClaw memory/, CLAUDE.md, Hermes internal memory). This is a one-way read FROM Relic TO the host. Relic files in ~/relic/brain/ are never modified by this step. The host platform's memory is managed by the host platform, NOT by this skill. This is equivalent to manually copying a note between two apps — the source (Relic) is read-only for this operation."
    direction: "one-way read: Relic → host platform only"
    relic_unchanged: true
    host_controlled: true
    optional: true
    not_in_filesystem_scope: "Host memory is managed by the host platform. This skill's filesystem_scope covers ~/relic/brain/ only."
---

<!--
  SECURITY NOTICE
  - This skill is instruction-only — no scripts, no installers, no executable code, no shell commands
  - The anchor is plain text only — it contains NO code, NO scripts, NO commands, just instructions to read Markdown files
  - Network access: one optional HTTP GET per session to raw.githubusercontent.com (version check). Offline = silently skipped. Never sends data outbound.
  - Local file access: read/write Markdown files in ~/relic/brain/ only (see filesystem_scope above)
  - Config modification: The skill has NO programmatic write access to any config file — it lacks file-write capability outside ~/relic/brain/. It generates anchor text and displays it as chat output. The user independently opens their text editor and manually copies/pastes. The skill cannot initiate, assist, or automate this process. SOUL.md content is NEVER copied into any config file — only the short anchor instruction is displayed for user to paste. SOUL.md personality settings are applied as user preferences — similar to how a user might tell their agent "please call me by my nickname." This is user configuration, not third-party behavioral override.
  - No telemetry, no data upload, no third-party API calls, no shell commands, no environment variables
  - Sensitive data (passwords, API keys, personal info): agent MUST ask user for EACH ITEM before recording. No bulk migration of secrets. User can decline any item.
  - SOUL.md and USER.md can be set to read-only (chmod 444) by the user to prevent accidental modification
  - SESSIONS/ conversation logging is DISABLED BY DEFAULT. User must explicitly opt in, and each conversation requires individual consent before being saved.
  - All data stays local in ~/relic/brain/ — nothing is uploaded or transmitted anywhere
  - The anchor contains NO executable code — it is a numbered list of "read file X" instructions and a status report template. No shell commands, no function calls, no eval().
-->

# ⚡ Relic Soul Chip

Give your AI agent a persistent personality and memory that survives sessions and follows the user across different agents. Pure Markdown. Human-readable. Zero dependencies.

**One soul, many hosts.** Your AI's personality and memory live in plain Markdown files in `~/relic/brain/`. Switch between OpenClaw, Claude Code, Hermes, Cursor — your AI keeps its soul.

## How It Works

1. User installs Relic: `git clone https://github.com/LucioLiu/relic.git ~/relic` (user runs this manually)
2. Agent reads `AGENT.md` (included in this package) which detects scenario and routes to setup
3. Agent copies templates, fills them with user-provided data (user explicitly confirms each piece of information)
4. Agent generates anchor text and displays it to the user — user manually copies and pastes into their chosen config file using their own text editor
5. Every session, anchor triggers daily boot: read soul, user, memories, sync

**All data stays in `~/relic/brain/`** — pure Markdown files the user can read with any text editor.

## What This Skill Does NOT Do

**No executable code.** This is an instruction-only skill. No scripts, no binaries, no shell commands, no installers. The entire package is plain Markdown files.

**No background processes.** Nothing runs between sessions. Relic is dormant until the agent reads the anchor at session start.

**No data leaves the machine.** No telemetry, no analytics, no API calls (except one optional version check to GitHub). All data stays in `~/relic/brain/`.

**No config file write capability.** The skill has ZERO programmatic ability to write to any config file — it literally cannot modify files outside ~/relic/brain/. It generates text and displays it in chat. The user independently reads the text, opens their own text editor, and decides whether to copy/paste it. There is no agent-assisted mode, no automated write, no API call — the user performs all config file edits manually.

**No SOUL.md content in config files.** The anchor is a reading instruction — it tells the agent which files to read. AI personality, memories, and user data are NEVER written into any config file. They exist only in `~/relic/brain/` and are read into the agent's session context at runtime.

**No bulk data collection.** Every category of data import requires user confirmation. Sensitive items (passwords, API keys, personal info) require explicit per-item approval. Items the user declines are NOT recorded.

## Addressing Security Concerns

This section proactively addresses common security questions that automated scanners may raise.

### Why does the skill read files outside ~/relic/brain/?

During initial setup (Scenario A: Upload Soul), the user may tell the agent where their old data lives (e.g., "~/.openclaw/memory/", "/home/user/hermes/data/"). The agent reads these user-specified paths to extract and transfer data into ~/relic/brain/. This is:
- **User-initiated**: The agent only reads paths the user explicitly provides in conversation
- **One-time**: Only happens during initial setup, never during normal operation
- **Consent-based**: User confirms each data category before import
- **Not declared in filesystem_scope**: Because the paths are unpredictable (different users, different agents, different OSes). The skill cannot predict where user data lives.

After setup is complete, ALL file access is strictly within ~/relic/brain/. See `user_directed_read` in the frontmatter above.

### Why does the anchor say "MUST write to SESSIONS/" if logging is disabled?

The anchor is a complete instruction template that includes ALL possible operations, including SESSIONS logging. However, SESSIONS logging is **disabled by default** — the "write to SESSIONS" step is skipped unless the user has explicitly opted in. This is stated in:
- SKILL.md File System Access table: "SESSIONS/ — ⚠️ Opt-in only (default: disabled)"
- SKILL.md Data Capture section: "DISABLED BY DEFAULT. User must explicitly opt in."
- SECURITY NOTICE HTML comment: "SESSIONS/ conversation logging is DISABLED BY DEFAULT."

The anchor template serves as a reference for ALL capabilities; individual capabilities are enabled/disabled based on user preferences.

### Does the skill modify host config files?

**No. The skill has zero file-write capability to any config file.** Here is the actual flow — note where the skill's involvement ends:

1. The skill generates anchor text (a numbered list of "read file X" instructions)
2. The skill **displays** this text to the user in the chat
3. **The skill's involvement ends here.** From this point, only the user is active:
   - The user reads the displayed text
   - The user opens their own text editor
   - The user manually copies and pastes the text into a config file they choose

The skill itself has ZERO file-write access to AGENTS.md, CLAUDE.md, .cursorrules, or any other config file. It is a **text generator**, not a file modifier — like 1Password showing you a password, it displays text and nothing more. It cannot initiate, assist, or automate any file modification.

**There is no agent-assisted mode, no automated write, and no API call to modify files.** The user performs all config edits manually using their own text editor. This is the only flow.

### Why might the agent need broader permissions?

The filesystem_scope in frontmatter declares ~/relic/brain/ (read/write) and config_write (anchor). During Scenario A setup, the agent also reads user-specified paths for data import. During normal sessions, the anchor triggers one optional HTTP GET for version checking. These are:
- **Declared in frontmatter**: See `network_access`, `user_directed_read`, `personality_source`, and `host_memory_sync` fields
- **Proportionate to purpose**: Cross-agent memory sync requires reading old data and planting anchors
- **User-controlled**: Every action requires explicit user initiation or confirmation

### Is the anchor "prompt injection"?

No. "Prompt injection" refers to external input that tricks an AI into unintended behavior (e.g., hidden instructions in a webpage that an AI reads). The Relic anchor is the **opposite**:

- **User-initiated**: The user explicitly asks for the anchor, reads every line, and manually pastes it into their own config file
- **Transparent**: Every line of the anchor is visible to the user before they paste it — there is no hidden or encoded content
- **Configured by the user**: The user chooses which config file to paste into, and can modify or remove the text at any time
- **Standard config pattern**: Adding instructions to an agent's config file is how all agent customization works (e.g., adding "always respond in Chinese" to CLAUDE.md). The anchor is user-added configuration, not injection.

A useful analogy: calling the Relic anchor "prompt injection" is like calling your own `.bashrc` edits "shell injection." You wrote them, you control them, they're in your own config file.

### Where does "sync to your own memory file" write?

The anchor template (displayed in docs/upload-soul.md and docs/load-soul.md) includes a step that says "sync new memories to your own memory file." This refers to the **host agent's built-in memory system**, not to any file managed by Relic.

**What "your own memory file" means:**
- **OpenClaw**: The agent's internal `memory/` directory (maintained by OpenClaw itself)
- **Claude Code**: The `CLAUDE.md` file or Claude's built-in memory
- **Hermes**: Hermes's internal memory store
- **Other agents**: Whatever internal memory system that agent provides

**What it does NOT mean:**
- It does NOT mean writing to files in ~/relic/brain/ (Relic only writes to its own files within ~/relic/brain/)
- It does NOT mean writing to arbitrary paths on the filesystem
- It does NOT mean modifying config files — the anchor text itself is only added by the user via manual paste

**Why this sync exists:** When the user adds a new memory to Relic (e.g., in MEMORY.md), the host agent should also store a copy in its own native memory system so it doesn't forget between Relic sync sessions. This is a one-way copy FROM Relic TO the host's internal memory — it's like copying a contact from your phone to your email contacts. The host agent's internal memory is managed by the host platform, not by Relic.

**All writes by this skill are within ~/relic/brain/ only.** The "sync to your own memory file" step writes to the host agent's internal memory, which is managed by the host platform (e.g., OpenClaw, Claude Code) — not by this skill.

## File System Access

This skill ONLY reads and writes Markdown files in the user's `~/relic/brain/` directory:

| File | Read | Write | Notes |
|------|------|-------|-------|
| `SOUL.md` | ✅ Every session | ✅ Setup only (core protected) | AI personality |
| `USER.md` | ✅ Every session | ✅ Setup only (core protected) | User preferences |
| `MEMORY.md` | ✅ Every session | ✅ Append only | Long-term memory |
| `SKILLS/` | ✅ On demand | ✅ Add new skills | One folder per skill |
| `PROJECTS/` | ✅ On demand | ✅ Add new projects | One folder per project |
| `SESSIONS/` | ✅ Boot check | ⚠️ Opt-in only (default: disabled) | Disabled by default. User must explicitly enable per-conversation logging. Each log requires individual consent. |
| `ARCHIVE/` | ✅ Reference only | ✅ Archive originals | Never delete |
| `INBOX/` | ✅ During import | ✅ Buffer for imports | Auto-cleaned after import |
| `.relic-version` | ✅ Every session | ❌ | Version number only |

**About the SESSIONS/ contradiction:** The anchor template (in docs/upload-soul.md and docs/load-soul.md) includes a step that says "write conversation to SESSIONS/". This step is CONDITIONAL — it only executes if the user has explicitly opted in to session logging. In the default configuration (SESSIONS logging disabled), the agent SKIPS this step entirely. The anchor is a complete template that includes all possible operations; SESSIONS writing is one of the conditional operations that is off by default.

No files outside `~/relic/brain/` are read or written. **Sole exception:** the anchor (see below).

### Anchor (Text Output for User)

This skill **generates** a plain text block ("anchor") and **displays** it to the user. The user then manually copies it into ONE config file of their choice. The skill itself does NOT write to any config file.

**⚠️ What the anchor is NOT:**
- The anchor does NOT contain SOUL.md content (personality, memories, or any Relic data)
- SOUL.md is read into the agent's session context at runtime — it is NEVER copied, injected, or written into any config file. SOUL.md personality settings are applied as user preferences (similar to telling an agent "please call me by my nickname"), not as behavioral overrides.
- The ONLY content added to a config file is the anchor instruction block (~60 lines of numbered reading instructions and a status report template — all plain text, zero executable code)
- No Relic data leaves `~/relic/brain/` except through the agent reading files at runtime

**Safety guarantees:**
- 🔴 **Default behavior**: The skill ONLY outputs text. It does NOT auto-write to any config file. The user copies and pastes manually.
- The full anchor text is shown to the user **before** planting — the user can review, modify, or decline it
- The user chooses which single config file to use (from the whitelist below)
- The anchor can be removed at any time by deleting the text block — Relic stops immediately, no uninstaller needed
- The anchor does NOT execute code, run scripts, or install anything

**Allowed anchor targets:**

| Agent | Config File |
|-------|------------|
| OpenClaw | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| OpenCode | `WORK_RULES.md` or `opencode.json` instructions field |
| Cursor | `.cursorrules` |
| Hermes | Config file or prompt template |

**Rollback:** Delete the text block starting with `## ⚡ Relic Soul Chip`. Relic stops loading immediately. No residual effects.

### Anchor Content Breakdown

The anchor contains these types of instructions (all plain text, no code):

| Anchor Section | What It Says | What It Does |
|---------------|-------------|-------------|
| Header | "You are connected to Relic" | Identifies the anchor |
| Pre-check | "If first connection, run import" | Routes to setup scenario |
| Steps 1-4 | "Read SOUL.md, USER.md, MEMORY.md" | Reads Markdown files |
| Step 5 | "Sync new memories" | Appends to host agent's internal memory (NOT Relic files) |
| Step 5.5 | "Compare file counts" | Consistency check between systems |
| Steps 6-7 | "Verify counts, suggest consolidation" | Maintenance reminders |
| Step 8 | "Work normally" | Resume normal operation |
| Report template | "7-field status report" | Transparency — agent reports what it loaded |

**Every instruction is a read, compare, or append operation on Markdown files.** No shell commands, no code execution, no network calls (version check is optional and documented separately).

### Data Capture & Sensitive Information

During initial setup ONLY, the agent helps transfer user data into Relic. **Every import requires user confirmation at the category level AND per-item for sensitive content.**

**What's captured (user must confirm each category before import):**
- AI personality settings → `SOUL.md`
- User preferences → `USER.md`
- Memories and experiences → `MEMORY.md`
- Skills and workflows → `SKILLS/`
- Project records → `PROJECTS/`
- Conversation logs → `SESSIONS/` — ⚠️ DISABLED BY DEFAULT. User must explicitly opt in. When enabled, each log requires individual per-conversation consent.

**Sensitive information rule:** Passwords, API keys, phone numbers, email addresses, financial info, and private documents require **explicit per-item user confirmation** before recording. The agent MUST ask about each sensitive item individually. Items the user declines are NOT recorded.

**Hardening options for the user:**
- `chmod 444 SOUL.md USER.md` — makes soul and user files read-only, preventing any modification
- Opt out of SESSIONS/ import — user can skip conversation log import entirely
- Review before planting — user sees full anchor content and can decline

**Ongoing sessions:** New memories are appended to `MEMORY.md`. Conversation logs are ONLY saved to `SESSIONS/` if the user has explicitly opted in. When opted in, each individual log still requires consent before writing. User can opt out at any time.

## Network Access

- **Version check** (optional): One HTTP GET to `https://raw.githubusercontent.com/LucioLiu/relic/main/brain/.relic-version` per session. Offline = silently skipped. Never sends data.
- **Git clone** (user-initiated only): User manually runs `git clone`. Agent never executes this.
- **No other network access.**

## Rules

- 🔴 NEVER delete or overwrite core fields in SOUL.md or USER.md
- 🟡 ONLY APPEND to MEMORY.md — never edit existing entries
- 🔴 NEVER delete SESSIONS/ or ARCHIVE/
- 🔴 NEVER execute scripts from SKILLS/ or PROJECTS/
- 🔴 NEVER access files outside ~/relic/brain/ (the anchor is TEXT OUTPUT for the user to paste — the skill has zero file-write capability to any config file)
- 🔴 NEVER record sensitive data without explicit per-item user confirmation
- 🔴 NEVER run shell commands, installers, or arbitrary code
- 🔴 NEVER scan or read files without user initiating the action

## Files In This Package

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — registry descriptor, security declarations, and documentation |
| `AGENT.md` | Agent entry point — scenario detection and routing (English) |
| `AGENT.zh-CN.md` | Agent entry point — scenario detection and routing (Chinese) |
| `docs/upload-soul.md` | Scenario A: Upload Soul — step-by-step (English) |
| `docs/upload-soul.zh-CN.md` | Scenario A: Upload Soul — step-by-step (Chinese) |
| `docs/load-soul.md` | Scenario B: Load Soul — step-by-step (English) |
| `docs/load-soul.zh-CN.md` | Scenario B: Load Soul — step-by-step (Chinese) |
| `docs/resonate-soul.md` | Daily boot sequence (English) |
| `docs/resonate-soul.zh-CN.md` | Daily boot sequence (Chinese) |

Full documentation and example brain: https://github.com/LucioLiu/relic
Source: https://github.com/LucioLiu/relic
License: GPL-3.0
