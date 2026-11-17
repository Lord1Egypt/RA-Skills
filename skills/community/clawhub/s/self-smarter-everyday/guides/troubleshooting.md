# Troubleshooting Guide

## Overview

Even well-configured systems encounter issues. This comprehensive troubleshooting guide covers every common failure mode of the Self-Smarter-Everyday skill, with diagnostic steps, recovery procedures, and prevention strategies. When the nightly routine doesn't fire, memory gets corrupted, prompts degrade, or performance regresses, this guide is your reference for getting things back on track.

---

## Issue 1: Cron Job Not Firing

### Symptoms

- No nightly report appears in the morning.
- No execution log for the expected date.
- The agent seems unaware that a nightly routine should have run.

### Diagnostic Steps

**Step 1: Verify cron job registration**

Check if the cron job exists in the OpenClaw configuration:

```bash
# Check openclaw.json for cron job definition
cat openclaw.json | jq '.cron.jobs[] | select(.name == "self-smarter-nightly")'
```

If nothing is returned, the cron job is not registered.

**Step 2: Check if the agent was running at 2:00 AM**

The cron can only fire if the OpenClaw Gateway is running. Check container uptime:

```bash
docker ps --filter name=finn-ubuntu --format "{{.Status}}"
```

If the container was restarted or stopped around 2:00 AM, the cron would have been missed.

**Step 3: Check gateway logs**

Look for cron-related entries in the gateway logs around the scheduled time:

```bash
# Check for cron execution attempts
docker logs finn-ubuntu 2>&1 | grep -i "cron\|self-smarter" | tail -20
```

**Step 4: Verify timezone**

Ensure the timezone in `config.json` matches your expectations:

```bash
cat skills/self-smarter-everyday/config.json | jq '.timezone'
```

### Recovery

1. **If cron job is missing:** Re-register it in `openclaw.json` or via the gateway cron management interface.
2. **If container was down:** Ensure the container has a restart policy (`--restart unless-stopped`). The next 2:00 AM run will proceed normally.
3. **If timezone is wrong:** Update `config.json` and restart the gateway to pick up the change.

### Prevention

- Add a **watchdog cron** that runs at 3:30 AM to check if the nightly report was generated. If not, it sends an alert.
- Ensure the container has a restart policy so it survives crashes and reboots.
- Test the cron job after any gateway restart.

---

## Issue 2: Memory Corruption

### Symptoms

- Nightly report shows "memory compaction failed" or "data integrity error."
- `MEMORY.md` references files that don't exist.
- Semantic search returns garbled or irrelevant results.
- Daily log files contain incomplete or corrupted content.
- The nightly routine crashes during the memory compaction phase.

### Diagnostic Steps

**Step 1: Check file integrity**

```bash
# Look for empty or zero-byte memory files
find memory/ -name "*.md" -empty

# Check for files with unusual content
find memory/ -name "*.md" -size 0

# Verify MEMORY.md references exist
grep -oP '\[.*?\]\((.*?)\)' MEMORY.md | grep -oP '\(.*?\)' | tr -d '()' | while read f; do
  [ -f "$f" ] || echo "MISSING: $f"
done
```

**Step 2: Check backup availability**

```bash
# List available backups
ls -la data/memory-compaction-backups/

# Find the most recent backup
ls -t data/memory-compaction-backups/ | head -5
```

**Step 3: Check QMD index health**

```bash
# Verify notmuch database
notmuch count '*'

# If this fails, the index needs rebuilding
```

### Recovery

**Level 1: Minor corruption (single file)**

1. Identify the corrupted file.
2. Restore from the most recent backup:
   ```bash
   cp data/memory-compaction-backups/YYYY-MM-DD/filename.md memory/
   ```
3. Re-index: `notmuch new`

**Level 2: Index corruption (search broken)**

1. Rebuild the notmuch index:
   ```bash
   rm -rf ~/.cache/notmuch/
   notmuch new
   ```
2. Verify search works: `notmuch count '*'`

**Level 3: Major corruption (multiple files)**

1. Stop the nightly routine (disable cron).
2. Restore all memory files from the most recent complete backup.
3. Rebuild the index.
4. Run the nightly routine in dry-run mode to verify.
5. Re-enable the nightly routine.

**Level 4: Catastrophic corruption (no good backup)**

1. Reconstruct MEMORY.md manually from whatever files survive.
2. Re-index surviving files.
3. Accept the data loss and establish a new baseline.
4. Review backup procedures to prevent recurrence.

### Prevention

- Always enable `backupBeforeCompact: true` in config.
- Implement atomic writes (write to temp file, then rename).
- Monitor disk space — compaction fails gracefully if space is below 50 MB.
- Run periodic integrity checks (weekly cron that validates MEMORY.md references).

---

## Issue 3: Prompt Degradation

### Symptoms

- Audit scores are declining over multiple nights despite prompt mutations.
- The agent's behavior is getting worse, not better.
- Users complain about quality decline.
- Prompt mutations are being accepted but don't produce expected improvements.

### Diagnostic Steps

**Step 1: Check prompt version history**

```bash
cd data/prompt-versions/
git log --oneline -20
```

Look at recent mutations and their fitness scores.

**Step 2: Compare current vs. baseline**

```bash
cat data/prompt-versions/baseline.json | jq '.scores'
cat data/audit-logs/$(date +%Y-%m-%d)-metrics.json | jq '.metrics'
```

**Step 3: Check for mutation accumulation**

Too many small mutations can interact in unexpected ways. Count mutations in the past 7 days:

```bash
git log --oneline --since="7 days ago" | wc -l
```

### Recovery

**Step 1: Rollback to last known good version**

```bash
cd data/prompt-versions/
# Find the last version with a good composite score
git log --oneline -20
# Revert to that version
git checkout <good-commit-hash> -- .
```

**Step 2: Reset the baseline**

If the baseline itself is stale, establish a new one from the current (post-rollback) state.

**Step 3: Reduce mutation rate**

Lower `maxMutationsPerNight` from 3 to 1. Increase `minImprovementThreshold` from 0.02 to 0.05. This makes the system more conservative.

**Step 4: Review mutation strategy**

Examine which types of mutations have been successful and which haven't. Focus future mutations on proven strategies.

### Prevention

- Implement a **circuit breaker**: if 3 consecutive mutations cause regression, pause prompt evolution for 7 days.
- Require higher fitness improvement thresholds for mutations to core behavioral rules.
- Maintain a "hall of fame" — prompt versions that achieved the best scores — and prefer reverting to those.

---

## Issue 4: Skill Conflicts

### Symptoms

- Two skills try to handle the same task, producing conflicting outputs.
- A newly created skill breaks an existing skill's workflow.
- The agent is confused about which skill to invoke.
- Skill invocation success rate drops.

### Diagnostic Steps

**Step 1: List all active skills and their triggers**

```bash
# Check available skills
ls -la skills/*/SKILL.md

# Check for overlapping trigger conditions
grep -r "when\|trigger\|use case" skills/*/SKILL.md | head -30
```

**Step 2: Check nightly report for skill-related issues**

```bash
grep -i "skill\|conflict\|overlap" data/audit-logs/$(date +%Y-%m-%d)-nightly-report.md
```

**Step 3: Review recent skill changes**

```bash
ls -lt data/skill-snapshots/versions/ | head -10
```

### Recovery

**Step 1: Identify the conflicting skills**

Determine which two (or more) skills are stepping on each other.

**Step 2: Clarify boundaries**

Update each skill's trigger conditions to be more specific and non-overlapping. Add explicit exclusion rules:

```markdown
## When NOT to use this skill
- If the task involves X, use the Y skill instead.
```

**Step 3: Retire redundant skills**

If one skill is a strict subset of another, retire the less capable one.

**Step 4: Test the resolution**

Run test scenarios that previously triggered the conflict. Verify only one skill is invoked.

### Prevention

- During skill creation, the nightly routine checks for overlap with existing skills.
- New skills include explicit "when NOT to use" sections.
- Skill assessments include a "conflict check" that scans for trigger overlap.

---

## Issue 5: Performance Regression

### Symptoms

- Composite audit score drops significantly (0.10+ in a single night).
- Specific dimension scores collapse.
- Token usage spikes without corresponding quality improvement.
- Error rate increases suddenly.

### Diagnostic Steps

**Step 1: Identify which dimension regressed**

```bash
# Compare today vs. yesterday
cat data/audit-logs/$(date -d 'yesterday' +%Y-%m-%d)-metrics.json | jq '.dimensions'
cat data/audit-logs/$(date +%Y-%m-%d)-metrics.json | jq '.dimensions'
```

**Step 2: Check for recent changes**

What changed in the last 24 hours?

- Prompt mutations applied?
- Skills created or modified?
- Memory compaction performed?
- External system changes?

**Step 3: Correlate with errors**

```bash
# Check error logs
ls -lt data/error-patterns/patterns/ | head -5
grep "error\|fail" logs/nightly-$(date +%Y-%m-%d).log | tail -20
```

### Recovery

**For prompt-related regression:**
1. Rollback to the previous prompt version.
2. Review the mutation that caused regression.
3. Add it to the "do not retry" list.

**For skill-related regression:**
1. Disable the recently created/modified skill.
2. Revert to the previous skill version.

**For environment-related regression:**
1. Check system resources: `free -m`, `df -h`, `docker stats`
2. Check external service status.
3. Restore any changed configurations.

**For memory-related regression:**
1. Restore memory files from backup.
2. Rebuild search index.
3. Check for conflicting memory entries.

### Prevention

- Run the nightly routine in dry-run mode after major changes.
- Implement canary testing: apply changes to a subset of interactions first.
- Monitor leading indicators (not just lagging ones) — a spike in retries today predicts errors tomorrow.

---

## Issue 6: Nightly Routine Takes Too Long

### Symptoms

- The nightly routine exceeds its 1-hour timeout.
- The routine is still running when the user starts their morning session.
- Resource usage during the routine impacts other services.

### Diagnostic Steps

**Step 1: Check phase durations**

```bash
# Extract phase timing from the execution log
grep "Phase.*complete\|Phase.*beginning" logs/nightly-$(date +%Y-%m-%d).log
```

**Step 2: Identify the slow phase**

Compare phase durations to expected ranges:

| Phase | Expected | Concern if > |
|-------|----------|--------------|
| Data Collection | 2-5 min | 10 min |
| Self-Audit | 3-8 min | 15 min |
| Memory Compaction | 2-5 min | 10 min |
| Prompt Evolution | 5-10 min | 20 min |
| Skill Gap Analysis | 3-7 min | 15 min |
| Reporting | 1-2 min | 5 min |

### Recovery

**Short-term:**
- Skip the slowest phase: `SELF_SMARTER_SKIP_PHASES="skill-gap-analysis"`
- Reduce fitness sample size: `promptEvolution.fitnessSampleSize: 10`
- Reduce daily log processing size: `memoryCompaction.maxDailyLogSizeKB: 250`

**Long-term:**
- Optimize the slow phase's algorithms.
- Consider running heavy phases on alternate nights.
- Upgrade VPS resources if consistently resource-constrained.

---

## Issue 7: False Positive Alerts

### Symptoms

- The system reports problems that aren't real.
- Anomaly alerts fire for normal variation.
- The nightly report contains alarming messages that don't require action.

### Diagnostic Steps

**Step 1: Review alert thresholds**

Check if thresholds are too tight for your usage patterns.

**Step 2: Analyze the alerting data**

```bash
# Count alerts over the past 30 days
grep -c "ALERT" data/audit-logs/*-nightly-report.md | tail -30
```

### Recovery

- Widen alert thresholds (e.g., change composite score alert from 0.15 drop to 0.20 drop).
- Increase the anomaly detection standard deviation multiplier from 2 to 3.
- Add a "quiet period" after known disruptive events (deployments, outages).

---

## Logging Analysis

### Log File Locations

| Log Type | Location | Retention |
|----------|----------|-----------|
| Execution logs | `logs/nightly-YYYY-MM-DD.log` | 30 days |
| Nightly reports | `data/audit-logs/YYYY-MM-DD-nightly-report.md` | Indefinite |
| Metrics JSON | `data/audit-logs/YYYY-MM-DD-metrics.json` | 90 days |
| Rollback log | `data/audit-logs/rollback-log.md` | Indefinite |
| Error patterns | `data/error-patterns/patterns/` | Indefinite |

### Useful Log Analysis Commands

```bash
# Find all errors in tonight's execution log
grep -i "error\|fail\|exception" logs/nightly-$(date +%Y-%m-%d).log

# Track composite score over the past week
for d in $(seq 7 -1 0); do
  date=$(date -d "$d days ago" +%Y-%m-%d)
  score=$(cat data/audit-logs/$date-metrics.json 2>/dev/null | jq -r '.compositeScore // "N/A"')
  echo "$date: $score"
done

# Count prompt mutations applied in the past month
cd data/prompt-versions && git log --oneline --since="30 days ago" | wc -l

# Find nights where routine took longer than 45 minutes
grep "Total duration:" logs/nightly-*.log | awk -F'm' '{if ($1 > 45) print FILENAME": "$0}'
```

---

## Emergency Procedures

### Complete System Reset

If all else fails and the self-improvement system is causing more harm than good:

1. **Disable the cron job** — stop the nightly routine immediately.
2. **Rollback all prompt changes** — revert to the initial baseline prompt.
3. **Restore memory from backup** — use the most recent known-good backup.
4. **Disable all evolved skills** — revert to the pre-evolution skill catalog.
5. **Diagnose offline** — analyze logs and data to understand what went wrong.
6. **Re-enable gradually** — start with just the self-audit phase, then add phases one at a time.

### Contact and Escalation

If the issue can't be resolved through this guide:

1. Review the nightly report for specific error messages.
2. Check the error pattern library for known issues.
3. Search the OpenClaw documentation for platform-level issues.
4. Flag the issue in the nightly report for human review.

---

## Summary

Most issues with the Self-Smarter-Everyday skill fall into a handful of categories: cron not firing, memory corruption, prompt degradation, skill conflicts, and performance regression. Each has clear diagnostic steps and recovery procedures. The key principles are: always backup before changes, version control everything, rollback quickly when things go wrong, and learn from each failure to prevent recurrence. The system is designed to be resilient — individual phase failures don't crash the entire routine, and automatic rollback protects against bad prompt mutations. But when things do go wrong, this guide provides the playbook for getting back on track quickly and safely.
