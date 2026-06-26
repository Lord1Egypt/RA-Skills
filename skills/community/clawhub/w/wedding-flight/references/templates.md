# Templates — wedding-flight

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "蜜月/婚礼想去哪里？" (Priority 2)
Both missing → "请告诉我出发城市和蜜月/婚礼目的地？"
```

### Round 2: Enhanced (use defaults if not stated)
```
Missing dep-date → Default: flexible (use date range)
Missing sort-type → Default: 2 (recommended)
Missing journey-type → Default: 1 (direct, honeymoon preference)
Missing seat-class-name → Default: economy (suggest business for honeymoon)
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Suggest popular honeymoon destinations: "热门蜜月：马尔代夫、巴厘岛、三亚、冲绳"
- ✅ Note: "婚庆旺季机票紧俏，建议提前预订"

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "wedding-flight",
  "params": { "origin": "", "destination": "", "dep_date": "", "sort_type": "2", "journey_type": "1" },
  "state": "collecting | executing | formatting | validating",
  "retry_count": 0
}
```

---

## 3. Output Templates

### 3.1 Standard Result

```markdown
## ✈️ Wedding/Honeymoon Flights: {origin} → {destination}

**Best: {airline} — ¥{price}**

| # | Flight | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 2 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
| 3 | {flight_no} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |

💍 **Wedding Tip:** 热门蜜月目的地，婚庆旺季建议提前预订！

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Wedding/Honeymoon Flights: {origin} → {destination}

No flights found for selected dates.

**Suggestions:**
1. Try flexible dates across wedding season
2. Consider connecting flights
3. Check nearby airports
```

### 3.3 CLI Failed

```markdown
## ✈️ Wedding/Honeymoon Flights: {origin} → {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2`
```
