# Installation

Install this as a folder named `raven-transfer` that contains:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/raven-transfer.mjs`
- `references/*.md`
- `tests/*.test.mjs`

## Codex-style install

Place the folder in your skills directory:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R ./raven-transfer "$CODEX_HOME/skills/raven-transfer"
```

Store API key in macOS Keychain (one-time setup):

```bash
security add-generic-password -a "$USER" -s "raven-api-key" -w "RVSEC-..." -U
```

Inject key into a permission-locked file before running commands:

```bash
mkdir -p "$HOME/.config/raven"
security find-generic-password -a "$USER" -s "raven-api-key" -w > "$HOME/.config/raven/raven_api_key"
chmod 600 "$HOME/.config/raven/raven_api_key"
export RAVEN_API_KEY_FILE="$HOME/.config/raven/raven_api_key"
```

Optional direct env injection (without writing plaintext in shell history):

```bash
export RAVEN_API_KEY="$(security find-generic-password -a "$USER" -s "raven-api-key" -w)"
```

## Generic agent install

Install the same folder into the agent's configured skills path.

Requirements:

- Node.js 18+ runtime
- One of:
  - `RAVEN_API_KEY_FILE` pointing to a key file with strict owner-only permissions (`chmod 600` or `chmod 400`)
  - `RAVEN_API_KEY` injected at runtime by a secret manager
- Optional:
  - `RAVEN_API_BASE`, `RAVEN_TIMEOUT_MS`, `RAVEN_READ_RETRIES`, `RAVEN_RETRY_DELAY_MS`
  - `RAVEN_DISABLE_LOCAL_STATE=1` to disable local state persistence

Example secret-manager injection pattern:

```bash
export RAVEN_API_KEY="$(
  <secret-manager-cli> read raven/api-key
)"
```

Security notes:

- Local idempotency state is written to `scripts/.state/transfer-state.json` with owner-only permissions.
- Add `scripts/.state/` to ignore/sync exclusions so runtime transfer metadata is not committed or backed up unintentionally.

## Post-install checks

Run from the skill folder:

```bash
node ./scripts/raven-transfer.mjs --help
node ./scripts/validate-skill-package.mjs
node --test ./tests/unit-normalizers.test.mjs
node --test ./tests/contract-live.test.mjs
```

Live contract tests are gated and skipped by default. To run them, set:

- `RAVEN_CONTRACT_TESTS=1`
- `RAVEN_TEST_ACCOUNT_NUMBER` and `RAVEN_TEST_BANK` (or `RAVEN_TEST_BANK_CODE`) for lookup contract tests

The transfer create contract test is intentionally hard-gated to avoid accidental money movement.
