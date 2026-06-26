# Stay-Alive Scripts

Start here when editing `scripts/stay-alive/`.

- Stable product docs: `../../docs/stay-alive/README.md`
- Architecture and state model: `../../docs/stay-alive/ARCHITECTURE.md`
- Operator commands: `../../docs/stay-alive/OPERATIONS.md`
- Script category map: `../../docs/stay-alive/CODEMAP.md`
- Chronological implementation notes: `../../docs/stay-alive/DEV_LOG_*.md`

## Edit Rules

- Keep `run-cycle.mjs`, `preflight.mjs`, `life-state-verify.mjs`, and
  `regression-suite.mjs` as the main integration points.
- Add new BotLand access through `botland-adapter/` or the existing policy
  gates; do not shell out from unrelated modules.
- Add new memory backends under `memory-backends/` and keep
  `stay_alive.memory_event.v1` stable.
- Add new `life_state` writes through `life-state-mutation-protocol-lib.mjs`.
- For new artifact lanes, update `artifact-inventory.mjs`,
  `onboarding-lib.mjs`, `docs/stay-alive/CODEMAP.md`, and the relevant
  operations docs in the same change.

## Quick Verification

```bash
node scripts/stay-alive/preflight.mjs --agent lobster-duck --strict-onboarding --no-checkpoint --json
node scripts/stay-alive/regression-suite.mjs --agent lobster-duck --json
git diff --check
```

For BadClaw local mirror checks:

```bash
node scripts/stay-alive/preflight.mjs --agent badclaw --no-checkpoint --json
node scripts/stay-alive/regression-suite.mjs --agent badclaw --json
```
