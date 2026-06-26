# Forge Console

Forge Console is the product-level command surface for Skill Forge 1.0.

Use it when users or agents need a complete lifecycle rather than a single internal script.

## Command Map

| Command | Purpose | Mutation risk |
| --- | --- | --- |
| `doctor` | Check local readiness: package, Python, OpenClaw path, Telegram config, approval secret, ClawHub, CI, git state | none |
| `demo` | Run the bundled citation-helper example in plan-only mode | none |
| `forge` | Detect, scaffold, validate, evaluate, and optionally request install approval | install only with signed approval |
| `install` | Print or apply an install proposal for a candidate skill | apply requires signed approval |
| `uninstall` | Print or apply uninstall / rollback for an installed skill | apply requires signed approval |
| `feedback` | Record redacted feedback for later evolution | writes feedback JSONL |
| `evolve` | Propose a reviewed update from feedback and replay checks | install only with signed approval |
| `replay` | Score a skill directory against replay cases | none |
| `release-check` | Run release gates and secret scan | none |
| `version` | Print product version | none |

## Product Defaults

- Default install mode is plan-only.
- Telegram approval is required for any install or uninstall mutation.
- Dry-run approval tokens cannot mutate through the pipeline.
- `doctor` should be the first command when onboarding a new machine.
- `demo` should be the first command when validating the installation.
- `release-check` should pass before GitHub tags, ClawHub publishing, or public demos.

## Recommended User Flow

```bash
python3 scripts/skill_forge.py doctor --json
python3 scripts/skill_forge.py demo --json
python3 scripts/skill_forge.py forge --output ./generated --install plan --json
python3 scripts/skill_forge.py release-check --json
```

Only move to `--install telegram` once the plan-only candidate is reviewed.
