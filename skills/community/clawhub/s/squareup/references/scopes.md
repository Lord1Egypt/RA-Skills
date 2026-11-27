# Square scopes

The OAuth scopes Square connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/squareup#permissions.

```bash
maton connection create squareup --scopes PAYMENTS_READ
```

| Scope | Requested |
| --- | --- |
| `PAYMENTS_WRITE` | By default |
| `PAYMENTS_READ` | By default |
| `CUSTOMERS_READ` | By default |
| `CUSTOMERS_WRITE` | By default |
| `ORDERS_READ` | By default |
| `ORDERS_WRITE` | By default |
| `ITEMS_READ` | By default |
| `ITEMS_WRITE` | By default |
| `BANK_ACCOUNTS_WRITE` | By default |
| `BANK_ACCOUNTS_READ` | By default |
| `PAYOUTS_READ` | By default |
| `INVOICES_WRITE` | By default |
| `INVOICES_READ` | By default |
| `LOYALTY_READ` | By default |
| `EMPLOYEES_READ` | By default |
| `TIMECARDS_READ` | By default |
| `TIMECARDS_WRITE` | By default |
| `TIMECARDS_SETTINGS_READ` | By default |
| `TIMECARDS_SETTINGS_WRITE` | By default |
| `APPOINTMENTS_READ` | By default |
| `APPOINTMENTS_WRITE` | By default |
| `APPOINTMENTS_ALL_READ` | By default |
| `APPOINTMENTS_ALL_WRITE` | By default |
| `APPOINTMENTS_BUSINESS_SETTINGS_READ` | By default |
| `MERCHANT_PROFILE_READ` | Always |
