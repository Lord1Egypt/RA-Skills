## Inventory and deliveries

Inventory and deliveries connect stock levels with inbound/outbound documents.

Base URL: `http://localhost:3000/api`.

---

### Inventory (`/inventory`)

#### List inventory (filter by warehouse/product)

```bash
curl "http://localhost:3000/api/inventory?warehouseId=&prodId=&limit=100&offset=0"
```

#### Get inventory for a specific warehouse and product

```bash
curl "http://localhost:3000/api/inventory/1/1"
```

---

### Deliveries (`/deliveries`)

#### List deliveries

```bash
curl "http://localhost:3000/api/deliveries?orderId=&warehouseId=&status=&limit=100&offset=0"
```

---

### Inventory transfers (`/transfers`)

#### List transfers

```bash
curl "http://localhost:3000/api/transfers?status=&fromWhId=&toWhId=&limit=100&offset=0"
```

#### Create a transfer

```bash
curl "http://localhost:3000/api/transfers" \
  -H "Content-Type: application/json" \
  -d '{
    "fromWhId": 1,
    "toWhId": 2,
    "requestDt": "2026-03-21",
    "reqDeliveryDt": "2026-03-22",
    "estDeliveryDt": "2026-03-23",
    "reason": "Rebalance stock",
    "lines": [
      {
        "prodId": 1,
        "qtyRequestedTotal": 10,
        "qtyApprovedTotal": 10,
        "qtyDoneTotal": 0
      }
    ]
  }'
```

---

### Inventory adjustments (`/inventory-adjustments`)

#### List inventory adjustments

```bash
curl "http://localhost:3000/api/inventory-adjustments?status=&warehouseId=&limit=100&offset=0"
```

#### Create an inventory adjustment

```bash
curl "http://localhost:3000/api/inventory-adjustments" \
  -H "Content-Type: application/json" \
  -d '{
    "warehouseId": 1,
    "adjType": "A",
    "adjDt": "2026-03-21",
    "remarks": "Stock count adjustment",
    "lines": [
      { "prodId": 1, "qtyTotal": 3 }
    ]
  }'
```

