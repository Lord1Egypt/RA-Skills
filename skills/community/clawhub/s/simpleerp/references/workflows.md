## End-to-end workflow examples

These workflows show how to chain multiple endpoints together for common ERP tasks. For global rules and the domain map, see [SKILL.md](../SKILL.md).

Base URL: `http://localhost:3000/api`.

## Table of contents

- Workflow 1: Create customer → Create sale order
- Workflow 2: Create supplier → Create purchase order
- Workflow 3: Check inventory and related deliveries

---

### Workflow 1: Create customer → Create sale order

1. **Create customer**

```bash
curl "http://localhost:3000/api/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "partnerName": "Customer Co",
    "currencyCode": "USD",
    "language": "en",
    "priceListId": 1
  }'
```

2. **Create sale order for that customer** (replace `1` with returned customer id if needed)

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
    "lines": [
      {
        "prodId": 1,
        "prodName": "Product One",
        "sku": "SKU-001",
        "qtyRequestedTotal": 5,
        "qtyApprovedTotal": 5,
        "unitPrice": 10.5,
        "effectivePrice": 10.5,
        "subTotal": 52.5
      }
    ]
  }'
```

---

### Workflow 2: Create supplier → Create purchase order

1. **Create supplier (new partner)**

```bash
curl "http://localhost:3000/api/suppliers" \
  -H "Content-Type: application/json" \
  -d '{
    "partnerName": "Supplier Inc",
    "currencyCode": "USD",
    "language": "en",
    "email": null,
    "mobile": null,
    "address": null,
    "warehouseId": null
  }'
```

2. **Create purchase order for that supplier**

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

### Workflow 3: Check inventory and related deliveries

1. **Check inventory for a product in a warehouse**

```bash
curl "http://localhost:3000/api/inventory?warehouseId=1&prodId=1&limit=10&offset=0"
```

2. **List deliveries for a related order**

```bash
curl "http://localhost:3000/api/deliveries?orderId=1&warehouseId=1&status=&limit=50&offset=0"
```

