# Coding acceptance: 4 checks

Once the code is written, don't rush into release. Go through these four checks
in order.

## Check 1 — Does the implementation match the design?

You agreed on a design in Stage 2. Now verify the code matches:

- [ ] Is every functional point implemented?
- [ ] Did the AI silently "simplify away" any feature?
- [ ] Are the output format and interaction style what you expected?

**If not aligned**: keep iterating until the implementation matches the design.
Don't advance to the next check until alignment is solid.

---

## Check 2 — Edge case handling

Ask the AI to explicitly cover edge cases:

- [ ] Empty input or malformed input
- [ ] External API / service unavailable
- [ ] File not found, permission denied, other IO errors
- [ ] Dependency skill / tool not installed (clear guidance to user)

**Prompt template**: "Please review this skill's edge case handling. List each
edge case, the current behavior, and any gaps."

---

## Check 3 — Code + doc review (at least 2 passes)

### Pass 1 — Script stability & edge cases

For every file, the AI gives a verdict per checklist item (✅/⚠️/❌):

**Shell scripts**
- [ ] With `set -e` / `set -euo pipefail`, can a `$()` subshell failure
  unintentionally terminate the script? (Common: missing command, broken pipe
  segment) — guard high-risk spots with `|| true` or `|| echo "fallback"`
- [ ] Are external commands (python3, jq, curl, etc.) checked for existence
  with a friendly message on absence, rather than crashing?
- [ ] Before numeric comparison, is the variable validated as a number?
  (`[[ "$VAR" =~ ^[0-9]+$ ]]`)
- [ ] Are path variables hardcoded? Use `${VAR:-default}` fallback.
- [ ] Are files/dirs checked for existence (`[ -f ]` / `[ -d ]`) before use?
- [ ] Under `pipefail`, does every pipe segment exit cleanly?

**Python scripts**
- [ ] Any bare `except:` or `except Exception:` that swallows real errors?
- [ ] File IO wrapped in try/except with clear error messages?
- [ ] Third-party packages bundled or with install instructions?
- [ ] Any string formatting with injection risk (shell command concat, SQL, etc.)?

**SKILL.md docs**
- [ ] Any hardcoded user-specific paths (e.g. `~/username/...`)? Use auto-detect
  or relative paths.
- [ ] When calling other skills (markdown systems, web search, etc.), is the
  fallback path documented for when those skills aren't available?
- [ ] Every file under `references/` referenced from SKILL.md with a clear
  "when to use it" note?
- [ ] Trigger phrases in `description` cover the realistic ways users would
  ask for this skill?

### Pass 2 — Cross-perspective gap-hunt

Re-read every file from the perspective of "a first-time user who has never
seen this skill before":

- [ ] Walking through SKILL.md step by step, is the success/failure criterion
  for each step explicit?
- [ ] In edge conditions (network down, no permission, missing dep), does any
  step hang silently without informing the user?
- [ ] Are there steps the AI would "intuitively skip" but the doc never
  explicitly forbids?
- [ ] Any hardcoded values, swallowed exceptions, or logic dead-ends still
  hiding after Pass 1?

After each pass, the AI must: **list every finding**, propose a concrete fix
for each issue, wait for user confirmation, fix, then re-verify that item.

---

## Check 4 — Smoke tests (at least 2 passes)

Run the skill end-to-end in a real environment.

**Pass 1 (script-level)**: Run every script directly. Check exit codes and
output formats match expectations.

**Pass 2 (functional-level)**: Simulate a real user scenario end-to-end,
covering the happy path plus at least one error scenario.

**Requirements**:
- Tests must run in a real environment, not just "code review by analysis"
- Every test must produce concrete output as evidence
- If a test fails, fix the issue, then re-run **both** passes in full —
  not just the changed part
