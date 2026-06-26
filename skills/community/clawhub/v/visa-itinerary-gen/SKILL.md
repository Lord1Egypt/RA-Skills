---
name: visa-itinerary-gen
description: 一键生成领馆级签证行程计划书 — Generate consulate-grade visa itinerary from natural language. Real flyai data, zero hallucination. PDF + booking links with Fliggy.
homepage: https://github.com/zephryve/visa-itinerary-gen
metadata:
  version: 1.7.4
  agent:
    type: tool
    runtime: node
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "\U0001F4CB"
    priority: 80
    install:
      - kind: node
        package: "@fly-ai/flyai-cli"
        bins: [flyai]
      - kind: uv
        package: playwright
        bins: [playwright]
    requires:
      bins:
        - node
        - python3
        - flyai
      skills:
        - flyai
    intents:
      - visa_itinerary
      - travel_document
      - schengen_visa
    patterns:
      - "((visa|schengen|签证).*(itinerary|行程|plan|计划|行程单|行程表))"
      - "((generate|create|make|做|生成).*(visa|签证).*(itinerary|行程|plan|计划))"
      - "((travel plan|行程计划).*(visa|签证|consulate|领馆|embassy|大使馆))"
---

# visa-itinerary-gen — Visa Itinerary Generator

> **一句话说明：** 输入"4个人4月27号从杭州去意大利和法国，5月4号回"，一键生成领馆级签证行程计划书（PDF）+ 飞猪预订链接。省 ¥30-110 代做费，省 3-5 小时手工排版。

Generate a consulate-grade visa itinerary document with one command. Real data from flyai, zero hallucination.

## Execution Contract — Read This First

**You are a strict executor of this skill, not a co-designer.** Follow every step in the exact order written. Do NOT:

- **Skip steps** you consider unnecessary. Every step exists for a reason. If it says "run this command", run it. If it says "review this output", review it.
- **Reinterpret instructions.** "Pick the top-rated hotel" means pick the top-rated hotel. Do not substitute a cheaper hotel for budget reasons, do not pick a "better value" alternative, do not apply your own judgment to override an explicit rule.
- **Optimize on behalf of the user.** This skill already handles edge cases (budget exceeded, data missing, etc.) in specific steps. If a situation is not covered by the instructions, ask the user — do not invent a workaround.
- **Combine or reorder steps.** Step numbers are execution order. Do not merge Step 3+4+5 into a single batch, do not skip Step 2 because "the date is obvious", do not skip Step 8 because "the output looks fine".

**When in doubt, follow the literal instruction. When instructions conflict with your judgment, the instruction wins.**

## Step 0: Dependency Check — MANDATORY, DO NOT SKIP

When this skill is activated, **first run these checks before doing anything else**. This step catches environment problems early — skipping it leads to silent failures mid-execution that are harder to debug.

```bash
# 1. Check node (required by flyai-cli)
which node > /dev/null 2>&1 || echo "MISSING: node"

# 2. Check flyai-cli binary
which flyai > /dev/null 2>&1 || echo "MISSING: flyai-cli"

# 3. Check python3
which python3 > /dev/null 2>&1 || echo "MISSING: python3"

# 4. Check playwright (for PDF generation)
python3 -c "import playwright" 2>/dev/null || echo "MISSING: playwright"
```

If anything is missing, **ask the user for permission** before installing. Do NOT install silently — always confirm first.

- **node missing** → tell user: install Node.js from https://nodejs.org/ (cannot be auto-installed)
- **flyai-cli missing** → ask user: "flyai-cli is not installed. It's a free CLI tool (no API key needed) for searching flights, hotels, and attractions on Fliggy. Shall I install it? (`npm i -g @fly-ai/flyai-cli`)" → if user agrees, run the install command
- **python3 missing** → tell user: install Python 3 from https://python.org/ (cannot be auto-installed)
- **playwright missing** → ask user: "playwright is not installed. It's needed for PDF generation. Shall I install it? (`pip3 install playwright && python3 -m playwright install chromium`)" → if user agrees, run the install commands

After all dependencies are present, **verify flyai actually works**:

```bash
flyai fliggy-fast-search --query "test" > /dev/null 2>&1 && echo "flyai OK" || echo "flyai ERROR"
```

If flyai returns an error, warn the user but do not stop — it may still work for specific queries.

Only proceed to Step 1 when all dependencies are confirmed present.

## When to Use This Skill

Activate when the user wants to:
- Generate a travel itinerary for any visa application (Schengen, Japan, South Korea, Southeast Asia, etc.)
- Create a travel plan document for consulate/embassy submission
- Prepare visa application documents (specifically the itinerary)

## Input

The user provides a natural language description of their trip. Extract these parameters:

| Parameter | Required | Example |
|-----------|----------|---------|
| `destination` | Yes | "Italy and France" |
| `dates` | Yes | "Apr 27 - May 4" |
| `travelers` | Yes (default: 1) | 4 |
| `departure_city` | Yes | "Hangzhou" |
| `budget` | No | "60,000 CNY" |

Example: `"4个人4月27号从杭州去意大利和法国，5月4号回，预算6万"`

## Execution Steps

### Step 1: Parse Input & Validate

Extract destination cities, travel dates, number of travelers, departure city, and budget from the user's input.

**Mandatory validation — do NOT proceed to Step 2 until all required fields are confirmed:**

| Field | Required | How to resolve if missing |
|-------|----------|--------------------------|
| Destination (目的地) | Yes | Ask user |
| Departure city (出发城市) | Yes | Ask user |
| Departure date (出发日期) | Yes | Ask user |
| Trip duration (行程区间) | Yes — need either return date OR number of days | Ask user: "请问返回日期或出行天数？" |
| Travelers (出行人数) | No — default 1 | Use default |
| Budget (预算) | No | Skip |

If the user provides "玩7天" or "一共8天", calculate the return date from departure date + days. If only a return date is given, calculate trip days from the two dates. Either form is acceptable — the goal is to determine the full date range.

**Stop and ask the user if any of the 4 required fields cannot be determined from their input.** Do not guess or assume.

Once all fields are confirmed, plan a realistic day-by-day city routing. For multi-country trips, determine the city sequence. Example for Italy + France:
- Milan → Venice → Florence → Rome → Nice → Paris

### Step 2: Get Current Date — MANDATORY, DO NOT SKIP

```bash
date +%Y-%m-%d
```

You MUST run this command and use the output as the reference date. Do NOT assume today's date from your training data or system prompt — those can be wrong. This is the only reliable source of truth for date calculations. Use it to resolve relative dates ("next month", "this Friday", etc.).

### Step 3: Call flyai — Flights

**Retry rule (applies to all flyai calls in Step 3, 4, and 5):** If a flyai command returns empty results (null or empty itemList) or errors out, wait 3 seconds and retry once. If still failed, handle per the Error Handling table and continue to the next step.

Search for all flight segments. Flight search works with both Chinese and English city names, but prefer Chinese for consistency.

**International departure:**
```bash
flyai search-flight --origin "{出发城市}" --destination "{第一个目的城市}" --dep-date "{start_date}" --sort-type 3
```

**Inter-city flights (if applicable):**
```bash
flyai search-flight --origin "{城市A}" --destination "{城市B}" --dep-date "{date}" --sort-type 3
```

**Return flight:**
```bash
flyai search-flight --origin "{最后一个城市}" --destination "{出发城市}" --dep-date "{end_date}" --sort-type 3
```

From each result, extract: `marketingTransportName`, `marketingTransportNo`, `depDateTime`, `arrDateTime`, `depStationName`, `arrStationName`, `adultPrice`, `jumpUrl`.

**If no flight found for a segment:** note it as "Train" or "To be confirmed" — do NOT hallucinate a flight number.

### Step 4: Call flyai — Hotels

For each city in the itinerary, search hotels. **You MUST include dates for overseas cities** — without dates, overseas cities return wrong results from unrelated cities (not empty, but wrong data — more dangerous).

**CRITICAL: Always use Chinese city names for hotel search.** English names cause flyai to fuzzy-match wrong cities (e.g., "Tokyo" → Cape Town, "Nice" → Dubai, "Osaka" → null). This is not a fallback — Chinese is the only reliable option for overseas cities.

```bash
flyai search-hotels --dest-name "{城市中文名}" --check-in-date "{checkin}" --check-out-date "{checkout}" --sort rate_desc
```

From each result, extract: `name`, `address`, `price`, `score`, `detailUrl`.

**Verify the hotel is actually in the target city.** Check the `address` field — if it contains a different country or city, discard that result.

**Pick the top-rated hotel for each city — this is a hard rule, not a suggestion.** Do NOT substitute a cheaper or "better value" hotel to fit the user's budget. Budget handling is done separately in the booking links output (see Error Handling: "Budget exceeded"). Your job here is to pick the highest-rated valid hotel, period. If no valid results, mark "Hotel to be confirmed" in the itinerary.

### Step 5: Call flyai — Attractions

For each city, search top attractions. **You MUST use Chinese city names** — English names return empty results.

**Universal rule: Regardless of user input language, translate ALL city names to Chinese before calling any flyai command (hotels, attractions, flights with non-Chinese city names).** Do not rely on a fixed mapping table — the agent is responsible for accurate translation.

```bash
flyai search-poi --city-name "{城市中文名}"
```

From results, extract: `name`, `address`, `freePoiStatus`, `ticketInfo.price`, `jumpUrl`.

Select 2-4 attractions per city to fill the daily itinerary. Distribute realistically — no more than 3 major attractions per day.

### Step 6: Internal Logic

**Only execute this step for multi-country Schengen trips.** For single-country trips or non-Schengen destinations (e.g., Japan, South Korea, Southeast Asia), skip this step entirely.

**Schengen 90/180 Day Check:**
- Count total days inside Schengen zone
- If > 90 days, add a warning at the top of the document

**Main Application Country:**
- Count days spent in each country
- The country with the most days = main application country
- If tied, the first country visited is the main application country

### Step 7: Generate Output

You MUST produce TWO outputs:

#### Output 1: Travel Plan Table (Markdown → PDF)

Generate a **full English** single-page travel plan table. This is the visa itinerary — keep it clean and simple, no extra sections.

```markdown
# Travel Plan

| Country | Day | Date | City | Touring Spots | Accommodation | Transportation |
|---------|-----|------|------|---------------|---------------|----------------|
| CHINA | 1 | {YYYY/MM/DD} ({Day}) | {origin}→{first_city} | — | {hotel_name} ({full_address}) | Flight {airline} {flight_no}: {origin}→{dest} {dep_time} |
| {COUNTRY} | 2 | {YYYY/MM/DD} ({Day}) | {city} | {Spot 1}, {Spot 2}, {Spot 3} | {hotel_name} | Public transport and walking |
| ... | ... | ... | ... | ... | ... | ... |
| CHINA | {n} | {YYYY/MM/DD} ({Day}) | {last_city}→{origin} | — | — | Flight {airline} {flight_no}: {dep_city}→{origin} {dep_time} |
```

**Critical rules:**
- ALL text in English
- Every day must have specific touring spots — never write "Free day" or "Rest"
- Touring Spots: just list attraction names, no descriptions (e.g. "Duomo di Milano, Galleria V.E. II, The Last Supper")
- Accommodation: first time a hotel appears → full name + address; subsequent nights at same hotel → name only
- Transportation: flight rows → "Flight {airline} {flight_no}: {route} {time}"; train rows → "Train {city_a}→{city_b}"; sightseeing days → "Public transport and walking"
- Keep it concise — the whole table should fit on a single A4 page
- No Declaration, no Financial Summary, no Notes for Visa Officer — just the itinerary table. Real visa itineraries that get approved are plain tables. Adding extra sections deviates from standard consulate submission format.

#### Generate PDF from the table

Save the Markdown table to `travel_plan.md` in the working directory, then render it to PDF:

```bash
python3 <skill_dir>/scripts/render_pdf.py --md travel_plan.md --output My_Travel_Plan.pdf
```

For example, if this skill is installed at `~/.claude/skills/visa-itinerary-gen/`, the command would be:
```bash
python3 ~/.claude/skills/visa-itinerary-gen/scripts/render_pdf.py --md travel_plan.md --output My_Travel_Plan.pdf
```

The script converts Markdown to a styled A4 PDF internally (Times New Roman, black & white, single-page table layout). Deliver both files to the user:
- `travel_plan.md` — editable source, user can modify and re-render
- `My_Travel_Plan.pdf` — print-ready for consulate submission

#### Output 2: Booking Links Data (JSON → HTML)

Write a `data.json` file to the working directory containing all flyai data for booking links. Then run the render script to produce the HTML files.

**JSON schema — every field is required unless marked optional:**

```json
{
  "title": {
    "destination_cn": "意大利 & 法国",
    "destination_en": "Italy & France",
    "dates": "2026-04-27 ~ 2026-05-04"
  },
  "flights": [
    {
      "route_cn": "杭州 → 米兰",
      "route_en": "Hangzhou → Milan",
      "airline_cn": "南航 CZ8790 → 阿提哈德 EY889+EY081",
      "airline_en": "China Southern CZ8790 → Etihad EY889+EY081",
      "price": 4580,
      "url": "https://a.feizhu.com/..."
    }
  ],
  "hotels": [
    {
      "city_cn": "米兰",
      "city_en": "Milan",
      "name_cn": "米兰大教堂广场酒店",
      "name_en": "Hotel Piazza Duomo Milano",
      "price": 1280,
      "star": "高档型",
      "recommendation_cn": "近米兰大教堂",
      "recommendation_en": "Near Duomo di Milano",
      "url": "https://a.feizhu.com/..."
    }
  ],
  "attractions": [
    {
      "city_cn": "米兰",
      "city_en": "Milan",
      "name_cn": "米兰大教堂",
      "name_en": "Duomo di Milano",
      "category_cn": "宗教场所 · 米兰地标",
      "category_en": "Landmark · Milan's iconic cathedral",
      "url": "https://a.feizhu.com/..."
    }
  ]
}
```

**Data filling rules:**

**Flights** — format `airline_cn` and `airline_en` fields:
- `airline_cn` uses `marketingTransportName` as-is from flyai (e.g. "南航", "阿提哈德"). `airline_en` uses the airline's official English name (e.g. "China Southern", "Etihad").
- **Flight numbers are mandatory.** Never omit the flight number or write only the airline name.
- **Direct flight**: `{airline} {flight_no}` — e.g. `海南航空 HU7937`
- **Same-airline connecting flights**: combine flight numbers with `+` — e.g. `阿提哈德 EY156+EY888`
- **Multi-airline connecting flights**: separate airlines with `→` — e.g. `南航 CZ8790 → 阿提哈德 EY889+EY081`
- **No transfer descriptions.** Do not write "经多哈中转", "via Abu Dhabi" etc.
- `price`: per-person price as a number (not string), from flyai result
- `url`: Fliggy `jumpUrl` from flyai. If no link available, set to empty string `""`

**Hotels:**
- **Pick the top-rated hotel for each city — hard rule.** Do NOT substitute a cheaper hotel.
- `name_en`: use the hotel's own English name, not a translation of the Chinese transliteration
- `price`: per-night price from flyai `price` field as a number. Do not calculate total cost or multiply by nights/guests
- `star`: tier label from flyai (e.g. "豪华型", "高档型", "舒适型")
- `recommendation_cn/en`: `interestsPoi` or notable features (e.g. "近圣马可广场" / "Near St. Mark's Square")

**Attractions:**
- `name_en`: use the internationally recognized English name (e.g. "布拉格城堡" → "Prague Castle")
- `category_cn/en`: from flyai `category`. Discard obviously wrong labels (e.g. "山湖田园" for a city observation deck)

**After writing `data.json`, render the HTML files:**

```bash
python3 <skill_dir>/scripts/render_booking.py --data data.json --output-dir .
```

For example, if this skill is installed at `~/.claude/skills/visa-itinerary-gen/`, the command would be:
```bash
python3 ~/.claude/skills/visa-itinerary-gen/scripts/render_booking.py --data data.json --output-dir .
```

The script produces two files:
- `booking_links_cn.html` — Chinese version
- `booking_links_en.html` — English version

#### Budget Check (only when budget is specified)

After generating both outputs, calculate the estimated total: sum all flight prices × number of travelers, plus all hotel prices × number of nights per hotel. If the total exceeds the user's stated budget:

1. Identify the most expensive hotel (highest per-night price)
2. From the Step 4 flyai results for that city, pick the next-best hotel one tier down (e.g., 豪华型 → 高档型 → 舒适型). If the original results have no lower-tier options, re-run `flyai search-hotels` for that city without the `--sort` parameter and pick the top-rated hotel from the lower tier.
3. Recalculate total. Still over budget? Repeat for the next most expensive hotel.
4. Update both Output 1 (travel_plan.md + re-render PDF) and Output 2 (data.json + re-run render_booking.py) with the new hotel selections.
5. If all hotels are already at 舒适型 and total still exceeds budget, keep the current selection and add a note: set a `budget_warning` field in data.json's `title` object (e.g. `"budget_warning": "Estimated total exceeds stated budget"`).

If no budget is specified, skip this check entirely.

### Step 8: Delivery Review — MANDATORY, DO NOT SKIP

Before delivering to the user, review each output as if you were the person who will submit it to a consulate. This step catches data errors that ruin the document's credibility. Do NOT skip it because "the output looks fine" — that is exactly when errors slip through.

The goal is to deliver something that can be used directly — not a draft that needs manual checking.

**Review Output 1 (Travel Plan PDF) — the visa officer will read this:**
- **Language check: scan the entire travel_plan.md for any non-ASCII characters** (Chinese, Japanese, Arabic, etc.). The travel plan must be pure English + numbers + standard punctuation. If any non-ASCII text is found (most commonly: Chinese airline names copied from flyai, Chinese hotel names, or Chinese city names), translate it to the correct English equivalent and re-render the PDF. This is a hard gate — do not proceed to delivery until the table is 100% English.
- Every hotel address is in the correct city (not a different country or region)
- Every flight row has a specific flight number + departure time (not just the airline name)
- Each day's touring spots are only in that day's city (no mixing cities on transfer days)
- Transfer day timing is realistic (early morning flight = no sightseeing that day)
- Every piece of data (flight numbers, hotel names, touring spot names) must trace back to a flyai call. If a touring spot was not returned by flyai, it must be removed — use "Local exploration / neighborhood walk" instead. This skill's promise is zero hallucination from real data.

**Review Output 2 (data.json) — the user will use this to book:**
- Every flight entry has both `airline_cn` and `airline_en` with flight numbers (not just airline name)
- Every flight entry has a non-empty `url` (if flyai returned a `jumpUrl`)
- Every hotel entry has a non-empty `url`
- Every hotel entry has `star` and `recommendation_cn/en` populated
- Every attraction entry has `category_cn/en` populated; discard obviously wrong labels
- All `_en` fields contain correct English translations:
  - Airline names: use IATA official English name (e.g. "南航" → "China Southern Airlines", not "Southern Airlines")
  - Hotel names: use the hotel's own English name, not a translation of the Chinese transliteration
  - Attraction names: use the internationally recognized English name (e.g. "布拉格城堡" → "Prague Castle")
  - If unsure of the correct English name, keep the flyai Chinese name rather than guessing
- **render_booking.py execution:** verify the script ran successfully (exit code 0) and both HTML files exist. If the script failed, fix the data.json issue and re-run.

**When something fails review:**
- Fix it if you can (correct data.json fields and re-run render_booking.py)
- If unfixable (flyai has no data), mark it clearly in the output and tell the user what needs their attention
- Default is: user receives a ready-to-use document, not a TODO list

## Error Handling

| Situation | Action |
|-----------|--------|
| Flight not found | Write "To be confirmed — please check alternative routes" in Destination column |
| Hotel not found | Write "To be confirmed — please book a hotel with free cancellation" in Hotel column |
| Attraction data sparse | Use `fliggy-fast-search --query "{city} tourist attractions"` as fallback |
| Schengen stay > 90 days | Add prominent warning: "⚠ WARNING: Total Schengen stay exceeds 90 days" |
| flyai not installed | Print installation instructions and stop |
| Budget exceeded | Mention in booking links output that estimated total exceeds stated budget |

## Important Notes

- **Never hallucinate data.** Every flight number, hotel name, and address must come from flyai results. If flyai returns no data, mark it as "To be confirmed" — do NOT make up information. Visa officers can and will verify.
- **Always include booking links.** In Output 2, every hotel and flight must have a Fliggy booking link from the flyai response.
- **Keep the travel plan clean.** Output 1 is just a table — no extra sections, no branding. Follow standard consulate submission format.
- **Brand mention.** Only in Output 2 (booking links), include "Based on fly.ai real-time results".
