## Sales and purchasing documents

This reference covers sales and purchasing documents plus related AR/AP views.

Base URL: `http://localhost:3000/api`.

## Table of contents

- Sale orders (`/sale-orders`)
- Purchase orders (`/purchase-orders`)
- Invoices and payments (read-only views)

---

### Sale orders (`/sale-orders`)

#### List sale orders

```bash
curl "http://localhost:3000/api/sale-orders?status=&customerId=&limit=100&offset=0"
```

#### Create a sale order

```bash
curl "http://localhost:3000/api/sale-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 1,
    "customerName": "Customer Co",
    "custWarehouseId": 1,
    "priceListId": 1,
    "reqDeliveryDt": "2026-03-15",
    "targetDeliveryDt": "2026-03-20",
    "deliveryAddress": "123 Delivery St",
    "sourceWarehouseId": 1,
    "remarks": null,
    "lines": [
      {
        "prodId": 1,
        "prodName": "Product One",
        "sku": "SKU-001",
        "qtyRequestedTotal": 10,
        "qtyApprovedTotal": 10,
        "unitPrice": 10.5,
        "effectivePrice": 10.5,
        "subTotal": 105
      }
    ]
  }'
```

---

### Purchase orders (`/purchase-orders`)

#### List purchase orders

```bash
curl "http://localhost:3000/api/purchase-orders?status=&supplierId=&limit=100&offset=0"
```

#### Create a purchase order

```bash
curl "http://localhost:3000/api/purchase-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "supplierId": 1,
    "supplierName": "Supplier Inc",
    "reqDeliveryDt": "2026-03-15",
    "targetDeliveryDt": "2026-03-20",
    "expirationDt": "2026-04-01",
    "targetWarehouseId": 1,
    "deliveryAddress": null,
    "remarks": null,
    "lines": [
      {
        "prodId": 1,
        "prodName": "Product One",
        "sku": "SKU-001",
        "qtyRequestedTotal": 10,
        "qtyApprovedTotal": 10,
        "unitPrice": 8,
        "effectivePrice": 8,
        "subTotal": 80
      }
    ]
  }'
```

---

### Invoices and payments (read-only views)

These endpoints are read-only and are intended for AR/AP and accounting views.

- **List sale invoices**  

```bash
curl "http://localhost:3000/api/sale-invoices?customerId=&status=&limit=100&offset=0"
```

- **List purchase invoices**  

```bash
curl "http://localhost:3000/api/purchase-invoices?supplierId=&status=&limit=100&offset=0"
```

- **List customer payments (AR)**  

```bash
curl "http://localhost:3000/api/cust-payments?customerId=&status=&limit=100&offset=0"
```

- **List supplier payments (AP)**  

```bash
curl "http://localhost:3000/api/payments?supplierId=&status=&limit=100&offset=0"
```

For returns and credit/debit memos, see [returns-and-memos.md](returns-and-memos.md).

