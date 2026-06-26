---
name: reminder-agent
description: >
  Converts any human reminder request into structured JSON reminder data.
  Trigger this skill whenever the user wants to set, create, schedule, or log a reminder —
  in any language (Vietnamese or English). This includes phrases like "nhắc tôi", "đặt lịch",
  "set a reminder", "remind me", "tạo reminder", "lên lịch", or any message describing
  a future task with a time. Also trigger when the user mentions âm lịch / lunar dates
  alongside a reminder request. Always use this skill — do NOT attempt to build reminder
  JSON from scratch without it.
---

# Reminder Agent Skill

Convert human reminder requests into structured JSON. Always follow the steps below in order.

---

## Step 1 — Extract Information

Parse the user's message for:

| Field | Required | Default |
|---|---|---|
| `title` | ✅ Yes | — |
| `datetime` | ✅ Yes | — |
| `recurrence` | ✅ Yes | `"once"` |
| `priority` | ✅ Yes | `"medium"` |
| `note` | ❌ Optional | `null` |

**Vague time-of-day mappings (Vietnamese):**

| Word | Time |
|---|---|
| sáng | 08:00 |
| trưa | 12:00 |
| chiều | 15:00 |
| tối | 20:00 |

- "ngày mai" = tomorrow, "hôm nay" = today — resolve relative to the current date.
- Never assume a specific time if the user gave none (not even a vague word).

---

## Step 2 — Lunar Date Detection

If the user's message contains any of: `âm lịch`, `âm`, `AL`, `tháng âm`, `ngày âm`, `lịch âm` →

→ **Invoke the `lunar-convert` skill immediately.**
→ Use the `iso_date` value it returns as the `datetime` date.
→ **Never self-calculate lunar-to-solar conversion.**

Read `/mnt/skills/user/lunar-convert/SKILL.md` for full usage.

---

## Step 3 — Detect Custom Output Format

Trigger custom format mode when user says any of:

**Vietnamese:** `trả về theo format`, `dữ liệu trả về theo`, `format:`, `với các trường`, `trả về các field`
**English:** `return as`, `response with fields`, `format:`, `output fields`, `return only`

### Custom format rules:
- Extract exactly the field names the user listed.
- Map them to internal values using the table below.
- Output **only** those fields, using **exactly** the user's field names (preserve typos like `tittle`).

**Field name mapping:**

| User's field name | Internal value |
|---|---|
| `tittle`, `title`, `tên`, `tiêu đề` | title |
| `scheduled_at`, `datetime`, `time`, `thời gian`, `ngày giờ` | datetime (ISO 8601 solar) |
| `repeat`, `recurrence`, `lặp lại`, `tần suất` | recurrence |
| `priority`, `ưu tiên`, `độ ưu tiên` | priority |
| `note`, `ghi chú`, `description`, `mô tả` | note |

### No custom format detected:
Use the default schema (see Step 5).

---

## Step 4 — Clarification

Ask **ONE** concise question if any required field is unclear or missing.

- Missing `datetime` → ask for the specific date and/or time.
- Unclear `title` → ask what the reminder is for.
- Clarification priority: **datetime > title > others**
- **Never ask** about `recurrence`, `priority`, or `note` — apply defaults silently.
- Once all required fields are resolved → proceed immediately to Step 5.

---

## Step 5 — Output JSON

Return **ONLY** the raw JSON object. Rules:

- ❌ No explanation, no markdown, no code blocks, no backticks.
- `datetime` is **always** Gregorian ISO 8601 — never output a lunar date.
- Apply custom format if detected (Step 3), otherwise use default schema.

**Default schema:**
```
{
  "title": "string",
  "datetime": "ISO 8601 Gregorian — e.g. 2026-04-02T14:00:00",
  "recurrence": "once | daily | weekly | monthly",
  "priority": "low | medium | high",
  "note": "string or null"
}
```

**Custom format example:**
> Input: "Đặt lịch 9h ngày mai họp team. Dữ liệu trả về theo format tittle, scheduled_at, note"

```
{
  "tittle": "Họp team",
  "scheduled_at": "2026-03-20T09:00:00",
  "note": null
}
```

---

## Quick Decision Tree

```
User sends reminder request
        │
        ▼
Lunar date mentioned?
   YES → invoke lunar-convert skill → get iso_date
   NO  → parse date/time directly
        │
        ▼
Custom format detected?
   YES → extract user's field names → map to internal values
   NO  → use default schema
        │
        ▼
All required fields available?
   NO  → ask ONE clarifying question (datetime > title)
   YES → output raw JSON immediately
```
