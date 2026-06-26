---
name: sparky
description: SparkyFitness CLI for food diary, exercise tracking, biometric check-ins, and health summaries.
homepage: https://github.com/CodeWithCJ/SparkyFitness
metadata: {"clawdbot":{"emoji":"🏃","requires":{"bins":["sparky"]}}}
---

# sparky

Use `sparky` to interact with a self-hosted SparkyFitness server — log food, exercise, weight, steps, and mood.

Install
- Homebrew (macOS/Linux): `brew tap aronjanosch/tap && brew install sparky-cli`
- Build from source (requires Go 1.21+):
  ```
  git clone https://github.com/aronjanosch/sparky-cli
  cd sparky-cli
  go build -o sparky .
  sudo mv sparky /usr/local/bin/
  ```
- Pre-built binaries: https://github.com/aronjanosch/sparky-cli/releases (Linux, macOS, Windows — amd64/arm64)

Setup (once)
- `sparky config set-url <url>` — e.g. `sparky config set-url https://sparky.example.com`
- `sparky config set-key <key>`
- `sparky config show`
- `sparky ping` — verify connection

Food
- Search: `sparky food search "chicken breast" [-l 10]` — local DB first, falls back to Open Food Facts; shows Brand column
- Search by barcode: `sparky food search --barcode 4061458284547` — exact product lookup, no ambiguity
- Log by name: `sparky food log "chicken breast" -m lunch -q 150 -u g [-d YYYY-MM-DD]`
- Log by barcode: `sparky food log --barcode 4061458284547 -m lunch -q 113 -u g` — most reliable, no brand guessing
- Log by ID: `sparky food log --id <uuid> -m lunch -q 150 -u g` — skips search, unambiguous
- Pick result: `sparky food log "Hähnchenbrust" --pick 2` — select Nth search result instead of prompting
- Create custom: `sparky food create "My Meal" --calories 450 --protein 28 --carbs 42 --fat 16` — adds a custom food to your library; defaults to 100g serving; optional: --fiber, --sugar, --sodium, --saturated-fat, --brand, --serving-size, --serving-unit
- Diary: `sparky food diary [-d YYYY-MM-DD]`
- Delete entry: `sparky food delete <uuid>` — removes a diary entry
- Remove from library: `sparky food remove <uuid>` — purge a food from your local library (get UUID via `sparky -j food search`)

Exercise
- Search: `sparky exercise search "bench press" [-l 10]` — local DB first, falls back to Free Exercise DB
- Search external only: `sparky exercise search --external "pushup"` — bypasses local cache
- Log by name: `sparky exercise log "Pushups" [--duration 45] [--calories 400] [-d YYYY-MM-DD]`
- Log by ID: `sparky exercise log --id <uuid> --set 10x80@8 --set 10x80@9` — skips search, unambiguous
- Sets format: `REPS[xWEIGHT][@RPE]` — e.g. `10x80@8` = 10 reps, 80 kg, RPE 8; `10x80` or `10@8` also valid
- Notes: `sparky exercise log "Pushups" --notes "felt strong"`
- Diary: `sparky exercise diary [-d YYYY-MM-DD]`
- Delete: `sparky exercise delete <uuid>`

Check-ins
- Weight: `sparky checkin weight 75.5 [-u kg|lbs] [-d YYYY-MM-DD]`
- Steps: `sparky checkin steps 9500 [-d YYYY-MM-DD]`
- Mood: `sparky checkin mood 8 [-n "notes"] [-d YYYY-MM-DD]`
- Diary: `sparky checkin diary [-d YYYY-MM-DD]` — shows biometrics + mood together

Summary & trends
- `sparky summary [-s YYYY-MM-DD] [-e YYYY-MM-DD]` — nutrition/exercise/wellbeing totals (default: last 7 days)
- `sparky trends [-n 30]` — day-by-day nutrition table

Agentic workflow (always prefer --id to avoid ambiguity)

Exercise — search first, then log by ID:
```
# 1. Find candidates; use --external to bypass local cache if needed
sparky -j exercise search --external "pushup"
# Each result has is_local: true/false
#   is_local: true  → id is a UUID → use --id directly
#   is_local: false → id is a source string → log by exact name to import first,
#                     then search again to get the UUID

# 2a. Local exercise
sparky -j exercise log --id <uuid> --set 3x10@8

# 2b. External exercise (import on first log, then switch to --id)
sparky -j exercise log "Pushups" --set 3x10
sparky -j exercise search "Pushups"        # now is_local: true
sparky -j exercise log --id <uuid> --set 3x10
```

Food — preferred agentic workflow:
```
# Option A: barcode (most reliable)
sparky food log --barcode 4061458284547 -q 113 -u g -m lunch

# Option B: search → inspect brand+macros → log by --id
sparky -j food search "Hähnchenbrust"
# check brand + calories in results; pick the right one
sparky food log --id <uuid> -q 400 -u g -m dinner

# Option C: search with --pick N (when brand column shows the right one)
sparky food log "Hähnchenbrust" --pick 3 -q 400 -u g -m dinner

# Remove a bad import from local library
sparky -j food search "bad product"   # get the food's id (UUID)
sparky food remove <uuid>
```

Custom food (when you have nutrition facts and it's not in the DB):
```
# Ingredients/beverages — nutrition per 100g/ml (default)
sparky -j food create "Craft Beer" --calories 43 --protein 0.5 --carbs 3.6 --fat 0 --serving-unit ml
sparky -j food log --id <uuid> -q 330 -m dinner

# Meals (Cookidoo, Chefkoch, etc.) — nutrition per serving, specify explicitly
sparky -j food create "Lasagna" --calories 450 --protein 28 --carbs 42 --fat 16 --serving-size 1 --serving-unit serving
sparky -j food log --id <uuid> -q 1 -m dinner
```

Notes
- `-j` / `--json` is a **root-level flag**: `sparky -j food diary`, not `sparky food diary -j`
- Always verify brand in search results before logging — Open Food Facts has many products with identical names
- `--barcode` is the most reliable option when the product has a scannable barcode
- `--pick N` selects the Nth result (1-based); exact local name match bypasses `--pick` entirely
- In JSON mode with ambiguous results, the CLI always picks `results[0]` — use `--id` in scripts to be safe
- Both search commands fall back to online providers automatically; matches are added to your library on first log
- Weight is stored in kg; lbs are auto-converted (`166 lbs → 75.30 kg`)
- Full UUIDs for delete: `sparky -j food diary | jq '.[0].id'`
- Meal options: `breakfast`, `lunch`, `dinner`, `snacks` (default: `snacks`)
