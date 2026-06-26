# Workspace Hygiene Skill

Auto-maintains workspace cleanliness. Prevents context bloat that burns tokens on every session boot.

## Triggers
- Cron: runs daily at 06:00 Europe/Berlin
- Manual: when Zinou says "clean up", "audit workspace", "hygiene check"
- Auto: after any session that creates 10+ files

## Rules

### 1. BOOT FILE SIZE LIMITS (hard limits, enforce or trim)
- AGENTS.md: max 50 lines
- MEMORY.md: max 80 lines
- STATE.md: max 60 lines
- SOUL.md: no limit (identity, changes rarely)
- USER.md: max 40 lines
- IDENTITY.md: max 30 lines
- TOOLS.md: no limit (reference, not loaded often)
- HEARTBEAT.md: max 20 lines

If any file exceeds its limit:
1. Identify bloat (action logs, duplicate info, stale references)
2. Move old content to `memory/archive/YYYY-MM-DD-<topic>.md`
3. Leave a 1-line pointer: `See archive/YYYY-MM-DD-<topic>.md`
4. Log the trim in today's daily note

### 2. ROOT WORKSPACE RULES
- NO image/video files in workspace root → `archive/frames/` or `archive/media/`
- NO package.json/package-lock.json in root (belongs in subprojects)
- NO temp scripts in root → `/tmp/` for those
- NO .secrets in root → always in `talonforge/.secrets/`
- Only .md files and directories allowed in workspace root

### 3. MEMORY/ RULES
- Only keep files actively needed this week
- Daily notes older than 3 days → archive (except today's)
- Stale files (not updated in 7+ days, not referenced by STATE.md) → archive
- Fragment daily notes (multiple per day) → consolidate into one
- `claude-task.md` → archive when >7 days stale, keep latest 500 lines
- Never delete, always archive to `memory/archive/`

### 4. AUTO-ARCHIVE PATTERNS
After any session:
- If temp files created in `/tmp/` → leave them (auto-cleaned)
- If files created in workspace root → move to proper location
- If memory/ grows past 10 active files → audit for archiving

### 5. BLOAT SIGNALS (check for these)
- MEMORY.md action log >5 entries → consolidate to archive
- Same info in 2+ files → keep one, archive the other
- Files with "TODO" or "DRAFT" older than 3 days → flag or archive
- Empty files (<10 bytes) → delete
- Duplicate daily notes → merge

### 6. ARCHIVE STRUCTURE
```
memory/archive/
  action-log-day1-3.md
  day3-fragments/
  frames/
  media/
  <date>-<topic>.md
```

### 7. REPORT FORMAT
After each run, log to today's daily notes:
```
## Workspace Hygiene (HH:MM)
- Trimmed: X files, Y lines removed
- Archived: Z files
- Boot load: N lines (was M lines)
- Status: CLEAN / NEEDS ATTENTION
```

## Cron Setup
Run: `0 6 * * *` (daily at 06:00 Europe/Berlin)
This is a lightweight check — most days it does nothing. Only acts when bloat exists.