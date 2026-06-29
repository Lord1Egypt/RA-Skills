# 使用指南

## 工作日计算

```python
summary = calculate_total_workdays(2026)
# 返回:
# {
#   "year": 2026,
#   "total_workdays": 247,
#   "total_holidays": 118,
#   "holiday_count": 28,
#   "compensatory_count": 5
# }
```

```python
calendar = generate_weekly_calendar(2026)
for week in calendar:
    print(f"第{week['week_number']}周")
    for day in week['days']:
        if day['date']:
            print(f"  {day['date']}: {day['day_type']}")
```

```python
result = sync_year(2026, 2025)
# 返回: {"holidays_synced": 7, "compensatory_synced": 4}
```

## 日程管理

```python
event, msg = add_schedule_event(
    title="团队会议", date="2026-05-20",
    start_time="14:00", end_time="15:00",
    description="项目进度讨论", category="会议"
)
```

```python
events = get_schedule_by_date("2026-05-20")
for e in events:
    print(f"{e.start_time}-{e.end_time} {e.title}")

slots = find_free_slots(date="2026-05-20", start_search="09:00", end_search="18:00", min_duration=30)

events = get_schedules_by_date_range("2026-05-20", "2026-05-25")
```

```python
msg = delete_schedule_event(event_id)
msg = update_schedule_event(event_id, title="新标题", status="completed")

schedule_text = generate_today_schedule()
schedule_text = generate_daily_schedule("2026-05-20", 14)
```

## 容灾备份

每次 `add_schedule_event()` 自动创建 `.bat` 备份文件：
- 存储在 `data/backups/schedule_backup_01.bat ~ 09.bat`
- 最多保留 9 个，循环覆盖
- 恢复：双击 `.bat` 文件或 `cmd /c data/backups/schedule_backup_03.bat`
