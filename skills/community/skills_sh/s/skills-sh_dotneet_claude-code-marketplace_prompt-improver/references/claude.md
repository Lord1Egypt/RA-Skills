# Claude Code Specific Guidance (Additions)

Use this file when the skill is running inside Claude Code. These additions complement the generic guidance in SKILL.md.

## Plan Mode Terminology
- If the task is complex or ambiguous, explicitly request **Plan Mode** first.
- Suggested phrasing: "use Plan Mode to explore, then propose a plan. after approval, implement with tests."

## File/Context Inputs
- Prefer `@path` references (e.g., `@src/auth/index.ts`) over describing locations.
- For large logs or outputs, pipe them in: `cat error.log | claude`.
- Paste screenshots or images directly when visual verification is needed.

## Verification in Claude Code
- Ask for concrete commands to run (tests/build/lint) and expected results.
- For UI changes, request screenshot comparison when possible.

## Parallelism
- If useful, ask to use subagents for research or independent review to keep main context clean.

## Permissions/Docs
- If external docs are needed, include the URL and ask for allowlisting via `/permissions` when required.
