---
name: simpleerp
description: >-
  Provides procedures for calling the SimpleERP HTTP API. Runtime: shell with curl/curl.exe or PowerShell (Invoke-WebRequest/Invoke-RestMethod). Credentials: send x-api-key on requests except GET /api/health; obtain the key from the user or environment variable SIMPLEERP_API_KEY. Covers list/get/create/update/delete and reports across products, inventory, warehouses, orders, invoices, payments, returns, master data, and admin. Use when the user asks to call SimpleERP, the SimpleERP API, or simpleerp-api for HTTP operations. Do not use for unrelated work, scraping, bypassing security, long jobs not exposed by the API, or when localhost:3000 or a user-stated base URL cannot be reached.
---

# SimpleERP API

Use HTTP against the SimpleERP backend. Read domain examples only from the linked reference files; this file stays a navigator and global rules.

## Agent execution policy

- If completing the user request requires running commands/scripts (including `curl` commands or PowerShell `Invoke-WebRequest` / `Invoke-RestMethod`), **run them automatically**. Do not ask the user to run/execute anything.
- **`GET /api/health`** may run **without** an API key. **All other** HTTP calls need a resolved `x-api-key` per **Credentials** below; if no key is available after that resolution, **ask once** for the key before issuing authenticated requests (then continue running commands automatically).

## Environment

- **Base URL**: `http://localhost:3000`. Resource paths are under `/api` (example: `http://localhost:3000/api/products`). If the user names another host, use it instead of localhost.
- **Clients**: Prefer `curl` on Unix-like shells; on Windows, `curl.exe` or `Invoke-WebRequest` / `Invoke-RestMethod` in PowerShell.

### Credentials

- **Header**: `x-api-key` on every request except `GET /api/health`.
- **Resolution order**: (1) API key the user provided in this conversation, if any; (2) environment variable **`SIMPLEERP_API_KEY`**; (3) if still missing, **ask once** for the key, then proceed.
- **Do not** invent keys, search arbitrary files for secrets, or read unrelated workspace paths to find credentials.

- **Production**: Admin routes need `admin_access`. Most resources map to explicit `PERMISSION_ID` checks; a few route modules use `permissions.<name> || {}` in code, and where that map has no entry yet, `requirePermission` receives a falsy id and **does not enforce a named permission** (API key still required). See [references/ENDPOINTS.md](references/ENDPOINTS.md) (Notes).

**Minimal GET example**

```bash
curl "http://localhost:3000/api/health"
```

```powershell
Invoke-WebRequest -Method GET -Uri "http://localhost:3000/api/health"
```

**Template**

```bash
curl "http://localhost:3000/api/<resource>?<query_params>"
```

## Domain reference map

| Need | Open |
|------|------|
| All paths, methods, auth notes | [references/ENDPOINTS.md](references/ENDPOINTS.md) |
| Sys-par, currencies, warehouses, partners, customers, suppliers | [references/master-data-endpoints.md](references/master-data-endpoints.md) |
| Products, price lists, related master data | [references/products-and-pricing.md](references/products-and-pricing.md) |
| Inventory, deliveries, transfers, adjustments | [references/inventory-and-deliveries.md](references/inventory-and-deliveries.md) |
| Sale/purchase orders, invoices, payments | [references/documents-sales-purchasing.md](references/documents-sales-purchasing.md) |
| Returns, credit memos, debit notes | [references/returns-and-memos.md](references/returns-and-memos.md) |
| Users, API keys, permissions | [references/admin-and-permissions.md](references/admin-and-permissions.md) |
| Chained flows (customer → sale order, etc.) | [references/workflows.md](references/workflows.md) |
| Report route copy-paste curls | [references/reports.md](references/reports.md) |
| List query allowlists (`buildFilters`), workspace paths | [references/query-filters.md](references/query-filters.md) |

## Dynamic list query filters

Most list endpoints build `WHERE` from a **fixed allowlist** of query parameters (bind variables; unknown params ignored). See [references/query-filters.md](references/query-filters.md) for how `buildFilters` works and **workspace-root-relative** paths to `simpleerp-api` source files.

- **Common**: `limit`, `offset` on list endpoints; many support `status` or foreign-key ids.
- **Examples**
  - `/sys-par` — `codePrefix`, `limit`, `offset`
  - `/currencies` — `status`, `limit`, `offset`
  - `/tax` — `status`, `limit`, `offset`
  - `/partners` — `status`, `limit`, `offset`
  - `/products` — `status`, `sku`, `limit`, `offset`
  - `/customers`, `/suppliers`, `/brands`, `/categories`, `/price-lists`, `/areas`, `/warehouses` — `status`, `limit`, `offset`
  - `/credit-terms` — `status`, `limit`, `offset`
  - `/uom` — `status`, `prodId`, `limit`, `offset`
  - `/warehouse-zones` — `warehouseId`, `status`, `limit`, `offset`
  - `/bank-accounts` — `status`, `currencyCode`, `warehouseId`, `limit`, `offset`
  - `/exchange-rates` — `source`, `limit`, `offset`
  - `/memberships` — `status`, `limit`, `offset`
  - `/inventory` — `warehouseId`, `prodId`, `limit`, `offset`
  - `/deliveries` — `orderId` (SALE_ORDER only), `warehouseId`, `status`, `limit`, `offset`
  - `/sale-orders` — `status`, `customerId`, `limit`, `offset`
  - `/purchase-orders` — `status`, `supplierId`, `limit`, `offset`
  - `/cust-returns` — `status`, `customerId`, `saleOrderId`, `limit`, `offset`
  - `/cust-credit-memos`, `/cust-debit-notes` — `status`, `customerId`, `limit`, `offset`
  - `/supp-returns`, `/supp-credit-memos`, `/supp-debit-notes` — `status`, `supplierId`, `limit`, `offset`
  - `/transfers` — `status`, `fromWhId`, `toWhId`, `limit`, `offset`
  - `/inventory-adjustments` — `status`, `warehouseId`, `limit`, `offset`
  - `/permissions` — `functionId`, `limit`, `offset`
  - `/user-permissions` — `userId`, `permissionId`, `limit`, `offset`
  - `/api-key-permissions` — `apiKeyId`, `permissionId`, `limit`, `offset`

Prefer explicit filters and small `limit` values.

## Report endpoints workflow

Use when the user needs a report and must pick accounts, products, warehouses, partners, customers, or suppliers.

1. **Discover (optional)** — `GET /api/reports`. Use `includeData=true` for quick aggregates. Example: `GET /api/reports?includeData=true&topN=10`
2. **Resolve IDs** — Helper lists: `/api/reports/helpers/warehouses`, `.../customers`, `.../products`, `.../partners`, `.../suppliers`, `.../accounts` (for GL). If the user gives names or SKU, search helpers first, then call the report.
3. **CSV multi-select** — `productIds=1,2,3`, `warehouseIds=10,11`, `customerIds=5,9`, `supplierIds=7`, `accountIds=100,101`. Dedupe IDs; use `limit` / `offset` where supported.
4. **Call the report** — Date window: `fromDate=YYYY-MM-DD`, `toDate=YYYY-MM-DD`. Full path table: [references/ENDPOINTS.md](references/ENDPOINTS.md) (Reports). **Copy-paste curls:** [references/reports.md](references/reports.md).

`GET /api/reports` returns categories, accessibility metadata, and optional aggregate data; it normalizes singular/CSV filter aliases and may return `warnings` for bad filters or permissions.

## Safety, pagination, and troubleshooting

- Start with small `limit` (e.g. 20–50); narrow with `status`, `customerId`, `supplierId`, `warehouseId`, `prodId`, and other allowlisted query params from **Dynamic list query filters** where available.
- Use `GET` for reads; `POST` to create; `PUT`/`PATCH` to update; `DELETE` only when requested and safe. Prefer deactivating via `status` over deleting master data or financial documents.
- **400**: often missing required fields (e.g. `priceListId` on customers, order dates). **409**: duplicates or constraints (e.g. SKU, partner).
