# Getting Started with Self-Smarter-Everyday

## Overview

The **Self-Smarter-Everyday** skill transforms your AI agent into a continuously self-improving system. Every night at 2:00 AM local time, the agent wakes up, reflects on the day's interactions, audits its own performance, compacts its memory, evolves its prompts, and identifies skill gaps — all autonomously. By morning, the agent is measurably better than it was the night before.

This guide walks you through everything you need to get up and running, from prerequisites to your first successful nightly cycle.

---

## Prerequisites

Before installing this skill, make sure your environment meets the following requirements:

### Software Requirements

- **OpenClaw Gateway** version 0.2026.06 or later — the skill relies on the cron scheduler and memory subsystem introduced in this version.
- **Node.js** v20 or later (v24 LTS recommended).
- **Git** 2.40+ — prompt versions and skill snapshots are tracked in a local git repository.
- **Python 3.11+** — some analysis scripts use Python for token counting and statistical evaluation.
- **jq** — used for JSON manipulation in audit reports.

### Workspace Requirements

- A functioning `~/.openclaw/workspace/` directory with at least the following files:
  - `AGENTS.md` — agent operating rules
  - `SOUL.md` — agent persona definition
  - `MEMORY.md` — memory index file
- At least **500 MB of free disk space** — memory archives, audit logs, and prompt version history accumulate over time.
- Write access to the workspace directory for the agent runtime user.

### Existing Skills (Recommended)

While not strictly required, the following skills enhance the self-improvement loop:

- **self-improving** — provides the foundational self-correction memory structure.
- **proactivity** — enables the agent to take initiative based on patterns it discovers.
- **aar-loop** — After Action Review loop for structured post-task reflection.

If you don't have these installed yet, the nightly routine will still work but may produce less nuanced improvements.

---

## Installation Step-by-Step

### Step 1: Create the Skill Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/guides
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/scripts
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/templates
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/data/audit-logs
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/data/prompt-versions
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/data/skill-snapshots
mkdir -p ~/.openclaw/workspace/skills/self-smarter-everyday/data/memory-compaction-backups
```

### Step 2: Copy Skill Files

Place the `SKILL.md` file in the skill root directory. Copy all guide files into the `guides/` subdirectory. Copy analysis and automation scripts into `scripts/`.

### Step 3: Initialize the Git Repository for Prompt Versioning

```bash
cd ~/.openclaw/workspace/skills/self-smarter-everyday/data/prompt-versions
git init
git config user.email "agent@local"
git config user.name "Self-Smarter Agent"
echo "# Prompt Version History" > README.md
git add README.md
git commit -m "Initial commit: prompt version repository"
```

### Step 4: Create the Configuration File

Create `~/.openclaw/workspace/skills/self-smarter-everyday/config.json` with the following structure:

```json
{
  "nightlyRunHour": 2,
  "nightlyRunMinute": 0,
  "timezone": "Asia/Jakarta",
  "enableSelfAudit": true,
  "enableMemoryCompaction": true,
  "enablePromptEvolution": true,
  "enableSkillGapAnalysis": true,
  "enableErrorPatternLearning": true,
  "auditScoringWeights": {
    "accuracy": 0.30,
    "tokenEfficiency": 0.20,
    "responseTime": 0.15,
    "errorRate": 0.20,
    "userSatisfaction": 0.15
  },
  "memoryCompaction": {
    "maxDailyLogSizeKB": 500,
    "promotionThresholdScore": 0.7,
    "demotionThresholdScore": 0.3,
    "backupBeforeCompact": true
  },
  "promptEvolution": {
    "maxMutationsPerNight": 3,
    "fitnessSampleSize": 20,
    "rollbackOnRegression": true,
    "minImprovementThreshold": 0.02
  },
  "reporting": {
    "writeDailyReport": true,
    "weeklySummaryDay": "Sunday",
    "reportPath": "data/audit-logs"
  }
}
```

### Step 5: Register the Cron Job

Use the OpenClaw cron scheduler to register the nightly routine. The exact mechanism depends on your OpenClaw version. Typically this is done through the gateway configuration or via the cron management interface.

The cron expression for 2:00 AM daily is:

```
0 2 * * *
```

With timezone set to your local zone (e.g., `Asia/Jakarta` for WIB).

### Step 6: Verify Installation

Run a manual test to confirm everything is wired up correctly:

```bash
# Check that the skill directory exists and has the expected structure
ls -la ~/.openclaw/workspace/skills/self-smarter-everyday/

# Verify config is valid JSON
cat ~/.openclaw/workspace/skills/self-smarter-everyday/config.json | jq .

# Verify git repo is initialized
cd ~/.openclaw/workspace/skills/self-smarter-everyday/data/prompt-versions && git log --oneline

# Check that required scripts are executable
ls -la ~/.openclaw/workspace/skills/self-smarter-everyday/scripts/
```

---

## Initial Configuration

After installation, review and adjust these settings based on your environment:

### Timezone

The default timezone is `Asia/Jakarta` (WIB, UTC+7). If your agent operates in a different timezone, update the `timezone` field in `config.json`. This is critical because the nightly routine is designed to run during low-activity hours. Running it during peak hours could interfere with active conversations.

### Resource Limits

If your agent runs on a resource-constrained VPS (less than 2 GB RAM), consider reducing the scope of the nightly routine:

- Set `enableSkillGapAnalysis` to `false` initially — this is the most resource-intensive phase.
- Reduce `promptEvolution.fitnessSampleSize` from 20 to 10.
- Set `memoryCompaction.maxDailyLogSizeKB` to 250 instead of 500.

### Audit Scoring Weights

The default weights prioritize accuracy and error rate. Adjust these based on what matters most for your use case. For example, if you're running a high-volume customer service agent, you might increase `tokenEfficiency` to reduce costs.

---

## Your First Nightly Run

Once the cron job is registered, the first nightly run will occur at the next 2:00 AM. Here's what to expect:

### Phase 1: Data Collection (approximately 2-5 minutes)

The agent gathers raw data from the day's interactions: session transcripts, memory updates, error logs, and token usage statistics. It reads the daily memory file (`memory/YYYY-MM-DD.md`) and any session logs.

### Phase 2: Self-Audit (approximately 3-8 minutes)

The agent evaluates its performance across five dimensions: accuracy, token efficiency, response time, error rate, and user satisfaction signals. Each dimension receives a score from 0.0 to 1.0. A weighted composite score is calculated.

### Phase 3: Memory Compaction (approximately 2-5 minutes)

High-value memories (score above promotion threshold) are promoted to long-term storage. Low-value or redundant memories are demoted or archived. The daily log is compressed into a summary.

### Phase 4: Prompt Evolution (approximately 5-10 minutes)

Based on audit findings, the agent proposes small mutations to its system prompts. These mutations are tested against a fitness function using sampled historical interactions. If a mutation improves fitness, it's committed to the prompt version repository. If it causes regression, it's rolled back.

### Phase 5: Skill Gap Analysis (approximately 3-7 minutes)

The agent reviews interactions where it struggled or gave suboptimal responses. It identifies patterns that suggest missing capabilities. If a gap is significant and recurring, it creates a skill creation request or updates an existing skill.

### Phase 6: Reporting (approximately 1-2 minutes)

A nightly report is generated and saved to `data/audit-logs/YYYY-MM-DD-nightly-report.md`. This report includes scores, changes made, and recommendations for human review.

**Total expected duration: 15-35 minutes** depending on the day's activity volume and resource constraints.

---

## What to Expect in the First Week

- **Night 1-2:** Baseline establishment. Scores may be moderate as the system calibrates its measurement framework. Don't be alarmed by initial scores — they're a starting point.
- **Night 3-4:** First prompt mutations appear. Small improvements in token efficiency are usually the first visible gain.
- **Night 5-7:** Memory compaction starts showing results. The agent's memory index becomes more focused. You may notice the agent referencing older interactions more accurately.

---

## Troubleshooting Common Issues

### The Cron Job Doesn't Fire

**Symptom:** No nightly report appears in the morning.

**Diagnostic steps:**
1. Check if the cron job is registered: look at the OpenClaw cron configuration.
2. Verify the timezone setting matches your expectations.
3. Check if the agent was running at 2:00 AM — if the container was stopped, the cron won't fire.
4. Look for errors in the gateway logs around the scheduled time.

**Fix:** Re-register the cron job. Ensure the container is running overnight. Consider adding a watchdog cron that checks if the nightly report was generated.

### Permission Errors During Memory Compaction

**Symptom:** Nightly report shows "memory compaction failed" with permission denied errors.

**Fix:** Ensure the agent runtime user has write access to the `memory/` directory and all subdirectories under `skills/self-smarter-everyday/data/`.

### Prompt Evolution Produces No Changes

**Symptom:** Prompt version repository shows no new commits after several nights.

**This may be normal** if the agent performed well that day and no mutations passed the fitness threshold. Check the nightly report — it should indicate whether mutations were attempted and why they were rejected.

### High Memory Usage During Nightly Run

**Symptom:** The agent container runs out of memory during the nightly routine.

**Fix:** Reduce the scope of individual phases in `config.json`. Lower `fitnessSampleSize`, reduce `maxDailyLogSizeKB`, or disable the most resource-intensive phase temporarily.

---

## Verification Steps

After the first successful nightly run, verify the following:

1. **Nightly report exists:** Check `data/audit-logs/YYYY-MM-DD-nightly-report.md` for today's date.
2. **Audit scores are present:** The report should contain scores for all five dimensions.
3. **Memory compaction ran:** Check that `memory/` files were updated and backup files exist in `data/memory-compaction-backups/`.
4. **Prompt versions are tracked:** Run `git log --oneline` in the prompt-versions directory — there should be at least one commit if mutations were applied.
5. **Skill gap analysis produced output:** The nightly report should list any identified gaps and actions taken.

If all five checks pass, your Self-Smarter-Everyday skill is fully operational. The agent will now improve itself every night while you sleep.

---

## Next Steps

Once you've confirmed the basic setup is working, explore the detailed guides for each component:

- **Nightly Routine Setup** — deep dive into cron configuration and monitoring.
- **Self-Audit Implementation** — customize what gets audited and how scores are calculated.
- **Memory Management** — fine-tune compaction thresholds and namespace design.
- **Prompt Optimization** — understand mutation strategies and fitness evaluation.
- **Skill Evolution** — learn how new skills are discovered and created.
- **Error Patterns** — build a pattern library for automatic error prevention.
- **Performance Tracking** — set up dashboards and trend analysis.
- **Integration Playbook** — connect with other skills and external systems.
- **Troubleshooting** — comprehensive reference for when things go wrong.

Welcome to continuous self-improvement. Your agent just got smarter.
