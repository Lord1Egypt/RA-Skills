# Templates — seasonal-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞往哪个城市？" (Priority 2)
Both missing → "请告诉我出发城市和目的地城市？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing season/dates → "哪个季节出行？暑假/寒假/淡季？"
Missing sort-type → Default: 2 (recommended), off-season → 3 (cheapest)
Missing journey-type → Default: none (show all)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest seasonal windows: "暑期推荐7-8月搜索", "淡季推荐3-4月/11月"
- ✅ Warn about peak season pricing: "旺季票价较高，建议尽早预订"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "seasonal-flight",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date_start": "",
    "dep_date_end": "",
    "sort_type": "2"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Seasonal Flights: {origin} → {destination}

**Best seasonal option: {airline} — ¥{price} ({season_label})**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 🏷️ Season | 📎 Book |
|---|--------|---------|---------|----------|----------|-----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {peak/off} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {peak/off} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | {peak/off} | [Book]({detailUrl}) |

📅 **Seasonal Tip:** {seasonal_advice}

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Seasonal Flights: {origin} → {destination}

No flights found for the selected season window.

**Suggestions:**
1. Expand date range by ±7 days
2. Try nearby airports
3. Consider shoulder season dates
```

### 3.3 CLI Failed

```markdown
## ✈️ Seasonal Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 2`

Real-time data requires a working flyai-cli.
```
