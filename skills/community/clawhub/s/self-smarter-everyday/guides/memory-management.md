# Memory Management Guide

## Overview

Memory is the agent's most valuable asset. It contains everything the agent has learned — user preferences, past decisions, error lessons, project context, relationship history, and operational knowledge. Without effective memory management, the agent's context window fills with noise, important information gets lost, and the self-improvement loop has no reliable foundation to work from.

The Self-Smarter-Everyday skill implements a tiered memory management system that automatically promotes, demotes, compacts, and archives memories based on their usage patterns, relevance, and value scores. This guide covers the complete memory management lifecycle.

---

## Tiered Storage Architecture

### Memory Tiers

The system uses four tiers of memory storage, each with different characteristics:

**Tier 1: Working Memory (Hot)**

- **Location:** In-context during sessions
- **Contents:** Current conversation, active task context, recently accessed memories
- **Size limit:** Bounded by model context window (typically 128K tokens)
- **Access speed:** Immediate (already in context)
- **Volatility:** Lost when session ends

**Tier 2: Daily Logs (Warm)**

- **Location:** `memory/YYYY-MM-DD.md` files
- **Contents:** Detailed records of each day's interactions, decisions, and events
- **Size limit:** Configurable, default 500 KB per day
- **Access speed:** Fast (file read, semantic search via QMD)
- **Volatility:** Persistent, but subject to compaction

**Tier 3: Long-Term Memory (Cool)**

- **Location:** `MEMORY.md`, `memory/*.md` topic files, `lessons/*.md`
- **Contents:** Curated high-value knowledge, lessons learned, user preferences, project summaries
- **Size limit:** No hard limit, but managed through promotion/demotion
- **Access speed:** Moderate (file read, semantic search)
- **Volatility:** Persistent, protected from automatic deletion

**Tier 4: Archive (Cold)**

- **Location:** `data/memory-compaction-backups/`, `archive/`
- **Contents:** Compacted daily logs, retired project data, historical records
- **Size limit:** Bounded by available disk space
- **Access speed:** Slow (requires decompression or deep search)
- **Volatility:** Persistent, but not actively indexed

### Data Flow Between Tiers

```
Working Memory ←→ Daily Logs ←→ Long-Term Memory ←→ Archive
     (hot)          (warm)           (cool)            (cold)
```

- **Promotion:** Memory moves up (cold → hot) when accessed frequently or deemed high-value.
- **Demotion:** Memory moves down (hot → cold) when it becomes stale or low-value.
- **Compaction:** Multiple daily logs are compressed into summaries before archiving.

---

## Configuring Promotion and Demotion Thresholds

### Promotion Criteria

A memory is promoted from daily logs to long-term storage when:

1. **Value score exceeds promotion threshold** — Default: 0.7
2. **Accessed 3+ times in 7 days** — Frequently accessed memories are likely important.
3. **Referenced in a lesson learned** — Memories connected to lessons are inherently valuable.
4. **Contains user preferences or decisions** — These are almost always long-term relevant.
5. **Explicitly marked by the user** — "Remember this" always triggers promotion.

### Demotion Criteria

A memory is demoted from long-term storage to archive when:

1. **Value score falls below demotion threshold** — Default: 0.3
2. **Not accessed in 90+ days** — Stale memories that haven't been needed.
3. **Superseded by newer information** — Outdated facts replaced by current ones.
4. **Redundant with other memories** — Duplicate information consolidated.
5. **Project completed and archived** — Project-specific memories move to archive when the project ends.

### Configuring Thresholds

In `config.json`:

```json
{
  "memoryCompaction": {
    "promotionThresholdScore": 0.7,
    "demotionThresholdScore": 0.3,
    "maxDailyLogSizeKB": 500,
    "backupBeforeCompact": true,
    "accessRecencyWeight": 0.4,
    "accessFrequencyWeight": 0.3,
    "explicitMarkerWeight": 0.3
  }
}
```

**Tuning guidance:**

- **Higher promotion threshold (0.8+)** — Only the most critical memories are promoted. Long-term memory stays small and focused but may miss important context.
- **Lower promotion threshold (0.5)** — More memories are promoted. Long-term memory grows faster but provides richer context.
- **Higher demotion threshold (0.4+)** — Memories are removed from long-term storage more aggressively. Keeps long-term memory lean but risks losing useful context.
- **Lower demotion threshold (0.2)** — Memories persist longer in long-term storage. Safer but long-term memory grows continuously.

---

## Compaction Schedules

### Daily Compaction

At the end of each nightly routine, the current day's log is reviewed:

1. **Extract key events** — Identify the most important interactions, decisions, and outcomes.
2. **Generate summary** — Create a compressed summary (target: 20% of original size).
3. **Preserve lessons** — Any lessons learned are extracted to `lessons/` files.
4. **Update indices** — MEMORY.md is updated with references to new long-term memories.

### Weekly Compaction

Every Sunday night (configurable), the past week's daily logs are further compacted:

1. **Merge daily summaries** — Seven daily summaries are combined into one weekly summary.
2. **Extract trends** — Patterns across the week are identified and recorded.
3. **Promote/demote** — Memory tier transitions are executed based on the week's access patterns.
4. **Archive originals** — Original daily logs are moved to the archive tier.

### Monthly Compaction

On the first night of each month:

1. **Merge weekly summaries** — Four weekly summaries become one monthly summary.
2. **Update long-term indices** — MEMORY.md is reviewed and updated.
3. **Prune long-term memory** — Memories below the demotion threshold are archived.
4. **Generate monthly report** — A summary of memory changes is included in the nightly report.

---

## Namespace Design

### Memory Naming Conventions

Well-organized namespaces make memory retrieval faster and more accurate.

**Recommended namespace structure:**

```
memory/
├── YYYY-MM-DD.md              # Daily logs (auto-generated)
├── projects/
│   ├── {project-name}.md      # Project-specific context
│   └── ...
├── preferences/
│   ├── user-preferences.md    # User likes, dislikes, habits
│   └── workflow-preferences.md
├── people/
│   ├── {person-name}.md       # Contact info, relationship context
│   └── ...
├── decisions/
│   ├── YYYY-MM-{topic}.md     # Key decisions and rationale
│   └── ...
├── lessons/
│   ├── YYYY-MM-DD-{slug}.md   # Individual lesson files
│   └── ...
└── reference/
    ├── api-notes.md           # API documentation notes
    ├── infrastructure.md      # VPS, Docker, network notes
    └── ...
```

### Naming Rules

1. **Use lowercase with hyphens** — `project-name.md`, not `ProjectName.md`
2. **Include dates when temporal** — `2026-08-10-decision.md`, not `decision.md`
3. **Use descriptive slugs** — `docker-deploy-traefik-fix.md`, not `fix.md`
4. **Avoid special characters** — letters, numbers, hyphens only
5. **Keep filenames under 60 characters** — for filesystem compatibility

---

## Conflict Resolution Strategies

### Types of Memory Conflicts

**1. Contradictory Information**

Two memories contain conflicting facts. Example: one memory says "User prefers dark mode" and another says "User switched to light mode."

**Resolution:** The most recent memory wins. The older memory is updated with a note: "Superseded by [date] memory — user switched to light mode."

**2. Duplicate Information**

The same fact exists in multiple memory files.

**Resolution:** Consolidate to a single authoritative location. Other locations receive a pointer: "See [authoritative location] for current information."

**3. Stale References**

A memory references something that no longer exists — a file path that was moved, a person who left, a project that ended.

**Resolution:** Mark as stale with timestamp. Move to archive if not accessed in 30 days. If the reference is critical (e.g., a file path used in automation), flag for human review.

**4. Scope Overlap**

Two memory files cover overlapping topics, making it unclear which one to consult.

**Resolution:** Merge into a single file with clear sections. Update all references to point to the merged file.

### Conflict Detection Algorithm

During nightly compaction, the system scans for conflicts:

1. **Semantic similarity scan** — Embeddings-based comparison to find memories discussing the same topic.
2. **Entity extraction** — Identify named entities (people, projects, URLs, file paths) and check for contradictions.
3. **Temporal ordering** — When contradictions are found, use timestamps to determine which is current.
4. **Confidence scoring** — If temporal ordering doesn't resolve the conflict (same timestamp), flag for human review.

---

## Backup Procedures

### Backup Strategy

Memory data is backed up before every compaction operation. The backup strategy follows the 3-2-1 rule adapted for agent memory:

- **3 copies** — active memory, backup before compaction, weekly archive
- **2 media** — filesystem + git repository (for long-term memories tracked in version control)
- **1 offsite** — optional: push memory git repository to a remote for disaster recovery

### Backup Execution

```bash
# Before compaction, create a timestamped backup
BACKUP_DIR="data/memory-compaction-backups/$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

# Backup daily logs
cp memory/2026-08-10.md "$BACKUP_DIR/"

# Backup long-term memory index
cp MEMORY.md "$BACKUP_DIR/"

# Backup lessons
cp -r lessons/ "$BACKUP_DIR/lessons/"

# Record backup metadata
echo '{"date": "2026-08-10", "files": 12, "totalSizeKB": 847}' > "$BACKUP_DIR/metadata.json"
```

### Backup Retention

- **Daily backups:** Retained for 14 days
- **Weekly backups:** Retained for 8 weeks
- **Monthly backups:** Retained indefinitely

---

## Recovery from Corruption

### Signs of Memory Corruption

- Daily log files contain garbled or incomplete content
- MEMORY.md references files that don't exist
- Semantic search returns nonsensical results
- QMD index is out of sync with actual files
- Nightly routine crashes during memory compaction phase

### Recovery Procedures

**Procedure 1: Restore from Backup**

```bash
# Find the most recent good backup
ls -la data/memory-compaction-backups/

# Restore the specific corrupted file
cp data/memory-compaction-backups/2026-08-09/MEMORY.md MEMORY.md

# Re-index with notmuch (if using QMD)
notmuch new
```

**Procedure 2: Rebuild Index**

If the QMD index is corrupted but the source files are intact:

```bash
# Delete and rebuild the index
rm -rf ~/.cache/notmuch/
notmuch new
```

**Procedure 3: Partial Recovery**

If only part of a memory file is corrupted:

1. Open the backup version and the current version side by side.
2. Identify the corrupted section.
3. Manually merge the good parts of both versions.
4. Save the merged version and re-index.

**Procedure 4: Nuclear Option**

If corruption is widespread:

1. Stop the nightly routine (disable cron).
2. Restore all memory files from the most recent complete backup.
3. Re-index everything.
4. Run the nightly routine in dry-run mode to verify.
5. Re-enable the nightly routine.

### Prevention

- **Always backup before compaction** — the `backupBeforeCompact` config option should always be `true`.
- **Validate file integrity** — the nightly routine checks file checksums before and after compaction.
- **Use atomic writes** — memory files are written to a temp file first, then renamed, preventing partial writes.
- **Monitor disk space** — compaction fails gracefully if disk space is below 50 MB.

---

## Summary

Memory management is the foundation of effective self-improvement. Without well-organized, properly curated memories, the agent can't learn from its past. The tiered storage system keeps hot memories accessible while archiving cold ones. Promotion and demotion thresholds ensure the right information is in the right place. Compaction schedules prevent unbounded growth. Conflict resolution keeps memories consistent. And backup procedures ensure nothing is permanently lost. Invest time in tuning these parameters for your specific usage patterns — the quality of memory management directly impacts the quality of self-improvement.
