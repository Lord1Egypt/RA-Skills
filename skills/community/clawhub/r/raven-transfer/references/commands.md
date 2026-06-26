# Command Reference

## Common

- Script: `node ./scripts/raven-transfer.mjs`
- Auth source: one of `RAVEN_API_KEY_FILE` (preferred) or `RAVEN_API_KEY`
- Optional hardening env var: `RAVEN_DISABLE_LOCAL_STATE=1`
- Output format: JSON object

Success envelope:

- `{"ok": true, ...}`

Failure envelope:

- `{"ok": false, "error": "...", "raw": {...}}`

Normalized fields used across commands:

- `available_balance` (NGN available balance when known)
- `fee`
- `total_debit`
- `status` (normalized)
- `raw_status` (provider value when available)

## `--cmd=balance`

Fetch wallet balances with compatibility for old and new Raven payloads.

Example:

```bash
node ./scripts/raven-transfer.mjs --cmd=balance
```

Output includes:

- `wallets`
- `available_balance` (NGN)
- `balance` (NGN)
- `status`, `raw_status`, `fee`, `total_debit`

## `--cmd=banks`

Optional:

- `--search=<keyword>`

Example:

```bash
node ./scripts/raven-transfer.mjs --cmd=banks --search="gt"
```

Output includes:

- `banks`: list of `{ "name": string, "code": string }`

## `--cmd=lookup`

Required:

- `--account_number=<number>`
- one of `--bank=<name_or_code>` or `--bank_code=<code>`

Example:

```bash
node ./scripts/raven-transfer.mjs --cmd=lookup --account_number=0690000031 --bank_code=058
```

Compatibility behavior:

- Sends `bank` field in request body for current Raven contract.
- Also includes `bank_code` when supplied for compatibility.

Output includes:

- `account_name`
- `account_number`
- `bank`
- normalized status fields

## `--cmd=transfer-status`

Check latest transfer state (including reversal) using Raven single-transaction API.

Required:

- one of `--trx_ref=<ref>` or `--merchant_ref=<ref>`

Behavior:

- If only `--merchant_ref` is passed, the script resolves `trx_ref` from local state.
- Queries `GET /get-transfer?trx_ref=<ref>`.
- Updates local transfer state with latest status using a strict allowlist of non-PII fields.
- If `RAVEN_DISABLE_LOCAL_STATE=1`, pass `--trx_ref` directly because `merchant_ref` resolution from local state is unavailable.

Example:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer-status --trx_ref=rav_9f2f...
```

Output includes:

- `trx_ref`
- `merchant_ref`
- `status`
- `raw_status`
- `settlement_guidance`
- `checked_at`

## `--cmd=transfer`

Required:

- `--amount=<number>`
- `--bank=<bank_name>`
- `--account_number=<number>`
- `--account_name=<resolved_name>`

Optional:

- `--bank_code=<code>`
- `--expected_fee=<number>` (defaults to `0`)
- `--merchant_ref=<idempotency_ref>`
- `--narration=<text>`
- `--currency=NGN`
- `--confirm="CONFIRM TXN_..."`

Flow:

1. First call without `--confirm` returns `status=requires_confirmation` and `confirmation_token`.
2. Re-run same payload with `--confirm` token to submit transfer.

Example preview call:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer --amount=5000 --bank="GTBank" --bank_code=058 --account_number=0690000031 --account_name="John Doe" --expected_fee=50 --merchant_ref="INV-182"
```

Example execution call:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer --amount=5000 --bank="GTBank" --bank_code=058 --account_number=0690000031 --account_name="John Doe" --expected_fee=50 --merchant_ref="INV-182" --confirm="CONFIRM TXN_ABC123DEF456"
```

Execution output includes:

- `trx_ref`
- `merchant_ref`
- `available_balance`
- `fee`
- `total_debit`
- `projected_post_balance`
- `status`
- `raw_status`
- `settlement_guidance`
- `status_check_command`

## `--cmd=transfer-merchant`

Same as `transfer`, plus required:

- `--merchant=<merchant_name>`

Example preview:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer-merchant --merchant="Acme Stores" --amount=5000 --bank="GTBank" --bank_code=058 --account_number=0690000031 --account_name="Acme Stores Ltd" --expected_fee=50 --merchant_ref="SETTLE-ACME-182"
```
