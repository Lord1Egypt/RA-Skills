# Usage Guide

## Typical flow for a medium task

1. Initialize task notes.
   - Run: `python3 /home/nick/.openclaw/workspace/skills/small-context-coding/scripts/init_task.py "fix login timeout" <repo-root>`
2. Fill in `plan.md` with goal, likely files, and verification method.
3. Read only the files needed for the first step.
4. If one subsystem needs isolated investigation, spawn one sub-agent for that subsystem.
5. Make the smallest useful change.
6. Run one targeted verification step.
7. Update `checkpoint.md` before moving to the next phase.

## Typical flow for a large task

1. Initialize task notes.
2. Write a phased plan before editing.
3. Split work into investigation, implementation, and verification.
4. Delegate only bounded subproblems.
5. Keep the main session as coordinator.
6. After each phase, compress findings into `checkpoint.md`.
7. Re-read the checkpoint instead of relying on long chat history.

## Example sub-agent briefs

Generate reusable brief files with:

```bash
python3 /home/nick/.openclaw/workspace/skills/small-context-coding/scripts/generate_subagent_brief.py \
  "fix login timeout" \
  "auth, http client, retry-related files" \
  "pytest -k login_timeout -q" \
  <repo-root>
```

This creates:
- `notes/<task>/subagents/investigation.brief.md`
- `notes/<task>/subagents/implementation.brief.md`
- `notes/<task>/subagents/test.brief.md`

### Investigation
"Trace the login timeout path. Inspect only auth, http client, and retry-related files. Return touched files, key findings, and likely fix points. Do not edit files."

### Implementation
"Implement the agreed timeout fix only in the auth client path. Keep changes minimal. Run the targeted test after editing. Return changed files and any risks."

### Tests
"Add or repair targeted tests for the login timeout behavior. Do not refactor unrelated tests. Return test evidence and any remaining gaps."

## Smoke test

To verify the helper workflow end to end, run:

```bash
python3 /home/nick/.openclaw/workspace/skills/small-context-coding/scripts/smoke_test.py
```

This checks that task notes and sub-agent brief files can be generated from outside the target repo directory.

## When not to use this skill

Do not use the full workflow for trivial one-line edits or simple file reads. In those cases, work directly and verify quickly.
