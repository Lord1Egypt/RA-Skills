# Templates — red-flights

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
Missing dep-date → Default: tonight. Tell user: "默认查今晚红眼航班"
Missing dep-hour-start → Default: 21 (9 PM)
Missing dep-hour-end → Default: 6 (6 AM)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about time range — red eye implies 21:00–06:00

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "red-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "dep_hour_start": "21",
    "dep_hour_end": "6",
    "sort_type": "3"
  },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Red Eye Flights: {origin} → {destination}

**Cheapest red eye: ¥{price} departing at {dep_time}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

💡 **Tip:** Red eye flights save 30-60% vs daytime. Consider airport lounge for late-night comfort.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Red Eye Flights: {origin} → {destination}

No red eye flights found for {date}.

**Tried:**
- ✅ Searched 21:00–06:00 departures → 0 results
- ✅ Expanded to all departure times → {count} daytime flights available

**Suggestions:**
1. Try a different date
2. Consider daytime flights on this route
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Red Eye Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --dep-hour-start 21 --dep-hour-end 6 --sort-type 3`

Real-time data requires a working flyai-cli.
```
