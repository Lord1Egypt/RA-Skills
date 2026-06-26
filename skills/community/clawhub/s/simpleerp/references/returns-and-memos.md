## Returns and memos

This reference covers customer and supplier returns, and related credit/debit memos.

Base URL: `http://localhost:3000/api`.

---

### Customer returns (`/cust-returns`)

#### List customer returns

```bash
curl "http://localhost:3000/api/cust-returns?status=&customerId=&saleOrderId=&limit=100&offset=0"
```

#### Create a customer return

```bash
curl "http://localhost:3000/api/cust-returns" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 1,
    "saleOrderId": 10,
    "warehouseId": 1,
    "custWarehouseId": 1,
    "deliveryAddress": "Return Address",
    "status": "D",
    "lines": [
      {
        "prodId": 1,
        "qtyNormal": 2,
        "qtyDamaged": 0,
        "unitPrice": 10.5
      }
    ]
  }'
```

---

### Customer credit memos and debit notes (list only)

- **List customer credit memos** — `GET /api/cust-credit-memos?status=&customerId=&limit=100&offset=0`
- **List customer debit notes** — `GET /api/cust-debit-notes?status=&customerId=&limit=100&offset=0`

---

### Supplier returns (`/supp-returns`)

#### List supplier returns

```bash
curl "http://localhost:3000/api/supp-returns?status=&supplierId=&limit=100&offset=0"
```

#### Create a supplier return

```bash
curl "http://localhost:3000/api/supp-returns" \
  -H "Content-Type: application/json" \
  -d '{
    "supplierId": 1,
    "supplierRefNo": "RET-001",
    "returnDt": "2026-03-20",
    "currencyCode": "USD",
    "warehouseId": 1,
    "remarks": null,
    "lines": [
      {
        "prodId": 1,
        "qtyNormal": 5,
        "qtyDamaged": 0,
        "qtyReturnAvail": 5,
        "normalPrice": 8,
        "damagedPrice": 0
      }
    ]
  }'
```

---

### Supplier credit memos and debit notes (list only)

- **List supplier credit memos** — `GET /api/supp-credit-memos?status=&supplierId=&limit=100&offset=0`
- **List supplier debit notes** — `GET /api/supp-debit-notes?status=&supplierId=&limit=100&offset=0`
