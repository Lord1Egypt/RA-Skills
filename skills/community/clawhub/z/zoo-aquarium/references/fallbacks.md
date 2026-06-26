# Fallbacks — Attraction Category

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli && flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Attractions Found

```bash
# Broader category
flyai search-poi --city-name "{city}" --poi-level 5
# Broad search
flyai keyword-search --query "{city} attractions"
```

## Case 2: Wrong City Name

```
→ Try Chinese/English variants → Ask user to confirm
```

## Case 3: Category Returns Empty

```bash
flyai search-poi --city-name "{city}"  # Remove category filter
```

## Case 4: Parameter Conflict

```bash
flyai search-poi --city-name "{city}"
flyai keyword-search --query "{city} things to do"
```

## Case 5: API Timeout

```
Retry once → Simplify → Report honestly.
```
