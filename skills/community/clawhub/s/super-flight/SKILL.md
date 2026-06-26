---
name: super-flight
description: Multi-date flight price comparison assistant. Supports one-way multi-date (≤7 days) comparison via a two-stage flow — discover candidate flights, then lock 1–2 flights and run a date×price matrix. Binds hard constraints to personas (亲子/商务/学生/老人/蜜月 — family/business/student/senior/honeymoon), defaults sort order from historical orders, and provides explainable recommendations. Triggers on: 机票查询/多日期比价/拼假/周末比价/最便宜几天/同航班不同日价格/家庭出行机票/商务票比价/蜜月机票, flight search, multi-date price comparison, cheapest days, same flight across dates, family/business/honeymoon flight planning.
compatibility: Requires flyai-cli to be installed (npm i -g @fly-ai/flyai-cli)
license: MIT
---

# ✈️ Multi-Date Flight Price Comparison Assistant

Built on `flyai search-flight`, this skill is designed around the "one-way multi-date price comparison" scenario via a two-stage flow: **Discover** → **Lock & Compare**. It does not blindly recommend the lowest price — it filters by persona hard constraints, then ranks with reference to historical orders and explains every recommendation.

## Triggers

Activate when the user talks about comparing flight prices, contrasting the same route across different dates, stitching together long weekends, asking "which days are cheap", "Fridays this month", "around Qingming", the price of a specific flight across multiple days, or planning a trip with children / for business / with seniors / for a honeymoon / as a student.

### Quick Examples

- **"比一比这个月周五北京去上海，哪天最便宜" / "Compare Beijing→Shanghai on Fridays this month, which is cheapest"** → Stage 1 + Stage 2
- **"4/26 北京到上海，推荐几趟" / "Recommend some flights Beijing→Shanghai on 4/26"** → Stage 1
- **"CA1883 这周还有哪天便宜" / "Which days are cheap for CA1883 this week"** → Stage 2 (skip Stage 1)
- **"带娃下周去三亚，哪天合适" / "Traveling with kids to Sanya next week, which day works"** → Persona=亲子 (family) + Stage 1
- **"商务，4/22 早上到上海" / "Business trip, arrive Shanghai morning 4/22"** → Persona=商务 (business) + Stage 1 + time-window filter

## Prerequisites

- `flyai-cli`: `npm i -g @fly-ai/flyai-cli`
- Verify: `flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-26` returns JSON

Optional for better results:
```bash
flyai config set FLYAI_API_KEY "your-key"
```
Get the key at https://flyai.open.fliggy.com/. If a CLI method is missing, upgrade with: `npm i -g @fly-ai/flyai-cli`.

## Data Files

```
super-flight/
├── SKILL.md                      ← this file
├── references/
│   └── search-flight.md          ← flyai search-flight params & response schema
└── assets/
    ├── personas.json             ← hard constraints for 5 personas (read-only)
    ├── preferences.json          ← long-term user preferences (location/companions/airlines/sort)
    └── history.json              ← selection history (append-only)
```

This skill **only** reads/writes `assets/preferences.json` and `assets/history.json`. Do not touch any other paths.

## Input Safety Validation (pre-execution checks)

All user inputs must pass the following validation before being spliced into a `flyai search-flight` command, to prevent shell injection:

| Parameter | Allowed character set | Max length |
|-----------|----------------------|------------|
| City name (origin/destination/transfer-city) | Chinese characters, letters, digits, spaces | 20 |
| Dates (dep-date/back-date and start/end variants) | digits + `-`, must match `YYYY-MM-DD` | 10 |
| Hours (dep-hour-start/end, arr-hour-start/end) | integer 0–23 | 2 |
| Flight number (transport-no) | uppercase letters + digits, comma-separated | 200 |
| Cabin class (seat-class-name) | Chinese characters, letters, commas | 30 |
| journey-type | only `1` or `2` | 1 |
| sort-type | only `1–8` | 1 |
| max-price / total-duration-hour | positive integer | 6 |

**Rejection policy**: if any of the following characters appear → reject immediately, ask the user to re-enter, and **do not execute any command**:
`` ` `` `$` `(` `)` `{` `}` `;` `&` `|` `\` `<` `>` `!` `'` `"` newline.

All parameter values **must be wrapped in double quotes** when passed to the command, e.g. `--origin "北京"`.

## Global Workflow

```
User input
  ↓
1. Detect persona (optional) → load hard constraints
  ↓
2. Decide the stage:
   - "recommend a few flights" only → Stage 1
   - "which days are cheap" / "compare multiple dates" → Stage 1 + Stage 2
   - user gave a specific flight number → jump to Stage 2
  ↓
3. Run Stage 1 (Discover) or Stage 2 (Lock & Compare)
  ↓
4. Append to history.json
```

### Persona Detection

Personas are keyed in `personas.json` by their **Chinese canonical key** (亲子, 商务, 学生, 老人, 蜜月). Each entry also carries an `aliases` array of English aliases. Both Chinese and English trigger words are supported — match either and resolve to the same canonical key.

| User trigger words (CN + EN) | Canonical key | Alias |
|------------------------------|---------------|-------|
| 带娃, 带孩子, 带宝宝, 亲子, 儿童票 / with kids, kids, children, family, parent-child, child ticket | `亲子` | `family` |
| 出差, 商务, 开会, 短差 / business, business trip, work trip, meeting | `商务` | `business` |
| 学生, 预算, 便宜, 穷游 / student, budget, cheap, backpacking | `学生` | `student` |
| 带爸妈, 带爷爷, 带老人, 老人家 / with parents, with grandparents, senior, seniors, elderly | `老人` | `senior` |
| 蜜月, 婚假, 度假, 渡假 / honeymoon, wedding leave, vacation, holiday | `蜜月` | `honeymoon` |

**Lookup rule**: when matching a user phrase, check both the canonical Chinese key and every value in `aliases` (case-insensitive, whitespace/hyphen-tolerant). Always store and reference the **canonical Chinese key** internally (e.g. in `history.json`'s `persona_tag`, `preferences.per_persona_overrides`). Display can use either form or both (e.g. `【亲子 / family】`).

- When matched, load the corresponding hard constraints from `personas.json` and call them out in the first output, e.g. "Applied 【亲子 / family】 defaults: no red-eye + transfer ≥ 60min."
- No match → **do not force a persona**; proceed with the generic flow (no hard constraints).
- If the user volunteers "this trip is our honeymoon" or "we're on our honeymoon", accept it directly and resolve to `蜜月`.

## Stage 1: Discover

### 1.1 Input Collection

Required core parameters:

| Parameter | Meaning | What to do when missing |
|-----------|---------|-------------------------|
| Origin | `--origin` | If `preferences.home_city` has a value, first ask "Depart from {home_city} by default?"; otherwise ask directly |
| Destination | `--destination` | Ask directly |
| Departure date | `--dep-date` | Parse natural language ("tomorrow", "next Friday", "4/26"), convert to YYYY-MM-DD; if unparseable, ask |

**Batch the question**: ask for everything missing in a single turn; avoid multi-round pinging.

### 1.2 Hard-Constraint Pre-Filter + Explicit Label

Map persona hard constraints to CLI parameters:

| Hard constraint | Maps to |
|-----------------|---------|
| `journey_type: 1` | `--journey-type 1` |
| `reject_redeye_departure: true` | `--dep-hour-start 6 --dep-hour-end 23` |
| `reject_overnight_arrival: true` | `--arr-hour-start 6 --arr-hour-end 23` |
| `min_transfer_minutes: 60` | filter out results with transfer wait < 60min in post-processing (the API does not support this directly) |

The output header **must** make the filter explicit, e.g.:

> Applied 【老人 / senior】 filter: direct only + daytime departure (6:00–23:00) + daytime arrival.
> Reply "不过滤 / no filter" to see all results.

### 1.3 Default Sort (derived from historical orders)

Before querying, read `history.json`:
1. Filter records with the same `origin→destination` route (most recent 20).
2. If there are matching records:
   - Compute the distribution of `sort_used` across them → pick the most frequent as this turn's default.
   - Example prompt: "Last time for 北京→上海 you sorted by 【price ascending】; keep it? (yes / switch to recommended / switch to direct-first)"
3. If there are no matching records: default to `--sort-type 2` (platform recommended) and note in the recommendation reason: "First query on this route, using platform recommended sort."

### 1.4 Call search-flight

```bash
flyai search-flight \
  --origin "{origin}" \
  --destination "{destination}" \
  --dep-date "{YYYY-MM-DD}" \
  [--journey-type 1] \
  [--dep-hour-start N --dep-hour-end N] \
  [--arr-hour-start N --arr-hour-end N] \
  [--seat-class-name "经济舱"] \
  [--max-price N] \
  --sort-type {N}
```

### 1.5 Output Top 3–5

Take the first 3–5 rows of `itemList` (after secondary filtering by hard constraints):

```markdown
### ✈️ 4/26 (Sun) 北京→上海 · Top 3 picks
> Applied 【亲子 / family】 filter: no red-eye (dep 23:00–06:00) | Sort: price ascending (carried over from last time)

| # | Flight | Dep → Arr | Duration | Cabin | Price | Reason |
|---|--------|-----------|----------|-------|-------|--------|
| A ⭐ | CA1883 (Air China) | 21:00→23:20 | 2h20m | Economy | from ¥580 | Lowest price + you picked this last time |
| B   | MU5137 (China Eastern) | 08:00→10:15 | 2h15m | Economy | from ¥620 | Morning daytime flight, good with kids |
| C   | CZ3104 (China Southern) | 15:30→17:50 | 2h20m | Economy | from ¥650 | Afternoon departure, no early wake-up |

[Book A]({jumpUrl_A}) [Book B]({jumpUrl_B}) [Book C]({jumpUrl_C})
```

**Always end with**: "Want to pick 1–2 flights and compare their prices across other dates? (enter multi-date comparison)"

### 1.6 International Long-Haul Fallback: Direct → Connecting

If the first search (direct, `--journey-type 1`) returns **too few qualifying results** on a **long-haul international route**, automatically retry with a connecting search and filter out unsuitable transfers. This is a fallback, not a default — most domestic routes should stay direct-only.

**Trigger conditions (all must hold)**:
1. Qualifying results (after persona hard-constraint filtering) **< 3**.
2. Route is **international**: origin country ≠ destination country. Heuristic — if either city resolves to a non-mainland-China airport code (common cues: `HKG`, `TPE`, `NRT`/`HND`, `ICN`, `BKK`, `SIN`, `KUL`, `CDG`, `LHR`, `FRA`, `JFK`/`LAX`, `SYD`, `DXB`, …) or the `depCityCode`/`arrCityCode` returned by the first call straddles mainland China and anywhere else.
3. Route is **long-haul**: any of
   - straight-line distance roughly ≥ 3,000 km (e.g. Asia↔Europe/North America/Oceania/Middle East/Africa),
   - or the direct `totalDuration` returned by the first call is ≥ 6h,
   - or no direct results at all on a cross-region pair (e.g. 上海→伦敦, 北京→纽约, 广州→巴黎).

   Short intra-Asia hops (北京→首尔, 上海→东京, 香港→曼谷) do **not** qualify — keep them direct-only unless the user explicitly asks for transfers.

**Retry call**:

```bash
flyai search-flight \
  --origin "{origin}" \
  --destination "{destination}" \
  --dep-date "{YYYY-MM-DD}" \
  --journey-type 2 \
  [--seat-class-name ...] \
  [--max-price ...] \
  --sort-type {N}
```

Do **not** pre-set `--transfer-city` — let the API surface options, then filter in post-processing.

**Transfer filter rules (post-process `itemList`)**:

| Rule | Threshold | Reason |
|------|-----------|--------|
| Max segments | ≤ 2 (one transfer only) | Two transfers on long-haul = fatigue + missed-connection risk |
| Transfer wait time | 90 min ≤ wait ≤ 6 h | <90 min too tight for international customs/immigration; >6 h wastes the day |
| Total duration penalty | reject if total > 1.6 × direct `totalDuration` (or > 2 × if no direct baseline) | Avoid absurd detours |
| Overnight transfer | reject if transfer window fully covers 00:00–05:00 at the transfer city | Sleeping in airport hurts, especially for 老人/亲子 |
| Persona-specific | 老人 (senior) / 亲子 (family): min transfer ≥ 120 min + no overnight transfer + same terminal preferred when data available | Slower pace, kids/elderly need buffer |
| Visa risk (advisory, not filter) | flag `transfer-city` in US / UK / Canada / Australia as "may require transit visa" | Inform user; don't silently drop |

**Output format (distinguish direct vs. transfer)**:

```markdown
### ✈️ 6/12 (Fri) 上海→伦敦 · Top picks
> Direct flights matching 【商务 / business】 filter: only 1 → expanded to connecting (long-haul international).
> Transfer filter: ≤1 stop | wait 90min–6h | no overnight | total ≤ 1.6× direct duration.

**Direct (1)**
| # | Flight | Dep → Arr | Duration | Cabin | Price |
|---|--------|-----------|----------|-------|-------|
| A ⭐ | CA855 (Air China) | 13:30→18:55 | 12h25m | Economy | from ¥4,800 |

**Connecting (2, filtered from 14)**
| # | Route | Dep → Arr | Total | Transfer | Cabin | Price |
|---|-------|-----------|-------|----------|-------|-------|
| B | CX367→CX251 (Cathay, via HKG) | 08:40→翌日 06:55 | 16h15m | HKG 2h10m | Economy | from ¥3,650 |
| C | EK303→EK001 (Emirates, via DXB) | 23:55→翌日 07:30 | 14h35m | DXB 2h50m | Economy | from ¥3,980 |

🚫 Filtered out: 5 × overnight transfers, 4 × wait >6h, 3 × two-stop itineraries.
```

**Degradation**:
- If connecting search also returns 0 after filtering → show the unfiltered top 3 with a warning banner ("No itinerary fully satisfies the transfer rules; showing the closest matches — please check the transfer carefully").
- If the retry call itself fails → keep the direct-only result and tell the user "Connecting search unavailable, showing direct results only".

**Do not retry with connecting** when: user explicitly said "直飞 / direct only", or persona hard constraint has `journey_type: 1` marked `strict: true` in `personas.json` (honor it).

## Stage 2: Lock & Compare

### 2.1 Inputs

- **Candidate flights**: 1–2 flight numbers (chosen from Stage 1 picks, or supplied directly).
- **Date set**: in the user's own words.

### 2.2 Date Parsing & Confirmation (critical)

User's natural language → candidate date list → **ask the user to confirm selection** (never silently merge):

| User says | Parsed as |
|-----------|-----------|
| "Fridays this month" | all remaining Fridays in the current month |
| "around Qingming" | holiday date ± 2 days + adjacent weekend |
| "4/22, 4/25, 4/26" | the three listed dates |
| "next weekend" | next Saturday and Sunday |
| "May Day holiday" | 5/1–5/5 |

**Display format**:
```markdown
I parsed the following candidate dates (N total) — please confirm:
- [ ] 4/22 (Tue)
- [ ] 4/29 (Tue)
- [ ] 5/6  (Tue)
- [ ] 5/13 (Tue)
(Last time on this route you picked 4/22 and 5/6 — carry over?)

**At most 7 dates are kept.** Reply with the dates to keep, or say "全选 / all".
```

**Historical reference**: which dates the user picked last time on the same route, used as the default suggested tick.

### 2.3 Call Strategy: One Call Per Day, In Parallel

- At most 7 days × 2 flights = 14 parallel calls.
- Per call:
  ```bash
  flyai search-flight \
    --origin "{origin}" \
    --destination "{destination}" \
    --dep-date "{YYYY-MM-DD}" \
    --transport-no "{flight_no}" \
    [pass through persona hard constraints]
  ```
- A single failure or sold-out day → mark as "—", do not abort the whole flow.
- From each response's `itemList`, take the `adultPrice` for the matching flight number (if multiple rows, take the lowest).

### 2.4 Output: Flight × Date Matrix + Recommendation

```markdown
### 📊 Multi-Date Price Matrix
> Applied 【亲子 / family】 filter: no red-eye | Flights: CA1883, MU5137 | Dates: 4/22, 4/29, 5/6, 5/13

| Flight | 4/22(Tue) | 4/29(Tue) | 5/6(Tue) | 5/13(Tue) | Flight's lowest |
|--------|-----------|-----------|----------|-----------|-----------------|
| CA1883 (Air China 21:00→23:20) | ¥580 | ¥620 | ¥550🔽 | ¥600 | 5/6 |
| MU5137 (China Eastern 08:00→10:15) | ¥640 | ¥680 | ¥620 | ¥540🔽 | 5/13 |

🔽 = lowest cross-date price for that flight
🔥 Global lowest: MU5137 @ 5/13 ¥540

### Recommended Combinations

**Top pick ⭐ MU5137 @ 5/13 (¥540)**
> Global lowest; daytime morning flight, friendly with kids; ¥72 below this matrix's average.
[Book]({jumpUrl})

**Alt 1: CA1883 @ 5/6 (¥550)**
> Second-lowest; late departure means a full day of activities before flying.
[Book]({jumpUrl})

**Alt 2: CA1883 @ 4/22 (¥580)**
> Closest date; matches your historical preference for late-night direct flights.
[Book]({jumpUrl})
```

Each recommendation reason **must** cite at least one of: cross-date lowest, historical preference, persona match, time-window advantage.

### 2.5 Overriding Hard Constraints

If the user says things like "red-eye is OK" or "transfers are fine":

```
Override detected: persona 【亲子 / family】 defaults to no red-eye, but this turn you said "red-eye is OK".
Allowing it for this query. For future queries:
  🔄 One-time exception (recommended)
  🔁 Always accept → modify persona override, write to preferences.per_persona_overrides
```

Do not interrupt the current query flow — ask after delivering the recommendations.

## History Recording

After the user settles on an option (confirms booking / abandons / only shortlists), append to `assets/history.json`:

```json
{
  "ts": "2026-04-20T14:30:00+08:00",
  "persona_tag": "亲子",
  "origin": "北京",
  "origin_airport": "PEK",
  "destination": "上海",
  "destination_airport": "SHA",
  "dep_date": "2026-05-06",
  "transport_no": "CA1883",
  "marketing_carrier": "国航",
  "seat_class_name": "经济舱",
  "dep_time": "21:00",
  "arr_time": "23:20",
  "journey_type": 1,
  "price": 550,
  "result": "purchased",
  "sort_used": "price_asc",
  "overrode_constraints": [],
  "note": null
}
```

**Rules**:
- `result` is required; values: `purchased` / `abandoned` / `shortlisted` (abandonments matter as much as purchases — they serve as negative signal).
- Keep all historical records; append only, never overwrite.
- Validate JSON before writing; if the existing file's `records` array is corrupt → back up, rebuild as empty array, and notify the user.

## Output Conventions

- **Data must come from the `flyai search-flight` response**: price, time windows, flight numbers, duration, etc. — never computed or fabricated.
- **Filter notice must come first**: the first line of output always includes an "Applied 【X】 filter: Y" summary.
- **Recommendation reasons must be traceable**: each reason must be grounded in data (price, history, persona, time-window); never invented.
- **Prices are labeled "from"**: e.g. `from ¥580`, indicating the lowest-cabin price, subject to actual purchase.
- **When the response contains `jumpUrl`**: every recommendation must provide `[Book]({jumpUrl})`.
- **Empty / thin result handling**: if qualifying results <3 on a long-haul international route, auto-fallback to connecting search per §1.6 and report the expansion in the header. Otherwise (domestic / short-haul, or fallback still empty) prompt: "No flights after 【X】 filter, relax? 🔓 clear filter / 🔁 change dates / ✈️ include transfers".
- **Branding**: append "Data from fly.ai" at the end of every output.

## Interaction Examples

### Example 1: family persona, full two-stage flow

```
User: 带娃，这个月周五北京到上海，看看哪天便宜

Reply:
Detected 【亲子 / family】 trip; loaded defaults: no red-eye + transfer ≥ 60min.
Remaining Fridays this month: 4/24, 5/1 (holiday), 5/8, 5/15. Note 5/1 is the first day of Labor Day holiday and prices tend to be higher.
Last time on this route you picked 4/24 and 5/8 — carry over?

> User: all of them

Great, 4 dates. Pick a flight first? Querying Stage 1 on 4/24:

[Stage 1: top 3–5 output]

> User: CA1883 and MU5137

[Stage 2: 4×2=8 parallel calls, output matrix]
```

### Example 2: directly locking a specific flight

```
User: CA1883 这周还有哪天便宜

Reply:
Detected a specified flight CA1883; skipping the discovery stage.
"This week" = 4/21 (Mon) – 4/27 (Sun), 7 days in total. Query all of them?

> User: weekdays only

OK, querying CA1883 for 4/21–4/25.

[Stage 2: 5 parallel calls, output single-flight price series]
```

### Example 3: overriding a hard constraint

```
User: 带娃，但红眼也行，越便宜越好

Reply:
Override detected: 【亲子 / family】 defaults to no red-eye; allowing this turn per your request. I'll ask after the query whether to make it permanent.

[Run query, including red-eye flights]

You allowed red-eye just now. Going forward:
  🔄 Just this once (next time still reject)
  🔁 Always accept (write to preferences.per_persona_overrides.亲子.allow_redeye)
```

## Troubleshooting

- `flyai search-flight` method not found → upgrade: `npm i -g @fly-ai/flyai-cli`.
- Response with `status != 0` → show the `message` field to the user and suggest retrying or adjusting keywords.
- Single-day call fails → mark the corresponding matrix cell as "—" and continue overall.
- If `--transport-no` with two flight numbers causes the API to error → automatically fall back to "per-flight, per-day" serial calls.

## Detailed Reference

- [flyai search-flight parameters & response schema](references/search-flight.md)
