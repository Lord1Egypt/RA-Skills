# security Architecture

## Goal

Provide a thin, backend-backed command-safety CLI for live pre-execution safety checks.

## Layout

```text
security/
  SKILL.md
  ARCHITECTURE.md
  scripts/
    safety.py
  modeio_guardrail/
    cli/
      safety.py
  tests/
    test_safety_contract.py
```

## Boundaries

- `scripts/safety.py` is the repo-local wrapper for the live safety CLI.
- `modeio_guardrail/cli/safety.py` owns request shaping, retry behavior, JSON envelope formatting, and CLI flow.
- `tests/` are maintainer contract coverage and stay out of the ClawHub upload surface.

## Runtime flow

1. Accept instruction text plus optional context/target.
2. Call the configured safety backend with retry on transient failures.
3. Normalize the backend payload into the stable success/error envelope.
4. Return a machine-readable decision for the caller to enforce.
