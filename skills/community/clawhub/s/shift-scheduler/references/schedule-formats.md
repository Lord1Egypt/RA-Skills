# Schedule Data Formats

## Supported Input Formats

### Format A: CSV/Excel
Standard tabular format. One row per shift assignment.

Required columns:
```
date        | staff_id  | staff_name | start_time | end_time | location | role
2024-07-15  | zhang_san | 张三       | 10:00      | 19:00    | 收银台   | 收银员
2024-07-15  | li_si     | 李四       | 14:00      | 22:00    | 卖场     | 导购
```

Optional columns:
- `break_start` / `break_end` — lunch/rest break
- `on_call` — boolean, whether staff is emergency on-call
- `manager_on_duty` — boolean, designates shift manager

---

### Format B: Text Table (pasted by manager)
Common when managers paste from WeChat or type manually.

```
7月15日班表：
早班（10:00-19:00）：张三、李四
晚班（14:00-22:00）：王五、赵六
值班店长：王经理（全天）
```

Parse with `scripts/parse_schedule.py --format text`.

---

### Format C: Google Sheets
Share a public-read link or service account access.
Structure must match Format A (tabular, same column names).

Config:
```json
{
  "source": "google_sheets",
  "sheet_url": "https://docs.google.com/spreadsheets/d/...",
  "sheet_name": "7月排班",
  "header_row": 1
}
```

---

### Format D: WeCom Calendar
Pull from WeCom's calendar API if org uses it for scheduling.
Each calendar event = one shift. Event title format: `[staff_name] [role]`.

---

## Structured Schedule Schema

After parsing any format, normalize to:

```json
{
  "schedule_id": "2024-07-w3",
  "period": { "start": "2024-07-15", "end": "2024-07-21" },
  "shifts": [
    {
      "shift_id": "s001",
      "date": "2024-07-15",
      "staff_id": "zhang_san",
      "staff_name": "张三",
      "start_time": "10:00",
      "end_time": "19:00",
      "break_minutes": 60,
      "location": "收银台",
      "role": "收银员",
      "on_call": false,
      "manager_on_duty": false
    }
  ],
  "manager_on_duty": {
    "2024-07-15": { "staff_id": "wang_mgr", "name": "王经理", "phone": "138..." }
  }
}
```

## Validation Rules

After parsing, validate:
- No staff member has two overlapping shifts on the same day
- At least one manager_on_duty per day the store is open
- No gaps > 2 hours during store open hours without coverage
- Minimum [N] staff per shift (configurable, default 2)

Report validation errors before activating the new schedule.
