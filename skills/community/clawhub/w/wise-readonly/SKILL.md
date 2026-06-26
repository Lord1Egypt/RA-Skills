---
name: wise-readonly
description: Read-only Wise API operations for account inspection, FX lookups, recipients, and transfer history. Use when asked to list profiles, balances, recipients, transfers, quotes, delivery estimates, or check current/historical rates without creating transfers, recipients, quotes, or any other mutable resources.
---

Read-only Wise API skill for OpenClaw.

## Requirements
- `WISE_API_TOKEN` environment variable.
- Network access from the runtime host to `https://api.wise.com`.

## Supported Commands
- `list_profiles` (PII-redacted by default)
- `get_profile --profile-id <id>` (PII-redacted by default)
- `list_balances --profile-id <id> [--types STANDARD,SAVINGS]`
- `get_balance --profile-id <id> --balance-id <id>`
- `get_exchange_rate --source <CUR> --target <CUR>`
- `get_exchange_rate_history --source <CUR> --target <CUR> --from <ISO> --to <ISO> [--group day|hour|minute]`
- `get_temporary_quote --source <CUR> --target <CUR> [--source-amount <N> | --target-amount <N>]`
- `get_quote --quote-id <id>`
- `list_recipients --profile-id <id> [--currency <CUR>]` (PII-redacted by default)
- `get_recipient --account-id <id>` (PII-redacted by default)
- `get_account_requirements --source <CUR> --target <CUR> --source-amount <N>`
- `list_transfers --profile-id <id> [--status <s>] [--created-date-start <ISO>] [--created-date-end <ISO>] [--limit <N>] [--offset <N>]` (PII-redacted by default)
- `get_transfer --transfer-id <id>` (PII-redacted by default)
- `get_delivery_estimate --transfer-id <id>`

Command runner:
- `scripts/wise_readonly.mjs`

## Privacy and Safety
- Profile/recipient/transfer responses redact common PII fields by default.
- Add `--raw` only when strictly necessary.
- This skill performs no write operations.
- Disallowed operations include quote creation, transfers, recipient create/update/delete, funding, and cancellation.

## Quick Test
```bash
export WISE_API_TOKEN=...
node scripts/wise_readonly.mjs list_profiles
node scripts/wise_readonly.mjs list_balances --profile-id <id>
node scripts/wise_readonly.mjs get_exchange_rate --source GBP --target EUR
```

## Release Notes
### 1.0.3
- Expanded read-only API coverage based on `wise-mcp` patterns.
- Added read-only commands for balances, recipients, transfers, quote lookup, delivery estimate, and historical rates.
- Kept strict no-write policy (no create/fund/cancel/delete operations).
- Improved metadata clarity for ClawHub and OpenClaw UI.

### 1.0.2
- Added ClawHub secret metadata (`WISE_API_TOKEN` required/primary).
- Added explicit UI policy to disable implicit invocation by default.

### 1.0.1
- Added PII redaction defaults and sanitized error handling.
- Removed write-capable quote creation path.

### 1.0.0
- Initial read-only profile/balance/rate implementation.

## Source Reference
This skill extends read-only coverage using endpoint/tool patterns from:
https://github.com/Szotasz/wise-mcp

## Acknowledgements
This skill is inspired by wise-mcp by Szotasz:
https://github.com/Szotasz/wise-mcp
