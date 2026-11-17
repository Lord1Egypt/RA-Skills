# Onboarding — references/onboarding.md

`scripts/onboarding.py` turns a fresh checkout into a running, verified
installation. It is interactive by design: several steps must be performed by
a human at a keyboard.

## Steps

### 0. Preflight — `install.sh`

```bash
bash skills/swarm-arena/install.sh
```

Checks: Python ≥ 3.10; all 27 scripts present and `py_compile`-clean; config
parses and validates; credentials visible in env (warning only in paper mode);
`lighter-sdk` importable (hard requirement only for `live` /
`autonomous_live`). Paper mode needs zero third-party packages.

### 1. Credentials (env-first, never stored)

Read from the environment first; prompted only when missing:

| Variable | Notes |
|---|---|
| `LIGHTER_API_PRIVATE_KEY` | prompted via `getpass` (no echo) |
| `LIGHTER_API_KEY_INDEX` | integer 2–254, from the Lighter UI |
| `LIGHTER_ACCOUNT_INDEX` | integer; auto-discovered from `LIGHTER_L1_ADDRESS` when provided |
| `LIGHTER_L1_ADDRESS` | optional; drives `accountsByL1Address` discovery |

All output masks secrets to the last 4 characters (`...a1b2`). Credentials are
never written to any file — not the config, not state, not logs.

### 2. Live verification (fail hard)

For `live` and `autonomous_live` modes only, onboarding must prove the
credentials work before writing anything:

1. Mint an auth token via the SDK (`create_auth_token_with_expiry`).
2. Read the account (`GET /api/v1/account?by=index&value=...`) with that token.

Any failure is fatal: **no `config.json` is written.** Paper/approval modes
skip this step entirely.

### 3. Risk parameters

Prompts with sane defaults: allowed symbols (`ETH,BTC,SOL`), base value per
trade ($100), leverage bounds (2–10, client-side caps), max notional per trade
($500), max total exposure ($2000), max daily loss ($100), allow shorts (yes).

### 4. Consent gate (one-way)

`autonomous_live` is offered only here. Enabling it requires typing exactly:

```
ACCEPT
```

- Non-TTY stdin → consent refused by default.
- This is the **only** code path in the entire skill that can set
  `autonomous_live_consent: true`. All other scripts read it; none write it.
- `resume.py --mode autonomous_live` checks the latch; it cannot create it.
- To revoke: halt, then delete `config.json` and re-onboard (or edit the file
  by hand — it is yours).

### 5. Write + schedule + first cycle

- `config.json` written atomically with permissions `0600`.
- `register_crons.py` prints ready-to-paste crontab lines.
- Optional immediate first cycle (`autonomous_runner.py`), typically a paper
  scan to prove the pipeline end-to-end.

## After onboarding

```bash
python3 scripts/status.py config.json          # health check
python3 scripts/autonomous_runner.py config.json   # manual cycle
```

Export credentials in the environment that runs cron (systemd
`EnvironmentFile`, launchd wrapper, or your shell profile) before switching to
a live mode.
