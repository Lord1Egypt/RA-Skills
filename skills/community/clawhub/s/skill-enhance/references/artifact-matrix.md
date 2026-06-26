# Artifact Matrix

Use this file to decide which package artifacts are required.

## Usually Required

- `SKILL.md`
- `agents/openai.yaml`

## Strongly Recommended for Reusable Skills

- `README.md`
- `evals/evals.json`
- focused `references/`

## Often Useful for Release Contexts

- changelog or release-note draft
- packaging notes
- reference checklists

## Decision Rule

If the skill is meant only for one local experiment, keep the package light.
If the skill is meant to be shared, reviewed, or published, the package should be fuller.

