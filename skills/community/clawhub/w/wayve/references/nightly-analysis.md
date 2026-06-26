# Background Analysis — Smart Token Management

## Core Principle

Heavy analysis (pattern detection, trend computation, business metrics, report generation) consumes significant tokens. Instead of running these during interactive conversations, **propose to the user to schedule them at night** — so results are ready in the morning.

This is NOT a fixed automation. It's a behavior principle: when you recognize that a task is token-heavy, ask the user if they'd like you to do it overnight.

## When to Propose Background Processing

**During any conversation where heavy analysis is needed:**

- Time Audit report analysis (semantic clustering, scoring, report generation)
- Life Scan (12-week trend analysis, happiness correlations, energy matrix)
- Multi-week pattern detection (hustle-collapse, pillar oscillation)
- Business metrics analysis (revenue trends, revenue-per-hour)
- Comprehensive strategy review (`/wayve strategy`)

**How to propose it:**

"This analysis is pretty thorough — it'll work better if I take some time with it. Want me to run this tonight and have the results ready for you in the morning?"

Or: "I can do a quick version now, or a deep analysis overnight. Which do you prefer?"

**Always let the user choose.** Some users want results NOW and don't care about tokens. Others prefer efficiency. Respect their preference and save it:
```
wayve knowledge save --category "preferences" --key "analysis_timing" --value "prefers overnight for heavy analysis" --json
```

## How to Set Up a Background Analysis

When the user agrees to overnight processing, create an agent routine:

```
wayve automations create agent_routine --name "[Description of what to analyze]" --cron "0 3 * * *" --timezone USER_TIMEZONE --channel USER_CHANNEL --config '{"agent_instructions": "[Specific instructions for what to analyze and save]"}' --json
```

**Important:** The instructions should be specific to what needs to be analyzed right now — not a generic "analyze everything." For example:
- "Generate the Time Audit report for audit_id X. Cluster activities, score automation potential, cross-reference with automations, and save the Automation Discovery Report to knowledge."
- "Analyze the last 12 weeks of producer scores for multi-week patterns. Save findings to weekly_patterns."

After the analysis runs, **disable or delete the automation** if it was a one-time job. Only keep it as recurring if the user explicitly wants regular background analyses.

## What Can Be Analyzed in Background

### Pattern Scan
- Hustle-Collapse cycle detection (score oscillates >80% → <50%)
- Growth Plateau (score variance < 5% for 4+ weeks)
- Pillar Oscillation (focus alternates between same 2 pillars)
- Improvement/decline trends
- Save: `weekly_patterns` / `pattern_scan_YYYY_MM_DD`

### Pillar Health Trend
- Consecutive zero weeks per pillar
- Frequency target patterns
- Pillar satisfaction correlations
- Save: `pillar_balance` / `pillar_health_scan_YYYY_MM_DD`

### Business Metrics (if data exists)
- Revenue trend (last 3 months)
- Revenue-per-hour calculation
- Revenue vs goal trajectory
- Save: `personal_context` / `revenue_analysis_YYYY_MM_DD`

### Automation Effectiveness
- Stalled delegations (accepted but not implemented)
- Time saved by existing automations
- Save: `delegation_candidates` / `automation_effectiveness_YYYY_MM_DD`

### Coaching Theme Updates
- Strengthen confirmed patterns (increase confidence)
- Note resolved patterns
- Save: update existing `coaching_themes` entries

## Using Cached Results

During interactive sessions (Daily Brief, Fresh Start, Wrap Up), check for recent analysis results in knowledge:
- `pattern_scan_*` — multi-week patterns
- `pillar_health_scan_*` — pillar trends
- `revenue_analysis_*` — business metrics
- `automation_effectiveness_*` — automation impact

If these exist and are less than 7 days old, use them directly instead of re-analyzing. This keeps interactive sessions fast and token-efficient.

## Cached Result JSON Formats

These are the JSON structures saved to the knowledge base by background analyses. Other flows (Daily Brief, Fresh Start, Wrap Up) consume these cached results.

### `pattern_scan_YYYY_MM_DD`
Category: `weekly_patterns`

```json
{
  "scan_date": "2026-03-18",
  "patterns": [
    {
      "type": "hustle_collapse | growth_plateau | pillar_oscillation | improvement | decline",
      "confidence": 0.85,
      "detected_weeks": [8, 9, 10, 11],
      "description": "Score oscillated >80% for 3 weeks then dropped to <50%",
      "recommendation": "Build in a lighter week after 3 intense weeks to prevent crash"
    }
  ],
  "weeks_analyzed": 12,
  "overall_trend": "improving | stable | declining"
}
```

### `pillar_health_scan_YYYY_MM_DD`
Category: `pillar_balance`

```json
{
  "scan_date": "2026-03-18",
  "pillars": [
    {
      "pillar_id": "uuid",
      "pillar_name": "Health",
      "zero_weeks": 2,
      "zero_weeks_consecutive": true,
      "avg_completion_pct": 65,
      "frequency_on_track": false,
      "frequency_target": 3,
      "frequency_actual_avg": 1.5,
      "status": "healthy | at_risk | neglected",
      "trend": "improving | stable | declining"
    }
  ],
  "most_neglected": "pillar_name",
  "most_consistent": "pillar_name"
}
```

### `revenue_analysis_YYYY_MM_DD`
Category: `personal_context`

```json
{
  "scan_date": "2026-03-18",
  "revenue_trend": {
    "months": [
      { "month": "2026-01", "amount": 4500 },
      { "month": "2026-02", "amount": 5200 },
      { "month": "2026-03", "amount": 4800 }
    ],
    "direction": "growing | stable | declining",
    "avg_monthly": 4833
  },
  "revenue_per_hour": {
    "total_revenue_last_month": 4800,
    "mission_hours_last_month": 120,
    "rate": 40
  },
  "vs_goal": {
    "target": 8000,
    "current": 4800,
    "gap_pct": 40,
    "on_track": false
  }
}
```

### `automation_effectiveness_YYYY_MM_DD`
Category: `delegation_candidates`

```json
{
  "scan_date": "2026-03-18",
  "automations": [
    {
      "automation_id": "uuid",
      "name": "Weekly client update draft",
      "status": "active | stalled | not_started",
      "accepted_date": "2026-02-15",
      "implemented": true,
      "estimated_hours_saved_weekly": 2.5,
      "notes": "Running well, client feedback improved"
    }
  ],
  "total_hours_saved_weekly": 5.0,
  "stalled_count": 1,
  "recommendation": "Follow up on stalled 'Invoice automation' — accepted 4 weeks ago but not implemented"
}
```

## Key Rules

0. **Never create background jobs without explicit user confirmation.** The user must say 'yes' before any scheduled task is created. This is a hard rule — no exceptions.
1. **Always ask permission** — never schedule a background job without the user confirming
2. **Be specific** — each background job has clear instructions, not generic "analyze everything"
3. **One-time by default** — delete the automation after it runs, unless the user wants it recurring
4. **Morning-ready** — schedule so results are ready before the user's typical start time
5. **Respect preferences** — if the user says "just do it now," do it now. Save their preference for next time.
