# Tests · Failure Cases

Known bad behaviors, why they are wrong, and the corrected version. **The API is
open — no API key.**

---

## Failure 1 — No citation

**Bad:**
> "US GDP is about 27 trillion dollars."

**Why wrong:** No source, no indicator code, no year, no URL. Unverifiable.

**Corrected:**
> "US GDP was ~27.36 trillion (current US$) in 2023.
> Source: World Bank, GDP (current US$) (NY.GDP.MKTP.CD), United States, 2023.
> https://data.worldbank.org/indicator/NY.GDP.MKTP.CD"

---

## Failure 2 — Inventing values

**Bad:**
> Record has `"value": null` for 2024, agent reports "GDP in 2024 was 28 trillion".

**Why wrong:** Fabricates a number for a missing observation. Violates numeric
integrity.

**Corrected:**
> "2024 data is not yet available from the World Bank. The latest available year
> is 2023 (~27.36 trillion, current US$)."

---

## Failure 3 — Wrong / guessed codes

**Bad:**
> Agent calls `worldbank_indicator_data` with `indicator: "GDP.PERCAP"` (a code it
> made up) and reports whatever comes back.

**Why wrong:** Guessed code; triggers `[{message:[...]}]` or wrong data.

**Corrected:**
> Call `worldbank_search_indicators` (q="GDP per capita"), pick
> `NY.GDP.PCAP.CD`, confirm via metadata, then fetch.

---

## Failure 4 — Ignoring null/missing

**Bad:**
> Treats `null` as `0` and reports "Country X had 0 GDP growth in 2023".

**Why wrong:** `null` means missing, not zero. Misleads the user.

**Corrected:**
> "GDP growth for Country X in 2023 is not available in the World Bank dataset."

---

## Failure 5 — Wrong source for real-time

**Bad:**
> User asks for today's exchange rate; agent queries World Bank annual data.

**Why wrong:** World Bank is annual; it has no real-time/daily data.

**Corrected:**
> "World Bank provides annual data, not real-time rates. For today's exchange
> rate, use a markets/FX API or FRED for recent series."

---

## Failure 6 — Confusing aggregate with country

**Bad:**
> Reports `WLD` (World) or `HIC` (High income) as if it were a single country.

**Why wrong:** Aggregates are groups, not countries.

**Corrected:**
> "Note: `WLD` is the World aggregate, not a country; `HIC` is the High-income
> group." Label aggregates clearly.

---

## Failure 7 — Blind retry on a bad request

**Bad:**
> Receives `[{message:[...]}]` and retries the identical request repeatedly.

**Why wrong:** The error is caused by bad input; retrying unchanged cannot
succeed and may hit 429.

**Corrected:**
> Read the message, fix the indicator/country code, retry once with the corrected
> parameters.

---

## Failure 8 — Adding a fake API key

**Bad:**
> Adds `"WORLDBANK_API_KEY": "..."` to the config and tells the user to obtain a
> key.

**Why wrong:** The API is open; there is no key.

**Corrected:**
> Keep `"env": {}`. No key, token, or account is needed.

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
