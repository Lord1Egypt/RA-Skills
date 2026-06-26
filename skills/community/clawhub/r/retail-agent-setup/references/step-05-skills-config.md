# Step 05 — Skills Configuration

## Goal
Activate and configure the specific skill modules the agent will use.
Each skill has toggle (on/off), parameters, and a data source binding.

---

## Skills Registry

### Core Skills (always enabled, no configuration needed)

| Skill | What It Does |
|-------|-------------|
| `retail-knowledge` | Answers product, policy, and store questions from the knowledge base |
| `policy-handler` | Looks up return, exchange, warranty, and promotion rules |

---

### Role-Recommended Skills

#### 🔍 `product-recommender`
**What it does:** Suggests products based on customer needs, budget, recipient, occasion
**Requires:** Product catalog in knowledge base (Step 03)
**Parameters:**
```json
{
  "max_recommendations": 3,
  "show_price": true,
  "show_variants": true,
  "upsell_enabled": true,
  "upsell_threshold_pct": 20
}
```
**Default on for:** Shopping Guide, All-in-One

---

#### 📦 `inventory-query`
**What it does:** Checks real-time or near-real-time stock levels
**Requires:** Live API connection (preferred) or daily-synced data
**Parameters:**
```json
{
  "data_source": "api | daily_sync | static",
  "api_endpoint": "https://...",
  "api_key": "env:INVENTORY_API_KEY",
  "cache_ttl_minutes": 30,
  "low_stock_threshold": 3,
  "show_stockroom_qty": true
}
```
**Default on for:** Stock Manager, All-in-One
**If no API:** Use `data_source: "static"` with manual import from Step 03

---

#### 🏷️ `promotion-engine`
**What it does:** Calculates final price after discounts, bundles, thresholds
**Requires:** Promotion entries in knowledge base (Step 03)
**Parameters:**
```json
{
  "allow_stacking": false,
  "show_calculation_steps": true,
  "currency": "CNY",
  "round_to": 2
}
```
**Default on for:** Shopping Guide, All-in-One

---

#### 🎧 `complaint-handler`
**What it does:** Classifies complaints, generates empathetic responses, routes escalations
**Requires:** Policy entries + escalation config (Step 09)
**Parameters:**
```json
{
  "sentiment_analysis": true,
  "auto_escalate_keywords": ["投诉", "曝光", "律师", "消协", "骗子"],
  "refund_auto_approve_limit": 0,
  "response_style": "empathetic"
}
```
**Default on for:** Customer Service Rep, All-in-One

---

#### 📊 `report-generator`
**What it does:** Generates daily, weekly, and monthly sales/performance reports
**Requires:** POS or ERP API connection; or daily data export
**Parameters:**
```json
{
  "report_schedule": "daily_18:00",
  "metrics": ["revenue", "transactions", "top_products", "returns"],
  "comparison": "wow",
  "delivery_channel": "wecom",
  "recipients": ["manager_wecom_id"]
}
```
**Default on for:** Store Manager Assistant, All-in-One

---

#### 📅 `shift-scheduler`
**What it does:** Answers shift queries, sends reminders, handles swap requests
**Requires:** Staff list + schedule data (Step 02)
**Parameters:**
```json
{
  "schedule_source": "manual | google_sheets | api",
  "schedule_url": "...",
  "remind_before_hours": 12,
  "allow_swap_requests": true
}
```
**Default on for:** Store Manager Assistant (optional)

---

#### 🎓 `training-quiz`
**What it does:** Runs interactive product knowledge quizzes for staff
**Requires:** Product catalog + FAQs in knowledge base
**Parameters:**
```json
{
  "quiz_mode": "flashcard | multiple_choice | scenario",
  "questions_per_session": 10,
  "pass_score": 80,
  "track_completion": true
}
```
**Default on for:** Training Officer, All-in-One (optional)

---

## Configuration Flow

1. Show recommended skills based on role (pre-checked)
2. Let user toggle on/off
3. For each enabled skill, show parameters with defaults pre-filled
4. Ask only for values that can't be inferred: API keys, manager contacts, etc.
5. Validate each skill's data source binding before saving

---

## Output Format

```json
{
  "active_skills": [
    {
      "skill_id": "product-recommender",
      "enabled": true,
      "config": { "max_recommendations": 3, "upsell_enabled": true }
    },
    {
      "skill_id": "inventory-query",
      "enabled": true,
      "config": { "data_source": "daily_sync", "cache_ttl_minutes": 60 }
    },
    {
      "skill_id": "complaint-handler",
      "enabled": false
    }
  ]
}
```

Save as `skills_config` in agent memory. Proceed to Step 06.

---

## Skill Dependencies Warning

Before saving, check for broken dependencies:

| If this skill is enabled | And this is missing | Warn |
|--------------------------|--------------------|----|
| `inventory-query` | No data source configured | ⚠️ "Inventory queries will return 'unknown' until a data source is connected." |
| `report-generator` | No POS/ERP API | ⚠️ "Reports will be empty until sales data is connected." |
| `promotion-engine` | No promotions in knowledge base | ⚠️ "Add current promotions in Step 03 for this skill to work." |
| `complaint-handler` | No escalation contacts | ⚠️ "Set escalation contacts in Step 09 to complete complaint routing." |
