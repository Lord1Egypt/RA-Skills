# Reference · Response Fields

The shape of World Bank responses, the `[meta, data]` pagination wrapper, null
handling, and how to cite. **The API is open — no API key.**

---

## Observation record fields

Each data observation has these fields:

| Field | Type | Description |
|-------|------|-------------|
| `indicator` | `{ id, value }` | Indicator code and human name. |
| `country` | `{ id, value }` | Country **ISO2** code (`id`) and name (`value`). |
| `countryiso3code` | string | The **ISO3** code (e.g. `USA`). |
| `date` | string | The year, e.g. `"2023"`. |
| `value` | number \| `null` | The observation; **`null` = missing**. |
| `unit` | string | Unit (often empty; check metadata for the real unit). |
| `obs_status` | string | Observation status flag (often empty). |
| `decimal` | number | Decimal precision hint. |

Example:

```json
{
  "indicator": { "id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)" },
  "country": { "id": "US", "value": "United States" },
  "countryiso3code": "USA",
  "date": "2023",
  "value": 27360935000000,
  "unit": "",
  "obs_status": "",
  "decimal": 0
}
```

---

## Pagination wrapper `[meta, data]`

World Bank **data** endpoints return a two-element array:

```json
[
  { "page": 1, "pages": 3, "per_page": 50, "total": 142, "lastupdated": "2024-12-16" },
  [ /* observation records */ ]
]
```

| Meta field | Meaning |
|------------|---------|
| `page` | Current page. |
| `pages` | Total pages. |
| `per_page` | Rows per page. |
| `total` | Total matching rows. |
| `lastupdated` | When the source was last refreshed (use for caching). |

- **Dedicated tools** unwrap this and hand you the **data array** (index 1).
- **`worldbank_request`** returns the **raw** pair; read index 0 for meta, index
  1 for records. If `pages > 1`, fetch the next page with `params: { "page": 2 }`.

---

## Null values

`value: null` means **no observation** for that country/year — typically a
recent year not yet published, or a gap in coverage.

- Report it as "data not available".
- **Never** substitute `0` or an invented number.

---

## How to cite

Use this format with fields from the record + metadata:

> **World Bank, <indicator.value> (<indicator.id>), <country.value>, <date>.**
> https://data.worldbank.org/indicator/<indicator.id>

Concrete:

> **World Bank, GDP (current US$) (NY.GDP.MKTP.CD), United States, 2023.**
> https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
