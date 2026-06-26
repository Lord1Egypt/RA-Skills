# Usage Guide — How the Agent Invokes safe-change

This document tells the AI agent exactly when to run each script, what to do with the output, and how to make decisions based on the result.

---

## When to Activate

Activate safe-change before any of the following:

- User says "I want to change / refactor / rename X"
- User asks "is it safe to modify X?"
- Agent is about to edit a file that is not a leaf (no importers) in the dependency graph
- Agent detects that a change touches a file with `@Controller`, `@Injectable`, or `export default` at module level
- User mentions a deploy is planned within the next hour

Skip safe-change for:
- New files with no existing importers
- README / documentation-only changes
- Files clearly marked as private helpers (single-file usage)

---

## Phase 1 — Run the Scanner

```bash
# From the project root
node skills/safe-change/scripts/scan-impact.mjs <target-file>
```

Or with an explicit root (monorepo):

```bash
node skills/safe-change/scripts/scan-impact.mjs src/auth/auth.service.ts --root ./backend
```

**The script is read-only.** It will never modify source files.

Capture the JSON output. Parse it. Move to Phase 2.

---

## Phase 2 — Interpret the JSON

Key fields and what they mean:

| Field | Meaning | Agent action |
|-------|---------|--------------|
| `imports.count` | Number of files that import the target | High count = more blast radius |
| `routes.endpoints` | API routes affected by a controller change | List them explicitly in the report |
| `tests.gap` | `true` if no spec files cover the target | Warn the user — tests first, change second |
| `env_vars` | ENV vars read in the target file | Must be rotated in all environments |
| `migrations.recent_count` | Migrations modified in last 7 days | Flag compatibility risk |
| `risk_score` | `low` / `medium` / `high` | Drives the checkpoint behavior |

---

## Phase 3 — Render the Report

Format the JSON as a Markdown report. Template:

```markdown
## Safe Change Report — <target>

**Risk Score: <RISK_SCORE in uppercase>**
Risk factors: <risk_factors joined by ", ">

### Importers (<count>)
<list each importer on a bullet>

### API Routes Affected
<table: Controller | Endpoints>
(If none: "None detected")

### Test Coverage
<list covering test files>
Gap: <yes/no>

### ENV Variables Referenced
<bullet list, or "None">

### Recent Migrations (last 7 days)
<list recent_files, or "None">

---
**Checkpoint:** <risk message + go/no-go question>
```

---

## Phase 4 — Checkpoint Behavior

The agent MUST pause here. Do not proceed to editing without explicit user confirmation.

### Risk Score: LOW

> "Risk score is LOW — <factors>. Proceeding looks safe. Shall I continue?"

Acceptable to proceed with a brief confirmation (single word "yes" is enough).

### Risk Score: MEDIUM

> "Risk score is MEDIUM — <factors>. Review the importers and ENV vars above before confirming. Do you want to proceed? (yes / no / adjust scope)"

Do not proceed until the user explicitly says yes.

### Risk Score: HIGH

> "Risk score is HIGH — <factors>. Recommendation: split this change into smaller steps OR add missing tests before proceeding. Do you want to proceed anyway? (yes / no / let me split it)"

If the user says "proceed anyway," log the decision and proceed. Do not silently skip this.

---

## Phase 5 — Make the Change

Apply the change the user requested. Normal agent behavior.

---

## Phase 6 — Run the Verify Gate

After the change is applied:

```bash
bash skills/safe-change/scripts/verify-gate.sh
```

Or with a custom root:

```bash
bash skills/safe-change/scripts/verify-gate.sh --root ./backend
```

**Interpret the exit code:**

- Exit 0 — all checks passed, report success to user
- Exit 1 — a check failed. Report which step failed. Do NOT auto-fix silently. Present the error output and ask the user how to proceed.

---

## Monorepo Setup

If the project has separate `backend/` and `frontend/` directories:

```bash
# For a NestJS backend file
node skills/safe-change/scripts/scan-impact.mjs backend/src/users/users.service.ts --root ./backend
bash skills/safe-change/scripts/verify-gate.sh --root ./backend

# For a Next.js frontend file
node skills/safe-change/scripts/scan-impact.mjs frontend/src/components/UserCard.tsx --root ./frontend
bash skills/safe-change/scripts/verify-gate.sh --root ./frontend
```

---

## Piping to Agent Context

If the agent needs to include the raw JSON in a system message:

```bash
node skills/safe-change/scripts/scan-impact.mjs src/auth/auth.service.ts --json
```

The `--json` flag produces identical output but signals scripting intent clearly.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `target file not found` | Path is relative to wrong directory | Use `--root` to set project root explicitly |
| `importers: []` when you know there are importers | File uses barrel re-exports | Check `index.ts` files; see `limitations.md` |
| `routes.endpoints: []` on a known controller | Custom decorator wrapping `@Controller` | See `limitations.md` — manual verification needed |
| `tests.gap: true` but spec exists | Spec does not import target directly | Spec may use a mock factory — manual verification |
