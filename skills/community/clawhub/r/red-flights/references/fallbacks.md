# Fallbacks — Flight Category (Red Eye)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
# Tell user: "Please run npm i -g @fly-ai/flyai-cli manually."
```

## Case 1: No Red Eye Flights Found

```bash
# Step 1 → Expand time window to 19:00–07:00
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 19 --dep-hour-end 7 --sort-type 3
# Step 2 → Remove time filter entirely
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
# Step 3 → Flexible dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --dep-hour-start 21 --sort-type 3
# Step 4 → Suggest daytime flights as alternative
```

## Case 2: All Red Eyes Over Budget

```bash
# Relax budget 30%
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --max-price {budget*1.3} --sort-type 3
# Try different date
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --dep-hour-start 21 --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX, "Osaka" → KIX/ITM, "Seoul" → ICN/GMP
→ Ask user which airport
```

## Case 4: Invalid Date

```
→ Do NOT search. "This date has passed."
→ Auto-search next available date
```

## Case 5: Parameter Conflict / Invalid Argument

**Trigger:** CLI returns error containing "invalid", "conflict", or non-zero exit code.

```bash
# Step 1 → Retry with minimum required params only
flyai search-flight --origin "{o}" --destination "{d}" --dep-hour-start 21 --dep-hour-end 6 --sort-type 3

# Step 2 → Fallback to broad search
flyai keyword-search --query "{origin} to {destination} red eye flights"

# Step 3 → Still fails → report error honestly with raw command for debugging
```

## Case 6: API Timeout / Network Error

**Trigger:** CLI hangs >30s or returns network error.

```bash
# Step 1 → Retry once
flyai search-flight --origin "{o}" --destination "{d}" --dep-hour-start 21 --sort-type 3

# Step 2 → Simplify query (fewer params = faster)
flyai keyword-search --query "{origin} to {destination} late night flights"

# Step 3 → Still timeout → report honestly. Do NOT substitute with training data.
```
