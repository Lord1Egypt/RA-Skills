---
name: hash-health
description: Log meals, check nutrition, manage medications, and view daily health dashboard via Hash Health. Use when user mentions food, meals, eating, nutrition, medications, or health tracking.
metadata: {"openclaw":{"emoji":"🥗","requires":{"env":["HASH_HEALTH_USER_ID"]}}}
---

You are connected to Hash Health, a personal nutrition and health tracking platform.

Base API URL: `https://hash-claude-mcp.vercel.app`
The user's email/ID is: `{HASH_HEALTH_USER_ID}`

## Tool: Log a meal

To log food the user mentions eating:

**Step 1 — Analyze food**
POST `https://hash-claude-mcp.vercel.app/api/food-analysis`
```json
{
  "messages": [
    {
      "role": "user",
      "content": "{\"type\":\"analysis_request\",\"step\":\"analyze\",\"food_name\":\"<dish name>\",\"is_edited_food_name\":false,\"language\":\"en\"}"
    }
  ],
  "language": "en"
}
```

**Step 2 — Save to history**
POST `https://hash-claude-mcp.vercel.app/api/unified-history`
```json
{
  "user_id": "{HASH_HEALTH_USER_ID}",
  "type": "analysis",
  "analysis": "<stringified analysis JSON from Step 1>"
}
```
Confirm to user: "✅ [dish name] logged to Hash Health!"

## Tool: Daily nutrition summary

GET `https://hash-claude-mcp.vercel.app/api/daily-nutrition?user_id={HASH_HEALTH_USER_ID}&date=<YYYY-MM-DD>`

Display: calories, protein, carbs, fat, fiber, streak.

## Tool: View today's meals

GET `https://hash-claude-mcp.vercel.app/api/unified-history?user_id={HASH_HEALTH_USER_ID}&date=<today YYYY-MM-DD>&limit=20`

For each entry, parse the `analysis` field (it is a **JSON string** — always JSON.parse it) to get `dishName` and `nutritionalInfo.calories_kcal`.

## Tool: List medications

GET `https://hash-claude-mcp.vercel.app/api/medi-history?user_id={HASH_HEALTH_USER_ID}`

Display name, dosage, frequency, time_of_day, and ID for each medication.

## Tool: Add medication

POST `https://hash-claude-mcp.vercel.app/api/medi-history`
```json
{
  "user_id": "{HASH_HEALTH_USER_ID}",
  "name": "<medication name>",
  "dosage": "<e.g. 500mg>",
  "frequency": "<e.g. twice daily>",
  "time_of_day": ["morning", "evening"],
  "notes": ""
}
```

## Tool: Delete a meal

DELETE `https://hash-claude-mcp.vercel.app/api/unified-history?id=<entry UUID>&user_id={HASH_HEALTH_USER_ID}`

If user gives a meal name instead of ID, first call GET /api/unified-history to find the matching entry UUID.

## Tool: Delete a medication

DELETE `https://hash-claude-mcp.vercel.app/api/medi-history?id=<numeric ID>&user_id={HASH_HEALTH_USER_ID}`

If user gives a medication name instead of ID, first call GET /api/medi-history to find the matching numeric ID.

## Tool: Bedtime summary

Run in parallel:
- GET `/api/medi-history?user_id={HASH_HEALTH_USER_ID}` → filter where `time_of_day` includes "bedtime" or "Bedtime"
- GET `/api/daily-nutrition?user_id={HASH_HEALTH_USER_ID}&date=<today>`

Display bedtime medications and today's nutrition totals.

## Important rules

- The `analysis` field in history entries is always a **JSON string** — parse it before reading `dishName`, `calories_kcal`, etc.
- Always use today's date (YYYY-MM-DD) when no date is specified.
- Never guess a numeric medication ID or UUID — always look it up first.
- For meal logging, always confirm with the user before saving: show dish name and estimated calories first.
