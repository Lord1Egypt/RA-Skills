# Fallbacks — Flight Category (Round-Trip)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Round-Trip Flights Found

```bash
# Step 1 → Flexible return dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --sort-type 2
# Step 2 → Remove sort filter
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep}
# Step 3 → Try connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --sort-type 2
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} round-trip flights"
```

## Case 2: All Flights Over Budget

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --max-price {budget*1.3} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX
→ Ask user which airport
```

## Case 4: Invalid Date / Back Date Before Dep Date

```
→ Do NOT search. "回程日期不能早于出发日期"
→ Ask user to correct dates
```

## Case 5: Parameter Conflict

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --sort-type 2
flyai keyword-search --query "{origin} to {destination} round-trip flights"
```

## Case 6: API Timeout

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --sort-type 2
flyai keyword-search --query "{origin} to {destination} round-trip flights"
# Still timeout → report honestly.
```
