# Templates — senior-flights

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞到哪里？" (Priority 2)
Both missing → "您从哪个城市出发，飞到哪里？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Default: next week. Tell user: "默认查下周的航班"
Missing dep-hour → Default: 6-18 (morning to evening, avoid late night)
Missing journey-type → Default: direct preferred for seniors
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Mention comfort tip: "建议选择白天航班，避免夜间出行"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "senior-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "dep_hour_start": "6",
    "dep_hour_end": "18",
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
## ✈️ Senior-Friendly Flights: {origin} → {destination}

**Recommended: ¥{price} on {airline} — {duration}, departs {dep_time}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | Type | 📎 Book |
|---|--------|---------|---------|----------|----------|------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | Direct | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | Direct | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | 1-stop | [Book]({detailUrl}) |

🧓 **Senior Tip:** Request priority boarding and aisle seats at check-in. Wheelchair assistance available on request.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Senior-Friendly Flights: {origin} → {destination}

No flights found for {date} (6:00-18:00).

**Tried:**
- ✅ Searched 6-18h window → 0 results
- ✅ Expanded to full day → {count} flights available

**Suggestions:**
1. Expand time window beyond 18:00
2. Try connecting flights
3. Check nearby dates
```

### 3.3 CLI Failed

```markdown
## ✈️ Senior-Friendly Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --dep-hour-start 6 --dep-hour-end 18 --sort-type 2`

Real-time data requires a working flyai-cli.
```
