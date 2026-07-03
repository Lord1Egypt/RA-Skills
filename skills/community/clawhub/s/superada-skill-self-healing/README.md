# self-healing

A public OpenClaw skill for making important agent work resilient.

It wraps long-running or fragile work with:

- checkpoint files
- fallback model retries
- watchdog crons
- proof-of-completion requirements
- explicit blocker reporting

## Install

```bash
openclaw skills install github:henrino3/enterprise-crew-skills/self-healing
```

## Use it when

- a remote health check needs to keep going after failures
- a build/deploy/test run may take longer than a direct chat turn
- a subagent might time out or hit model/provider failures
- the operator needs proof before “done” is acceptable

## Core pattern

1. Create `/tmp/self-heal-LABEL.json`.
2. Spawn a worker with checkpoint/resume instructions.
3. Require a proof artifact such as `/tmp/self-heal-LABEL-report.md`.
4. Schedule a recurring watchdog.
5. If the worker dies without proof, respawn with the next fallback model.
6. When proof is verified, disable the watchdog and report the evidence.

See [`SKILL.md`](./SKILL.md) for the full prompt templates and rules.
