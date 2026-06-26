---
name: orient
description: Fetches issue context, auto-detects task type, maps to branch prefix, presents brief.
---

Phase gate: EXPLORE checkpoint. This skill MUST complete all steps before proceeding to Isolate.

## Steps

1. **Fetch issue context** (if issue number provided):
   ```bash
   gh issue view <number> --json title,body,labels,assignees
   ```
   If no issue number provided, ask the user to describe the task.
   If `gh` is not available (remote session without GH_TOKEN), skip issue fetch and proceed with manual description.

2. **Auto-detect task type** from labels or description:
   | Label / keyword | Type | Branch prefix |
   |----------------|------|---------------|
   | `bug`, error, crash, broken, fix | Bugfix | `fix/` |
   | `enhancement`, `feature`, add, want, should, new | Feature | `feat/` |
   | `chore`, `config`, deps, ci, tooling | Chore | `chore/` |
   | `docs`, documentation, readme | Docs | `docs/` |
   | Default | Feature | `feat/` |

3. **Scan for relevant ADRs**:
   ```bash
   ls "$(git rev-parse --show-toplevel)/ai-workspace/decisions/"*.md 2>/dev/null | head -20
   ```
   Check ADR titles/filenames for keywords matching the issue title/body. If matches found, read the relevant ADR and surface it.
   If ADR scan finds contradictions, surface explicitly: "This task may conflict with ADR-NNN"

4. **Check for interrupted work**:
   If `"$(git rev-parse --show-toplevel)/.branch-context.md"` exists, read it and include in the brief (resuming work).

5. **Read recent memory**:
   ```bash
   tail -20 "$(git rev-parse --show-toplevel)/ai-workspace/MEMORY.md" 2>/dev/null
   ```

6. **Present brief**:
   ```
   ## Orient Brief
   **Task**: [title or description]
   **Type**: [bugfix/feature/chore/docs] → branch prefix: [fix/feat/chore/docs]/
   **Suggested branch**: [prefix]/[kebab-case-name]
   **Relevant ADRs**: [list or "none found"]
   **Resuming?**: [yes — from .branch-context.md / no]
   **Files likely affected**: [educated guess from issue description + ADR context]
   ```

7. **Auto-route** using the one-sentence rule:
   - Can the entire diff for this task be described in ONE sentence? → **Direct to Isolate** (skip Design/Review)
   - Otherwise → **Plan first** (proceed to Design after Isolate)

   Present the routing decision. The agent auto-decides — no human input required. If human is present, they can override.

## Edge Cases
- No issue number + no user description → ask for a description
- `gh` not available → skip issue fetch, proceed with manual description
- No ADRs directory → skip ADR scan
