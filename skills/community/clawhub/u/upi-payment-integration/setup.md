# Setup (first use)

Before coding or debugging, confirm these prerequisites.

## 1) Environment and provider

- Provider selected: `<name>`
- Environment selected: `sandbox` or `production`
- Provider docs and dashboard access confirmed

## 2) Secrets and config

Store secrets outside chat and source control.

Required env vars:

- `UPI_PROVIDER_KEY_ID`
- `UPI_PROVIDER_KEY_SECRET`
- `UPI_WEBHOOK_SECRET`
- `UPI_MERCHANT_ID`

Optional but recommended:

- `DATABASE_URL`
- `UPI_RECON_SCHEDULE`
- `UPI_ENV`

## 3) Network and endpoints

- Public HTTPS webhook endpoint available
- Signature verification approach finalized
- IP allowlist / firewall policy reviewed

## 4) Data model readiness

- Payments table with idempotency anchor exists
- Webhook event ledger exists
- Reconciliation audit table exists

## 5) Team ownership

- Engineering owner:
- On-call owner:
- Finance reconciliation owner:
- Support escalation owner:

If any of the above is missing, pause implementation and resolve blockers first.

