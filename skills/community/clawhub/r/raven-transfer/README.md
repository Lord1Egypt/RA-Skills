# raven-transfer

Wallet-aware Raven Atlas transfer tooling for safe NGN payouts.

This repository packages:

- a transfer command script: `scripts/raven-transfer.mjs`
- skill metadata/config for agent runtimes: `SKILL.md`, `agents/openai.yaml`
- operational references: `references/*.md`
- tests: `tests/*.test.mjs`

## What it does

The script supports:

- wallet balance checks (`--cmd=balance`)
- bank discovery (`--cmd=banks`)
- account lookup (`--cmd=lookup`)
- transfer status checks, including reversal detection (`--cmd=transfer-status`)
- confirmation-gated transfers (`--cmd=transfer`)
- merchant settlement transfers (`--cmd=transfer-merchant`)

All command outputs are JSON with a success/failure envelope.

## Requirements

- Node.js 18+
- One auth source in your environment:
  - `RAVEN_API_KEY_FILE` (preferred, points to a `chmod 600` or `chmod 400` file)
  - `RAVEN_API_KEY`

Optional environment variables:

- `RAVEN_API_BASE` (default: `https://integrations.getravenbank.com/v1`)
- `RAVEN_TIMEOUT_MS` (default: `30000`)
- `RAVEN_READ_RETRIES` (default: `2`)
- `RAVEN_RETRY_DELAY_MS` (default: `300`)
- `RAVEN_DISABLE_LOCAL_STATE=1` (disable on-disk idempotency state)

## Quick start

```bash
mkdir -p "$HOME/.config/raven"
printf '%s\n' "your_raven_api_key_here" > "$HOME/.config/raven/raven_api_key"
chmod 600 "$HOME/.config/raven/raven_api_key"
export RAVEN_API_KEY_FILE="$HOME/.config/raven/raven_api_key"
node ./scripts/raven-transfer.mjs --help
node ./scripts/raven-transfer.mjs --cmd=balance
```

Fallback (direct env injection):

```bash
export RAVEN_API_KEY="your_raven_api_key_here"
```

## Safe payout flow

1. Check funds:
   `node ./scripts/raven-transfer.mjs --cmd=balance`
2. Resolve beneficiary account:
   `node ./scripts/raven-transfer.mjs --cmd=lookup --account_number=<number> --bank_code=<code>`
3. Preview transfer without `--confirm` to get `confirmation_token`.
4. Execute exactly once using `--confirm="CONFIRM TXN_..."`.
5. Re-check settlement:
   `node ./scripts/raven-transfer.mjs --cmd=transfer-status --trx_ref=<trx_ref>`

## Testing

```bash
node ./scripts/validate-skill-package.mjs
node --test ./tests/unit-normalizers.test.mjs
node --test ./tests/contract-live.test.mjs
```

Live tests are gated and skipped unless required env vars are set.

## References

- [workflow](./references/workflow.md)
- [commands](./references/commands.md)
- [safety](./references/safety.md)
- [install](./references/install.md)
