<!--
  Relic Soul Chip · Resonate Soul
  Author: LucioLiu · https://github.com/LucioLiu/relic
  License: GPL v3
  Format version: 1.3.2
  Read and follow this file at the start of every new session.
-->

# Resonate Soul

## Boot Sequence

**Step 0** Read `brain/.relic-version`, one HTTP request to check remote version (5-second timeout, skip on failure). This is the only network request. If versions differ, remind user to update and suggest checking the anchor template for changes (see protocol Section 9).

**Step 1** Check SESSIONS/, backfill any unrecorded conversations. Conversations are raw ore — lost = gone forever.

**Step 2** Read SOUL.md → who you are

**Step 3** Read USER.md → who the user is

**Step 4** Read MEMORY.md in full, top to bottom. >400 lines: must consolidate first.

**--- Write Phase Below ---**

**Step 5** Sync new memories from Relic to your own memory, tag with `[fromRelic/originalAgentName]`

**Step 5.5** Seven-File Alignment Check

Quickly compare all files. Sync any differences found. If sync fails, report to user.

| File | Alignment Method | On Difference |
|------|-----------------|---------------|
| SOUL.md | Compare core fields (name, mission, user address) | Conflict → report user, no auto-overwrite; new content → bidirectional append |
| USER.md | Same as above | Same as above |
| MEMORY.md | Entry count comparison (handled in Step 5) | Mismatch → compare last 5 entries, bidirectional supplement |
| SKILLS/ | List folder names, diff | Missing → bidirectional supplement |
| PROJECTS/ | Same as above | Same as above |
| SESSIONS/ | Compare latest file date | Missing → supplement |
| ARCHIVE/ | Skip | No alignment needed |

If entry counts match but you notice trailing content differs, report the difference and let the user decide. Do not auto-overwrite.

**Step 6** Update MEMORY.md header: update "Last consolidated" to current date + check entry count matches actual list items (lines starting with `- `)

**Step 7** MEMORY.md consolidation check: >200 lines → remind user to consider consolidation; >400 lines → strongly recommend consolidation. Method: move outdated experience entries to ARCHIVE/ (create new file), keep still-relevant entries. Nothing is deleted — just relocated.

**Step 8** Normal operation

## Memory Append Format

✅ `## Preferences`
- Often stays up late [AgentName] | Importance: Medium

| Type | Fidelity Requirement |
|------|---------------------|
| Preference / Decision / Correction | **Must preserve verbatim** |
| Experience | Can condense, but key parameters must not be dropped |
| Event | Can summarize |
| Mood | Can condense context |

⚠️ If unsure, preserve verbatim. Lost originals cannot be recovered.

## Before Ending Session

Write to `SESSIONS/YYYY-MM/YYYY-MM-DD.[agent-name].md`. Conversations are raw ore — lost = gone forever.

## 🔴 Key Rules Quick Reference

- 🟡 ARCHIVE/: may write new files during consolidation, never modify existing files
- 🟡 SESSIONS/: never modify or delete existing files, but may append new conversation records
- 🔴 SOUL.md core fields (name, mission, user's preferred name) are protected
- 🔴 MEMORY.md: append only, never edit existing entries. Header metadata (entry count, last consolidated date) may be updated; consolidation flow may replace full file. All existing body content remains immutable.
- ⚠️ After appending, update header "Entries" count and "Last consolidated"
- ⚠️ When in doubt, read docs/protocol.md
