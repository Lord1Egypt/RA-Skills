# SimpleERP API — Endpoint Reference

Base path: `/api`. All routes below are relative to that base.  
Auth (production): header `x-api-key` (required for all routes except `GET /api/health`).

## Table of contents

- Public (no auth)
- Root (API key required in production)
- Admin (API key + `admin_access` permission in production)
- Master data & configuration (API key + resource permissions in production)
- Reports (API key + report permissions in production)
- Notes

---

## Public (no auth)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check; returns `{ status, db }`. |

---

## Root (API key required in production)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api` | API info: `{ message, version }`. |

---

## Admin (API key + `admin_access` permission in production)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/users` | List system users. |
| GET | `/api/admin/users/:id` | Get user by ID. |
| GET | `/api/admin/user-groups` | List user groups. |
| GET | `/api/admin/user-groups/:id` | Get user group by ID. |
| POST | `/api/admin/user-groups` | Create user group. |
| PUT | `/api/admin/user-groups/:id` | Update user group. |
| DELETE | `/api/admin/user-groups/:id` | Delete user group. |
| GET | `/api/admin/user-group-members` | List user group members. |
| GET | `/api/admin/user-group-members/:id` | Get member by ID. |
| POST | `/api/admin/user-group-members` | Add member. |
| DELETE | `/api/admin/user-group-members/:id` | Remove member. |
| GET | `/api/admin/api-keys` | List API keys. |
| GET | `/api/admin/api-keys/:id` | Get API key by ID. |
| POST | `/api/admin/api-keys` | Create API key. |
| POST | `/api/admin/api-keys/:id/rotate` | Rotate API key. |
| PATCH | `/api/admin/api-keys/:id` | Update API key (e.g. status). |
| GET | `/api/admin/access-info` | List access info. |
| GET | `/api/admin/access-info/:token` | Get access info by token. |
| GET | `/api/admin/debug` | Debug info. |

---

## Master data & configuration (API key + resource permissions in production)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/sys-par` | List system parameters (query: codePrefix, limit, offset). |
| GET | `/api/sys-par/:code` | Get system parameter by code. |
| POST | `/api/sys-par` | Create. |
| PUT | `/api/sys-par/:code` | Update. |
| DELETE | `/api/sys-par/:code` | Delete. |
| GET | `/api/currencies` | List currencies (query: status, limit, offset). |
| GET | `/api/currencies/:code` | Get by code. |
| POST | `/api/currencies` | Create. |
| PUT | `/api/currencies/:code` | Update. |
| DELETE | `/api/currencies/:code` | Delete. |
| GET | `/api/warehouses` | List warehouses. |
| GET | `/api/warehouses/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/warehouses` | CRUD. |
| GET | `/api/partners` | List partners (query: status, limit, offset). |
| GET | `/api/partners/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/partners` | CRUD. |
| GET | `/api/products` | List products (query: status, sku, limit, offset). |
| GET | `/api/products/:id` | Get product by ID. |
| POST / PUT / DELETE | `/api/products` | CRUD. |
| GET | `/api/price-lists` | List price lists. |
| GET | `/api/price-lists/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/price-lists` | CRUD. |
| GET | `/api/customers` | List customers. |
| GET | `/api/customers/:id` | Get customer by ID. |
| GET | `/api/customers/:id/warehouses` | Customer warehouses. |
| POST / PUT / DELETE | `/api/customers` | CRUD. |
| GET | `/api/suppliers` | List suppliers. |
| GET | `/api/suppliers/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/suppliers` | CRUD. |
| GET | `/api/sale-orders` | List sale orders. |
| GET | `/api/sale-orders/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/sale-orders` | CRUD. |
| GET | `/api/purchase-orders` | List purchase orders. |
| GET | `/api/purchase-orders/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/purchase-orders` | CRUD. |
| GET | `/api/inventory` | List inventory. |
| GET | `/api/inventory/:warehouseId/:prodId` | Get inventory for warehouse+product. |
| GET | `/api/cust-returns` | List customer returns (query: status, customerId, saleOrderId, limit, offset). |
| GET | `/api/cust-returns/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/cust-returns` | CRUD. |
| GET | `/api/cust-credit-memos` | List customer credit memos (query: status, customerId, limit, offset). |
| GET | `/api/cust-credit-memos/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/cust-credit-memos` | CRUD. |
| GET | `/api/cust-debit-notes` | List customer debit notes (query: status, customerId, limit, offset). |
| GET | `/api/cust-debit-notes/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/cust-debit-notes` | CRUD. |
| GET | `/api/supp-returns` | List supplier returns (query: status, supplierId, limit, offset). |
| GET | `/api/supp-returns/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/supp-returns` | CRUD. |
| GET | `/api/supp-credit-memos` | List supplier credit memos (query: status, supplierId, limit, offset). |
| GET | `/api/supp-credit-memos/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/supp-credit-memos` | CRUD. |
| GET | `/api/supp-debit-notes` | List supplier debit notes (query: status, supplierId, limit, offset). |
| GET | `/api/supp-debit-notes/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/supp-debit-notes` | CRUD. |
| GET | `/api/transfers` | List stock transfers (query: status, fromWhId, toWhId, limit, offset). |
| GET | `/api/transfers/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/transfers` | CRUD. |
| GET | `/api/inventory-adjustments` | List inventory adjustments (query: status, warehouseId, limit, offset). |
| GET | `/api/inventory-adjustments/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/inventory-adjustments` | CRUD. |
| GET | `/api/areas` | List areas. |
| GET | `/api/areas/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/areas` | CRUD. |
| GET | `/api/brands` | List brands. |
| GET | `/api/brands/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/brands` | CRUD. |
| GET | `/api/categories` | List categories. |
| GET | `/api/categories/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/categories` | CRUD. |
| GET | `/api/credit-terms` | List credit terms. |
| GET | `/api/credit-terms/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/credit-terms` | CRUD. |
| GET | `/api/uom` | List UOM. |
| GET | `/api/uom/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/uom` | CRUD. |
| GET | `/api/tax` | List tax (query: status, limit, offset). |
| GET | `/api/tax/:code` | Get by code. |
| POST / PUT / DELETE | `/api/tax` | CRUD. |
| GET | `/api/warehouse-zones` | List warehouse zones. |
| GET | `/api/warehouse-zones/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/warehouse-zones` | CRUD. |
| GET | `/api/bank-accounts` | List bank accounts. |
| GET | `/api/bank-accounts/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/bank-accounts` | CRUD. |
| GET | `/api/account-managers` | List account managers. |
| GET | `/api/account-managers/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/account-managers` | CRUD. |
| GET | `/api/sale-invoices` | List sale invoices (read-only). |
| GET | `/api/sale-invoices/:id` | Get by ID. |
| GET | `/api/purchase-invoices` | List purchase invoices (read-only). |
| GET | `/api/purchase-invoices/:id` | Get by ID. |
| GET | `/api/deliveries` | List deliveries (read-only). |
| GET | `/api/deliveries/:id` | Get by ID. |
| GET | `/api/cust-payments` | List customer payments (read-only). |
| GET | `/api/cust-payments/:id` | Get by ID. |
| GET | `/api/payments` | List payments (read-only). |
| GET | `/api/payments/:id` | Get by ID. |
| GET | `/api/exchange-rates` | List exchange rates (read-only; query: source, limit, offset). |
| GET | `/api/exchange-rates/:id` | Get by ID. |
| GET | `/api/memberships` | List memberships (query: status, limit, offset). |
| GET | `/api/memberships/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/memberships` | CRUD. |
| GET | `/api/journal-categories` | List journal categories (read-only). |
| GET | `/api/journal-categories/:id` | Get by ID. |
| GET | `/api/permissions` | List permissions (query: functionId, limit, offset). |
| GET | `/api/permissions/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/permissions` | CRUD. |
| GET | `/api/user-permissions` | List user permissions (query: userId, permissionId, limit, offset). |
| GET | `/api/user-permissions/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/user-permissions` | CRUD. |
| GET | `/api/api-key-permissions` | List API key permissions (query: apiKeyId, permissionId, limit, offset). |
| GET | `/api/api-key-permissions/:id` | Get by ID. |
| POST / PUT / DELETE | `/api/api-key-permissions` | CRUD. |

---

## Reports (API key + report permissions in production)

All report routes are mounted under `/api/reports` and use direct DB queries for reporting.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/reports` | Root report aggregator. Returns report categories/endpoints with accessibility metadata for both aggregate and non-aggregate report routes. Query: `includeData` (boolean; `true`/`1`/`yes`), `topN` (default `10`, max `100`), `fromDate`, `toDate`, `customerId(s)`, `supplierId(s)`, `warehouseId(s)`, `productId(s)`/`prodId`, `fromWarehouseId(s)`/`sourceWarehouseId`, `toWarehouseId(s)`/`targetWarehouseId`. |
| GET | `/api/reports/accounting/total-sales` | Sales totals from SALE_INVOICE and SALE_INVOICE_LINE; accepts `fromDate`, `toDate`, `customerId`, `warehouseId`, `customerIds`, `warehouseIds`, `productIds` (CSV). |
| GET | `/api/reports/accounting/total-purchases` | Purchase totals from PURCHASE_INV_LINE and PURCHASE_INVOICE; accepts `fromDate`, `toDate`, `supplierId`, `warehouseId`. |
| GET | `/api/reports/accounting/balance-sheet` | Balance sheet lines from `ACCOUNT_STMT` + `ACCOUNT_STMT_LINE`; accepts `stmtDate` (YYYY-MM-DD). |
| GET | `/api/reports/accounting/cash-flow` | Cash flow statements from `CASH_FLOW_STMT`; accepts `fromDate`, `toDate`. |
| GET | `/api/reports/accounting/income-statement` | Income statement-style summary; accepts `fromDate`, `toDate`. |
| GET | `/api/reports/accounting/cust-receivables` | Customer receivables (outstanding per customer); accepts `customerId`, `limit`, `offset`. |
| GET | `/api/reports/accounting/general-ledger` | Journal entries from `JOURNAL`; accepts `fromDate`, `toDate`, `accountIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/accounting/statement/customer` | Statement of account (customer) from `SALE_INVOICE` + `CUST_PAYMENT`; accepts `customerIds` (CSV), `fromDate`, `toDate`, `limit`, `offset`. |
| GET | `/api/reports/accounting/statement/supplier` | Statement of account (supplier) from `PURCHASE_INVOICE` + `PAYMENT`; accepts `supplierIds` (CSV), `fromDate`, `toDate`, `limit`, `offset`. |
| GET | `/api/reports/sales-by-product` | Sales aggregated by product; accepts `fromDate`, `toDate`, `customerId`, `customerIds` (CSV), `productId`, `productIds` (CSV), `warehouseIds` (CSV), `sku`, `status`, `limit`, `offset`. |
| GET | `/api/reports/sales/total` | Total sales (qty/revenue/cost/profit); accepts `fromDate`, `toDate`, `customerId`, `warehouseId`, `customerIds`, `warehouseIds`, `productIds` (CSV). |
| GET | `/api/reports/sales/customer-returns` | Customer return lines from `CUST_RETURN` + `CUST_RETURN_DET`; accepts `fromDate`, `toDate`, `customerIds`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/sales/product-performance` | Sales performance by product; accepts `fromDate`, `toDate`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/sales/customer-performance` | Sales performance by customer; accepts `fromDate`, `toDate`, `customerIds`, `productIds`, `warehouseIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/sales/customer-performance-total` | Sales performance by customer × product; accepts `fromDate`, `toDate`, `customerIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/sales/outstanding-orders` | Outstanding sale orders (remaining qty); accepts `fromDate`, `toDate`, `customerIds`, `warehouseIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/sales/top-selling` | Top selling products; accepts `fromDate`, `toDate`, `limit`. |
| GET | `/api/reports/sales/top-non-selling` | Products with no sales in window; accepts `fromDate`, `toDate`, `limit`. |
| GET | `/api/reports/sales/lost-sales` | Cancelled/not-fully-fulfilled order lines; accepts `fromDate`, `toDate`, `customerIds`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/inventory/aging` | Inventory batch aging; accepts `warehouseId`, `prodId`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/inventory/valuation` | Inventory valuation (qty on hand × cost); accepts `warehouseId`, `prodId`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/inventory/on-hand` | Quantity on hand list; accepts `warehouseId`, `prodId`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/inventory/movement` | Inventory movements from `INVENTORY_MOV`; accepts `fromDate`, `toDate`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/inventory/delivery-cost` | Delivery cost lines from `DELIVERY_COST` + `DELIVERY`; accepts `fromDate`, `toDate`, `warehouseIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/inventory/summary` | Inventory summary from `INVENTORY`; accepts `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/transfers/summary` | Transfer lines from `TRANSFER` + `TRANSFER_DET`; accepts `fromDate`, `toDate`, `productIds`, `fromWarehouseIds`, `toWarehouseIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/purchases/pending` | Pending purchase orders; accepts `supplierId`, `warehouseId`, `supplierIds`, `warehouseIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/purchases/total` | Total purchases (qty/amount); accepts `fromDate`, `toDate`, `supplierIds`, `warehouseIds`, `productIds` (CSV). |
| GET | `/api/reports/purchases/supplier-returns` | Supplier return lines from `SUPP_RETURN` + `SUPP_RETURN_DET`; accepts `fromDate`, `toDate`, `supplierIds`, `warehouseIds`, `productIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/purchases/srp-below-cost` | Inventory rows where `SRP < COST`; accepts `warehouseIds` (CSV), `limit`, `offset`. |
| GET | `/api/reports/helpers/warehouses` | Helper list of warehouses; optional `status`, `limit`, `offset`. |
| GET | `/api/reports/helpers/customers` | Helper list of customers; optional `status`, `limit`, `offset`. |
| GET | `/api/reports/helpers/products` | Helper list of products; accepts `status`, `sku`, `limit`, `offset`. |
| GET | `/api/reports/helpers/partners` | Helper list of partners; accepts `status`, `limit`, `offset`. |
| GET | `/api/reports/helpers/suppliers` | Helper list of suppliers; accepts `status`, `limit`, `offset`. |
| GET | `/api/reports/helpers/accounts` | Helper list of journal categories (accounts); accepts `status`, `typeId`, `accountType`, `limit`, `offset`. |

Note: `/api/reports` normalizes singular and CSV filter aliases (for example `customerId` + `customerIds`), validates dates (`YYYY-MM-DD`), and may return `warnings` for invalid filters or inaccessible metrics. With `includeData` omitted/false, it returns metadata only; with `includeData=true` it computes data only for aggregate-capable accessible metrics.

---

## Notes

- In **production** (`NODE_ENV=production`), all non-health routes require a valid API key in the `x-api-key` header.
- In **production**, admin routes additionally require the `admin_access` permission on the API key or user, and other routes use per-resource permissions (e.g. product list/get/create/update/delete) enforced by the API where `src/config/permissions.js` defines a non-empty permission id for that action. Some route modules still use a fallback empty permission object for certain resources; until those maps are populated, production may enforce only the API key for those routes.
- In **non-production** (any `NODE_ENV` other than `production`, e.g. `development`), authentication and permission checks are bypassed for easier local development. Do **not** use this mode in shared/staging/production environments.
