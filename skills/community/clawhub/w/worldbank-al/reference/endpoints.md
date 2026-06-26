# Reference · Endpoints & Tools

The 6 MCP tools and the generic passthrough pattern. All map to
`https://api.worldbank.org/v2`; the server always sends `format=json`. **The API
is open — no API key.**

---

## The 6 tools

| Tool | Maps to | Inputs | Returns |
|------|---------|--------|---------|
| `worldbank_search_indicators` | indicator catalog (filtered) | `q`, `limit?` | `[{ id, name, ... }]` |
| `worldbank_indicator_metadata` | `/indicator/{id}` | `indicator` | metadata object |
| `worldbank_indicator_data` | `/country/{country}/indicator/{indicator}` | `country`, `indicator`, `date?`, `mrv?`, `per_page?`, `page?` | data array of records |
| `worldbank_country` | `/country/{country}` (or list) | `country?` | country metadata |
| `worldbank_topics` | `/topic` | — | `[{ id, value, sourceNote }]` |
| `worldbank_request` | **any** `/v2` endpoint | `endpoint`, `params?` | raw `[meta, data]` |

---

## Generic passthrough pattern (`worldbank_request`)

Use when no dedicated tool fits. `endpoint` is a **path relative to the base**
(no scheme, host, or leading slash). `params` are query parameters; `format=json`
is added automatically. Returns the **raw** `[paginationMeta, dataArray]`.

Common endpoints reachable this way:

| `endpoint` | Returns |
|------------|---------|
| `topic` | All topics |
| `source` | Data sources (with `lastupdated`) |
| `region` | Regions |
| `incomelevel` | Income-level groups (HIC, UMC, LMC, LIC, …) |
| `lendingtype` | Lending types (IBD, IDX, …) |
| `topic/{id}/indicator` | Indicators under a topic |
| `country/{country}/indicator/{indicator}` | Data (same as dedicated tool) |

Example:

```json
{ "tool": "worldbank_request",
  "arguments": { "endpoint": "topic/3/indicator", "params": { "per_page": 50 } } }
```

---

## Response unwrapping

- **Dedicated tools** unwrap `[meta, data]` and return the **data array**.
- **`worldbank_request`** returns the **raw `[meta, data]`** — read index 0 for
  pagination, index 1 for records.

---

## Catalog pointer

For the full, authoritative endpoint and indicator catalog, consult the World
Bank API docs:

- API basic call structure & developer info:
  https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- Indicator browser: https://data.worldbank.org/indicator

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
