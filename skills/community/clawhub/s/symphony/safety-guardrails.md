# Symphony Safety Guardrails

Apply these controls before running unattended orchestration.

## Trust Boundary

Symphony is intended for trusted environments. Treat it as high-privilege automation:
- it reads tracker data continuously
- it executes hook commands
- it runs coding agents with repository write access

Do not run in unknown repositories or unvetted infrastructure.

## Filesystem Safety

- Keep `workspace.root` dedicated to Symphony runs.
- Enforce per-issue workspace directories.
- Never run hook scripts outside the workspace directory.
- Deny destructive cleanup commands that traverse parent directories.

## Hook Safety

- Use `set -euo pipefail` in multiline shell hooks when possible.
- Prefer pinned clone targets and deterministic setup commands.
- Keep secrets in environment variables, not inline in `WORKFLOW.md`.
- Declare required credentials up front (`LINEAR_API_KEY`, OpenAI auth, and Git remote auth).
- Treat hook failures in `after_create` and `before_run` as hard stop signals.

## Agent Safety Defaults

- Start with conservative policy (`approval_policy: on-request` or stricter).
- Use `thread_sandbox: workspace-write` unless a safer profile is available.
- Avoid `danger-full-access` unless the user explicitly approves the risk.
- Keep `max_concurrent_agents` low during first rollout.

## Operational Guardrails

- Use a test Linear project for first deployment.
- Require evidence of one clean end-to-end run before scaling.
- Enable logs and keep snapshots for incident reconstruction.
- Define explicit terminal states to stop orphaned runs.

## Stop Conditions

Pause orchestration immediately when:
- workflow parsing fails repeatedly
- tracker auth is missing or invalid
- hooks cause repeated unsafe side effects
- workspace cleanup targets unexpected paths
