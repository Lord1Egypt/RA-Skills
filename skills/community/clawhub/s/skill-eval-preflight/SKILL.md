---
name: skill-eval-preflight
description: Validate OpenClaw skills during authoring. Use when creating, revising, or preparing a skill for release and you need to scaffold `evals/` files, check readiness for a first eval pass, review whether the frontmatter description has clear trigger coverage, or generate static comparison artifacts before deeper runtime evaluation.
---

# Skill Eval

Use this skill as an **authoring-side preflight** for OpenClaw skills.

It is not a full runtime evaluator. It helps a skill author move from "this skill exists" to "this skill is structured well enough for first-pass evaluation and later regression work."

## Good Requests

This skill is a good fit for requests like:

- "Set up eval files for this skill before I publish it."
- "Check whether this skill is ready for a first eval pass."
- "Review the description and tell me whether trigger coverage is clear enough."
- "Generate with-skill and without-skill static comparison artifacts for this skill."

## Not A Good Fit

Do not rely on this skill alone for requests like:

- large-scale live runtime benchmarking
- scoring response quality across many real conversations
- tool-call correctness or factuality audits
- end-to-end production regression testing

Use a deeper evaluator after this step when you need those capabilities.

## Best Fit

Use this skill when you need to:

- initialize `evals/` files for a new or existing skill
- confirm a skill is ready for a first eval pass
- make positive and negative trigger coverage explicit
- catch placeholder content before sharing a skill
- write static run summaries and with-skill/without-skill comparison artifacts

Use a deeper evaluator after this step when you need live runtime experiments, tool-call quality checks, or richer output scoring.

## Position In The Flow

Recommended sequence:

`skill-vetter -> install/review -> skill-eval -> deeper runtime eval`

- `skill-vetter` answers: "Is this skill safe enough to inspect or install?"
- `skill-eval` answers: "Is this skill structured well enough to evaluate seriously?"
- a deeper evaluator answers: "How well does the skill perform in practice?"

## Workflow

1. Confirm the target folder is a skill directory with `SKILL.md`.
2. If the skill came from another repo or another person, do a safety review first.
3. If `evals/` does not exist, initialize it with:
   - `evals/evals.json`
   - `evals/triggers.json`
   - `evals/README.md`
4. Replace placeholder prompts with realistic authoring examples.
5. Run the readiness check before any deeper benchmarking.
6. If readiness fails, fix the missing pieces first instead of forcing a run.
7. Generate static run artifacts only after the inputs are usable.

## Scripts

Initialize eval files:

```bash
python3 scripts/init_eval.py /path/to/skill
```

Check readiness:

```bash
python3 scripts/check_eval_readiness.py /path/to/skill
```

Run static eval checks:

```bash
python3 scripts/run_eval.py /path/to/skill
python3 scripts/run_eval.py /path/to/skill --check readiness
python3 scripts/run_eval.py /path/to/skill --check triggers
python3 scripts/run_eval.py /path/to/skill --check artifacts
python3 scripts/run_eval.py /path/to/skill --check files
python3 scripts/run_eval.py /path/to/skill --mode with-skill
python3 scripts/run_eval.py /path/to/skill --mode without-skill --run-group demo-baseline
python3 scripts/compare_runs.py /path/to/skill --run-group demo-baseline
```

## Readiness Rules

A skill is ready for first-pass evaluation only when:

- `SKILL.md` exists
- the frontmatter `description` is real and not a placeholder
- `evals/evals.json` has at least one non-placeholder eval case
- `evals/triggers.json` has at least one positive and one negative non-placeholder trigger case

## What This Skill Checks Well

- missing or empty eval scaffolding
- placeholder prompts that would make an eval meaningless
- missing positive/negative trigger coverage
- empty or malformed `expected_artifacts`
- malformed optional `files` declarations
- static with-skill/without-skill run artifact organization

## Current Limits

`run_eval.py` does **not** perform live trigger experiments against the OpenClaw runtime.
It does **not** score real outputs for quality, factuality, or tool correctness.

Today it performs static validation passes that:

- verify trigger files exist
- verify cases are non-placeholder
- verify positive and negative sets are both populated
- verify eval cases have usable `expected_artifacts`
- verify declared `files` entries are well-formed
- write mode-specific run summaries for later comparison

## Why Publish This Skill

This skill is for authors who do not yet need a full eval lab, but do need a clean starting point.
It is most useful as a lightweight preflight and scaffolding step before deeper evaluation.

## Release Readiness Checklist

Before calling a skill "ready for release," aim for all of the following:

- the description names concrete trigger scenarios
- positive and negative trigger cases both exist
- placeholder content is gone
- each eval case describes observable expected artifacts
- static run summaries can be generated without errors

## Compare Runs

Use `compare_runs.py` after both modes exist in the same `run-group`.

It compares:

- overall pass/fail
- per-check pass/fail
- mode-specific errors
- mode-specific notes

It writes comparison artifacts under the run-group root.

## References

Read [references/eval_format.md](references/eval_format.md) when you need the expected file formats and field meanings.
