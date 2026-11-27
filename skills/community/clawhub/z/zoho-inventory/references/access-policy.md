# Zoho Inventory access policy

An access policy limits which endpoints Zoho Inventory connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-inventory#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho Inventory: its 162 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-inventory --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "inventory/v1/items/batches"},
    {"method": "GET", "path": "inventory/v1/items/batches/{id}"},
    {"method": "GET", "path": "inventory/v1/bills"},
    {"method": "GET", "path": "inventory/v1/bills/{id}"},
    {"method": "GET", "path": "inventory/v1/categories"},
    {"method": "GET", "path": "inventory/v1/categories/{id}"},
    {"method": "GET", "path": "inventory/v1/bundles"},
    {"method": "GET", "path": "inventory/v1/bundles/{id}"},
    {"method": "GET", "path": "inventory/v1/compositeitems"},
    {"method": "GET", "path": "inventory/v1/compositeitems/{id}"},
    {"method": "GET", "path": "inventory/v1/contacts/{id}/contactpersons"},
    {"method": "GET", "path": "inventory/v1/contacts/{id}/contactpersons/{id}"},
    {"method": "GET", "path": "inventory/v1/contacts"},
    {"method": "GET", "path": "inventory/v1/contacts/{id}"},
    {"method": "GET", "path": "inventory/v1/contacts/{id}/address"},
    {"method": "GET", "path": "inventory/v1/contacts/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/contacts/{id}/statements/email"},
    {"method": "GET", "path": "inventory/v1/creditnotes"},
    {"method": "GET", "path": "inventory/v1/creditnotes/refunds"},
    {"method": "GET", "path": "inventory/v1/creditnotes/templates"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}/email"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}/emailhistory"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}/invoices"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}/refunds"},
    {"method": "GET", "path": "inventory/v1/creditnotes/{id}/refunds/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/currencies"},
    {"method": "GET", "path": "inventory/v1/settings/currencies/{id}"},
    {"method": "GET", "path": "inventory/v1/customerpayments"},
    {"method": "GET", "path": "inventory/v1/customerpayments/{id}"},
    {"method": "GET", "path": "inventory/v1/deliverychallans"},
    {"method": "GET", "path": "inventory/v1/deliverychallans/templates"},
    {"method": "GET", "path": "inventory/v1/deliverychallans/{id}"},
    {"method": "GET", "path": "inventory/v1/deliverychallans/{id}/documents/{id}"},
    {"method": "GET", "path": "inventory/v1/inventoryadjustments"},
    {"method": "GET", "path": "inventory/v1/inventoryadjustments/{id}"},
    {"method": "GET", "path": "inventory/v1/autocomplete/inventorycounts/items"},
    {"method": "GET", "path": "inventory/v1/autocomplete/inventorycounts/storages"},
    {"method": "GET", "path": "inventory/v1/inventorycountitems/{id}/trackingdetails"},
    {"method": "GET", "path": "inventory/v1/inventorycounts"},
    {"method": "GET", "path": "inventory/v1/inventorycounts/{id}"},
    {"method": "GET", "path": "inventory/v1/inventorycounts/{id}/items/{id}/storages"},
    {"method": "GET", "path": "inventory/v1/recurringinventorycounts"},
    {"method": "GET", "path": "inventory/v1/recurringinventorycounts/{id}"},
    {"method": "GET", "path": "inventory/v1/invoices"},
    {"method": "GET", "path": "inventory/v1/invoices/pdf"},
    {"method": "GET", "path": "inventory/v1/invoices/print"},
    {"method": "GET", "path": "inventory/v1/invoices/templates"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}/attachment"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}/creditsapplied"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}/email"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}/paymentreminder"},
    {"method": "GET", "path": "inventory/v1/invoices/{id}/payments"},
    {"method": "GET", "path": "inventory/v1/itemgroups"},
    {"method": "GET", "path": "inventory/v1/itemgroups/{id}"},
    {"method": "GET", "path": "inventory/v1/itemdetails"},
    {"method": "GET", "path": "inventory/v1/itemmasters"},
    {"method": "GET", "path": "inventory/v1/itemmasters/{id}"},
    {"method": "GET", "path": "inventory/v1/items"},
    {"method": "GET", "path": "inventory/v1/items/transactions/deliverychallans"},
    {"method": "GET", "path": "inventory/v1/items/transactions/invoices"},
    {"method": "GET", "path": "inventory/v1/items/transactions/moveorders"},
    {"method": "GET", "path": "inventory/v1/items/transactions/purchaseorders"},
    {"method": "GET", "path": "inventory/v1/items/transactions/putaways"},
    {"method": "GET", "path": "inventory/v1/items/transactions/salesorders"},
    {"method": "GET", "path": "inventory/v1/items/transactions/salesreceipts"},
    {"method": "GET", "path": "inventory/v1/items/{id}"},
    {"method": "GET", "path": "inventory/v1/items/{id}/image"},
    {"method": "GET", "path": "inventory/v1/itemvariants"},
    {"method": "GET", "path": "inventory/v1/itemvariants/{id}"},
    {"method": "GET", "path": "inventory/v1/variants/{id}/openingstock"},
    {"method": "GET", "path": "inventory/v1/bills/{id}/landedcosts/{id}"},
    {"method": "GET", "path": "inventory/v1/landedcosts/billdetails"},
    {"method": "GET", "path": "inventory/v1/locations"},
    {"method": "GET", "path": "inventory/v1/locations/{id}"},
    {"method": "GET", "path": "inventory/v1/locations/{id}/users"},
    {"method": "GET", "path": "inventory/v1/moveorders"},
    {"method": "GET", "path": "inventory/v1/moveorders/{id}"},
    {"method": "GET", "path": "inventory/v1/moveorders/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/moveorders/{id}/documents/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/moveorders"},
    {"method": "GET", "path": "inventory/v1/organizations"},
    {"method": "GET", "path": "inventory/v1/organizations/{id}"},
    {"method": "GET", "path": "inventory/v1/packages"},
    {"method": "GET", "path": "inventory/v1/packages/print"},
    {"method": "GET", "path": "inventory/v1/packages/{id}"},
    {"method": "GET", "path": "inventory/v1/picklists"},
    {"method": "GET", "path": "inventory/v1/picklists/searchprlineitems"},
    {"method": "GET", "path": "inventory/v1/picklists/searchso"},
    {"method": "GET", "path": "inventory/v1/picklists/searchsolineitems"},
    {"method": "GET", "path": "inventory/v1/picklists/{id}"},
    {"method": "GET", "path": "inventory/v1/picklists/{id}/advancedtrackingdetails"},
    {"method": "GET", "path": "inventory/v1/pricebooks"},
    {"method": "GET", "path": "inventory/v1/purchasereturns"},
    {"method": "GET", "path": "inventory/v1/purchasereturns/{id}"},
    {"method": "GET", "path": "inventory/v1/purchaseorders"},
    {"method": "GET", "path": "inventory/v1/purchaseorders/{id}"},
    {"method": "GET", "path": "inventory/v1/purchasereceives"},
    {"method": "GET", "path": "inventory/v1/purchasereceives/{id}"},
    {"method": "GET", "path": "inventory/v1/purchasereceives/{id}/documents/{id}"},
    {"method": "GET", "path": "inventory/v1/putaways"},
    {"method": "GET", "path": "inventory/v1/putaways/{id}"},
    {"method": "GET", "path": "inventory/v1/putaways/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/putaways/{id}/documents/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/putaways"},
    {"method": "GET", "path": "inventory/v1/items/{id}/locations/replenishments"},
    {"method": "GET", "path": "inventory/v1/items/{id}/warehouses/replenishments"},
    {"method": "GET", "path": "inventory/v1/replenishments/orders"},
    {"method": "GET", "path": "inventory/v1/replenishments/tasks"},
    {"method": "GET", "path": "inventory/v1/replenishments/tasks/details"},
    {"method": "GET", "path": "inventory/v1/replenishments/tasks/{id}"},
    {"method": "GET", "path": "inventory/v1/replenishments/{id}"},
    {"method": "GET", "path": "inventory/v1/reports/replenishments/tasks"},
    {"method": "GET", "path": "inventory/v1/reportingtags"},
    {"method": "GET", "path": "inventory/v1/reportingtags/options"},
    {"method": "GET", "path": "inventory/v1/reportingtags/{id}/options/all"},
    {"method": "GET", "path": "inventory/v1/retainerinvoices"},
    {"method": "GET", "path": "inventory/v1/retainerinvoices/templates"},
    {"method": "GET", "path": "inventory/v1/retainerinvoices/{id}"},
    {"method": "GET", "path": "inventory/v1/retainerinvoices/{id}/attachment"},
    {"method": "GET", "path": "inventory/v1/retainerinvoices/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/retainerinvoices/{id}/email"},
    {"method": "GET", "path": "inventory/v1/salesorders"},
    {"method": "GET", "path": "inventory/v1/salesorders/{id}"},
    {"method": "GET", "path": "inventory/v1/salesreturns"},
    {"method": "GET", "path": "inventory/v1/salesreturns/{id}"},
    {"method": "GET", "path": "inventory/v1/items/serialnumbers"},
    {"method": "GET", "path": "inventory/v1/items/serialnumbers/{id}"},
    {"method": "GET", "path": "inventory/v1/shipmentorders/{id}"},
    {"method": "GET", "path": "inventory/v1/compositeitems/{id}/defaultstoragemapping"},
    {"method": "GET", "path": "inventory/v1/items/{id}/defaultstoragemapping"},
    {"method": "GET", "path": "inventory/v1/items/{id}/storagelocationsmapping"},
    {"method": "GET", "path": "inventory/v1/storagelocations"},
    {"method": "GET", "path": "inventory/v1/storagelocations/{id}"},
    {"method": "GET", "path": "inventory/v1/storagezones"},
    {"method": "GET", "path": "inventory/v1/storagezones/{id}"},
    {"method": "GET", "path": "inventory/v1/tasks"},
    {"method": "GET", "path": "inventory/v1/tasks/{id}"},
    {"method": "GET", "path": "inventory/v1/tasks/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/tasks/{id}/documents/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/taxauthorities"},
    {"method": "GET", "path": "inventory/v1/settings/taxauthorities/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/taxes"},
    {"method": "GET", "path": "inventory/v1/settings/taxes/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/taxexemptions"},
    {"method": "GET", "path": "inventory/v1/settings/taxexemptions/{id}"},
    {"method": "GET", "path": "inventory/v1/settings/taxgroups/{id}"},
    {"method": "GET", "path": "inventory/v1/transferorders"},
    {"method": "GET", "path": "inventory/v1/transferorders/{id}"},
    {"method": "GET", "path": "inventory/v1/users"},
    {"method": "GET", "path": "inventory/v1/users/me"},
    {"method": "GET", "path": "inventory/v1/users/{id}"},
    {"method": "GET", "path": "inventory/v1/vendorcredits"},
    {"method": "GET", "path": "inventory/v1/vendorcredits/refunds"},
    {"method": "GET", "path": "inventory/v1/vendorcredits/{id}"},
    {"method": "GET", "path": "inventory/v1/vendorcredits/{id}/bills"},
    {"method": "GET", "path": "inventory/v1/vendorcredits/{id}/comments"},
    {"method": "GET", "path": "inventory/v1/vendorcredits/{id}/refunds"},
    {"method": "GET", "path": "inventory/v1/vendorcredits/{id}/refunds/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Zoho Inventory endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | inventory/v1/items/batches | read | batches | Open in ChatGPT. |
| POST | inventory/v1/items/batches | write | batches | Open in ChatGPT. |
| DELETE | inventory/v1/items/batches | write | batches | Open in ChatGPT. |
| POST | inventory/v1/items/batches/active | write | batches | Open in ChatGPT. |
| POST | inventory/v1/items/batches/inactive | write | batches | Open in ChatGPT. |
| GET | inventory/v1/items/batches/{id} | read | batches | Open in ChatGPT. |
| PUT | inventory/v1/items/batches/{id} | write | batches | Open in ChatGPT. |
| DELETE | inventory/v1/items/batches/{id} | write | batches | Open in ChatGPT. |
| POST | inventory/v1/items/batches/{id}/active | write | batches | Open in ChatGPT. |
| POST | inventory/v1/items/batches/{id}/inactive | write | batches | Open in ChatGPT. |
| PUT | inventory/v1/bill/{id}/customfields | write | bills | Open in ChatGPT. |
| GET | inventory/v1/bills | read | bills | Open in ChatGPT. |
| POST | inventory/v1/bills | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/approve | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/submit | write | bills | Open in ChatGPT. |
| GET | inventory/v1/bills/{id} | read | bills | Open in ChatGPT. |
| PUT | inventory/v1/bills/{id} | write | bills | Open in ChatGPT. |
| DELETE | inventory/v1/bills/{id} | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/approve | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/approve/final | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/reject | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/status/open | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/status/void | write | bills | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/submit | write | bills | Open in ChatGPT. |
| GET | inventory/v1/categories | read | categories | Open in ChatGPT. |
| POST | inventory/v1/categories | write | categories | Open in ChatGPT. |
| GET | inventory/v1/categories/{id} | read | categories | Open in ChatGPT. |
| PUT | inventory/v1/categories/{id} | write | categories | Open in ChatGPT. |
| DELETE | inventory/v1/categories/{id} | write | categories | Open in ChatGPT. |
| GET | inventory/v1/bundles | read | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/bundles | write | compositeitems | Open in ChatGPT. |
| GET | inventory/v1/bundles/{id} | read | compositeitems | Open in ChatGPT. |
| PUT | inventory/v1/bundles/{id} | write | compositeitems | Open in ChatGPT. |
| DELETE | inventory/v1/bundles/{id} | write | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/bundles/{id}/bundled | write | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/bundles/{id}/confirmed | write | compositeitems | Open in ChatGPT. |
| GET | inventory/v1/compositeitems | read | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/compositeitems | write | compositeitems | Open in ChatGPT. |
| GET | inventory/v1/compositeitems/{id} | read | compositeitems | Open in ChatGPT. |
| PUT | inventory/v1/compositeitems/{id} | write | compositeitems | Open in ChatGPT. |
| DELETE | inventory/v1/compositeitems/{id} | write | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/compositeitems/{id}/active | write | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/compositeitems/{id}/image | write | compositeitems | Open in ChatGPT. |
| DELETE | inventory/v1/compositeitems/{id}/image | write | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/compositeitems/{id}/inactive | write | compositeitems | Open in ChatGPT. |
| POST | inventory/v1/contacts/contactpersons | write | contact-persons | Open in ChatGPT. |
| PUT | inventory/v1/contacts/contactpersons/{id} | write | contact-persons | Open in ChatGPT. |
| DELETE | inventory/v1/contacts/contactpersons/{id} | write | contact-persons | Open in ChatGPT. |
| POST | inventory/v1/contacts/contactpersons/{id}/primary | write | contact-persons | Open in ChatGPT. |
| GET | inventory/v1/contacts/{id}/contactpersons | read | contact-persons | Open in ChatGPT. |
| GET | inventory/v1/contacts/{id}/contactpersons/{id} | read | contact-persons | Open in ChatGPT. |
| GET | inventory/v1/contacts | read | contacts | Open in ChatGPT. |
| POST | inventory/v1/contacts | write | contacts | Open in ChatGPT. |
| GET | inventory/v1/contacts/{id} | read | contacts | Open in ChatGPT. |
| PUT | inventory/v1/contacts/{id} | write | contacts | Open in ChatGPT. |
| DELETE | inventory/v1/contacts/{id} | write | contacts | Open in ChatGPT. |
| POST | inventory/v1/contacts/{id}/active | write | contacts | Open in ChatGPT. |
| GET | inventory/v1/contacts/{id}/address | read | contacts | Open in ChatGPT. |
| GET | inventory/v1/contacts/{id}/comments | read | contacts | Open in ChatGPT. |
| POST | inventory/v1/contacts/{id}/email | write | contacts | Open in ChatGPT. |
| POST | inventory/v1/contacts/{id}/inactive | write | contacts | Open in ChatGPT. |
| GET | inventory/v1/contacts/{id}/statements/email | read | contacts | Open in ChatGPT. |
| POST | inventory/v1/contacts/{id}/statements/email | write | contacts | Open in ChatGPT. |
| GET | inventory/v1/creditnotes | read | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/refunds | read | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/templates | read | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id} | read | credit-notes | Open in ChatGPT. |
| PUT | inventory/v1/creditnotes/{id} | write | credit-notes | Open in ChatGPT. |
| DELETE | inventory/v1/creditnotes/{id} | write | credit-notes | Open in ChatGPT. |
| PUT | inventory/v1/creditnotes/{id}/address/billing | write | credit-notes | Open in ChatGPT. |
| PUT | inventory/v1/creditnotes/{id}/address/shipping | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/approve | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/attachment | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id}/comments | read | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/comments | write | credit-notes | Open in ChatGPT. |
| DELETE | inventory/v1/creditnotes/{id}/comments/{id} | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/converttoopen | write | credit-notes | Open in ChatGPT. |
| DELETE | inventory/v1/creditnotes/{id}/documents/{id} | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id}/email | read | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/email | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id}/emailhistory | read | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id}/invoices | read | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/invoices | write | credit-notes | Open in ChatGPT. |
| DELETE | inventory/v1/creditnotes/{id}/invoices/{id} | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id}/refunds | read | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/refunds | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/creditnotes/{id}/refunds/{id} | read | credit-notes | Open in ChatGPT. |
| PUT | inventory/v1/creditnotes/{id}/refunds/{id} | write | credit-notes | Open in ChatGPT. |
| DELETE | inventory/v1/creditnotes/{id}/refunds/{id} | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/reject | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/status/draft | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/submit | write | credit-notes | Open in ChatGPT. |
| PUT | inventory/v1/creditnotes/{id}/templates/{id} | write | credit-notes | Open in ChatGPT. |
| POST | inventory/v1/creditnotes/{id}/void | write | credit-notes | Open in ChatGPT. |
| GET | inventory/v1/settings/currencies | read | currencies | Open in ChatGPT. |
| POST | inventory/v1/settings/currencies | write | currencies | Open in ChatGPT. |
| GET | inventory/v1/settings/currencies/{id} | read | currencies | Open in ChatGPT. |
| PUT | inventory/v1/settings/currencies/{id} | write | currencies | Open in ChatGPT. |
| DELETE | inventory/v1/settings/currencies/{id} | write | currencies | Open in ChatGPT. |
| PUT | inventory/v1/customerpayment/{id}/customfields | write | customer-payments | Open in ChatGPT. |
| GET | inventory/v1/customerpayments | read | customer-payments | Open in ChatGPT. |
| POST | inventory/v1/customerpayments | write | customer-payments | Open in ChatGPT. |
| GET | inventory/v1/customerpayments/{id} | read | customer-payments | Open in ChatGPT. |
| PUT | inventory/v1/customerpayments/{id} | write | customer-payments | Open in ChatGPT. |
| DELETE | inventory/v1/customerpayments/{id} | write | customer-payments | Open in ChatGPT. |
| GET | inventory/v1/deliverychallans | read | delivery-challans | Open in ChatGPT. |
| POST | inventory/v1/deliverychallans | write | delivery-challans | Open in ChatGPT. |
| PUT | inventory/v1/deliverychallans/return | write | delivery-challans | Open in ChatGPT. |
| GET | inventory/v1/deliverychallans/templates | read | delivery-challans | Open in ChatGPT. |
| PUT | inventory/v1/deliverychallans/undo/return | write | delivery-challans | Open in ChatGPT. |
| GET | inventory/v1/deliverychallans/{id} | read | delivery-challans | Open in ChatGPT. |
| PUT | inventory/v1/deliverychallans/{id} | write | delivery-challans | Open in ChatGPT. |
| DELETE | inventory/v1/deliverychallans/{id} | write | delivery-challans | Open in ChatGPT. |
| PUT | inventory/v1/deliverychallans/{id}/address/shipping | write | delivery-challans | Open in ChatGPT. |
| POST | inventory/v1/deliverychallans/{id}/attachment | write | delivery-challans | Open in ChatGPT. |
| GET | inventory/v1/deliverychallans/{id}/documents/{id} | read | delivery-challans | Open in ChatGPT. |
| DELETE | inventory/v1/deliverychallans/{id}/documents/{id} | write | delivery-challans | Open in ChatGPT. |
| POST | inventory/v1/deliverychallans/{id}/status/delivered | write | delivery-challans | Open in ChatGPT. |
| POST | inventory/v1/deliverychallans/{id}/status/open | write | delivery-challans | Open in ChatGPT. |
| POST | inventory/v1/deliverychallans/{id}/status/returned | write | delivery-challans | Open in ChatGPT. |
| POST | inventory/v1/deliverychallans/{id}/status/undelivered | write | delivery-challans | Open in ChatGPT. |
| PUT | inventory/v1/deliverychallans/{id}/templates/{id} | write | delivery-challans | Open in ChatGPT. |
| GET | inventory/v1/inventoryadjustments | read | inventoryadjustments | Open in ChatGPT. |
| POST | inventory/v1/inventoryadjustments | write | inventoryadjustments | Open in ChatGPT. |
| GET | inventory/v1/inventoryadjustments/{id} | read | inventoryadjustments | Open in ChatGPT. |
| PUT | inventory/v1/inventoryadjustments/{id} | write | inventoryadjustments | Open in ChatGPT. |
| DELETE | inventory/v1/inventoryadjustments/{id} | write | inventoryadjustments | Open in ChatGPT. |
| POST | inventory/v1/inventoryadjustments/{id}/approve | write | inventoryadjustments | Open in ChatGPT. |
| POST | inventory/v1/inventoryadjustments/{id}/approve/final | write | inventoryadjustments | Open in ChatGPT. |
| POST | inventory/v1/inventoryadjustments/{id}/reject | write | inventoryadjustments | Open in ChatGPT. |
| POST | inventory/v1/inventoryadjustments/{id}/submit | write | inventoryadjustments | Open in ChatGPT. |
| GET | inventory/v1/autocomplete/inventorycounts/items | read | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/autocomplete/inventorycounts/storages | read | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/inventorycountitems/{id}/trackingdetails | read | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/inventorycounts | read | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/inventorycounts | write | inventorycounts | Open in ChatGPT. |
| DELETE | inventory/v1/inventorycounts | write | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/inventorycounts/{id} | read | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/inventorycounts/{id} | write | inventorycounts | Open in ChatGPT. |
| DELETE | inventory/v1/inventorycounts/{id} | write | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/inventorycounts/{id}/approve | write | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/inventorycounts/{id}/cancel | write | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/inventorycounts/{id}/count | write | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/inventorycounts/{id}/items/{id}/storages | read | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/inventorycounts/{id}/start | write | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/inventorycounts/{id}/submit | write | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/recurringinventorycounts | read | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/recurringinventorycounts | write | inventorycounts | Open in ChatGPT. |
| GET | inventory/v1/recurringinventorycounts/{id} | read | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/recurringinventorycounts/{id} | write | inventorycounts | Open in ChatGPT. |
| DELETE | inventory/v1/recurringinventorycounts/{id} | write | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/recurringinventorycounts/{id}/active | write | inventorycounts | Open in ChatGPT. |
| POST | inventory/v1/recurringinventorycounts/{id}/inactive | write | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/settings/inventorycounts | write | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/settings/preferences/inventorycounts | write | inventorycounts | Open in ChatGPT. |
| PUT | inventory/v1/invoice/{id}/customfields | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices | read | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/approve | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/email | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/pdf | read | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/print | read | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/submit | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/templates | read | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id} | read | invoices | Open in ChatGPT. |
| PUT | inventory/v1/invoices/{id} | write | invoices | Open in ChatGPT. |
| DELETE | inventory/v1/invoices/{id} | write | invoices | Open in ChatGPT. |
| PUT | inventory/v1/invoices/{id}/address/billing | write | invoices | Open in ChatGPT. |
| PUT | inventory/v1/invoices/{id}/address/shipping | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/approve | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/approve/final | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id}/attachment | read | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/attachment | write | invoices | Open in ChatGPT. |
| PUT | inventory/v1/invoices/{id}/attachment | write | invoices | Open in ChatGPT. |
| DELETE | inventory/v1/invoices/{id}/attachment | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id}/comments | read | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/comments | write | invoices | Open in ChatGPT. |
| PUT | inventory/v1/invoices/{id}/comments/{id} | write | invoices | Open in ChatGPT. |
| DELETE | inventory/v1/invoices/{id}/comments/{id} | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/credits | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id}/creditsapplied | read | invoices | Open in ChatGPT. |
| DELETE | inventory/v1/invoices/{id}/creditsapplied/{id} | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id}/email | read | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/email | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id}/paymentreminder | read | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/paymentreminder/disable | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/paymentreminder/enable | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/invoices/{id}/payments | read | invoices | Open in ChatGPT. |
| DELETE | inventory/v1/invoices/{id}/payments/{id} | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/reject | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/status/draft | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/status/sent | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/status/void | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/submit | write | invoices | Open in ChatGPT. |
| PUT | inventory/v1/invoices/{id}/templates/{id} | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/writeoff | write | invoices | Open in ChatGPT. |
| POST | inventory/v1/invoices/{id}/writeoff/cancel | write | invoices | Open in ChatGPT. |
| GET | inventory/v1/itemgroups | read | itemgroups | Open in ChatGPT. |
| POST | inventory/v1/itemgroups | write | itemgroups | Open in ChatGPT. |
| GET | inventory/v1/itemgroups/{id} | read | itemgroups | Open in ChatGPT. |
| PUT | inventory/v1/itemgroups/{id} | write | itemgroups | Open in ChatGPT. |
| DELETE | inventory/v1/itemgroups/{id} | write | itemgroups | Open in ChatGPT. |
| POST | inventory/v1/itemgroups/{id}/active | write | itemgroups | Open in ChatGPT. |
| POST | inventory/v1/itemgroups/{id}/inactive | write | itemgroups | Open in ChatGPT. |
| PUT | inventory/v1/item/{id}/customfields | write | items | Open in ChatGPT. |
| GET | inventory/v1/itemdetails | read | items | Open in ChatGPT. |
| GET | inventory/v1/itemmasters | read | items | Open in ChatGPT. |
| POST | inventory/v1/itemmasters | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemmasters/active | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemmasters/inactive | write | items | Open in ChatGPT. |
| GET | inventory/v1/itemmasters/{id} | read | items | Open in ChatGPT. |
| PUT | inventory/v1/itemmasters/{id} | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/itemmasters/{id} | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemmasters/{id}/active | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemmasters/{id}/inactive | write | items | Open in ChatGPT. |
| GET | inventory/v1/items | read | items | Open in ChatGPT. |
| POST | inventory/v1/items | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/items | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/active | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/disablestoragelocation | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/enablestoragelocation | write | items | Open in ChatGPT. |
| PUT | inventory/v1/items/grouping/{id} | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/inactive | write | items | Open in ChatGPT. |
| PUT | inventory/v1/items/locations/permissions | write | items | Open in ChatGPT. |
| PUT | inventory/v1/items/move/{id} | write | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/deliverychallans | read | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/invoices | read | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/moveorders | read | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/purchaseorders | read | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/putaways | read | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/salesorders | read | items | Open in ChatGPT. |
| GET | inventory/v1/items/transactions/salesreceipts | read | items | Open in ChatGPT. |
| POST | inventory/v1/items/ungroup | write | items | Open in ChatGPT. |
| GET | inventory/v1/items/{id} | read | items | Open in ChatGPT. |
| PUT | inventory/v1/items/{id} | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/items/{id} | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/active | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/backimage | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/items/{id}/backimage | write | items | Open in ChatGPT. |
| GET | inventory/v1/items/{id}/image | read | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/image | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/items/{id}/image | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/images | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/items/{id}/images | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/images/reorder | write | items | Open in ChatGPT. |
| PUT | inventory/v1/items/{id}/images/{id}/backimage | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/inactive | write | items | Open in ChatGPT. |
| PUT | inventory/v1/items/{id}/locations/permissions | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/serialnumber/validate | write | items | Open in ChatGPT. |
| POST | inventory/v1/items/{id}/serialnumber/validateandmap | write | items | Open in ChatGPT. |
| GET | inventory/v1/itemvariants | read | items | Open in ChatGPT. |
| POST | inventory/v1/itemvariants | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/itemvariants | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemvariants/active | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemvariants/inactive | write | items | Open in ChatGPT. |
| PUT | inventory/v1/itemvariants/move/{id} | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemvariants/ungroup | write | items | Open in ChatGPT. |
| GET | inventory/v1/itemvariants/{id} | read | items | Open in ChatGPT. |
| PUT | inventory/v1/itemvariants/{id} | write | items | Open in ChatGPT. |
| DELETE | inventory/v1/itemvariants/{id} | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemvariants/{id}/active | write | items | Open in ChatGPT. |
| POST | inventory/v1/itemvariants/{id}/inactive | write | items | Open in ChatGPT. |
| GET | inventory/v1/variants/{id}/openingstock | read | items | Open in ChatGPT. |
| PUT | inventory/v1/variants/{id}/openingstock | write | items | Open in ChatGPT. |
| POST | inventory/v1/bills/bulklandedcosts | write | landedcosts | Open in ChatGPT. |
| POST | inventory/v1/bills/{id}/landedcosts | write | landedcosts | Open in ChatGPT. |
| GET | inventory/v1/bills/{id}/landedcosts/{id} | read | landedcosts | Open in ChatGPT. |
| PUT | inventory/v1/bills/{id}/landedcosts/{id} | write | landedcosts | Open in ChatGPT. |
| DELETE | inventory/v1/bills/{id}/landedcosts/{id} | write | landedcosts | Open in ChatGPT. |
| GET | inventory/v1/landedcosts/billdetails | read | landedcosts | Open in ChatGPT. |
| GET | inventory/v1/locations | read | locations | Open in ChatGPT. |
| POST | inventory/v1/locations | write | locations | Open in ChatGPT. |
| GET | inventory/v1/locations/{id} | read | locations | Open in ChatGPT. |
| PUT | inventory/v1/locations/{id} | write | locations | Open in ChatGPT. |
| DELETE | inventory/v1/locations/{id} | write | locations | Open in ChatGPT. |
| POST | inventory/v1/locations/{id}/active | write | locations | Open in ChatGPT. |
| POST | inventory/v1/locations/{id}/inactive | write | locations | Open in ChatGPT. |
| POST | inventory/v1/locations/{id}/markasprimary | write | locations | Open in ChatGPT. |
| GET | inventory/v1/locations/{id}/users | read | locations | Open in ChatGPT. |
| POST | inventory/v1/settings/locations/enable | write | locations | Open in ChatGPT. |
| GET | inventory/v1/moveorders | read | moveorders | Open in ChatGPT. |
| POST | inventory/v1/moveorders | write | moveorders | Open in ChatGPT. |
| DELETE | inventory/v1/moveorders | write | moveorders | Open in ChatGPT. |
| GET | inventory/v1/moveorders/{id} | read | moveorders | Open in ChatGPT. |
| PUT | inventory/v1/moveorders/{id} | write | moveorders | Open in ChatGPT. |
| DELETE | inventory/v1/moveorders/{id} | write | moveorders | Open in ChatGPT. |
| POST | inventory/v1/moveorders/{id}/attachment | write | moveorders | Open in ChatGPT. |
| GET | inventory/v1/moveorders/{id}/comments | read | moveorders | Open in ChatGPT. |
| GET | inventory/v1/moveorders/{id}/documents/{id} | read | moveorders | Open in ChatGPT. |
| DELETE | inventory/v1/moveorders/{id}/documents/{id} | write | moveorders | Open in ChatGPT. |
| POST | inventory/v1/moveorders/{id}/markascompleted | write | moveorders | Open in ChatGPT. |
| POST | inventory/v1/moveorders/{id}/markasconfirmed | write | moveorders | Open in ChatGPT. |
| POST | inventory/v1/moveorders/{id}/markasinprogress | write | moveorders | Open in ChatGPT. |
| GET | inventory/v1/settings/moveorders | read | moveorders | Open in ChatGPT. |
| GET | inventory/v1/organizations | read | organizations | Open in ChatGPT. |
| POST | inventory/v1/organizations | write | organizations | Open in ChatGPT. |
| GET | inventory/v1/organizations/{id} | read | organizations | Open in ChatGPT. |
| PUT | inventory/v1/organizations/{id} | write | organizations | Open in ChatGPT. |
| GET | inventory/v1/packages | read | packages | Open in ChatGPT. |
| POST | inventory/v1/packages | write | packages | Open in ChatGPT. |
| GET | inventory/v1/packages/print | read | packages | Open in ChatGPT. |
| GET | inventory/v1/packages/{id} | read | packages | Open in ChatGPT. |
| PUT | inventory/v1/packages/{id} | write | packages | Open in ChatGPT. |
| DELETE | inventory/v1/packages/{id} | write | packages | Open in ChatGPT. |
| GET | inventory/v1/picklists | read | picklists | Open in ChatGPT. |
| POST | inventory/v1/picklists | write | picklists | Open in ChatGPT. |
| DELETE | inventory/v1/picklists | write | picklists | Open in ChatGPT. |
| GET | inventory/v1/picklists/searchprlineitems | read | picklists | Open in ChatGPT. |
| GET | inventory/v1/picklists/searchso | read | picklists | Open in ChatGPT. |
| GET | inventory/v1/picklists/searchsolineitems | read | picklists | Open in ChatGPT. |
| POST | inventory/v1/picklists/setstatus | write | picklists | Open in ChatGPT. |
| GET | inventory/v1/picklists/{id} | read | picklists | Open in ChatGPT. |
| PUT | inventory/v1/picklists/{id} | write | picklists | Open in ChatGPT. |
| DELETE | inventory/v1/picklists/{id} | write | picklists | Open in ChatGPT. |
| GET | inventory/v1/picklists/{id}/advancedtrackingdetails | read | picklists | Open in ChatGPT. |
| PUT | inventory/v1/picklists/{id}/advancedtrackingdetails | write | picklists | Open in ChatGPT. |
| POST | inventory/v1/picklists/{id}/comments | write | picklists | Open in ChatGPT. |
| DELETE | inventory/v1/picklists/{id}/comments/{id} | write | picklists | Open in ChatGPT. |
| POST | inventory/v1/picklists/{id}/setstatus | write | picklists | Open in ChatGPT. |
| GET | inventory/v1/pricebooks | read | pricebooks | Open in ChatGPT. |
| POST | inventory/v1/pricebooks | write | pricebooks | Open in ChatGPT. |
| PUT | inventory/v1/pricebooks/{id} | write | pricebooks | Open in ChatGPT. |
| DELETE | inventory/v1/pricebooks/{id} | write | pricebooks | Open in ChatGPT. |
| POST | inventory/v1/pricebooks/{id}/active | write | pricebooks | Open in ChatGPT. |
| POST | inventory/v1/pricebooks/{id}/inactive | write | pricebooks | Open in ChatGPT. |
| GET | inventory/v1/purchasereturns | read | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns | write | purchase-returns | Open in ChatGPT. |
| PUT | inventory/v1/purchasereturns/status/closed | write | purchase-returns | Open in ChatGPT. |
| PUT | inventory/v1/purchasereturns/status/reopen | write | purchase-returns | Open in ChatGPT. |
| GET | inventory/v1/purchasereturns/{id} | read | purchase-returns | Open in ChatGPT. |
| PUT | inventory/v1/purchasereturns/{id} | write | purchase-returns | Open in ChatGPT. |
| DELETE | inventory/v1/purchasereturns/{id} | write | purchase-returns | Open in ChatGPT. |
| PUT | inventory/v1/purchasereturns/{id}/address/billing | write | purchase-returns | Open in ChatGPT. |
| PUT | inventory/v1/purchasereturns/{id}/address/shipping | write | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns/{id}/attachment | write | purchase-returns | Open in ChatGPT. |
| DELETE | inventory/v1/purchasereturns/{id}/documents/{id} | write | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns/{id}/email | write | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns/{id}/status/fulfilled | write | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns/{id}/status/open | write | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns/{id}/status/unfulfilled | write | purchase-returns | Open in ChatGPT. |
| POST | inventory/v1/purchasereturns/{id}/status/void | write | purchase-returns | Open in ChatGPT. |
| GET | inventory/v1/purchaseorders | read | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/approve | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/submit | write | purchaseorders | Open in ChatGPT. |
| GET | inventory/v1/purchaseorders/{id} | read | purchaseorders | Open in ChatGPT. |
| PUT | inventory/v1/purchaseorders/{id} | write | purchaseorders | Open in ChatGPT. |
| DELETE | inventory/v1/purchaseorders/{id} | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/{id}/approve | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/{id}/approve/final | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/{id}/reject | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/{id}/status/cancelled | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/{id}/status/issued | write | purchaseorders | Open in ChatGPT. |
| POST | inventory/v1/purchaseorders/{id}/submit | write | purchaseorders | Open in ChatGPT. |
| GET | inventory/v1/purchasereceives | read | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives | write | purchasereceives | Open in ChatGPT. |
| DELETE | inventory/v1/purchasereceives | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/setstatusasintransit | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/setstatusasreceived | write | purchasereceives | Open in ChatGPT. |
| GET | inventory/v1/purchasereceives/{id} | read | purchasereceives | Open in ChatGPT. |
| PUT | inventory/v1/purchasereceives/{id} | write | purchasereceives | Open in ChatGPT. |
| DELETE | inventory/v1/purchasereceives/{id} | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/approve | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/attachment | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/comments | write | purchasereceives | Open in ChatGPT. |
| DELETE | inventory/v1/purchasereceives/{id}/comments/{id} | write | purchasereceives | Open in ChatGPT. |
| GET | inventory/v1/purchasereceives/{id}/documents/{id} | read | purchasereceives | Open in ChatGPT. |
| DELETE | inventory/v1/purchasereceives/{id}/documents/{id} | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/reject | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/setstatusasintransit | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/setstatusasreceived | write | purchasereceives | Open in ChatGPT. |
| POST | inventory/v1/purchasereceives/{id}/submit | write | purchasereceives | Open in ChatGPT. |
| GET | inventory/v1/putaways | read | putaways | Open in ChatGPT. |
| POST | inventory/v1/putaways | write | putaways | Open in ChatGPT. |
| GET | inventory/v1/putaways/{id} | read | putaways | Open in ChatGPT. |
| PUT | inventory/v1/putaways/{id} | write | putaways | Open in ChatGPT. |
| DELETE | inventory/v1/putaways/{id} | write | putaways | Open in ChatGPT. |
| POST | inventory/v1/putaways/{id}/attachment | write | putaways | Open in ChatGPT. |
| GET | inventory/v1/putaways/{id}/comments | read | putaways | Open in ChatGPT. |
| GET | inventory/v1/putaways/{id}/documents/{id} | read | putaways | Open in ChatGPT. |
| DELETE | inventory/v1/putaways/{id}/documents/{id} | write | putaways | Open in ChatGPT. |
| GET | inventory/v1/settings/putaways | read | putaways | Open in ChatGPT. |
| GET | inventory/v1/items/{id}/locations/replenishments | read | replenishment | Open in ChatGPT. |
| GET | inventory/v1/items/{id}/warehouses/replenishments | read | replenishment | Open in ChatGPT. |
| POST | inventory/v1/replenishments | write | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments | write | replenishment | Open in ChatGPT. |
| GET | inventory/v1/replenishments/orders | read | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/pause | write | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/resume | write | replenishment | Open in ChatGPT. |
| GET | inventory/v1/replenishments/tasks | read | replenishment | Open in ChatGPT. |
| GET | inventory/v1/replenishments/tasks/details | read | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/tasks/dismiss | write | replenishment | Open in ChatGPT. |
| POST | inventory/v1/replenishments/tasks/generate | write | replenishment | Open in ChatGPT. |
| GET | inventory/v1/replenishments/tasks/{id} | read | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/tasks/{id}/dismiss | write | replenishment | Open in ChatGPT. |
| GET | inventory/v1/replenishments/{id} | read | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/{id} | write | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/{id}/pause | write | replenishment | Open in ChatGPT. |
| PUT | inventory/v1/replenishments/{id}/resume | write | replenishment | Open in ChatGPT. |
| POST | inventory/v1/replenishments/{id}/tasks/generate | write | replenishment | Open in ChatGPT. |
| GET | inventory/v1/reports/replenishments/tasks | read | replenishment | Open in ChatGPT. |
| GET | inventory/v1/reportingtags | read | reporting-tags | Open in ChatGPT. |
| POST | inventory/v1/reportingtags | write | reporting-tags | Open in ChatGPT. |
| GET | inventory/v1/reportingtags/options | read | reporting-tags | Open in ChatGPT. |
| PUT | inventory/v1/reportingtags/reorder | write | reporting-tags | Open in ChatGPT. |
| POST | inventory/v1/reportingtags/{id} | write | reporting-tags | Open in ChatGPT. |
| PUT | inventory/v1/reportingtags/{id} | write | reporting-tags | Open in ChatGPT. |
| DELETE | inventory/v1/reportingtags/{id} | write | reporting-tags | Open in ChatGPT. |
| POST | inventory/v1/reportingtags/{id}/active | write | reporting-tags | Open in ChatGPT. |
| PUT | inventory/v1/reportingtags/{id}/criteria | write | reporting-tags | Open in ChatGPT. |
| POST | inventory/v1/reportingtags/{id}/inactive | write | reporting-tags | Open in ChatGPT. |
| POST | inventory/v1/reportingtags/{id}/option/{id}/active | write | reporting-tags | Open in ChatGPT. |
| POST | inventory/v1/reportingtags/{id}/option/{id}/inactive | write | reporting-tags | Open in ChatGPT. |
| PUT | inventory/v1/reportingtags/{id}/options | write | reporting-tags | Open in ChatGPT. |
| GET | inventory/v1/reportingtags/{id}/options/all | read | reporting-tags | Open in ChatGPT. |
| GET | inventory/v1/retainerinvoices | read | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices | write | retainer-invoices | Open in ChatGPT. |
| GET | inventory/v1/retainerinvoices/templates | read | retainer-invoices | Open in ChatGPT. |
| GET | inventory/v1/retainerinvoices/{id} | read | retainer-invoices | Open in ChatGPT. |
| PUT | inventory/v1/retainerinvoices/{id} | write | retainer-invoices | Open in ChatGPT. |
| DELETE | inventory/v1/retainerinvoices/{id} | write | retainer-invoices | Open in ChatGPT. |
| PUT | inventory/v1/retainerinvoices/{id}/address/billing | write | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/approve | write | retainer-invoices | Open in ChatGPT. |
| GET | inventory/v1/retainerinvoices/{id}/attachment | read | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/attachment | write | retainer-invoices | Open in ChatGPT. |
| GET | inventory/v1/retainerinvoices/{id}/comments | read | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/comments | write | retainer-invoices | Open in ChatGPT. |
| PUT | inventory/v1/retainerinvoices/{id}/comments/{id} | write | retainer-invoices | Open in ChatGPT. |
| DELETE | inventory/v1/retainerinvoices/{id}/comments/{id} | write | retainer-invoices | Open in ChatGPT. |
| DELETE | inventory/v1/retainerinvoices/{id}/documents/{id} | write | retainer-invoices | Open in ChatGPT. |
| GET | inventory/v1/retainerinvoices/{id}/email | read | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/email | write | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/status/draft | write | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/status/sent | write | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/status/void | write | retainer-invoices | Open in ChatGPT. |
| POST | inventory/v1/retainerinvoices/{id}/submit | write | retainer-invoices | Open in ChatGPT. |
| PUT | inventory/v1/retainerinvoices/{id}/templates/{id} | write | retainer-invoices | Open in ChatGPT. |
| GET | inventory/v1/salesorders | read | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders | write | salesorders | Open in ChatGPT. |
| DELETE | inventory/v1/salesorders | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/approve | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/status/confirmed | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/submit | write | salesorders | Open in ChatGPT. |
| GET | inventory/v1/salesorders/{id} | read | salesorders | Open in ChatGPT. |
| PUT | inventory/v1/salesorders/{id} | write | salesorders | Open in ChatGPT. |
| DELETE | inventory/v1/salesorders/{id} | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/{id}/approve | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/{id}/approve/final | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/{id}/reject | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/{id}/status/confirmed | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/{id}/status/void | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesorders/{id}/submit | write | salesorders | Open in ChatGPT. |
| POST | inventory/v1/salesreturnreceives | write | salesreturns | Open in ChatGPT. |
| DELETE | inventory/v1/salesreturnreceives/{id} | write | salesreturns | Open in ChatGPT. |
| GET | inventory/v1/salesreturns | read | salesreturns | Open in ChatGPT. |
| POST | inventory/v1/salesreturns | write | salesreturns | Open in ChatGPT. |
| GET | inventory/v1/salesreturns/{id} | read | salesreturns | Open in ChatGPT. |
| PUT | inventory/v1/salesreturns/{id} | write | salesreturns | Open in ChatGPT. |
| DELETE | inventory/v1/salesreturns/{id} | write | salesreturns | Open in ChatGPT. |
| GET | inventory/v1/items/serialnumbers | read | serialnumbers | Open in ChatGPT. |
| GET | inventory/v1/items/serialnumbers/{id} | read | serialnumbers | Open in ChatGPT. |
| POST | inventory/v1/shipmentorders | write | shipmentorders | Open in ChatGPT. |
| GET | inventory/v1/shipmentorders/{id} | read | shipmentorders | Open in ChatGPT. |
| PUT | inventory/v1/shipmentorders/{id} | write | shipmentorders | Open in ChatGPT. |
| DELETE | inventory/v1/shipmentorders/{id} | write | shipmentorders | Open in ChatGPT. |
| POST | inventory/v1/shipmentorders/{id}/status/delivered | write | shipmentorders | Open in ChatGPT. |
| PUT | inventory/v1/compositeitems/{id}/configure/defaultstorage | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/compositeitems/{id}/defaultstoragemapping | read | storage-locations | Open in ChatGPT. |
| PUT | inventory/v1/items/{id}/configure/defaultstorage | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/items/{id}/defaultstoragemapping | read | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/items/{id}/storagelocationsmapping | read | storage-locations | Open in ChatGPT. |
| PUT | inventory/v1/items/{id}/storagelocationsmapping | write | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/locations/{id}/storagelocations/disable | write | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/locations/{id}/storagelocations/enable | write | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/settings/warehouses/{id}/storagelocations/disable | write | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/settings/warehouses/{id}/storagelocations/enable | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/storagelocations | read | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/storagelocations | write | storage-locations | Open in ChatGPT. |
| DELETE | inventory/v1/storagelocations | write | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/storagelocations/active | write | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/storagelocations/inactive | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/storagelocations/{id} | read | storage-locations | Open in ChatGPT. |
| PUT | inventory/v1/storagelocations/{id} | write | storage-locations | Open in ChatGPT. |
| DELETE | inventory/v1/storagelocations/{id} | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/storagezones | read | storage-locations | Open in ChatGPT. |
| POST | inventory/v1/storagezones | write | storage-locations | Open in ChatGPT. |
| PUT | inventory/v1/storagezones/active | write | storage-locations | Open in ChatGPT. |
| PUT | inventory/v1/storagezones/inactive | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/storagezones/{id} | read | storage-locations | Open in ChatGPT. |
| PUT | inventory/v1/storagezones/{id} | write | storage-locations | Open in ChatGPT. |
| DELETE | inventory/v1/storagezones/{id} | write | storage-locations | Open in ChatGPT. |
| GET | inventory/v1/tasks | read | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks | write | tasks | Open in ChatGPT. |
| PUT | inventory/v1/tasks | write | tasks | Open in ChatGPT. |
| DELETE | inventory/v1/tasks | write | tasks | Open in ChatGPT. |
| GET | inventory/v1/tasks/{id} | read | tasks | Open in ChatGPT. |
| PUT | inventory/v1/tasks/{id} | write | tasks | Open in ChatGPT. |
| DELETE | inventory/v1/tasks/{id} | write | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks/{id}/attachment | write | tasks | Open in ChatGPT. |
| GET | inventory/v1/tasks/{id}/comments | read | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks/{id}/comments | write | tasks | Open in ChatGPT. |
| DELETE | inventory/v1/tasks/{id}/comments/{id} | write | tasks | Open in ChatGPT. |
| GET | inventory/v1/tasks/{id}/documents/{id} | read | tasks | Open in ChatGPT. |
| DELETE | inventory/v1/tasks/{id}/documents/{id} | write | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks/{id}/markascompleted | write | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks/{id}/markasongoing | write | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks/{id}/markasopen | write | tasks | Open in ChatGPT. |
| POST | inventory/v1/tasks/{id}/percentage | write | tasks | Open in ChatGPT. |
| GET | inventory/v1/settings/taxauthorities | read | taxes | Open in ChatGPT. |
| POST | inventory/v1/settings/taxauthorities | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/settings/taxauthorities/{id} | read | taxes | Open in ChatGPT. |
| PUT | inventory/v1/settings/taxauthorities/{id} | write | taxes | Open in ChatGPT. |
| DELETE | inventory/v1/settings/taxauthorities/{id} | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/settings/taxes | read | taxes | Open in ChatGPT. |
| POST | inventory/v1/settings/taxes | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/settings/taxes/{id} | read | taxes | Open in ChatGPT. |
| PUT | inventory/v1/settings/taxes/{id} | write | taxes | Open in ChatGPT. |
| DELETE | inventory/v1/settings/taxes/{id} | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/settings/taxexemptions | read | taxes | Open in ChatGPT. |
| POST | inventory/v1/settings/taxexemptions | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/settings/taxexemptions/{id} | read | taxes | Open in ChatGPT. |
| PUT | inventory/v1/settings/taxexemptions/{id} | write | taxes | Open in ChatGPT. |
| DELETE | inventory/v1/settings/taxexemptions/{id} | write | taxes | Open in ChatGPT. |
| POST | inventory/v1/settings/taxgroups | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/settings/taxgroups/{id} | read | taxes | Open in ChatGPT. |
| PUT | inventory/v1/settings/taxgroups/{id} | write | taxes | Open in ChatGPT. |
| DELETE | inventory/v1/settings/taxgroups/{id} | write | taxes | Open in ChatGPT. |
| GET | inventory/v1/transferorders | read | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders | write | transferorders | Open in ChatGPT. |
| DELETE | inventory/v1/transferorders | write | transferorders | Open in ChatGPT. |
| GET | inventory/v1/transferorders/{id} | read | transferorders | Open in ChatGPT. |
| PUT | inventory/v1/transferorders/{id} | write | transferorders | Open in ChatGPT. |
| DELETE | inventory/v1/transferorders/{id} | write | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders/{id}/approve | write | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders/{id}/approve/final | write | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders/{id}/intransit | write | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders/{id}/markastransferred | write | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders/{id}/reject | write | transferorders | Open in ChatGPT. |
| POST | inventory/v1/transferorders/{id}/submit | write | transferorders | Open in ChatGPT. |
| GET | inventory/v1/users | read | users | Open in ChatGPT. |
| POST | inventory/v1/users | write | users | Open in ChatGPT. |
| GET | inventory/v1/users/me | read | users | Open in ChatGPT. |
| GET | inventory/v1/users/{id} | read | users | Open in ChatGPT. |
| PUT | inventory/v1/users/{id} | write | users | Open in ChatGPT. |
| DELETE | inventory/v1/users/{id} | write | users | Open in ChatGPT. |
| POST | inventory/v1/users/{id}/active | write | users | Open in ChatGPT. |
| POST | inventory/v1/users/{id}/inactive | write | users | Open in ChatGPT. |
| POST | inventory/v1/users/{id}/invite | write | users | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits | read | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits | write | vendor-credits | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits/refunds | read | vendor-credits | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits/{id} | read | vendor-credits | Open in ChatGPT. |
| PUT | inventory/v1/vendorcredits/{id} | write | vendor-credits | Open in ChatGPT. |
| DELETE | inventory/v1/vendorcredits/{id} | write | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/approve | write | vendor-credits | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits/{id}/bills | read | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/bills | write | vendor-credits | Open in ChatGPT. |
| DELETE | inventory/v1/vendorcredits/{id}/bills/{id} | write | vendor-credits | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits/{id}/comments | read | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/comments | write | vendor-credits | Open in ChatGPT. |
| DELETE | inventory/v1/vendorcredits/{id}/comments/{id} | write | vendor-credits | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits/{id}/refunds | read | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/refunds | write | vendor-credits | Open in ChatGPT. |
| GET | inventory/v1/vendorcredits/{id}/refunds/{id} | read | vendor-credits | Open in ChatGPT. |
| PUT | inventory/v1/vendorcredits/{id}/refunds/{id} | write | vendor-credits | Open in ChatGPT. |
| DELETE | inventory/v1/vendorcredits/{id}/refunds/{id} | write | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/status/open | write | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/status/void | write | vendor-credits | Open in ChatGPT. |
| POST | inventory/v1/vendorcredits/{id}/submit | write | vendor-credits | Open in ChatGPT. |
