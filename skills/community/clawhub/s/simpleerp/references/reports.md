## Report curl examples

Copy-paste examples for common report routes. Base URL: `http://localhost:3000`. Add `-H "x-api-key: <key>"` in production.

**Workflow and helper URLs** are in [SKILL.md](../SKILL.md) (Report endpoints workflow). **Full route list** is in [ENDPOINTS.md](ENDPOINTS.md) (Reports).

### Discover root

```bash
curl "http://localhost:3000/api/reports"
curl "http://localhost:3000/api/reports?includeData=true&topN=10"
curl "http://localhost:3000/api/reports?includeData=true&fromDate=2026-01-01&toDate=2026-03-18&customerIds=1,2&warehouseIds=1&productIds=10,11"
```

### Sample report calls

```bash
# General ledger (multi-select accounts)
curl "http://localhost:3000/api/reports/accounting/general-ledger?fromDate=2026-01-01&toDate=2026-03-18&accountIds=1,2,3&limit=200&offset=0"

# Statement of account: customer (multi-select customers)
curl "http://localhost:3000/api/reports/accounting/statement/customer?fromDate=2026-01-01&toDate=2026-03-18&customerIds=1,2&limit=500&offset=0"

# Inventory movement (multi-select products + warehouses)
curl "http://localhost:3000/api/reports/inventory/movement?fromDate=2026-01-01&toDate=2026-03-18&warehouseIds=1,2&productIds=10,11&limit=200&offset=0"

# Transfer report (multi-select products, optional from/to warehouses)
curl "http://localhost:3000/api/reports/transfers/summary?fromDate=2026-01-01&toDate=2026-03-18&productIds=10,11&fromWarehouseIds=1&toWarehouseIds=2&limit=200&offset=0"

# Total purchases (multi-select suppliers/products/warehouses)
curl "http://localhost:3000/api/reports/purchases/total?fromDate=2026-01-01&toDate=2026-03-18&supplierIds=7,9&warehouseIds=1&productIds=10,11"

# Total sales (multi-select customers/products/warehouses)
curl "http://localhost:3000/api/reports/sales/total?fromDate=2026-01-01&toDate=2026-03-18&customerIds=1,2&warehouseIds=1&productIds=10,11"
```

### More accounting and inventory examples

```bash
curl "http://localhost:3000/api/reports/accounting/total-sales?fromDate=2026-01-01&toDate=2026-03-18&customerIds=1,2&warehouseIds=1&productIds=10,11"

curl "http://localhost:3000/api/reports/sales-by-product?fromDate=2026-01-01&toDate=2026-03-18&productIds=10,11&limit=20"

curl "http://localhost:3000/api/reports/inventory/aging?warehouseIds=1,2&productIds=10,11&limit=50"
```

Report routes require API key and report permissions in production.
