# Squarespace access policy

An access policy limits which endpoints Squarespace connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/squarespace#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Squarespace: its 25 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create squarespace --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "POST", "path": "v1/analytics/transaction-summaries"},
    {"method": "GET", "path": "1.0/authorization/member"},
    {"method": "GET", "path": "1.0/authorization/website"},
    {"method": "GET", "path": "v1/contacts"},
    {"method": "POST", "path": "v1/contacts/query"},
    {"method": "GET", "path": "v1/contacts/{id}"},
    {"method": "GET", "path": "v1/contacts/{id}/address-book"},
    {"method": "GET", "path": "v1/contacts/{id}/address-book/{id}"},
    {"method": "GET", "path": "v1/commerce/discounts"},
    {"method": "GET", "path": "v1/commerce/discounts/{id}"},
    {"method": "GET", "path": "v1/fulfillments/fulfillment-options"},
    {"method": "GET", "path": "1.0/commerce/inventory"},
    {"method": "GET", "path": "1.0/commerce/inventory/{id}"},
    {"method": "GET", "path": "1.0/commerce/orders"},
    {"method": "GET", "path": "1.0/commerce/orders/{id}"},
    {"method": "GET", "path": "v2/commerce/products"},
    {"method": "GET", "path": "v2/commerce/products/{id}"},
    {"method": "GET", "path": "v2/commerce/products/{id}/images/{id}/status"},
    {"method": "GET", "path": "1.0/profiles"},
    {"method": "GET", "path": "1.0/profiles/{id}"},
    {"method": "GET", "path": "1.0/commerce/store_pages"},
    {"method": "GET", "path": "1.0/commerce/transactions"},
    {"method": "GET", "path": "1.0/commerce/transactions/{id}"},
    {"method": "GET", "path": "1.0/webhook_subscriptions"},
    {"method": "GET", "path": "1.0/webhook_subscriptions/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Squarespace endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v1/analytics/transaction-summaries | read | analytics | Retrieve transaction summaries grouped by contact. |
| GET | 1.0/authorization/member | read | authorization | Retrieve basic details about the member who owns the OAuth token. |
| GET | 1.0/authorization/website | read | authorization | Retrieve basic details about the website. |
| GET | v1/contacts | read | contacts | Retrieve all contacts. |
| POST | v1/contacts | write | contacts | Create a contact. |
| POST | v1/contacts/query | read | contacts | Query contacts with filters. |
| GET | v1/contacts/{id} | read | contacts | Retrieve a specific contact. |
| PATCH | v1/contacts/{id} | write | contacts | Update a contact. |
| DELETE | v1/contacts/{id} | write | contacts | Delete a contact. |
| GET | v1/contacts/{id}/address-book | read | contacts | Retrieve the address book of a contact. |
| POST | v1/contacts/{id}/address-book | write | contacts | Create an address book entry for a contact. |
| GET | v1/contacts/{id}/address-book/{id} | read | contacts | Retrieve an address book entry of a contact. |
| PUT | v1/contacts/{id}/address-book/{id} | write | contacts | Update an address book entry of a contact. |
| DELETE | v1/contacts/{id}/address-book/{id} | write | contacts | Delete an address book entry of a contact. |
| GET | v1/commerce/discounts | read | discounts | Retrieve all discounts. |
| POST | v1/commerce/discounts | write | discounts | Create a discount. |
| GET | v1/commerce/discounts/{id} | read | discounts | Retrieve a specific discount. |
| PUT | v1/commerce/discounts/{id} | write | discounts | Update a discount. |
| DELETE | v1/commerce/discounts/{id} | write | discounts | Delete a discount. |
| GET | v1/fulfillments/fulfillment-options | read | discounts | Retrieve fulfillment options usable with discounts. |
| GET | 1.0/commerce/inventory | read | inventory | Retrieve all inventory. |
| POST | 1.0/commerce/inventory/adjustments | write | inventory | Adjust stock quantities. |
| GET | 1.0/commerce/inventory/{id} | read | inventory | Retrieve specific inventory by comma-separated variant IDs. |
| GET | 1.0/commerce/orders | read | orders | Retrieve all orders. |
| POST | 1.0/commerce/orders | write | orders | Create an order. |
| GET | 1.0/commerce/orders/{id} | read | orders | Retrieve a specific order. |
| POST | 1.0/commerce/orders/{id}/fulfillments | write | orders | Fulfill an order. |
| GET | v2/commerce/products | read | products | Retrieve all products. |
| POST | v2/commerce/products | write | products | Create a product. |
| GET | v2/commerce/products/{id} | read | products | Retrieve specific products by comma-separated product IDs. |
| POST | v2/commerce/products/{id} | write | products | Update a product. |
| DELETE | v2/commerce/products/{id} | write | products | Delete a product. |
| POST | v2/commerce/products/{id}/images | write | products | Upload a product image. |
| POST | v2/commerce/products/{id}/images/{id} | write | products | Update product image alt text. |
| DELETE | v2/commerce/products/{id}/images/{id} | write | products | Delete a product image. |
| POST | v2/commerce/products/{id}/images/{id}/order | write | products | Reorder a product image. |
| GET | v2/commerce/products/{id}/images/{id}/status | read | products | Retrieve the upload status of a product image. |
| POST | v2/commerce/products/{id}/variants | write | products | Create a product variant. |
| POST | v2/commerce/products/{id}/variants/{id} | write | products | Update a product variant. |
| DELETE | v2/commerce/products/{id}/variants/{id} | write | products | Delete a product variant. |
| POST | v2/commerce/products/{id}/variants/{id}/image | write | products | Assign an image to a product variant. |
| GET | 1.0/profiles | read | profiles | Retrieve all profiles. |
| GET | 1.0/profiles/{id} | read | profiles | Retrieve specific profiles by comma-separated profile IDs. |
| GET | 1.0/commerce/store_pages | read | store_pages | Retrieve all store pages. |
| GET | 1.0/commerce/transactions | read | transactions | Retrieve all transactions. |
| GET | 1.0/commerce/transactions/{id} | read | transactions | Retrieve specific transactions by comma-separated document IDs. |
| GET | 1.0/webhook_subscriptions | read | webhook_subscriptions | Retrieve all webhook subscriptions. |
| POST | 1.0/webhook_subscriptions | write | webhook_subscriptions | Create a webhook subscription. |
| GET | 1.0/webhook_subscriptions/{id} | read | webhook_subscriptions | Retrieve a specific webhook subscription. |
| POST | 1.0/webhook_subscriptions/{id} | write | webhook_subscriptions | Update a webhook subscription. |
| DELETE | 1.0/webhook_subscriptions/{id} | write | webhook_subscriptions | Delete a webhook subscription. |
| POST | 1.0/webhook_subscriptions/{id}/actions/rotateSecret | write | webhook_subscriptions | Rotate a webhook subscription secret. |
| POST | 1.0/webhook_subscriptions/{id}/actions/sendTestNotification | write | webhook_subscriptions | Send a test webhook notification. |
