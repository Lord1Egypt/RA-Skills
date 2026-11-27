# Zoho Inventory scopes

The OAuth scopes Zoho Inventory connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-inventory#permissions.

```bash
maton connection create zoho-inventory --scopes ZohoInventory.settings.READ
```

| Scope | Requested |
| --- | --- |
| `ZohoInventory.contacts.ALL` | By default |
| `ZohoInventory.items.ALL` | By default |
| `ZohoInventory.salesorders.ALL` | By default |
| `ZohoInventory.invoices.ALL` | By default |
| `ZohoInventory.purchaseorders.ALL` | By default |
| `ZohoInventory.customerpayments.ALL` | By default |
| `ZohoInventory.bills.ALL` | By default |
| `ZohoInventory.settings.READ` | By default |
| `ZohoInventory.FullAccess.ALL` | By default |
| `ZohoInventory.inventoryadjustments.ALL` | By default |
| `ZohoInventory.contacts.READ` | Optional |
| `ZohoInventory.items.READ` | Optional |
| `ZohoInventory.salesorders.READ` | Optional |
| `ZohoInventory.invoices.READ` | Optional |
| `ZohoInventory.purchaseorders.READ` | Optional |
| `ZohoInventory.customerpayments.READ` | Optional |
| `ZohoInventory.bills.READ` | Optional |
| `ZohoInventory.inventoryadjustments.READ` | Optional |
| `AaaServer.profile.READ` | Always |
