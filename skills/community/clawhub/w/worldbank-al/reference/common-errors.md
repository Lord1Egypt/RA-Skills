# Reference · Common Errors

Each entry: **cause** and the correct **agent reaction**. The API is **open — no
API key**, so authentication errors do not exist here.

---

## The message-array error body

```json
[ { "message": [ { "id": "120", "key": "Invalid value",
  "value": "The provided parameter value is not valid" } ] } ]
```

- **Cause:** an invalid parameter — almost always a wrong **indicator code** or
  **country code**, or a malformed param.
- **Reaction:** read `key`/`value`; fix the code/param using
  `worldbank_search_indicators` or `worldbank_country`; retry **once**. Do **not**
  blindly retry the same request.

---

## Empty data array `[]`

- **Cause:** valid request, but no rows for that country/indicator/date.
- **Reaction:** widen the `date` range, switch to `mrv: N`, or try another
  country. Verify the codes.

---

## Null values in records

- **Cause:** specific years have no observation (recent annual lag or coverage
  gap).
- **Reaction:** report "data not available" for those years. **Never invent** a
  number or use `0`.

---

## HTTP 429 (rate limited)

- **Cause:** too many requests to the free, open API.
- **Reaction:** the server retries with backoff (`WORLDBANK_MAX_RETRIES`). Slow
  down, batch queries, cache annual data.

---

## 5xx (upstream error)

- **Cause:** transient World Bank server issue.
- **Reaction:** the server retries with backoff; if persistent, treat as a
  temporary outage and inform the user.

---

## Timeout

- **Cause:** request exceeded `WORLDBANK_TIMEOUT_MS` (default 30000 ms),
  typically a very large pull.
- **Reaction:** narrow the query (fewer countries, smaller `per_page`, shorter
  range) or raise the timeout in config.

---

## XML instead of JSON

- **Cause:** calling the API **directly** without `format=json` (the API defaults
  to XML). Through the MCP tools this cannot happen — the server always sends
  `format=json`.
- **Reaction:** if calling the raw API yourself, add `?format=json`.

---

## Quick decision table

| Symptom | Likely cause | Reaction |
|---------|--------------|----------|
| `[{message:[...]}]` | Bad code/param | Fix and retry once |
| `[]` | No rows for query | Widen date / mrv / verify codes |
| `value: null` | Missing observation | Report "no data"; never invent |
| 429 | Rate limit | Back off, cache |
| 5xx | Upstream issue | Retry/transient outage |
| Timeout | Query too large | Narrow query / raise timeout |
| XML | Direct call w/o `format=json` | Add `format=json` |

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
