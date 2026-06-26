# Report Schema

Use this schema when `skill-optimizer` produces its audit report.

## Report Structure

Always use this top-level shape:

```md
# Skill Audit Report

## Executive Summary

## Findings

### Missed Trigger Cases

### Duplicate Or Overlapping Skills

### Metadata Quality Issues

### Risk And Safety Review

### Installation And Maintenance Workflow

## Action Queue
```

Only include sections that have meaningful content, but always include `Executive Summary`, `Findings`, and `Action Queue`.

## Finding Record

Each finding should contain:

- `id`
- `title`
- `category`
- `target_skills`
- `evidence`
- `why_it_matters`
- `recommended_action`
- `available_actions`

Recommended markdown shape:

```md
#### I01 - Duplicate copies of `baoyu-url-to-markdown`
- Category: `duplicate_skill`
- Target skills: `baoyu-url-to-markdown`
- Evidence:
  - Found active copies in multiple directories
  - Similar purpose and overlapping files indicate maintenance duplication
- Why it matters: Duplicate active copies raise maintenance cost and can create trigger ambiguity.
- Recommended action: `Merge`
- Available actions: `Fix / Merge / Delete / Keep and Skip`
```

## Action Queue Record

Each action queue item should be self-contained and easy for the user to choose from.

Use this shape:

```md
- `I01`
  Title: Duplicate copies of `baoyu-url-to-markdown`
  Recommendation: `Merge`
  Why: There are multiple active copies and no clear canonical source.
  Options: `Fix / Merge / Delete / Keep and Skip`
```

If the UI or conversation format benefits from more structure, the same information can be expressed in YAML-like blocks:

```yaml
id: I01
title: Duplicate copies of baoyu-url-to-markdown
category: duplicate_skill
target_skills:
  - baoyu-url-to-markdown
severity: medium
confidence: high
evidence:
  - Multiple active copies found in visible skill roots
why_it_matters: Duplicate active copies make maintenance and triggering less predictable
 recommended_action: Merge
 available_actions:
  - Fix
  - Merge
  - Delete
  - Keep and Skip
```

## Action Semantics

Keep the four actions stable:

- `Fix`
  Update metadata, trigger wording, safety language, structure, or stale files.
- `Merge`
  Consolidate duplicate or overlapping skills into a clearer single source of truth.
- `Delete`
  Remove the selected skill or duplicate copy after the user explicitly chooses deletion.
- `Keep and Skip`
  Record the finding as reviewed for now, but make no changes.

## User Reply Format

Prompt the user to reply using one line per action:

```text
I01 -> Fix
I02 -> Merge
I03 -> Delete
I04 -> Keep and Skip
```

If a chosen action is ambiguous, ask a narrow follow-up question before editing files.
