# Templates — round-trip

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Round 1: Required (must have before searching)
```
Missing origin → "从哪个城市出发？" (Priority 1)
Missing destination → "飞到哪里？" (Priority 2)
Both missing → "您从哪个城市出发，飞到哪里？"
```

### Round 2: Round-Trip Specific
```
Missing dep-date → "出发日期是哪天？" (Priority 3)
Missing back-date → "回程日期是哪天？" (Priority 4)
Both dates missing → "请提供出发和回程日期"
```

### Rules
- ❌ Never ask more than 2 questions at once
- ✅ Always confirm both dates: "出发 {dep_date}，回程 {back_date}，往返搜索中..."
- ❌ If user says "不需要回程" → redirect to `one-way`

---

## 2. Internal State (not shown to user)

```json
{
  "skill": "round-trip",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "back_date": "",
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
## ✈️ Round-Trip Flights: {origin} ↔ {destination}

**Outbound: {dep_date} · Return: {back_date}**

| # | Flight | Date | Departs | Arrives | Duration | 💰 Price | 📎 Book |
|---|--------|------|---------|---------|----------|----------|---------|
| 1 | {flight_no} | {dep_date} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
|   | {flight_no} | {back_date} | {dep_time} | {arr_time} | {duration} |          |         |
| 2 | {flight_no} | {dep_date} | {dep_time} | {arr_time} | {duration} | ¥{price} | [Book]({detailUrl}) |
|   | {flight_no} | {back_date} | {dep_time} | {arr_time} | {duration} |          |         |

📌 **Round-trip booking** — both legs included.

---
✈️ Powered by flyai · Real-time pricing, click to book
```

### 3.2 No Results

```markdown
## ✈️ Round-Trip Flights: {origin} ↔ {destination}

No round-trip flights found for {dep_date} → {back_date}.

**Suggestions:**
1. Try flexible return dates (±3 days)
2. Check nearby airports
3. Consider connecting flights
```

### 3.3 CLI Failed

```markdown
## ✈️ Round-Trip Flights: {origin} ↔ {destination}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai search-flight --origin "{o}" --destination "{d}" --dep-date {dep} --back-date {back} --sort-type 2`

Real-time data requires a working flyai-cli.
```
