<!--
  Relic Soul Chip · Scenario A: Upload Soul
  Your host has memories, Relic is empty. Follow this file step by step.
-->

# Scenario A: Upload Soul

> Your host has memories, but Relic is empty. Follow these steps to upload your soul, memories, and skills into Relic.
>
> ⚠️ Relic works best with 32K+ context, high-quality models. Models with very small context or low quality cannot follow this process correctly.
>
> 📖 This is the detailed standalone guide for Scenario A. The canonical protocol definition is in `docs/protocol.md` (Scenario A section, 10 steps). Step numbering differs between this guide and the protocol — follow **this guide** when executing Scenario A.

---

## Seven Memory Categories

Check every item before starting. All are mandatory:

1. ☐ `SOUL.md` — Soul (who am I)
2. ☐ `USER.md` — User (who are you)
3. ☐ `MEMORY.md` — Memory (preferences, decisions, experiences)
4. ☐ `SKILLS/` — Skills (learned abilities)
5. ☐ `PROJECTS/` — Plans (ongoing or completed plans)
6. ☐ `SESSIONS/` — Sessions (raw conversation logs)
7. ☐ `ARCHIVE/` — Archive (historical backups)

> "No data" ≠ "skip allowed" → must report "Category N: 0 items". Omitting any category is forbidden; fabricating data is forbidden.

## Red Line Quick Reference

| Step | Key Action | Red Line |
|------|-----------|----------|
| Inventory | Ask user what data they have to import, **act only on user instructions** | Do NOT scan or read files without user permission |
| SOUL | **Copy original text directly**, do NOT summarize or rewrite | Compressing details = violation |
| MEMORY | Preference/decision preserve verbatim, experience can condense | Losing key params = violation |
| SKILLS | Import all skill files, one folder per skill, no source restriction | Empty folders with no content ≠ skill |
| SESSIONS | Ask user for old conversation locations, preserve in full | Current session ≠ old conversation |
| PROJECTS | Ask user what to import per plan, folders with substantive content | Title + one line = not acceptable |
| Report | Report all 7 categories item by item, include "0 items" | Omitting any category = failure |
| Sensitive | Already in old host = transferable (tag "verified source"), new discovery = must ask user | |

---

## Step 1: Inventory — Ask User What Data They Have

🔴 **First**: Ask the user: "What data do you have that you want to import into Relic?" List ONLY what the user tells you — do NOT scan or read any files without user permission:
- Soul settings (N items), User preferences (N items), Memories (N entries), Skill files (N), Conversation files (N), Plan files (N), Archive files (N)
- Also list the data source locations (e.g., "~/.openclaw/workspace/memory/ has 42 files")

🔴 **Then**: Show the list to user and ask two questions:
1. "Above is all the old data I found. Import everything? Or would you like to be selective?"
2. "Are there any data sources I can't access that you'd like to add? (e.g., local files, exports from other platforms)"

If a category genuinely has no content, report "Category N: 0 items (no old data)" — never omit, never fabricate.
⚠️ Must wait for user confirmation before starting.

✅ **Completion Check**: All 7 categories listed with quantities? User confirmed? Any category skipped? (Skipped = failure)

## Step 2: SOUL + USER + MEMORY

### 2a. Initialize Files

Copy templates to active files:
```
SOUL.template.md → SOUL.md
USER.template.md → USER.md
MEMORY.template.md → MEMORY.md
```
Template files (.template.md) remain as backups. Also create directories if they don't exist: `SKILLS/`, `PROJECTS/`, `SESSIONS/`, `ARCHIVE/`, `INBOX/`

### 2b. Fill in SOUL.md and USER.md

⚠️ Must be as complete as possible — do NOT shortcut by only filling the name. If user has AI settings/role definitions/prompts from other platforms, ALL must be migrated.

🔴 **SOUL.md Fidelity Iron Rule**:
- If old host has a complete soul definition file, **copy the original text directly** — do NOT summarize or rewrite
- Only restructure when old content cannot directly map to template fields
- When restructuring, preserve ALL detail descriptions — do NOT compress into summaries
- Content that doesn't fit the template goes in "Other" section or file end — **NEVER discard**
- Original files MUST be archived to `ARCHIVE/raw/` for cross-reference

### 2c. Import Memories → MEMORY.md

⚠️ Raw source files are the fidelity baseline. Format conversion is refinement, not compression.

1. Place old agent's memory files into `INBOX/`
2. Append to `MEMORY.md` in Relic's new category-based format: under each category heading, add lines of the form:
   `- memory content [hostname] | Importance: high/medium/low`
3. Fidelity rules:

- Preference / Decision / Correction → preserve verbatim
- Experience → can condense, but key parameters must not be lost
- Event → can summarize
- Mood → can compress context

⚠️ When in doubt, preserve verbatim. Lost data cannot be recovered.

4. Ask user about sensitive information (see "Sensitive Information" below)
5. Sort by category order, not by timestamp
6. After writing, review MEMORY.md: ensure category sections exist and entries count per category is tracked

✅ Completion Check: MEMORY.md entries exist for each category and counts reflect actual entries

## Step 3: SKILLS + PROJECTS

### 3a. Import Skills → SKILLS/

⚠️ Format requirement: One folder per skill, with at least one `.md` description file inside.
```
SKILLS/debugging-workflow/README.md  ✅
SKILLS/installed-skills.md           ❌ (this is a list, not a skill)
```

Steps:
1. Ask the user: "What old skills/workflows/templates do you have that need importing? Tell me the content or file locations."
2. If the user provides a skill list: create one folder per skill, each with a README.md inside
3. If the user provides files: move them into corresponding folders, preserving original content

Filter rules:
- Bring: all skills/workflows/templates, including platform-specific tools
- Unsure: ask user. For mixed content, bring only methodology part.

No content → report "SKILLS/: 0 items (no old data)".

✅ Completion check: Does SKILLS/ contain multiple folders? Are there any flat single files (if so, split into folders)?

### 3b. Import Plans → PROJECTS/

⚠️ One folder per plan. Folders must have substantive content, not just a one-line summary.

Steps:
1. Collect all plan names from memories and conversations (based on user-provided information)
2. For each plan, ask the user: "What files should I import for plan [name]? Or should I just record key information?"
3. Based on user response and plan portability:
    - No special environment dependency → move actual files (not just README)
    - Partial dependency → move generic files, text descriptions for platform-specific
    - Fully dependent → at minimum, write a .md record file containing:
      * Plan goal and status
      * Key decisions and architecture choices
      * Known issues and next steps
      * Related file paths (if files are outside Relic)

No content → report "Plans/: 0 items (no old data)".

✅ **Completion check**: Does each plan folder have substantive content (not just title + one line)? Has the user been asked?

## Step 4: SESSIONS + ARCHIVE

### 4a. Import Conversations → SESSIONS/

⚠️ Conversations are raw ore — must be preserved in full, never summarized.

Steps:
1. Ask the user: "Do you have old conversation logs that need importing? If so, tell me the file location or paste the content."
2. If the user provides conversation files or content:
   - Organize by `YYYY-MM/` directories
   - Preserve original content unchanged and unsummarized
   - File naming: `YYYY-MM-DD.[agent-name].md`
3. If the user confirms no old conversations:
   - Report "SESSIONS/: 0 items (user confirmed no old conversations)"
   - Still create the `SESSIONS/YYYY-MM/` directory

**Forbidden**:
- Do NOT count only the current session as "imported" — the current session is not an old conversation
- Do NOT save summaries as raw records — must be full conversations or verbatim preserved

✅ **Completion check**: Are there historical conversations imported (not just the current session)? Is SESSIONS/ directory created?

### 4b. Archive Originals → ARCHIVE/

1. Fidelity check: original vs converted, warn if compression exceeds 50%
2. Move INBOX/ source files to `ARCHIVE/raw/` (never delete)
3. Update MEMORY.md header "Entries" count and "Last consolidated" to current date

✅ **Completion check**: Are original files saved in ARCHIVE/raw/?

## Step 5: Plant Anchor

⚠️ The anchor is the load-bearing wall. Without it = next session you forget Relic entirely → no memory sync.

Explain to the user: "The anchor is a short text block in your host's config file. It ensures every new session automatically reads Relic. Think of it as a 'boot check program'."

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
Step 5: Sync new memories from Relic to your own memory system (your platform's built-in memory, e.g. OpenClaw memory/, CLAUDE.md — NOT a file managed by Relic)
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
  → Tell user "Relic memory file is large, consolidation recommended. Consolidate now?"
  → If user agrees, execute consolidation (see docs/protocol.md Section 7)
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

If user absolutely refuses, record "Anchor not planted" in MEMORY.md and explain consequences.

**Anchor whitelist** (only write to these files):
- OpenClaw → AGENTS.md
- Claude Code → CLAUDE.md
- Hermes → config file or prompt template
- OpenCode → WORK_RULES.md or instructions
- Cursor → .cursorrules

⚠️ Do NOT write to any other file. Do NOT modify any Relic file.

## Step 6: Verification

Check seven memory sections (blocking — ALL must pass):

- SOUL.md — Core mission filled? Personality complete?
- USER.md — User preferences filled?
- MEMORY.md — Imported memories exist by category? Header counts reflect actual entries?
- SKILLS/ — Imported from old host (if any)? Format correct?
- PROJECTS/ — Imported plans exist? Format correct?
- SESSIONS/ — Directory created? Old conversations imported (if any)?
- ARCHIVE/ — Directory created? Originals archived (if any)?

Any item fails → go back to that step and redo.
All pass → ask user: "What's my AI's name? What's my name?" Both must match.

Suggest read-only permissions (Mac/Linux): `chmod 444 SOUL.md USER.md`

## Step 7: Report

Must report ALL 7 categories to the user, including those with "0 items". Omitting any category is forbidden.

Report format:
```
1. Soul (SOUL.md): Imported / Already exists
2. User (USER.md): Imported / Already exists
3. Memory (MEMORY.md): N entries imported
4. Skills (SKILLS/): N imported / 0 items (no old data)
5. Sessions (SESSIONS/): N files imported / Could not retrieve old conversations
6. Plans (PROJECTS/): N imported / 0 items (no old data)
7. Archive (ARCHIVE/): N source files archived
```

---

## Sensitive Information

**Case 1: Transferring existing data** (info user already provided in old host)
- If sensitive info already exists in old host files → can transfer directly, tag with `Source: old host data`
- No need to ask user again

**Case 2: First-time recording** (new sensitive info you discover)
- 🔑 Passwords, API keys, tokens
- 📱 Phone numbers, email addresses
- 🏠 Home/work addresses
- 💳 Financial information
- 📄 Private document content
- 🧬 Info user explicitly asked to keep confidential
- Unsure which case? → Treat as first-time recording, ask user first.

---

## After Completion

Tell the user:
- Relic folder path (e.g., `~/relic/brain/`)
- The seven memory files and their purposes
- Sync principle: hosts only sync at the start of each new session. Mid-conversation switching does NOT auto-sync.
- "Conversations are raw ore — once lost, gone forever. Build the habit of having hosts write regularly."

From now on, read `docs/resonate-soul.md` at the start of every session. Full protocol reference: `docs/protocol.md`
