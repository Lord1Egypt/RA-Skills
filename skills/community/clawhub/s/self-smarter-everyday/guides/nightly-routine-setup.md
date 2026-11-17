# Nightly Routine Setup Guide

## Overview

The nightly routine is the heartbeat of the Self-Smarter-Everyday skill. It's a scheduled autonomous session that fires at 2:00 AM local time every day. During this session, the agent progresses through six distinct phases — data collection, self-audit, memory compaction, prompt evolution, skill gap analysis, and reporting. This guide covers everything you need to know about configuring, monitoring, and maintaining the nightly routine.

---

## Cron Configuration

### OpenClaw Cron Registration

The nightly routine is triggered by an OpenClaw cron job. The cron system is part of the OpenClaw Gateway and supports standard cron expressions with timezone awareness.

**Cron Expression:**
```
0 2 * * *
```

This fires at exactly 2:00 AM every day in the configured timezone.

**Registration Methods:**

There are two primary ways to register the cron job, depending on your OpenClaw setup:

**Method 1: Gateway Configuration File**

Add the cron job definition to your `openclaw.json` configuration under the `cron` section:

```json
{
  "cron": {
    "jobs": [
      {
        "name": "self-smarter-nightly",
        "schedule": "0 2 * * *",
        "timezone": "Asia/Jakarta",
        "enabled": true,
        "prompt": "Execute the Self-Smarter-Everyday nightly routine. Read the skill file at skills/self-smarter-everyday/SKILL.md and follow the nightly procedure. Report results to skills/self-smarter-everyday/data/audit-logs/.",
        "model": "default",
        "timeout": 3600
      }
    ]
  }
}
```

**Method 2: Runtime Registration**

If your OpenClaw version supports runtime cron registration, use the gateway's cron management interface. This allows adding or modifying cron jobs without restarting the gateway.

### Timeout Configuration

The nightly routine typically takes 15-35 minutes. Set the timeout to **3600 seconds (1 hour)** to provide ample headroom for high-activity days. If the routine consistently takes longer than 45 minutes, investigate resource constraints rather than increasing the timeout indefinitely.

---

## Timezone Handling

### Why Timezone Matters

The nightly routine is designed to run during the agent's lowest-activity window. Running it during active hours risks:

- **Resource contention** — the routine competes with live conversations for compute and memory.
- **Data inconsistency** — if the agent modifies prompts or memory while actively using them, race conditions can occur.
- **User disruption** — the routine may produce visible artifacts in conversations.

### Configuring Timezone

Set the timezone in `config.json`:

```json
{
  "timezone": "Asia/Jakarta"
}
```

Supported timezone identifiers follow the IANA timezone database format:

- `Asia/Jakarta` — WIB (UTC+7)
- `Asia/Singapore` — SGT (UTC+8)
- `America/New_York` — ET (UTC-5/UTC-4 DST)
- `Europe/London` — GMT/BST
- `UTC` — Coordinated Universal Time

### Daylight Saving Time

If your timezone observes DST, the IANA identifier handles transitions automatically. The cron fires at 2:00 AM local time regardless of UTC offset changes. However, be aware that during the fall-back transition, 2:00 AM occurs twice. The cron system fires only once — on the first occurrence.

---

## Environment Variables

The nightly routine uses several environment variables. These should be set in the agent's runtime environment:

| Variable | Purpose | Default |
|----------|---------|---------|
| `SELF_SMARTER_CONFIG` | Path to config.json | `skills/self-smarter-everyday/config.json` |
| `SELF_SMARTER_LOG_LEVEL` | Logging verbosity (debug, info, warn, error) | `info` |
| `SELF_SMARTER_LOG_DIR` | Log output directory | `skills/self-smarter-everyday/logs/` |
| `SELF_SMARTER_MAX_MEMORY_MB` | Memory limit for the nightly session | `512` |
| `SELF_SMARTER_DRY_RUN` | When set to `true`, runs all phases but doesn't write changes | unset |
| `SELF_SMARTER_SKIP_PHASES` | Comma-separated list of phases to skip | unset |

### Dry Run Mode

Dry run mode is invaluable for testing. When enabled, the routine executes all phases normally but doesn't persist any changes — no prompt mutations are committed, no memory files are modified, no skill changes are applied. The nightly report is still generated, allowing you to review what would have happened.

Enable dry run:
```bash
export SELF_SMARTER_DRY_RUN=true
```

### Skipping Phases

If you want to test or run specific phases independently, use the skip list:

```bash
# Skip skill gap analysis (resource-intensive)
export SELF_SMARTER_SKIP_PHASES="skill-gap-analysis"

# Skip both prompt evolution and skill gap analysis
export SELF_SMARTER_SKIP_PHASES="prompt-evolution,skill-gap-analysis"
```

---

## Logging Setup

### Log Structure

The nightly routine produces three types of logs:

**1. Execution Log** (`logs/nightly-YYYY-MM-DD.log`)

A detailed, timestamped log of every action taken during the routine. This is your primary debugging resource.

```
[2026-08-10T02:00:01+07:00] INFO  Nightly routine started
[2026-08-10T02:00:01+07:00] INFO  Phase 1: Data Collection - beginning
[2026-08-10T02:00:03+07:00] INFO  Loaded 47 session transcripts from today
[2026-08-10T02:00:15+07:00] INFO  Phase 1: Data Collection - complete (14.2s)
[2026-08-10T02:00:15+07:00] INFO  Phase 2: Self-Audit - beginning
...
[2026-08-10T02:18:42+07:00] INFO  Nightly routine completed successfully
[2026-08-10T02:18:42+07:00] INFO  Total duration: 18m 41s
```

**2. Audit Log** (`data/audit-logs/YYYY-MM-DD-nightly-report.md`)

A human-readable markdown report summarizing the night's findings. This is the primary output you review each morning.

**3. Machine-Readable Metrics** (`data/audit-logs/YYYY-MM-DD-metrics.json`)

A JSON file containing structured metrics for dashboard integration and trend analysis.

### Log Rotation

Logs accumulate over time. Implement log rotation to prevent disk exhaustion:

- **Execution logs:** Retain for 30 days. Older logs are compressed and archived.
- **Audit reports:** Retain indefinitely — they're small and historically valuable.
- **Metrics files:** Retain for 90 days. Older data should be aggregated into weekly/monthly summaries.

A simple rotation script can be added to the nightly routine's cleanup phase:

```bash
# Remove execution logs older than 30 days
find logs/ -name "nightly-*.log" -mtime +30 -delete

# Compress metrics older than 90 days into monthly archives
find data/audit-logs/ -name "*-metrics.json" -mtime +90 -exec gzip {} \;
```

---

## Monitoring

### Health Checks

Implement a simple health check that runs each morning to verify the nightly routine completed successfully:

```bash
# Check if last night's report exists
if [ -f "data/audit-logs/$(date -d 'yesterday' +%Y-%m-%d)-nightly-report.md" ]; then
  echo "Nightly routine: OK"
else
  echo "Nightly routine: MISSED"
  # Trigger alert or manual investigation
fi
```

### Key Metrics to Monitor

Track these metrics over time to ensure the routine is healthy:

| Metric | Healthy Range | Alert Threshold |
|--------|---------------|-----------------|
| Total duration | 15-45 minutes | > 60 minutes |
| Audit composite score | 0.6-1.0 | < 0.4 for 3+ consecutive nights |
| Memory compaction ratio | 0.3-0.7 | < 0.1 or > 0.9 |
| Prompt mutations accepted | 0-3 per night | 0 for 7+ consecutive nights |
| Error rate during routine | < 5% | > 10% |

### Alerting

Set up alerts for critical failures:

- **Routine didn't fire** — no report generated by 3:00 AM.
- **Routine timed out** — execution exceeded the configured timeout.
- **Score regression** — composite audit score dropped by more than 0.15 in a single night.
- **Memory corruption detected** — compaction phase reported data integrity issues.

---

## Phase Details

### Phase 1: Data Collection

**What happens:** The agent reads all available data from the past 24 hours. This includes session transcripts, memory file changes, error logs, token usage records, and any user feedback signals.

**Inputs:**
- `memory/YYYY-MM-DD.md` — today's daily memory file
- Session history from active sessions
- Error logs from `logs/` directory
- Token usage statistics from the gateway

**Outputs:**
- A consolidated data package in memory, ready for analysis by subsequent phases.

**Expected duration:** 2-5 minutes depending on the number of sessions and volume of interactions.

### Phase 2: Self-Audit

**What happens:** The agent evaluates its performance across five dimensions. Each dimension is scored from 0.0 to 1.0. A weighted composite score is calculated using the weights defined in `config.json`.

**Scoring dimensions:**
1. **Accuracy** — Were responses correct and helpful? Measured by error rate, corrections needed, and user satisfaction signals.
2. **Token Efficiency** — Was token usage reasonable? Measured by tokens-per-response trends and comparison to baseline.
3. **Response Time** — Were responses delivered promptly? Measured by average response latency.
4. **Error Rate** — How often did things go wrong? Measured by error frequency and severity.
5. **User Satisfaction** — Did the user seem happy? Measured by positive/negative signals in conversation tone, explicit feedback, and correction frequency.

**Expected duration:** 3-8 minutes.

### Phase 3: Memory Compaction

**What happens:** The agent reviews its memory stores and optimizes them. High-value memories are promoted to long-term storage. Low-value or redundant memories are demoted or archived. The daily log is compressed into a concise summary.

**Expected duration:** 2-5 minutes.

### Phase 4: Prompt Evolution

**What happens:** Based on audit findings, the agent proposes small mutations to its system prompts. Mutations are tested against a fitness function using sampled historical interactions. Accepted mutations are committed to the prompt version git repository.

**Expected duration:** 5-10 minutes.

### Phase 5: Skill Gap Analysis

**What happens:** The agent reviews interactions where it struggled. It identifies patterns suggesting missing capabilities and decides whether to create new skills, modify existing ones, or flag gaps for human review.

**Expected duration:** 3-7 minutes.

### Phase 6: Reporting

**What happens:** A comprehensive nightly report is generated, summarizing all findings, changes made, and recommendations.

**Expected duration:** 1-2 minutes.

---

## Resource Requirements

### Minimum Resources

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 512 MB available | 1024 MB available |
| Disk | 500 MB free | 2 GB free |
| CPU | 1 core | 2+ cores |
| Time | 60 minutes timeout | 35 minutes typical |

### Resource Optimization

If resources are constrained:

1. **Reduce fitness sample size** — from 20 to 10 interactions per mutation test.
2. **Limit daily log processing** — cap at 250 KB instead of 500 KB.
3. **Skip skill gap analysis** — this phase is the most resource-intensive.
4. **Run on alternate nights** — change cron to `0 2 */2 * *` for every-other-night execution.

---

## Summary

The nightly routine is a carefully orchestrated sequence of self-improvement phases. Proper cron configuration, timezone handling, logging, and monitoring ensure it runs reliably. Start with the default settings, observe the first few nights, and adjust based on what you learn. The routine is designed to be resilient — if one phase fails, the others still execute, and the failure is recorded for investigation.
