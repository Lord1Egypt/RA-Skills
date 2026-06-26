# Publish Readiness

Use this file when the goal is to prepare a skill for sharing or release.

## Minimum Readiness Checklist

Before calling a skill publish-ready, check:

- the skill name is stable and understandable
- the description is strong enough for discovery
- `SKILL.md` is coherent and actionable
- `README.md` exists if humans will evaluate or install it
- `agents/openai.yaml` exists if metadata is needed
- `evals/evals.json` exists when the skill benefits from validation prompts
- references are sufficient for the intended workflow

## Readiness Levels

- **Draft**: early structure, still incomplete
- **Internally usable**: useful in one project, still rough
- **Release-candidate**: coherent package with validation material
- **Publish-ready**: clear package, clear docs, clear triggers, clear artifacts

## Important Rule

Do not call a skill publish-ready only because the validator passes.

