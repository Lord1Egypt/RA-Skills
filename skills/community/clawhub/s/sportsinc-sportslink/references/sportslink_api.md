# SportsLink API — reference (distilled from the 2024 Dealers spec)

The `scripts/sportslink.py` helper wraps all of this; read here when you need a
parameter, a field, or the semantics behind one.

## Basics

- **Base URL:** `https://api.sportsinc.com/`
- **Auth:** API key in the `X-API-KEY` request header. Request one from
  `mhoerner@hq.sportsinc.com`.
- **Limits:** max **1000 documents per call** — page. Don't retrieve before
  **~10:30am ET** (SI internal processing completes first).

## GET `/dealers/documents/` — the invoices

Returns JSON documents from the SportsWeb Invoice Center.

### Query parameters (all optional)

| Param | Type | Notes |
|---|---|---|
| `poNumber` | string | **Dealer PO number** — the match key to your ERP PO |
| `supplierDocNumber` | string | The underlying supplier's document number |
| `siDocNumber` | int | Sports Inc's document id (used to mark historical) |
| `siDocDate` / `siDocStartDate` / `siDocEndDate` | date `yyyy-MM-dd` | SI processing date. A single date or `start,end`. Start-only = on/after; end-only = on/before |
| `supplierDocDate` / `supplierDocStartDate` / `supplierDocEndDate` | date | Supplier document date, same range semantics |
| `lines` | bool (default false) | Include line-item data — **EDI documents only** |
| `active` | bool (default false) | Only documents **not** marked historical (the un-imported inbox) |
| `moveToHistorical` | bool (default false) | Mark the returned docs historical **on read** — ⚠️ do NOT use for billing (marks before you've billed); use the PATCH endpoint after billing instead |
| `excludeScannedDocuments` | bool (default false) | Only documents with line-item data (EDI); scanned/OCR docs have none |
| `fields` | string[] | Sparse fieldset — return only these properties |
| `page` / `pageSize` | int | Paging (`pageSize` default = total doc count) |
| `orderBy` (default `SIDocDate`) / `orderByDescending` | string / bool | Sorting |

Example: `GET /dealers/documents/?siDocDate=2024-01-31&lines=true&active=true`

### Response envelope

`{ items: [ …document… ], pageNumber, pageSize, totalPages, totalCount,
hasPreviousPage, hasNextPage, orderBy, orderByDescending }`

### Document (header) fields

`poNumber`, `siDocNumber`, `siDocDate`, `dueDate`, `discountDate`,
`requestedShipDate`, `shipDate`, `supplierDocNumber`, `supplierDocDate`,
`supplier`, `isCredit`, plus money: `merchandiseTotal`, `freightAmount`,
`freightAllowance`, `discountAmount`, `siUpcharge`, `svcHandleCharge`,
`salesTax`, `exciseTax`, `docTotal`. Also `termsOfPayment`, `termsOfDelivery`,
`carrier`, `weight`, `trackingNumber`, `methodOfPayment`, `supplierAddress{}`,
`shippingAddress{}`. Missing/OCR-unavailable properties are simply omitted.

### Line fields (EDI only)

`supplierItemNumber`, `upc`, `quantityShipped`, `quantityOrdered`,
`quantityBackOrdered`, `unit`, `listPrice`, `discountPercent`, `netPrice`,
`extension`, `size`, `color`, `description`.

`docTotal` = `merchandiseTotal` + `siUpcharge` + `svcHandleCharge` +
`freightAmount` + `salesTax` + `exciseTax` − `discountAmount` −
`freightAllowance` (SI-specific charges included — this is what you'll be
billed, and what the ERP bill's `expected_total` should tie to).

## PATCH `/dealers/documents/status` — mark consumed

Body: `{ "siDocNumbers": [12345, 23456], "isActive": false }`
- `isActive: false` → historical (moves to the Invoice Center "Historical" tab).
- `isActive: true` → back to active.

Responses: `204 No Content` (success), `400` (bad body), `401` (bad key).

**Use this to mark documents consumed AFTER a bill is created** — the exactly-once
seam. Prefer it over `moveToHistorical=true` on the GET, which marks on read.

## ⚠ Scanned documents return a **placeholder line**, not an empty array

Observed live on `siDocNumber` 24684277 (merchandise total 398.40, whose vendor
invoice really has two lines) — the API returned `lines` containing exactly one
row:

```json
{"supplierItemNumber": "", "upc": null, "size": null, "color": null, "unit": "",
 "quantityOrdered": 0, "quantityShipped": 0, "quantityBackOrdered": 0,
 "listPrice": 0.0, "discountPercent": null, "netPrice": 0.0, "extension": 0.0,
 "description": "SEE VENDOR INVOICE FOR DETAIL."}
```

The row is **not blank**. It carries SI's own instruction — the same sentence
printed on the cover page of the PDF. So a free-text `description` is not
evidence of a real line; here it is evidence of the opposite.

The spec's "scanned/OCR documents have no line data" is therefore not literally
true at the wire level, and the naive test for it is wrong:

```python
has_lines = bool(document.get("lines"))   # ← WRONG: true for a stub
```

That mistake is quiet and expensive. A scanned document announces itself as
EDI-backed, and any consumer branching on `has_lines` — the payables workflow
does, to decide between line-matching and escalating — line-matches against a
row of zeroes rather than escalating or reading the PDF.

`scripts/sportslink.py` filters these out. A line is real if it **identifies a
product** (`supplierItemNumber` or `upc`) or carries a **non-zero number**.
`description`, `size`, `color` and `unit` are descriptive and do not qualify on
their own: with every quantity and price at zero there is nothing billable, and
treating the description as identity is exactly what let this row through the
first time.

`has_lines` is computed from what survives; `placeholder_lines` counts the
dropped rows and `placeholder_note` keeps their text, so neither the filtering
nor SI's explanation is lost. A legitimately fully-backordered line — zero
shipped, but with an item number and a backorder quantity — is kept.

**Corollary worth applying elsewhere:** because the API can hand back line data
that is present but not complete, any line set is worth checking against
`merchandiseTotal` before it is billed, whether it came from EDI or a PDF.

## Failure modes to expect

- `401` — bad/expired key (the helper surfaces `auth_error`).
- Transient `429`/`5xx`/timeouts — the helper retries with backoff.
- Missing fields — OCR gaps or supplier-not-provided; simply absent, not null.
- Scanned docs — no `lines`; `has_lines: false` in the normalised shape.
