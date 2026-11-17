# paypal-reconcile

ClawHub-ready OpenClaw skill for fast, read-only PayPal reconciliation.

## Version
1.0.1

## Main optimization
Single-transaction lookups now use:
- target date ±3 days
- one-pass transaction-list extraction
- browser evaluate or scoped/efficient snapshots
- only plausible candidate detail pages

It must not switch to a full-year view for a normal lookup.

## Browser profile
Expected persistent profile:

`alibaba`

## Install
Copy the folder into:

`~/.openclaw/workspace/skills/`

Then restart OpenClaw if needed.

## Test

```bash
openclaw agent --agent main --message "/paypal-reconcile Find the PayPal transaction for USD 325.00 around May 20, 2026. Read-only."
```

## Publish to ClawHub

```bash
clawhub skill publish ./paypal-reconcile \
  --slug paypal-reconcile \
  --name "PayPal Reconcile" \
  --version 1.0.1 \
  --changelog "Optimize transaction lookup with narrow date windows and single-pass extraction"
```

Use `--dry-run` first if desired.

No passwords, cookies, OTPs, or browser state are included.
