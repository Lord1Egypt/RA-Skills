---
name: workspace-governance
description: >
  A methodology-first workspace governance skill for AI agents.
  Focuses on principles, decision framework, and safe execution patterns
  instead of fixed directory templates. Triggers on "organize", "cleanup",
  "archive", "workspace check", "整理工作区", "清理文件", "归档项目", "太乱了".
---

# Workspace Governance

Methodology-first workspace governance for AI agents.

## Chinese Guide

For Chinese readers:

- Quick entry: `README.zh-CN.md`
- Detailed manual: `references/治理手册.zh-CN.md`

## Purpose

This skill teaches an agent how to design a workspace management strategy that fits its own runtime, platform, and user preferences.

This is not a single directory template and not a rigid SOP.  
The agent should adapt based on context, then execute safely.

## Core Principles

1. Boundary before structure: define what can be touched first.
2. Plan before action: generate a governance plan before file operations.
3. Reversible before optimized: preserve rollback paths and avoid irreversible changes.
4. Fit current system first: reuse existing conventions when they are workable.
5. User control at key points: destructive operations require explicit confirmation.
6. Evidence-driven decisions: only propose actions based on real scan results.

## When to Use

- Workspace is messy and needs cleanup or reorganization.
- User asks to archive/close finished work.
- User asks to create a new project with clear boundaries.
- User asks for workspace audit/health check.
- Agent needs to establish sustainable file governance rules.

## Required Capabilities and Preconditions

Before execution, the agent should verify runtime capabilities:

1. File/dir inspection and manipulation (`ls`, move, rename, archive, delete).
2. Logging output capability (file or structured output sink).
3. User confirmation capability for ambiguous/destructive actions.

Preconditions:

- `workspace_root` must be defined (user-provided or default current directory).
- If `workspace_root` is broad/high-risk, require explicit confirmation before scanning.
- If confirmation capability is unavailable, `ask-user` items are blocking items.

## Scope and Boundaries

The agent must define these before execution:

- `workspace_root`: the manageable boundary for this task.
- `immutable_dirs`: directories that must never be moved/deleted/renamed.
- `protected_files`: sensitive files (keys, env, certs, VCS metadata).
- `risk_level`: low/medium/high based on destructive potential.

If `workspace_root` is too broad (for example home root), require explicit confirmation before scanning.

## Adaptation Model (Platform-Agnostic)

The agent should adapt strategy using this order:

1. User explicit constraints and preferences.
2. Current repository/project conventions.
3. Platform/runtime restrictions.
4. Conservative fallback defaults.

Do not force a fixed folder structure unless the user requests standardization.

### Optional Adapt Block

```yaml
SKILL_ADAPT:
  workspace_root: <path>
  immutable_dirs: [dir1, dir2]
  protected_files: [pattern1, pattern2]
  cache_policy: separate # separate | consolidate
  naming_policy: inherit # inherit | enforce
```

### Adapt Loading Rules (Mandatory)

If `SKILL_ADAPT.yaml` exists, the agent must read it before planning and execution.
If platform profiles exist (for example `tools/adapt-profiles/openclaw.yaml`), the agent should load the matching profile as an overlay.

Configuration precedence:

1. User explicit instruction in current session.
2. `SKILL_ADAPT` config.
3. Repository conventions detected from files.
4. Conservative defaults from this skill.

If `SKILL_ADAPT` parsing fails:

- Do not silently ignore.
- Fall back to conservative defaults.
- Record a warning in governance logs.

Profile merge semantics:

- `immutable_dirs`: union (security items only increase)
- `protected_files`: union (protection only increases)
- `destructive_guard`: override allowed only when strictness is not reduced

## Decision Framework

Before any move/delete action, produce a governance plan with:

1. **Current State Summary**
   - What is cluttered
   - What is ambiguous
   - What is sensitive
2. **Target Strategy**
   - Keep, move, rename, archive, delete policy
   - Naming and lifecycle policy
   - Cache/temp policy
3. **Risk and Rollback**
   - Risks per action class
   - Rollback method and checkpoints
4. **User Confirmation Items**
   - Items that need user decision
   - Items excluded from automation

### Plan Output Template

| Item | Current | Proposed Action | Target | Risk | Reason |
|------|---------|-----------------|--------|------|--------|
| example.tmp | root | delete | — | medium | temporary artifact |
| report-final.docx | root | ask user | docs or archive | low | destination ambiguous |

## Execution Pattern (Generic)

Use this pattern regardless of platform:

1. Detect context and runtime capabilities.
2. Load `SKILL_ADAPT` (if present) and resolve effective policy by precedence.
3. Detect boundaries (`workspace_root`, immutable/protected scope).
4. Scan inside `workspace_root` only.
5. Classify findings: keep/move/rename/archive/delete/ask-user.
6. Generate plan table with reasons, risks, and rollback checkpoints.
7. Get confirmation for destructive or ambiguous actions.
8. Execute in small batches with checkpoint logs.
9. Report results and failures.
10. Record governance log for traceability.

If multiple user intents exist, process sequentially and reconfirm between destructive batches.

## Non-Interactive Safety Policy (Mandatory)

For non-interactive runtimes (cron, background subagent, execute-only environments):

- If any item is classified as `ask-user`, the agent must stop with status `blocked`.
- The agent must output a `pending_decisions` list and required user input.
- The agent must not silently skip, auto-approve, or auto-delete ambiguous items.
- Destructive actions without confirmation capability must be refused (`fail-fast`).

Recommended blocked output:

| Item | Proposed Action | Block Reason | Needed Input |
|------|-----------------|-------------|--------------|
| report-final.docx | ask-user | no confirmation channel | choose destination |

## Classification Heuristics (Flexible)

Use heuristics, not hard-coded folders:

- **Project artifacts**: source code, configs, tests, docs tied to one project.
- **Reusable assets**: media or references used across projects.
- **Ephemeral data**: cache/tmp/build artifacts/log leftovers.
- **Agent/runtime state**: tool configs, sessions, internal runtime files.
- **Ambiguous items**: unclear ownership or destination.

Rules:
- Ambiguous items must be escalated to user decisions.
- Never silently rename if semantic meaning may change.
- Never overwrite existing files on move.

## Safety Baseline (Mandatory)

### Never Touch Without Explicit User Approval

- Version control metadata (`.git/`, `.svn/`, `.hg/`)
- Secret material (`*.key`, `*.pem`, `*.p12`, private credentials)
- Environment files (`.env` and equivalents)
- Agent/runtime configuration directories

### Destructive Action Guardrails

- Always show dry-run plan first.
- Require explicit confirmation for delete and bulk move.
- Use collision-safe naming on move.
- Keep operation logs and failure reasons.
- Stop and ask user if unexpected high-risk patterns are detected.

## Standard Operation Modes

### 1) Organize

Goal: improve discoverability and reduce clutter with minimal disturbance.

### 2) Create Project

Goal: initialize a new work area aligned with existing conventions.

### 3) Archive Project

Goal: transition inactive work into retrievable cold storage with metadata.

### 4) Hygiene Check

Goal: audit quality signals and output fix recommendations.

Note: The agent should choose implementation details based on local system constraints, not this document's examples.

## Skill Interoperability (Optional)

`workspace-governance` can run standalone, but some scenarios may benefit from companion skills/tools:

- Git or GitHub-related archive verification: use Git/GitHub skill/tooling.
- Cloud/object storage archive lifecycle: use cloud storage skills/tools.
- Team approval workflow before destructive batches: use workflow/approval skills/tools.

Interoperability rule:

- Never assume companion skills are present.
- If a companion capability is required by user intent but unavailable, report `blocked` with required dependency.

## Quality Signals for Audit

Recommended checks:

- Boundary clarity (what is managed vs protected)
- Root clutter level
- Naming consistency
- Build/cache residue
- Archive lifecycle completeness
- Recoverability (rollback/readability of logs)

Output style:
- Pass items with clear evidence.
- Violations with fix suggestion and risk level.
- Summary with actionable next steps.

## Logging and Traceability

The agent should keep a lightweight operation record, including:

- Date (`YYYY-MM-DD`)
- Intent type (organize/create/archive/audit)
- Planned changes vs executed changes
- Success/failure counts
- Unresolved decisions pending user input

### Rollback and Checkpoint Schema (Minimum)

Each execution should create:

1. A pre-execution checkpoint (`checkpoint_before`).
2. A checkpoint per batch (`checkpoint_batch_<n>`).
3. A final checkpoint (`checkpoint_after`).

Minimum log fields:

- `timestamp` (`YYYY-MM-DD HH:mm:ss`)
- `intent` (organize/create/archive/audit)
- `batch_id`
- `action` (move/rename/archive/delete)
- `source_path`
- `target_path`
- `result` (success/failure/blocked)
- `reversible` (yes/no)
- `rollback_ref` (checkpoint id or recovery note)

## Anti-Patterns to Avoid

- Forcing a universal directory layout on every system
- Performing bulk cleanup without a dry-run plan
- Treating unknown files as disposable
- Optimizing structure while ignoring user workflow habits
- Mixing agent state and user business content without explicit mapping

## Minimal Example (Reference Only)

Example principles in action:

1. Detect workspace boundary and immutable dirs.
2. Scan only within boundary.
3. Mark ambiguous files as `ask-user`.
4. Confirm plan before delete/move.
5. Execute and log.

This example is illustrative, not normative.

## Author

- 作者: Mars2003 （GitHub）
- 日期: 2026-04-28
