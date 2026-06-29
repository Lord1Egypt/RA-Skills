# Context Loading Policy

Skill2Team 1.9.2 follows a lean Skill Creator layout. `SKILL.md` contains only trigger-critical behavior. All long guidance is loaded on demand.

## Rule

Read the smallest set of supporting files needed for the active user request. Do not preload all references, data, prompts, assets, or scripts.

## Load map

| Request | Supporting context |
|---|---|
| Startup only | `references/startup-page.md`, `references/startup-routing.md` |
| Design | `references/design-workflow.md`, `references/agent-architecture-and-workflow-method.md`, `references/orchestration-design.md`, `references/flow-control-and-resume.md`, `references/design-package-conformance-and-reexecution.md`, `references/output-contracts.md`, `references/local-resource-allocation.md` |
| Package | `references/package-workflow.md`, `references/package-to-register-readiness.md`, `references/agent-registration-and-entrypoints.md`, `references/runtime-invocation-and-prompt-rewrite.md`, `references/target-team-execution-guard.md`, `references/team-usage-guide.md`, `references/design-package-conformance-and-reexecution.md`, `references/local-resource-allocation.md`, `assets/prompt-templates/` |
| Meta-team-first | `data/meta_team_contract.json`, `references/meta-team-execution.md`, `references/design-package-conformance-and-reexecution.md` |
| ClawHub / OpenClaw / Skill Creator packaging | `references/skill-creator-packaging.md`, `references/mit0-openclaw-clawhub-compliance.md`, `references/clawhub-publish-checklist.md` |
| Deterministic package generation | `scripts/generate_deployment_package.py` and the requested plan file only |
| Local package QA | `scripts/validate_package.py` only |

## Output discipline

Summarize loaded context. Do not paste full reference contents unless the user asks for the reusable text.
