---
description: "Generate an implementation plan to fix all findings from a security analysis run. Can auto-detect the latest run or target a specific one."
model: opus
---

# Security Analyst — Fix Plan Generator

Generate a structured implementation plan from an existing security analysis report. Each finding becomes an actionable task with fix code, regression tests, and effort estimates.

## Execution

**Read `references/constants.md` for all directory paths, filenames, and placeholder variables.**

### Step 1: Locate the Run

Check if the user provided a run directory path as an argument.

**If a path was provided:** Use it as `RUN_DIR`.

**If no path was provided:** Auto-detect the latest run:
1. List directories under `docs/security/runs/` sorted by name descending (newest first)
2. Pick the first one that contains `reports/final.md`
3. If none found, check for legacy path `docs/security/security-analysis-*.md` and use `docs/security/` as `RUN_DIR`
4. If still none found, tell the user: "No security analysis report found. Run `/security-analyst:full` first."

Set:
- `RUN_DIR` → the identified run directory
- `REPORT_PATH` → `{REPORTS_DIR}/final.md` (or legacy path)

Confirm with the user: "Found security analysis report at `{REPORT_PATH}`. Generate fix plan?"

### Step 2: Spawn Fix-Planner Agent

1. Read `{PROMPTS_DIR}/fix-planner.md`
2. Read `{TEMPLATES_DIR}/fix-plan.md`
3. Spawn agent using Task tool:
   - name: "fix-planner"
   - subagent_type: "general-purpose"
   - prompt: Content of fix-planner.md with placeholders replaced:
     - `{REPORT_PATH}` → absolute path to the security analysis report
     - `{FIX_PLAN_TEMPLATE_PATH}` → absolute path to fix-plan template
     - `{FINDING_TEMPLATE_PATH}` → absolute path to finding template
     - `{OUTPUT_PATH}` → `{REPORTS_DIR}/fix-plan.md`
     - `{RUN_DIR}` → the run directory path
4. Wait for completion

### Step 3: Present Results

1. Read the generated fix-plan
2. Present summary to user:
   - Total tasks generated
   - Quick wins count
   - Breakdown by priority tier (Immediate / Short-term / Medium-term / Backlog)
   - Root cause fixes count
   - Total estimated effort
3. Suggest: "Run the fix plan with `superpowers:executing-plans` or work through tasks manually."

**STOP. The fix plan is complete. Do not take any further actions or continue reasoning. Wait for the user to ask a follow-up question.**

## Output

- `{REPORTS_DIR}/fix-plan.md` — The implementation plan
