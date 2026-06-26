# Symphony Setup Runbook

Use this runbook to bootstrap a new Symphony deployment quickly and safely.

## Option A: Reference Elixir Implementation

1. Clone the repository:
   ```bash
   git clone https://github.com/openai/symphony
   cd symphony/elixir
   ```
2. Install runtime dependencies:
   ```bash
   mise trust
   mise install
   mise exec -- mix setup
   mise exec -- mix build
   ```
3. Export tracker credentials:
   ```bash
   export LINEAR_API_KEY=...
   export OPENAI_API_KEY=...
   ```
4. Start Symphony with a workflow file:
   ```bash
   mise exec -- ./bin/symphony ./WORKFLOW.md
   ```

## Option B: Build Your Own Implementation from `SPEC.md`

1. Implement workflow parsing (`WORKFLOW.md` YAML front matter + markdown prompt body).
2. Implement poll loop, candidate selection, and bounded concurrency.
3. Implement per-issue workspace lifecycle with hook execution.
4. Implement coding-agent app-server runner and event streaming.
5. Implement retry queue with exponential backoff and restart-safe recovery.

## Minimum Launch Checklist

- `WORKFLOW.md` parses with valid YAML front matter.
- `tracker.project_slug` and `LINEAR_API_KEY` are set.
- Codex auth is configured (`OPENAI_API_KEY` or active `codex login` session).
- Git credentials are available for the chosen repository remote (SSH key or token).
- Workspace root points to a safe writable directory.
- Hooks are idempotent and scoped to the workspace directory.
- Codex command supports app-server mode.

## First Dry Run

1. Set a low concurrency value (`agent.max_concurrent_agents: 1`).
2. Use a test Linear project with non-production issues.
3. Confirm one issue flows through: poll -> claim -> run -> handoff/terminal.
4. Review logs and runtime snapshot before increasing concurrency.

## Operational Notes

- If workflow parsing fails, dispatch pauses until fixed.
- If an issue becomes terminal while running, Symphony should stop that session and clean up safely.
- Keep all policy changes in version-controlled `WORKFLOW.md` for auditability.
