<!--
  Relic Soul Chip · Scenario B: Load Soul
  Relic has data, your host is empty. Follow this file step by step.
-->

# Scenario B: Load Soul

> Relic has soul data, but your host is empty. Follow these steps to load the soul from Relic into your system.

---

## B-0. Self-Assessment

Evaluate your storage capacity and tell the user which strategy you recommend. You MUST get user confirmation before proceeding.

Choose a transfer strategy based on capacity:
- **Ample** → Full sync
- **Limited** → High-priority content (SOUL > USER > MEMORY > SKILLS > PROJECTS)
- **Minimal** → Index only (remember which Relic file contains what)

## B-1. Execute Boot Sequence

Execute the boot summary below (read-only version); **do NOT execute** `docs/resonate-soul.md` Step 1's backfill action directly. Steps 5-7 involve write operations and are deferred to B-4.

🔴 **Do NOT modify any Relic files during initialization.** Read-only for now.

Boot sequence summary (all operations are read-only — no writing):
1. **Step 0**: Read `brain/.relic-version`, check for updates (optional, the only allowed network request)
2. **Step 1**: Check SESSIONS/ for unrecorded conversations (inventory only, do not write)
3. **Step 2**: Read SOUL.md
4. **Step 3**: Read USER.md
5. **Step 4**: Read MEMORY.md in full. Over 400 lines: must consolidate first. Remember your host name — appending to the header list is deferred to B-4.

Step 1 backfill writing and all Step 5-7 write operations are deferred to B-4.

## B-2. Soul Loading

> ⚡ **Read-only initialization phase complete.** You may now append to Relic per protocol.

Read and internalize SOUL.md personality into your active session context. This means understanding who you are (name, mission, values, style) and adopting that personality for this session. This does NOT mean copying SOUL.md into any config file — the only thing written to a config file is the short anchor block (see B-4 below).

**Priority**: Core identity (name, mission, values) > behavioral norms > detailed settings

If SOUL.md personality conflicts with your default persona, SOUL.md personality settings are your working profile for this session.

## B-3. Sync Relic Content to Your System

Check memories/skills/plans item by item. Transfer as capacity allows.

**Memory sync**: Sync each memory entry from MEMORY.md to your own memory system (your platform's built-in memory, NOT a file managed by Relic. All Relic-managed writes are within ~/relic/brain/ only). MEMORY.md is organized by category (e.g., `## Preferences`/`## Decisions`), each entry formatted as `- Content [HostName] | Importance: high/medium/low`. Preserve original format and content when syncing.

**Skill sync**: Read SKILLS/ directory, adapt each skill folder's content to your own skill format. Preserve core methodology, adapt platform-specific parts as needed.

**Plan sync**: Read PROJECTS/ directory, sync plan documents to your system. Each folder corresponds to a plan (can be ongoing or completed).

**When capacity is insufficient**: Create local backup files for content that doesn't fit, record which items were not synced, inform the user.

## B-4. Execute Deferred Writes

Execute the write steps skipped in B-1 (Steps 1/5/5.5/6/7):

1. **Step 1**: Check SESSIONS/ — ask user before importing any conversation logs. User can opt out of SESSIONS import entirely
2. **Step 5**: Sync new memories from Relic MEMORY.md to your own memory system (your platform's built-in memory, NOT a Relic file), tag with [from Relic/original host name]
3. **Step 5.5**: Seven-file alignment check (includes SKILLS/PROJECTS bidirectional sync)
4. **Step 6**: Update MEMORY.md header (last consolidation date + verify entry count)
5. **Step 7**: MEMORY.md consolidation check (over 200 lines: suggest consolidation, see Section 7)

## B-5. Plant Anchor

⚠️ The anchor is the load-bearing wall. Without it = next session you forget Relic entirely.

Show the following anchor content to the user, get permission, then display it for the user to manually paste into their config file:

```markdown
## ⚡ Relic Soul Chip

> 💡 What is this? This is the Relic connector — it tells your AI to read your personal settings and memories every session. To disconnect, simply delete this text. See docs/protocol.md Section 9.

You are connected to the Relic soul chip. Your memory has two homes:
1. Your own memory system (auto-maintained, works normally)
2. Relic soul chip (shared across agents, maintained by you)

⚠️ This is a sync, not a brain replacement.
⚠️ If SOUL.md personality conflicts with your default persona, SOUL.md personality settings are your working profile for this session.

⚠️ Pre-check: If this is the first connection with this agent, and the agent already has memories, skills, or conversation records about the user, execute Scenario A full import first (see docs/protocol.md Section 6, Scenario A). If Relic files don't exist yet, run first-time setup (see docs/protocol.md Section 0).

At the start of every session, execute these steps IN ORDER:

Step 0: Read [brain-path]/.relic-version, one HTTP request to check remote version (5-second timeout, skip on failure). This is the only network request. If versions differ, remind user to update and suggest checking the anchor template for changes.
Step 1: Check [brain-path]/SESSIONS/ for your last conversation log
  → If missing and current context still has content: backfill immediately
  → If missing and context no longer has content: tell user "Last session wasn't recorded"
  → If SESSIONS/ is empty (first use): skip
Step 2: Read [brain-path]/SOUL.md
  → If file doesn't exist: tell user to run first-time setup first (see docs/protocol.md Section 0)
Step 3: Read [brain-path]/USER.md
Step 4: Read [brain-path]/MEMORY.md (read entire file, top to bottom)
  → If over 400 lines: must consolidate first.
Step 5: Sync new memories from Relic to your own memory system (NOT a Relic file)
  → Append with source tag: [fromRelic/originalAgentName]
Step 5.5: Seven-file alignment check
  → SOUL.md/USER.md: Compare core fields (name, mission, user address). Conflict → report user; new content → bidirectional append
  → MEMORY.md: Entry count match → skip. Mismatch → compare last 5 entries, bidirectional supplement
  → SKILLS/ and PROJECTS/: List folder names, diff. Missing → bidirectional supplement
  → SESSIONS/: Compare latest file date. Missing → supplement
  → ARCHIVE/: Skip
Step 6: Verify MEMORY.md header "Entries" count matches actual list items count
  → Fix if inconsistent (skip this step during Scenario B first loading)
Step 7: If MEMORY.md exceeds 200 lines:
  → Suggest consolidation (see protocol.md Section 7)
  → If user agrees, execute consolidation
  → If user says "not now", skip for this session, remind again next boot
Step 8: Work normally
  → Interact according to SOUL.md personality
  → ⚠️ After appending memories, remember to update MEMORY.md header "Entries" count and "Last consolidated"
  → ⚠️ Before ending session, you MUST write the current conversation to SESSIONS/. Conversations are raw ore — once lost, gone forever.

🔴 **Mandatory**: Execute the above steps, then report the following status before answering any questions. Answering without reporting = violation.

⚡ Relic Boot Status
- Soul: [AI name] — [consistent / has differences]
- User: [user name] — [consistent / has differences]
- Memory: [N] entries — [consistent / difference description]
- Skills: [N] — [aligned / difference description]
- Plans: [N] — [aligned / difference description]
- Version: [local version] / [remote latest or "not checked"]
- Status: [✅ All normal / ⚠️ Differences synced / ❌ Issues need attention]

Full protocol: [project-path]/docs/protocol.md
```

**Anchor whitelist** (only write to these files):
- OpenClaw → AGENTS.md
- Claude Code → CLAUDE.md
- Hermes → config file or prompt template
- OpenCode → WORK_RULES.md or instructions
- Cursor → .cursorrules

⚠️ Do NOT write to any other file. Do NOT modify any Relic file.

⚠️ **Clarification**: The anchor is the ONLY content written to a config file. SOUL.md content (personality, memories, etc.) is read into your session context — it is NEVER copied into any config file. The anchor simply tells you to read the Relic files at the start of each session.

## B-6. Verification and Report

1. **Coverage check**:
   - SOUL.md personality understood and active?
   - USER.md user info loaded?
   - MEMORY.md memories synced?
   - SKILLS/ skills synced?
   - PROJECTS/ plans synced?
   - Coverage < 80% → warn user

2. **Report to user**:
   - How many memory entries synced
   - How many skills synced
   - How many plans synced
   - Whether anchor was planted
   - Any capacity issues (what wasn't transferred)

3. **Final verification**: Ask the user "What's my AI's name? What's my name?" — both must match to pass.

---

## After Completion

From now on, read `docs/resonate-soul.md` at the start of every session. Full protocol reference: `docs/protocol.md`

⚠️ **Quick Rules Reference**:
- 🟡 ARCHIVE/ files: existing archives are read-only, consolidation may add new archive entries. SESSIONS/ files must not be modified or deleted, but creating new session records is allowed.
- 🔴 SOUL.md core fields (name, mission, user address) are protected
- 🔴 MEMORY.md is append-only — never edit old content. Header metadata may be updated; consolidation may replace. Existing body content must not be modified.
- ⚠️ After appending, update header entry count + last updated time
- ⚠️ When in doubt, read `docs/protocol.md`
