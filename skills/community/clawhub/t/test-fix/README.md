# Test Fix — fix failing tests without cheating

[![skills.sh](https://skills.sh/b/WinSoftLabs30/test-fix-skill)](https://skills.sh/WinSoftLabs30/test-fix-skill)

When an AI agent is asked to fix failing tests, the default behavior is an eager intern:
it edits the test to match the broken code, deletes the flaky test, or changes five files
for a one-line bug — and calls it "fixed". This skill turns that into a careful senior dev.

## What it does

1. Runs the suite once and records every failing test.
2. Catches broken test files: a suite that fails to load is reported as a failure, never
   as green.
3. Reruns only the failing files to separate **flaky** (failed, then passed) from
   **consistent** (real failures).
4. Judges each consistent failure: **source bug** or **wrong test** (doubt goes to the
   code).
5. Proposes the smallest patch per failure as a diff in `patches/`, with cause and risk.
6. Waits for approval — it never applies anything on its own. Flaky means report only.

Hard rules baked in: never delete, skip or weaken a test; never edit an assertion before
proving the source is wrong; never apply without explicit approval.

## Install

```
npx skills add WinSoftLabs30/test-fix-skill
```

On ClawHub (OpenClaw): `openclaw skills install @winsoftlabs30/test-fix`, or
`clawhub install @winsoftlabs30/test-fix` with the ClawHub CLI.

Or copy `SKILL.md` into:

- **OpenCode** — `.opencode/skills/test-fix/` in your project, or
  `~/.config/opencode/skills/test-fix/` for every project
- **Claude Code** — `.claude/skills/test-fix/`
- **Other agents** — any that read the `SKILL.md` format (Cursor, Codex, Gemini CLI, ...)

No build step, no dependencies. Any Node version works for this manual edition.

## Use

Ask your agent: **"fix the failing tests"**. The skill loads and follows the workflow.

## Manual edition

This repository is the workflow and the hard rules. The paid edition on Agensi adds two
zero-dependency scripts that do the mechanical part — detect the runner, run once, print
failures as JSON, rerun only the failing files and classify each as flaky or consistent.

## License

MIT-0 — see [LICENSE](LICENSE). Use it, modify it, redistribute it, no attribution
needed. (ClawHub requires MIT-0, so both free channels use one license.)
