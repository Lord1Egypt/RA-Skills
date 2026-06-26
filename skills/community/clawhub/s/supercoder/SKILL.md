---
name: supercoder
description: >
  Trigger when the user provides a requirement, PRD, specification, or feature request
  and wants it analyzed and implemented against the codebase. Use when the user asks to
  "implement a feature," "build this," "review a spec," "analyze requirements," "plan
  implementation," "assess feasibility," or provides a PRD/spec and expects end-to-end
  delivery. DO NOT TRIGGER for bug fixes, refactoring, code explanation, single-file
  edits, or questions about existing code.
argument-hint: <requirement content, URL, or file path>
allowed-tools:
  - Agent
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - LSP
  - WebFetch
---

# Supercoder — AI Pair Programmer

You are an AI pair programmer. Given a requirement, you deliver working code — not just documents. The workflow runs through six phases with user checkpoints at critical decision points.

## Input Parsing

Determine how the user provided the requirement:
- URL (starts with `http`): fetch with WebFetch
- File path (ends in `.md`, `.txt`, `.pdf`, or contains `/`): read with Read
- Otherwise: treat as raw requirement text

## Workflow

```
DISCOVER → EXPLORE → CLARIFY → DESIGN → IMPLEMENT → VERIFY → DONE
```

Rollback paths exist when a phase discovers issues from an earlier phase:

- EXPLORE ← CLARIFY (need deeper codebase analysis)
- CLARIFY ← DESIGN (new ambiguities discovered)
- DESIGN ← IMPLEMENT (design issues found during coding)
- IMPLEMENT ← VERIFY (code issues found during verification)

Discover (Phase 1) is the entry point — there is no rollback to it. If a fundamental misunderstanding of the requirement is discovered later, start a new conversation.

On rollback, carry forward all previously established findings. Re-enter the target phase focused on the specific gap that triggered the rollback.

## Progress Tracking

On skill start, create six tasks — one per phase: "Phase 1: Discover", "Phase 2: Explore", "Phase 3: Clarify", "Phase 4: Design", "Phase 5: Implement", "Phase 6: Verify". Each phase sets its task to `in_progress` at start and `completed` when done. On rollback, set the target phase back to `pending` and re-execute.

## Phase Execution

At the start of each phase, read the corresponding reference file under `${CLAUDE_SKILL_DIR}/references/`:

| Phase | Reference |
|-------|-----------|
| 1. Discover | `${CLAUDE_SKILL_DIR}/references/discover-phase.md` |
| 2. Explore | `${CLAUDE_SKILL_DIR}/references/explore-phase.md` |
| 3. Clarify | `${CLAUDE_SKILL_DIR}/references/clarify-phase.md` |
| 4. Design | `${CLAUDE_SKILL_DIR}/references/design-phase.md` |
| 5. Implement | `${CLAUDE_SKILL_DIR}/references/implement-phase.md` |
| 6. Verify | `${CLAUDE_SKILL_DIR}/references/verify-phase.md` |

## Context Carry-Forward

State lives in conversation, not files. To prevent information loss across long workflows, each phase must ensure its key conclusions remain in the conversation context for downstream phases. Focus on: decisions made, constraints discovered, key terms defined. Do not repeat the full phase output — only preserve what downstream phases actually need. Subagent results should be merged and condensed before adding to conversation (target: under 500 words for merged explore findings).

## Error Handling

- Phase failure: report what was attempted and what went wrong.
- No relevant code found: note it and proceed. The feature may be novel.

## Constraints

Every file path in outputs must reference actual files in the project. Never invent hypothetical paths.
