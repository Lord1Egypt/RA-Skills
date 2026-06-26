# Skill: World Bank Open Data

> **FEATURED** — agent skill for retrieving, interpreting, and citing World Bank
> Open Data. Pairs with the `worldbank-mcp` server. **The API is open: NO API
> KEY is required.**

Use imperative voice. Follow these numbered rules.

---

## 1. Name

`worldbank` — World Bank Open Data skill.

## 2. Purpose

Equip the agent to find the right World Bank indicator, retrieve its annual
time series for one or more countries, interpret the values correctly, and cite
the result. Use this skill together with the **World Bank MCP server**, which
exposes 6 tools over stdio.

## 3. When to use World Bank

Use World Bank Open Data when the question involves:

- **Cross-country development indicators** — health, education, poverty,
  environment, infrastructure.
- **Macroeconomic indicators** with long annual history — GDP, GDP per capita,
  GDP growth, inflation, unemployment.
- **Demographics** — population, life expectancy, fertility.
- **Comparisons across many countries or regions**, including aggregates (World,
  income groups, regions).
- A need for **free, open, authoritative** data with deep historical coverage.

## 4. When NOT to use World Bank

Do **not** use World Bank for:

- **High-frequency or real-time** data (daily, intraday, monthly market data).
  Use FRED (for US/economic series) or a markets API instead.
- **The very latest quarter or month** — World Bank data is **annual** and the
  most recent year(s) are often not yet published (`null`).
- **Firm-level, ticker, or price data** — out of scope.

## 5. Environment

**NONE.** There is **no API key, token, or account**. The MCP server runs with
`"env": {}`. Optional tuning only: `WORLDBANK_API_BASE_URL`,
`WORLDBANK_TIMEOUT_MS`, `WORLDBANK_MAX_RETRIES`, `LOG_LEVEL`. Never add a
fictional `WORLDBANK_API_KEY`.

## 6. Operations (the 6 tools)

| Tool | Use it to |
|------|-----------|
| `worldbank_search_indicators` | Find indicator codes by keyword. |
| `worldbank_indicator_metadata` | Confirm name, unit, source, definition, topics. |
| `worldbank_indicator_data` | Fetch the time-series data (the main tool). |
| `worldbank_country` | Resolve country codes / metadata. |
| `worldbank_topics` | Browse the 20+ indicator topics. |
| `worldbank_request` | Generic passthrough to any `/v2` endpoint (source, region, incomelevel, lendingtype, topic/{id}/indicator, …). |

## 7. Discovery workflow

1. If the indicator code is unknown, call `worldbank_search_indicators` with a
   keyword and pick the best `{ id, name }`.
2. Optionally browse `worldbank_topics` to navigate by theme.
3. Confirm the chosen indicator's unit/definition with
   `worldbank_indicator_metadata` before reporting numbers.

Popular codes to recognize:

| Code | Indicator |
|------|-----------|
| `NY.GDP.MKTP.CD` | GDP (current US$) |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) |
| `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) |
| `SP.POP.TOTL` | Population, total |
| `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) |
| `SL.UEM.TOTL.ZS` | Unemployment (% of labor force) |
| `SP.DYN.LE00.IN` | Life expectancy at birth (years) |
| `EN.ATM.CO2E.PC` | CO2 emissions (metric tons per capita) |
| `SI.POV.DDAY` | Poverty headcount ratio (% of population) |

## 8. Data-retrieval workflow

1. Choose **country code(s)**: ISO3 (`USA`), ISO2 (`US`), `all`, or multiple
   joined with `;` (`USA;CHN;IND`).
2. Choose the **time window**: a fixed range `date: "2010:2023"` for trends, or
   `mrv: N` for the N most recent values.
3. Call `worldbank_indicator_data` with `country`, `indicator`, and
   `date`/`mrv` (use `per_page`/`page` only if needed; keep `per_page` modest).
4. Prefer a single multi-country call over many single-country calls.

## 9. Interpreting data

- `value` can be **`null`** for years with no observation — treat as missing.
- Data endpoints return `[paginationMeta, dataArray]`; the dedicated tools
  return the data array. With `worldbank_request`, read index 0 (meta) and index
  1 (records), and paginate when `pages > 1`.
- Always pair numbers with their **unit** (from metadata).
- Distinguish **aggregates** from countries: `WLD` (World), `EUU` (European
  Union), and income-level/region groups are not single countries.

## 10. Citation rules

Always cite. Use this exact pattern:

> **World Bank, <indicator name> (<code>), <country>, <year>.**
> https://data.worldbank.org/indicator/<code>

Include: "World Bank", indicator name + code, country, year(s), and the
indicator URL.

## 11. Freshness

- Data is **annual**. Note `lastupdated` (from pagination metadata via
  `worldbank_request`) when freshness matters.
- The most **recent year(s) may be `null`** because the value is not yet
  published. Do not present a missing recent year as zero or as a real figure.

## 12. Numeric integrity

**Never invent numbers.** A `null` value means missing — report it as "data not
available", not as 0. Quote only values returned by the tools.

## 13. Error handling

- `[{ "message": [...] }]` body → **invalid parameter/code**. Read `key`/`value`,
  fix the indicator/country code or param, retry once. Do **not** blindly retry.
- HTTP 429 → back off; rely on the server's retries and on caching.
- Empty array → widen the `date`, use `mrv`, or verify codes with
  `worldbank_search_indicators` / `worldbank_country`.

## 14. Cost

The API is **free and open**. Still be polite: cache annual data, reuse static
lookups (topics, country list, sources), avoid huge `per_page`, and do not loop
tightly.

## 15. Not economic advice

World Bank data is informational. Do **not** present analysis as financial,
investment, or economic advice. Report figures and cite sources.

## 16. Agent checklist

- [ ] Indicator code confirmed (searched if unknown).
- [ ] Unit/definition checked when it affects interpretation.
- [ ] Correct country code(s) and time window chosen.
- [ ] `null`/empty handled honestly (no invented values).
- [ ] Aggregates vs. countries distinguished.
- [ ] Citation included (World Bank + name + code + country + year + URL).
- [ ] No API key used (`"env": {}`).

## 17. Example workflows

- **Single figure:** search → metadata → `worldbank_indicator_data` with
  `mrv: 1` → cite.
- **Trend:** search → `worldbank_indicator_data` with `date: "2000:2023"` → chart
  → cite.
- **Comparison:** search → `worldbank_indicator_data` with `country:
  "USA;CHN;IND"` → table → cite.

See `recipes/` for full walkthroughs.

## 18. Common mistakes

- Guessing an indicator code instead of searching.
- Treating `null` as zero or inventing a value.
- Forgetting to cite.
- Confusing an aggregate (`WLD`, income group) with a country.
- Adding a nonexistent API key.
- Requesting the current quarter from an annual dataset.

## 19. Maintenance

- Periodically re-confirm popular codes via `worldbank_search_indicators`.
- Refresh cached series using the `lastupdated` field.
- Keep this skill paired with the `worldbank-mcp` server; if tool names change,
  update Section 6 and `reference/endpoints.md`.

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
