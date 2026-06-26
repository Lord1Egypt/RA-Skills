---
name: shift-scheduler
description: >
  Staff shift scheduling and management assistant for retail store managers and employees.
  Answers shift queries, sends reminders, handles swap requests, and manages on-call routing.
  Use when someone asks: 我今天几点上班, 班表, 排班, 换班, 请假, 谁在值班,
  what's my shift, who's working today, shift swap, schedule, 今天谁当班,
  cover my shift, time off request, 我想换班, 排班表查询.
metadata:
  openclaw:
    emoji: 📅
---

# Shift Scheduler

## Overview

This skill manages staff scheduling queries and shift-related requests.
It reads schedule data from the configured source and routes requests
to the appropriate manager for approval.

**Depends on:** Staff list + schedule data from Step 02 / Step 05 config.
**Configured in:** `skills_config.shift-scheduler`

---

## Data Source Options

| Source | Config Value | Setup |
|--------|-------------|-------|
| Google Sheets | `"google_sheets"` | Share link in config |
| Excel/CSV file | `"file"` | Path to schedule file |
| WeCom Calendar | `"wecom_calendar"` | WeCom API integration |
| Manual input | `"manual"` | Manager pastes schedule text |

**Reference:** [schedule-formats.md](references/schedule-formats.md)

---

## Query Types & Responses

### "我今天几点上班？"
1. Identify the asker (match to staff list by WeCom ID or name)
2. Look up today's shift in schedule data
3. Return: shift start/end time + location (if multi-floor/location)

```
张三，你今天的班是：
  📍 收银台  10:00 – 19:00（含1小时午休）
  搭班同事：李四、王五
```

### "今天谁在当班？" (Manager query)
```
今日在班人员（[date]）：
  早班 (09:00-17:00)：张三、李四
  晚班 (14:00-22:00)：王五、赵六
  值班店长：王经理
```

### "我想换班" (Swap request)
1. Confirm: who wants to swap, which shift, with whom (or open request)
2. Check if target staff is available (not already scheduled)
3. Submit to manager for approval (L1)
4. Notify both parties of outcome

### "我想请假" (Time-off request)
1. Confirm dates and reason (optional)
2. Submit to manager (L2 — always needs approval)
3. Check if replacement coverage is available; flag if not
4. Track request status; notify when approved/denied

### Proactive Shift Reminders
Send 12 hours before shift starts (configurable via `remind_before_hours`):
```
⏰ 上班提醒

张三，明天 [date] 你的班是：
  10:00 – 19:00（[location]）
  记得准时到岗～
```

---

## Swap Request Flow

```
员工申请换班
    ↓
检查被换员工排班（有无冲突）
    ↓
发送 L1 确认给店长
    ↓
店长确认 → 更新排班表 → 通知双方
店长拒绝 → 通知申请人 + 给出原因
    ↓
记录换班历史（避免频繁换班模式）
```

---

## On-Call Routing Integration

The shift schedule drives escalation routing in `complaint-handler` and `inventory-query`.

When an escalation fires:
1. Check current time against shift schedule
2. Route to whoever is listed as on-duty manager for this time slot
3. If no on-duty manager found: fall back to `off_hours_contact` in `permissions_config`

This ensures L2/L3 alerts always go to the right person, not just a fixed manager ID.

---

## Schedule Update

When manager pastes or uploads a new schedule:
1. Parse it using `scripts/parse_schedule.py`
2. Validate: no double-booking, all shifts covered, no gaps > 2 hours during open hours
3. Confirm with manager before activating
4. Archive previous schedule

**Script:** `scripts/parse_schedule.py` — parses Excel/text schedule into structured JSON.
**Reference:** [schedule-formats.md](references/schedule-formats.md)
