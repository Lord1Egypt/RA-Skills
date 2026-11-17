# Order Exception Action List

![Order exception action-list artwork](assets/promo-1600x900.png)

Turn a redacted order-status table, a normal workflow, and SLA rules into a practical human action list. It highlights overdue orders, missing information, and contradictory states, then prioritizes manual review. It never connects to a shop, calls an order API, or sends shipments, refunds, or notices.

## Input and result

Provide a redacted order table with an identifier, current status, status-update time, and available item/previous-status data; the normal state flow; and maximum dwell times plus a review time and timezone.

The Skill returns missing inputs when needed, an exception list, and a manual handling order. Source fields and values remain facts. Recommendations are marked as recommendations. Missing facts are requested rather than invented.

See the [success fixture](fixtures/success.md) and [missing-field fixture](fixtures/failure-missing-fields.md).

## Self-test

```bash
bash scripts/self-test.sh
```

This is a structural package check only: files, fields, image dimensions, and the declared fixtures. Real exception assessment requires real supplied data, workflow, and SLA rules.

## Scope and license

This is a Markdown-only workflow with no browser, login, or third-party API requirement. It produces a review list and does not modify orders. The purpose was informed by [ERPNext](https://github.com/frappe/erpnext) and its [README](https://github.com/frappe/erpnext/blob/develop/README.md); this repository contains original instructions and examples. Licensed under [MIT-0](LICENSE).
