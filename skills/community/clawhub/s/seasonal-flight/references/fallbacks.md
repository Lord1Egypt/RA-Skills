# Fallbacks — Flight Category (Seasonal Flight)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
# Tell user: "Please run npm i -g @fly-ai/flyai-cli manually."
```

## Case 1: No Seasonal Flights Found

```bash
# Step 1 → Expand date range ±7 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start-7} --dep-date-end {end+7} --sort-type 2
# Step 2 → Try single date
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {mid_season_date} --sort-type 2
# Step 3 → Try connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --journey-type 2 --sort-type 3
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} seasonal flights"
```

## Case 2: Peak Season Over Budget

```bash
# Try off-peak dates within season
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {shoulder_start} --dep-date-end {shoulder_end} --max-price {budget} --sort-type 3
# Try connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --max-price {budget} --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX
→ Ask user which airport
```

## Case 4: Invalid Date (Past Date)

```
→ Do NOT search. "This date has passed."
→ Suggest next available season
```

## Case 5: Parameter Conflict / Invalid Argument

**Trigger:** CLI returns error containing "invalid", "conflict", or non-zero exit code.

```bash
# Step 1 → Retry with minimum required params only
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2

# Step 2 → Fallback to broad search
flyai keyword-search --query "{origin} to {destination} seasonal flights"

# Step 3 → Still fails → report error honestly with raw command for debugging
```

## Case 6: API Timeout / Network Error

**Trigger:** CLI hangs >30s or returns network error.

```bash
# Step 1 → Retry once
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2

# Step 2 → Simplify query
flyai keyword-search --query "{origin} to {destination} flights"

# Step 3 → Still timeout → report honestly. Do NOT substitute with training data.
```
