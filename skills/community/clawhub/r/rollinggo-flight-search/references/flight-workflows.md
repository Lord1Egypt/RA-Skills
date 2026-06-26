# RollingGo Flight Workflow Tutorials

This file collects step-by-step flight search tutorials. Commands below use the installed `rollinggo-flight` binary for readability.

If you want the newest release on every run, use one of these prefixes instead:

- **npx:** `npx --yes rollinggo-flight@latest`
- **uvx:** `uvx --refresh --from rollinggo-flight@latest rollinggo-flight`

---

## Workflow 1: City name → airport code → flight search

```bash
# Step 1: Resolve airport codes
rollinggo-flight search-airports --keyword "Hangzhou"
# → finds cityCode: HGH

rollinggo-flight search-airports --keyword "Chengdu"
# → finds cityCode: CTU

# Step 2: Search flights
rollinggo-flight search-flights \
  --from-city HGH --to-city CTU \
  --from-date 2026-06-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

## Workflow 2: Round-trip business class

```bash
# Step 1: Confirm airport codes
rollinggo-flight search-airports --keyword "Beijing"
rollinggo-flight search-airports --keyword "Shanghai"

# Step 2: Search round-trip
rollinggo-flight search-flights \
  --from-airport PEK --to-airport PVG \
  --from-date 2026-07-01 --ret-date 2026-07-07 \
  --trip-type ROUND_TRIP \
  --adult-number 2 --child-number 0 \
  --cabin-grade BUSINESS
```

## Workflow 3: Search directly when airport codes are already known

```bash
# No need to resolve airports if IATA codes are already known
rollinggo-flight search-flights \
  --from-airport PEK --to-airport HKG \
  --from-date 2026-08-15 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

## Workflow 4: Set an API key once, then run multiple searches

```bash
# PowerShell
$env:ROLLINGGO_API_KEY="YOUR_API_KEY"

rollinggo-flight search-airports --keyword "Guangzhou"
rollinggo-flight search-airports --keyword "Singapore"
rollinggo-flight search-flights \
  --from-city CAN --to-city SIN \
  --from-date 2026-09-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```

## Workflow 5: Use table output for human-readable review

```bash
# Airport results in table format
rollinggo-flight search-airports \
  --keyword "Tokyo" \
  --format table

# Flight results in table format
rollinggo-flight search-flights \
  --from-city TYO --to-city BJS \
  --from-date 2026-10-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY \
  --format table
```

## Workflow 6: Loosen filters when no results are returned

```bash
# First attempt: exact airport-to-airport search
rollinggo-flight search-flights \
  --from-airport PKX --to-airport NRT \
  --from-date 2026-11-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade BUSINESS

# If no results: switch to city codes to include multiple airports
rollinggo-flight search-flights \
  --from-city BJS --to-city TYO \
  --from-date 2026-11-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade BUSINESS

# If still no results: lower the cabin requirement
rollinggo-flight search-flights \
  --from-city BJS --to-city TYO \
  --from-date 2026-11-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY
```
