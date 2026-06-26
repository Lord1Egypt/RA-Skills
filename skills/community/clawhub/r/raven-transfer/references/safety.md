# Safety and Reliability

## Required controls

- Always run `balance` before transfer.
- Always run `lookup` to resolve account name.
- Always require confirmation token flow before submit.
- Always perform pre-transfer check `available_balance >= amount + expected_fee`.
- Always use idempotency reference (`merchant_ref`) and duplicate-intent checks.
- Always run `transfer-status` for settlement verification before any resend decision.
- Never print raw secrets in command output; redact token-like values and sensitive keys.

## Retry policy

Automatic retries are allowed only for read operations:

- `balance`
- `banks`
- `lookup`

Transfer operations must never auto-retry:

- `transfer`
- `transfer-merchant`

If transfer fails, return actionable guidance and require fresh user confirmation.

## Idempotency policy

- Support caller-supplied `merchant_ref`.
- Reject duplicate `merchant_ref` values from local transfer state.
- Persist only minimal idempotency fields in `scripts/.state/transfer-state.json`:
  - refs: `merchant_ref`, `trx_ref`, `intent_hash`, `status`, `raw_status`, `amount`, `fee`, timestamps
  - intents: `intent_hash`, `merchant_ref`, `trx_ref`, `status`, `raw_status`, `amount`, `fee`, `updated_at`
- Never persist account name, account number, or raw provider payloads.
- Set file permissions to owner-only and avoid syncing `.state` to backups/repositories.
- Set `RAVEN_DISABLE_LOCAL_STATE=1` to disable local state persistence entirely.
- Reject repeated intent hashes with in-flight/successful statuses to prevent accidental double-send.

## Failure handling

When `ok=false`:

1. Show the `error` value.
2. Show `raw.retry_guidance`.
3. Ask user whether to retry read command or re-confirm transfer.

## Pending settlement guidance

If result status is `pending`, treat payout as submitted but not settled.

- Do not send again immediately.
- Verify settlement state via transfer reference before any retry.

## Reversal handling

If `transfer-status` returns `status=reversed`:

1. Treat payout as reversed.
2. Do not auto-resend.
3. Ask user for explicit approval before any new transfer.
