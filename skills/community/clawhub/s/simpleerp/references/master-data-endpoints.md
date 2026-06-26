## Master data endpoints

This reference groups core master data resources: system parameters, currencies, warehouses, account managers, partners, customers, and suppliers.

All examples assume the base URL `http://localhost:3000/api`.

## Table of contents

- System parameters (`/sys-par`)
- Currencies (`/currencies`)
- Warehouses (`/warehouses`)
- Account managers (`/account-managers`)
- Partners, customers, suppliers

---

### System parameters (`/sys-par`)

#### List system parameters

```bash
curl "http://localhost:3000/api/sys-par?codePrefix=&limit=100&offset=0"
```

#### Create a system parameter

```bash
curl "http://localhost:3000/api/sys-par" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "MY_PARAM",
    "description": "My parameter",
    "value": "value1",
    "internal": "N",
    "enabled": "Y",
    "dataType": "S"
  }'
```

---

### Currencies (`/currencies`)

#### List currencies

```bash
curl "http://localhost:3000/api/currencies?status=&limit=100&offset=0"
```

#### Create a currency

```bash
curl "http://localhost:3000/api/currencies" \
  -H "Content-Type: application/json" \
  -d '{
    "currencyCode": "USD",
    "symbol": "$",
    "description": "US Dollar",
    "status": "A"
  }'
```

---

### Warehouses (`/warehouses`)

#### List warehouses

```bash
curl "http://localhost:3000/api/warehouses?status=&limit=100&offset=0"
```

#### Create a warehouse

```bash
curl "http://localhost:3000/api/warehouses" \
  -H "Content-Type: application/json" \
  -d '{
    "warehouseName": "Main Warehouse",
    "address": "123 Street",
    "contactPerson": "John",
    "contactInfo": "john@example.com",
    "status": "A",
    "tags": null,
    "expenseAccount": null
  }'
```

---

### Account managers (`/account-managers`)

Account managers are optional links to internal users (`USER_ID`) and contact info for sales/account ownership on customers.

#### List account managers

```bash
curl "http://localhost:3000/api/account-managers?limit=100&offset=0"
```

#### Create an account manager

```bash
curl "http://localhost:3000/api/account-managers" \
  -H "Content-Type: application/json" \
  -d '{
    "mgrName": "Jane Smith",
    "userId": null,
    "contactInfo": "jane@example.com"
  }'
```

`mgrName` is required; `userId` and `contactInfo` are optional.

---

### Partners, customers, suppliers

Partners are shared between customers and suppliers. Use `/partners` to create a shared partner, then `/customers` or `/suppliers` for role-specific data.

#### Create a partner (`/partners`)

```bash
curl "http://localhost:3000/api/partners" \
  -H "Content-Type: application/json" \
  -d '{
    "partnerName": "Acme Corp",
    "isSupplier": "Y",
    "isCustomer": "Y",
    "email": "contact@acme.com",
    "mobile": null,
    "address": null,
    "url": null,
    "tin": null,
    "tags": null,
    "currencyCode": "USD",
    "status": "A",
    "remarks": null,
    "language": "en",
    "areaId": null
  }'
```

#### Create customer with new partner (`/customers`)

```bash
curl "http://localhost:3000/api/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "partnerName": "Customer Co",
    "currencyCode": "USD",
    "language": "en",
    "email": null,
    "mobile": null,
    "address": null,
    "billingAddress": null,
    "accountMgrId": null,
    "warehouseId": null,
    "creditLimit": 0,
    "priceListId": 1
  }'
```

#### Create customer from existing partner (`/customers`)

```bash
curl "http://localhost:3000/api/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "partnerId": 1,
    "billingAddress": null,
    "accountMgrId": null,
    "warehouseId": null,
    "creditLimit": 0,
    "priceListId": 1
  }'
```

#### List customer warehouses

```bash
curl "http://localhost:3000/api/customers/1/warehouses"
```

#### Suppliers (`/suppliers`)

Suppliers follow the same pattern as customers, with payloads matching the Postman “Suppliers” examples.

---

**See also:** [products-and-pricing.md](products-and-pricing.md), [documents-sales-purchasing.md](documents-sales-purchasing.md), [inventory-and-deliveries.md](inventory-and-deliveries.md).

