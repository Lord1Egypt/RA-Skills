# Error and Anti-Fabrication Reference

## Anti-Fabrication Rules (P0)

1. Use script stdout/stderr and exit code as the only source of truth.
2. Do not fabricate fields, values, statuses, timestamps, or IDs.
3. Do not infer unavailable fields; explicitly say the field is not returned.
4. Keep numeric precision unless user explicitly asks for rounding.
5. Preserve pagination fields: `total`, `page`, `pageSize`.
6. When script fails, report raw error first, then recovery command.

## Common Error Categories

### Auth/Config

- Missing `QE_API_KEY` / `QE_API_SECRET`
- Invalid credentials / permission issues

### Parameter Validation

- Missing required parameters
- Conflicting parameters (`--total-quantity` vs `--order-notional`)
- Invalid enum values or malformed timestamps

### Data Lookup

- Invalid symbol
- Invalid exchange
- Missing order ID
- Invalid `api-key-id`

### Business State

- Order state disallows operation (for example canceling a non-cancelable order)
- Insufficient balance/margin

### Network/Upstream

- Timeout, transport errors, upstream API failures

## Handling Pattern

1. Return raw script error.
2. Do not speculate on hidden causes.
3. Provide the next concrete retry/check command.
4. Keep response tied to the exact command that produced the output.
