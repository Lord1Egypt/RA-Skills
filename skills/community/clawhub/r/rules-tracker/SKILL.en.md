---
name: rules-tracker
description: Track rules/guidelines/constraints triggering, compliance and violations for quantitative evaluation of weak model execution quality. Auto-generate compliance report after each task. Suitable for development, learning, data organization self-review.
---

# Rules Tracker Skill

Track your rule compliance and generate execution reports.

## Core Functions

1. **Auto-track**: Record rule execution after task completion
2. **Compliance rate**: Calculate compliance percentage per rule group
3. **Problem diagnosis**: Identify frequently violated rules, provide improvement suggestions
4. **Historical review**: Aggregate data, analyze trends

## Usage

### Trigger Tracking (at task end)

```
Use this skill to track rule compliance.
```

### Key Rules List

Rules to track, grouped by:

| Rule Group | Includes | Weight |
|-----------|----------|--------|
| **Hard Rules** | No assumptions, must verify, mark inference, confirm changes | High |
| **Programming** | Minimal changes, Token budget, goal-first-then-action | Medium |
| **OpenCode Safety** | No sed, git switch, context recovery | High |
| **Weak Model** | Ask when uncertain, small steps, show evidence | Medium |

### Manual Label (during task)

When violating a rule:

```
[Rule Violated] {ruleID}: {reason}
Example: [Rule Violated] HR-2: concluded without verifying
```

When following a rule:

```
[Rule Followed] {ruleID}: {description}
Example: [Rule Followed] GS-1: backed up critical file
```

### Generate Report

After task completion, generate tracking report:

```markdown
# Rule Compliance Report

## Overview
- Rules Triggered: X
- Times Followed: Y
- Times Violated: Z
- Compliance Rate: Y/(Y+Z)*100%

## Rule Details
| RuleID | Rule Name | Triggered | Followed | Violated | Rate |
|--------|----------|----------|----------|----------|------|
| HR-1 | No Assumptions | X | Y | Z | W% |

## Problem Diagnosis
Most violated rules:
1. {ruleID} - {count} times
2. {ruleID} - {count} times

## Improvement Suggestions
- For frequently violated rules...
```

## Rule ID Quick Reference

### Hard Rules (HR-*)

| ID | Rule | Description |
|----|------|-----------|
| HR-1 | No Assumptions | Don't fabricate |
| HR-2 | Must Verify | Verify or ask when info insufficient |
| HR-3 | Mark Inference | Use "[Inference]" for guesses |
| HR-4 | Confirm Changes | Confirm when evidence insufficient |
| HR-5 | Backup | Backup critical files first |
| HR-6 | Honest Output | Don't fake results |

### Programming (PG-*)

| ID | Rule | Description |
|----|------|-----------|
| PG-1 | Minimal Changes | Only change what's necessary |
| PG-2 | Goal First | Write goal before action |
| PG-3 | Context Recovery | Recover from context |
| PG-4 | Token Budget | Keep within 8K |
| PG-5 | Closed-loop Verify | Verify before reporting |
| PG-6 | Fail Loud | Say "don't know" when uncertain |

### OpenCode Safety (OC-*)

| ID | Rule | Description |
|----|------|-----------|
| OC-1 | No Sed | Don't use sed for replacement |
| OC-2 | No Stdout Redirect | No cmd>file |
| OC-3 | Git Switch | Use git switch |
| OC-4 | Read Before Write | Read existing files first |
| OC-5 | Per-file Review | Review immediately after edit |

### Weak Model (WM-*)

| ID | Rule | Description |
|----|------|-----------|
| WM-1 | Ask When Uncertain | Ask for big things, decide small yourself |
| WM-2 | Confirm Each Step | Confirm for complex tasks |
| WM-3 | Small Iterations | Make small changes each time |
| WM-4 | Show Evidence | Give code/file evidence |

## Data Storage

Saved to:
- `memory/rules-tracker-{YYYY-MM-DD}.json`

## Auto-trigger

Can auto-generate reports at:
- daily heartbeat
- task completion keywords
- user request

## Improve AGENTS.md

Use tracking data to find problems:

| Problem Type | Metric | Improve Direction |
|-------------|-------|----------------|
| Frequent Violations | TOP3 violators | Simplify or strengthen |
| Never Triggered | 0 triggers may be redundant | Delete or merge |
| Conflicting Rules | Two rules both trigger | Clarify priority |
| Token Waste | Rule 6 exceeds 8K | Adjust budget |

### Common Conflicts

| Conflict | Description |
|----------|------------|
| WM-1 vs WM-2 | "Ask" vs "Confirm" → separate big/small |
| PG-2 vs PG-5 | "Goal-first" vs "Verify" → confirm goal first |

## Note

- This skill won't auto-enforce; you must actively label during tasks
- Compliance rate is a guide, not KPI
- Purpose: identify weak points, continuously improve AGENTS.md