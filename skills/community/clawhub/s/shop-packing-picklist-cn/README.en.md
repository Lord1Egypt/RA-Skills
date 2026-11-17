# Shipping Pick-and-Pack Checklist

Turn sanitized orders into a Markdown checklist for warehouse verification: per-order picks, confirmed kit components, aggregate quantities, and missing packing details. It never reads a backend, adjusts inventory, creates shipments, or claims dispatch completion.

Provide up to 20 sanitized orders (100 item/component lines), with SKU, quantity, unit, confirmed kit composition, gift eligibility, and packing rules. A gift threshold must include its unit; quantities for one SKU in different units are never added or converted without a supplied rule. The component summary includes confirmed kit components only; ordinary items and gifts remain in the per-order checklist. Missing units, kit compositions, or gift conditions are surfaced as open items; the Skill never invents gifts, inserts, or parcel counts.

```bash
npx skills add xxjrq/shop-packing-picklist-cn
sh scripts/self-test.sh
```

See the [successful fixture](fixtures/success-expected.md) and [missing-kit fixture](fixtures/failure-expected.md). The local reference generator is `scripts/generate_picklist.py`.

Business-purpose reference: [ERPNext Packing Slip](https://github.com/frappe/erpnext/blob/develop/erpnext/stock/doctype/packing_slip/packing_slip.json). This repository is original and licensed under MIT-0.
