## Products, price lists, and related master data

This reference covers product and pricing-related endpoints.

Base URL: `http://localhost:3000/api`.

---

### Products (`/products`)

#### List products

```bash
curl "http://localhost:3000/api/products?status=&sku=&limit=100&offset=0"
```

#### Create a product

```bash
curl "http://localhost:3000/api/products" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "SKU-001",
    "prodName": "Product One",
    "barcode": null,
    "baseUnit": "EA",
    "description": null,
    "status": "A",
    "forPurchase": "Y",
    "forSale": "Y",
    "tags": null,
    "srp": 10.5,
    "catId": null,
    "brandId": null
  }'
```

---

### Price lists (`/price-lists`)

#### List price lists

```bash
curl "http://localhost:3000/api/price-lists?status=&limit=100&offset=0"
```

#### Create a price list

```bash
curl "http://localhost:3000/api/price-lists" \
  -H "Content-Type: application/json" \
  -d '{
    "priceListName": "Default",
    "priceInclusion": "NET",
    "currencyCode": "USD",
    "srcPriceList": null,
    "status": "A",
    "customerId": null
  }'
```

---

### Other master-data resources

Other master-data resources (areas, brands, categories, credit terms, UOM, tax, warehouse zones, bank accounts, memberships, journal categories) follow a consistent pattern:

- List:

```bash
curl "http://localhost:3000/api/<resource>?status=&limit=100&offset=0"
```

- Create: use resource-specific fields in the JSON body. See [SKILL.md](../SKILL.md) (domain map) or the Postman collection for each resource (areas, brands, categories, credit terms, UOM, tax, warehouse zones, bank accounts, memberships). Example for a minimal payload:

```bash
curl "http://localhost:3000/api/<resource>" \
  -H "Content-Type: application/json" \
  -d '{"fieldName": "value", ...}'
```

