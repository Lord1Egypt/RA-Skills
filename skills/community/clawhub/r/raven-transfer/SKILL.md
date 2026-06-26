---
name: raven-transfer
description: Wallet-aware Raven Atlas transfer operations for NGN payouts. Use when an agent must check wallet balance, resolve Nigerian bank accounts, enforce explicit confirmation tokens, and execute idempotent confirmed transfers to bank beneficiaries or merchant settlement accounts.
---

# Raven Transfer Skill

Execute safe NGN payouts through Raven Atlas.

## Package artifacts

- `scripts/raven-transfer.mjs` (transfer CLI implementation)
- `agents/openai.yaml` (runtime metadata and env requirements)
- `references/*.md` (workflow, command contract, safety, install)
- `tests/*.test.mjs` (unit and live-contract checks)

## Use this skill process

1. Identify payout target type: `bank` or `merchant`.
2. Validate funding by checking NGN wallet balance before any transfer.
3. Resolve account name from account number and bank input.
4. Request explicit confirmation token from transfer preview.
5. Execute transfer exactly once with `--confirm="CONFIRM TXN_..."`.
6. Report normalized result fields (`available_balance`, `fee`, `total_debit`, `status`, `raw_status`).

Do not skip confirmation token checks. Do not auto-retry transfer submission.
Failed transfer note: yes, a failed Raven transfer is typically auto-reversed/refunded after a few minutes; wait, then re-check `transfer-status` and wallet balance before any retry.

## Required environment

- One auth source must be available in the runtime environment:
  - `RAVEN_API_KEY_FILE` (preferred, points to a `chmod 600`/`chmod 400` file)
  - `RAVEN_API_KEY`
- Optional runtime overrides:
  - `RAVEN_API_BASE` (default: `https://integrations.getravenbank.com/v1`)
  - `RAVEN_TIMEOUT_MS` (default: `30000`)
  - `RAVEN_READ_RETRIES` (default: `2`)
  - `RAVEN_RETRY_DELAY_MS` (default: `300`)
- Optional safety hardening:
  - `RAVEN_DISABLE_LOCAL_STATE=1` disables on-disk transfer state.

## Invocation policy

- Implicit model invocation should be disabled for this skill.
- Invoke explicitly with `$raven-transfer` when a transfer workflow is required.

## Run commands

Run all commands from this skill folder with:

```bash
node ./scripts/raven-transfer.mjs --cmd=<command> [flags]
```

Available commands:

- `balance`: check wallet balances and normalize NGN availability.
- `banks`: list banks (optional `--search`).
- `lookup`: resolve account name (`--account_number` plus `--bank` or `--bank_code`).
- `transfer-status`: fetch latest transfer status by `trx_ref`/`merchant_ref` and detect reversals.
- `transfer`: preview or execute bank transfer with confirmation token.
- `transfer-merchant`: preview or execute merchant settlement transfer.

## Merchant payouts

Treat a merchant payout as a normal bank transfer to the merchant settlement account.

Required merchant transfer details:

- merchant name
- merchant settlement bank name and bank code
- merchant settlement account number
- resolved account name from lookup
- amount
- expected fee estimate for pre-check
- narration

## Reference files

Read these before execution when needed:

- [references/workflow.md](references/workflow.md): deterministic execution workflow.
- [references/commands.md](references/commands.md): command flags and normalized output contract.
- [references/safety.md](references/safety.md): retry, idempotency, and duplicate prevention rules.
- [references/install.md](references/install.md): Codex and generic installation patterns.
