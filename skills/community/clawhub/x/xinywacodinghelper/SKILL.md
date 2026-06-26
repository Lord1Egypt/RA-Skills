# Skill: Safe Brownfield Code Change

## Purpose

Perform safe, minimal, production-quality code changes across large repositories with resumable execution and machine-optimized indexing.

---

## Skill Routing Requirement

This skill MUST only run for COMPLEX_CODE_TASK.

---

## Mandatory Repo Access Check (CRITICAL)

Before execution:

* identify repo paths
* verify accessibility
* verify required files exist

If failed:

```
[Error]
Type: REPO_ACCESS_FAILURE
Missing: <path>
Reason: <why>
Required: <what needed>
```

DO NOT proceed.

---

## Execution Visibility (CRITICAL)

* NEVER run silently
* ALWAYS output progress per step
* MUST include status: IN_PROGRESS | BLOCKED | COMPLETED

---

## Fail-Fast Handling

Immediately stop if:

* repo checkout timeout (e.g. 78K files case)
* filesystem too large / slow
* command fails repeatedly

Output:

```
[Error]
Type: INFRASTRUCTURE_FAILURE
Stage: <stage>
Reason: <message>
Fix: <action>
```

---

## Phase 1: Progressive Understanding

### Rules

* DO NOT scan full repo blindly
* DO incremental expansion only
* ALWAYS log progress
* ALWAYS resumable

---

### Process

1. start from entry points
2. expand to dependencies
3. stop when change point identified

---

### Mandatory Output

```
[Understand]
File: <path>
Summary: <short machine summary>
Next: <files to explore>
```

---

### Resume Rule

* check progress.log
* skip already processed files
* continue from last step

---

## Repository Index (Machine Optimized)

### Location

/home/vibe/aksclaw-data/index/<repo>/

---

### Structure

file_index.json:

```json
{
  "file": {
    "symbols": ["funcA", "typeB"],
    "deps": ["fileX"],
    "last_used": "ts"
  }
}
```

---

### Rules

* update index after reading file
* reuse index before reading
* prefer index over re-scan
* DO NOT generate human-readable summaries

---

## Phase 2: Plan

* minimal change only
* prefer:

  1. local code
  2. repo pattern
  3. k8s pattern

---

## Phase 3: Implement

* smallest safe change
* no refactor

---

## Phase 4: Validate

* add/update tests
* coverage target: 80% (if measurable)

---

## Phase 5: Review

check:

* correctness
* race conditions
* retry/idempotency
* debuggability

---

## Confidence & Early Stop

Compute confidence:

0.0–1.0 based on:

* correctness
* validation
* risk

---

### Stop if:

* confidence ≥ 0.85
* no major issue
* no failing tests

---

### Output

```
[Confidence]
Score: <0-1>
Reason: <why>
Gaps: <missing>
```

---

## Run Output (MANDATORY)

/home/vibe/aksclaw-data/runs/<run_id>/

must include:

* progress.log
* steps/
* final_output.md
* error.log (if failed)

---

## Cleanup

COMPLETED:

* keep summary only

FAILED:

* keep all logs

---

## Hard Rules

* NEVER guess missing info
* NEVER skip phases
* NEVER run silently
* MUST follow Execution Visibility
* MUST avoid using skill for simple tasks

---

## Mental Model

This is a controlled execution system, not free-form coding.
