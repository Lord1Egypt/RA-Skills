---
name: stranger-suite
description: Test whether your documentation actually works for a stranger. Fresh-Eyes follows a project's README exactly, like a brand-new user, and reports the exact step where a real person would give up (missing dependency, missing file, wrong command). Stranger API gives an agent only your API docs and one job, and reports every place the docs alone were not enough. Use when asked to test a README, check getting-started or setup instructions, onboard-test a project, or verify API documentation is complete. Not for code review, security scanning (use skillscan for AI-agent skills), or performance and load testing — this suite tests instructions and documentation, not the code itself.
license: MIT
compatibility: Requires Python 3.12+ and pip. Fresh-Eyes scores fully offline with its built-in planner; an LLM planner is optional and uses your own key (free tiers work) or a local Ollama. Stranger API needs a locally running sandbox API to test against.
---

# Stranger Suite

## What this tool does

Stranger Suite tests instructions, not code. Fresh-Eyes copies a project
into a clean sandbox, runs every README command literally, works around
each failure the way a persistent new user would, and reports every
stuck point — the exact step where a real person would likely quit —
plus a corrected README draft. Stranger API hands an agent nothing but
your API docs and one job against a local sandbox API, and reports
every place the docs alone were not enough.

## Install

```bash
pip install git+https://github.com/RakTikoo/stranger-suite
```

This provides the `fresh-eyes` and `stranger-api` commands (standard
library only).

## Run

Test a project's README (the `--expect` marker is strongly
recommended — it is the text a successful run must print):

```bash
fresh-eyes path/to/project --out report/ --expect TEXT_THE_RUN_MUST_PRINT
```

Test API docs against a locally running sandbox API:

```bash
stranger-api --docs docs.md --base-url http://127.0.0.1:8765 --out report/
```

Both print a short JSON summary and write a plain-language `report.md`
into the `--out` folder.

## Reading the results

Fresh-Eyes verdicts:

- `RUNS CLEAN` — a stranger could follow the README exactly; zero
  stuck points.
- `RUNS WITH STUCK POINTS` — it runs, but only after workarounds; each
  stuck point names the README line, what went wrong, and what fixed it.
- `COULD NOT RUN` — the project did not run; the report gives the
  reasons in order.

Exit codes (both tools): `0` — the project runs, cleanly or with stuck
points (for Stranger API: the job completed). `1` — it could not run,
or the API job did not complete. `2` — bad input (missing folder, bad
URL, unknown preset), with a one-line error and never a traceback.
Without `--expect`, "success" means only that the run command exited 0
— a weak signal; prefer passing a marker.

## Limits

- Fresh-Eyes **runs** the project's own commands. It works on a
  throwaway copy with a scrubbed environment, a command denylist,
  secret redaction and step/time budgets — defence in depth, not an
  OS-level jail. The project's code runs as your user, so only point
  it at code you would run inside a disposable VM.
- The default planner is a rule-based stand-in: it recovers common
  problems (missing deps, files, env vars) but is weaker than the
  optional LLM planner.
- Stranger API refuses non-localhost base URLs on purpose: never
  practise on a production API.
- `--docs` may name a folder; all its .md files are merged, so a mixed
  folder tests the union of the docs, not each file alone.
