# Changelog

## 0.1.1

- make `init_relic.py` non-destructive on re-run so existing vault files are preserved
- repair malformed `manifest.json` during capture instead of failing note writes
- skip malformed NDJSON inbox lines during distillation instead of aborting the run
- add regression tests for init idempotency, capture recovery, confidence bounds, and malformed inbox handling

## 0.1.0

- initial ClawHub/OpenClaw release of the Relic skill package
- bundled optional `relic-capture` hook for passive capture on `agent:stop`
- local-first vault workflow for capture, distillation, proposals, drift detection, and export
- portable `RELIC_VAULT_PATH` contract across scripts and hooks
- package docs, tests, and metadata aligned for publication
