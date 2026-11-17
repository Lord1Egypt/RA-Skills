# Workflow Gating Detail

The full step-by-step workflow lives in `SKILL.md` (Execution Workflow). This file only supplements the per-step default-deny gating details, to avoid duplication with `SKILL.md`.

## Scan Disclosure

The batch system scan (`scan_all.*`) is **skipped entirely without explicit consent** (prints a notice, exits 0, no output). With consent (set `STATSOFT_AUTO_WRITE` to `1`, or `STATSOFT_CONFIRM` to `1` plus an interactive `y`) it returns the full `{path, version}` JSON. `STATSOFT_REVEAL` governs **per-software setup** output only — it does not affect the batch scan.

## Persistence Gate

`config.json` is written only with explicit authorization: set `STATSOFT_AUTO_WRITE` to `1` (non-interactive / agent) or `STATSOFT_CONFIRM` to `1` plus an interactive `y`. All writes go through `scripts/common/write_config.py`:

- Accepts either canonical `config.json` (skill root **or** `scripts/windows-only/`) as the target, and **mirrors the write to the other canonical location** so the two never diverge (fail-closed, dual-canonical);
- Before writing, takes a timestamped backup `config.json.bak.yyyymmdd_hhmmss`, then atomically replaces.

Persistence happens only with explicit opt-in (set `STATSOFT_AUTO_WRITE` to `1`, or `STATSOFT_CONFIRM` to `1` plus an interactive `y`). All writes go through `scripts/common/write_config.py`, which enforces a single canonical target and a timestamped backup before atomic replace.

## Third-party Binaries

Launching third-party binaries solely for version/checksum verification requires `STATSOFT_VERIFY` set to `1`; compiling and running a user-supplied Stan model (untrusted native code) requires `STATSOFT_CMDSTAN_RUN` set to `1`.
