# Workflow

Follow this exact sequence for every payout.

## 1) Collect transfer intent

Capture:

- target type: `bank` or `merchant`
- amount (NGN)
- expected fee estimate (NGN)
- bank name and optional bank code
- account number
- narration
- merchant name (for merchant payouts)
- optional caller-supplied merchant reference

## 2) Validate wallet funds

Run:

```bash
node ./scripts/raven-transfer.mjs --cmd=balance
```

Confirm `available_balance` covers `amount + expected_fee`.

## 3) Resolve recipient identity

If bank code/name is unknown, search:

```bash
node ./scripts/raven-transfer.mjs --cmd=banks --search="GTBank"
```

Resolve account holder:

```bash
node ./scripts/raven-transfer.mjs --cmd=lookup --account_number=0690000031 --bank_code=058
```

## 4) Request confirmation token

Run transfer command without `--confirm`.

Example:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer --amount=5000 --bank="GTBank" --bank_code=058 --account_number=0690000031 --account_name="John Doe" --expected_fee=50 --merchant_ref="INV-182"
```

The script returns:

- `status=requires_confirmation`
- `confirmation_token`
- echo of recipient, amount, fee, total debit, projected post-balance

## 5) Execute transfer once

Submit with the exact confirmation token:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer --amount=5000 --bank="GTBank" --bank_code=058 --account_number=0690000031 --account_name="John Doe" --expected_fee=50 --merchant_ref="INV-182" --confirm="CONFIRM TXN_..."
```

Use the same pattern for `transfer-merchant` with `--merchant`.

## 6) Report outcome

Always report:

- `trx_ref`
- `merchant_ref`
- `fee`
- `total_debit`
- `status`
- `raw_status`

If `status=pending`, include settlement guidance and avoid duplicate send.

## 7) Re-check settlement status

Before concluding reconciliation (or before any resend decision), fetch current transfer state:

```bash
node ./scripts/raven-transfer.mjs --cmd=transfer-status --trx_ref=<trx_ref>
```

If status returns `reversed`:

- stop any automatic resend
- notify user that the transfer reversed
- create a fresh transfer only after explicit user approval
