# Skill Eval Notes for Skill Eval

This folder lets `skill-eval` validate its own authoring-side preflight workflow.

Files:
- `evals.json`: realistic author requests for first-pass skill evaluation
- `triggers.json`: positive and negative trigger checks for the skill description

Before publishing updates:
1. Keep at least one realistic eval case for scaffolding/readiness.
2. Keep both positive and negative trigger cases.
3. Make sure expected artifacts describe observable authoring outcomes.
4. Do not claim live runtime evaluation unless the scripts actually support it.

Recommended commands:
- `python3 ~/.openclaw/skills/skill-eval/scripts/check_eval_readiness.py ~/.openclaw/skills/skill-eval`
- `python3 ~/.openclaw/skills/skill-eval/scripts/run_eval.py ~/.openclaw/skills/skill-eval`
- `python3 ~/.openclaw/skills/skill-eval/scripts/run_eval.py ~/.openclaw/skills/skill-eval --mode without-skill --run-group self-check`
- `python3 ~/.openclaw/skills/skill-eval/scripts/compare_runs.py ~/.openclaw/skills/skill-eval --run-group self-check`
