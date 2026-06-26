---
name: skill-auditor
description: Periodically audit all workspace skills, learnings, memory, and configuration files to recommend refactoring, new skill ideas, and workflow improvements. Triggered automatically via cron every 7 days, or manually with "audit skills", "skill review", "workspace health", or "improve workflow". Sends recommendations directly to Telegram without user prompting.
---

# Skill Auditor

Automated weekly workspace health check. Evaluates skills, learnings, memory, and config files. Delivers actionable recommendations to Telegram.

## Pipeline architecture

4-phase sequential pipeline with internal parallelism:

### Phase 1: Digest (`opencode-go/kimi-k2.5`)

Ingest all workspace files in one long-context call:
- `skills/*/SKILL.md` and associated scripts/tests
- `.learnings/LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md`
- `SOUL.md`, `AGENTS.md`, `USER.md`, `TOOLS.md`, `MEMORY.md`, `HEARTBEAT.md`
- recent `memory/*.md` files (last 14 days)

Output: `audit-state.json` with per-file summaries, staleness scores, overlap detection, gap analysis.

Optimization: hash watched files against `state.json` from last run. Skip unchanged files to prevent token burn.

Also: `web_search` for best practices relevant to detected gaps.

### Phase 2: Evaluate (parallel)

**Phase 2A** (`opencode-go/glm-5`): Score each skill on effectiveness, token efficiency, coverage, staleness, overlap, alignment with USER.md goals. Propose new skill ideas.

**Phase 2B** (`openai-codex/gpt-5.3-codex`): Score independently. Generate concrete refactor proposals. Propose new skill ideas.

Both output structured evaluation JSON.

### Phase 3: Judge (`openai-codex/gpt-5.4`)

Receives: `audit-state.json` + both evaluation outputs.

- Cross-validate proposals, resolve conflicts
- Filter: only recommend changes with clear ROI
- Classify each recommendation:
  - 🟢 **safe refactor** — low-risk, can PR directly after approval
  - 🟡 **needs review** — structural change or new skill creation
  - 🔴 **informational** — trend or observation, no action yet
- Confidence threshold: ≥0.7 to recommend, ≥0.85 for safe-refactor classification

Output: `final-recommendations.json`

### Phase 4: Deliver (main session)

Format recommendations as Telegram message and send. Archive to `memory/audits/YYYY-MM-DD.json`.

## Recommendation format

Each recommendation:

```json
{
  "id": "rec-001",
  "type": "refactor | new-skill | config-update | deprecate | merge",
  "severity": "green | yellow | red",
  "target": "skills/context-optimizer/SKILL.md",
  "title": "compress context-optimizer references section",
  "rationale": "...",
  "proposed_action": "...",
  "confidence": 0.87,
  "agreed_by": ["glm-5", "gpt-5.3-codex"]
}
```

## Telegram delivery format

```
📋 Weekly Skill Audit — YYYY-MM-DD

🟢 Safe refactors (N):
  1. [title] → [one-line action]

🟡 Needs review (N):
  2. [title]

🔴 Informational (N):
  3. [title]

Reply with a number for details, or "approve 1,2" to greenlight.
```

If no strong recommendations: send "no action needed this week" one-liner.

If quality score is low across all recommendations: send nothing.

## Scheduling

**Primary:** OpenClaw cron, every 7 days (Sunday 10:00 AM ET):

```
openclaw cron add --schedule "0 10 * * 0" --model openai-codex/gpt-5.4 --label skill-auditor-weekly --prompt "Read skills/skill-auditor/SKILL.md and execute the full audit pipeline. Deliver results to Telegram."
```

**State tracking:** `memory/audits/last-run.json` records last execution timestamp. Heartbeat checks if last run was >10 days ago and alerts.

**Manual trigger:** User says "audit skills" or "review workflow".

## Evaluation criteria

Each file/skill scored on:
1. **Effectiveness** — achieves stated purpose? (1-5)
2. **Token cost** — bloated? shorter without losing value? (1-5)
3. **Coverage** — workflow gaps not addressed by any skill? (binary + description)
4. **Freshness** — last meaningful update vs relevance decay
5. **Overlap** — duplicates content in another file/skill? (list pairs)
6. **Alignment** — matches USER.md goals and SOUL.md persona? (1-5)

## Safety rules

- No automatic file edits. Recommendations are advisory until approved.
- Green recommendations produce diff previews; actual changes require explicit "approve" reply.
- Respect all workspace GitHub handling rules — no repo-visible changes without Omar's approval.

## File structure

```
skills/skill-auditor/
├── SKILL.md
├── scripts/
│   ├── build_audit_state.py
│   ├── merge_evaluations.py
│   └── format_telegram.py
└── tests/
    ├── test_build_audit_state.py
    ├── test_merge_evaluations.py
    └── test_format_telegram.py
```

Runtime artifacts (not tracked in repo):
```
memory/audits/
├── last-run.json
├── YYYY-MM-DD.json
└── state.json (file hashes for change detection)
```

## Validation checklist

1. All 3 helper scripts exist and pass unit tests.
2. Dry-run mode completes full pipeline without sending messages.
3. At least one real audit cycle delivers a well-formatted Telegram message.
4. Recommendations are advisory-only (no auto-edits without approval).
5. Unchanged files are skipped via hash comparison.
6. Confidence thresholds are enforced.
