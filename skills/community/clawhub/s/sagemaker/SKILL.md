---
name: SageMaker
description: Unified memory-and-growth operating system for agents. Use when you need consistent layered memory (short/mid/long/knowledge), self-model-driven promotion rules, preflight/retro loops, and gate-based recovery so any equipped agent can run the same self-calibration workflow.
---

# Neuro Memory Core

Implement one shared behavior loop:

`experience -> short_term evidence -> mid_term synthesis -> (knowledge or long_term) -> self-model calibration -> next-task behavior`

## Install / Bootstrap

Preferred safe path (no execution-policy bypass): create/verify these artifacts directly:

- `memory/short_term/`
- `memory/mid_term/MEMORY.md`
- `memory/long_term/MEMORY.md`
- `memory/knowledge.md`
- `memory/check_memory.json` (dual-gate schema)

If this skill bundle includes `scripts/install.ps1`, you may run it without bypassing execution policy:

```powershell
powershell -File "skills/SageMaker/scripts/install.ps1"
```

Optional (if bundled installer supports it): apply HEARTBEAT template with backup:

```powershell
powershell -File "skills/SageMaker/scripts/install.ps1" -ApplyHeartbeatTemplate
```

## Canonical Files

- `memory/short_term/YYYY-MM-DD.md` (raw evidence)
- `memory/mid_term/MEMORY.md` (near-term reusable conclusions)
- `memory/long_term/MEMORY.md` (stable collaboration constraints)
- `memory/knowledge.md` (transferable methods/policies)
- `self-model.md` (current strengths/failures/growth themes/uncertainties)
- `memory/check_memory.json` (daily/weekly gate state)

## Required Promotion Rules

### Update `self-model.md` only when:
1. recurring failure mode is re-validated
2. strength gains new evidence
3. active growth theme should switch

### Update `memory/knowledge.md` only when:
1. method is reusable across multiple scenarios
2. explicit evidence supports it
3. rule can be expressed as `if X then Y`

### Update `memory/long_term/MEMORY.md` only when:
1. improves long-term collaboration quality
2. is not short-term fluctuation

## Entry Quality Contract (mid/long)

Every promoted item must include:
- `reason`
- `evidence`
- `confidence` (`low|medium|high`)

## Task Coupling (Mandatory)

For medium/high complexity tasks:
1. read `self-model.md` + `memory/knowledge.md`
2. write preflight checklist:
   - goal
   - success criteria
   - risks
   - uncertainty
3. include one post-task reflection item before execution starts

## Gate Model (`memory/check_memory.json`)

Use dual gate state:

```json
{
  "daily_need_update": 1,
  "daily_update_done": 0,
  "weekly_need_update": 1,
  "weekly_update_done": 0
}
```

Semantics:
- `1/0` = pending
- `0/1` = done
- anything else = invalid; normalize to `1/0`

## Scheduling Pattern

- Daily cycle: promote short->mid + prune short-term retention
- Weekly cycle: promote mid->long
- Heartbeat: recovery path only (when gate remains pending)

Strict rule: success is valid only if gate flips to done.

## Core-file Safety

Core-file changes must be proposal-first:
- draft proposal
- get approval
- then apply

Core files include: `SOUL.md`, `IDENTITY.md`, `AGENTS.md` and equivalent identity/behavior governance files.
