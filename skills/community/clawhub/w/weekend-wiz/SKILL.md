---
name: weekend-wiz
description: Weekend schedule management assistant with magical organization powers. Create, update, and visualize weekend schedules with HTML rendering and automated reminders. Use when users need to manage their weekend calendar, add schedules, set reminders, or generate visual schedule screenshots. Supports markdown schedule files, beautiful HTML visualization, cron reminders, and automatic cleanup of expired events. Named after the wizard-like ability to magically organize your weekends.
---

# WeekendWiz 🧙‍♂️

Your magical weekend schedule assistant that helps you organize your free time with style.

A personal schedule management system that helps users organize their calendar with visual HTML rendering and automated reminders.

## Features

- **Markdown Schedule Management**: Central schedule storage in `memory/schedule.md`
- **HTML Visualization**: Beautiful, mobile-friendly schedule cards
- **Automated Reminders**: Cron-based reminder system
- **High-Quality Screenshots**: 2x resolution screenshots for sharing
- **Auto Cleanup**: Removes expired events automatically

## Workflow

When user adds/modifies a schedule:

1. **Update `memory/schedule.md`** — Main schedule file
2. **Delete expired events** — Auto-cleanup past dates
3. **Update HTML visualization** — Generate `schedule.html`
4. **Generate screenshot** — High-quality PNG for sharing
5. **Set cron reminders** — Automated reminders at specified times

## File Structure

```
memory/
├── schedule.md          # Main schedule (markdown table format)
├── schedule.html        # Visual HTML version
└── YYYY-MM-DD.md        # Daily notes (optional)
```

## Schedule.md Format

```markdown
# 📅 日程表

## 本周日程

### 3月14日（周六）
| 时间 | 事项 | 地点 | 备注 |
|------|------|------|------|
| 08:30-11:00 | 报税 | 税务APP | 已设提醒：3/13 18:00 |


## 未来日程
_暂无记录_

## 历史日程
_已过期日程自动归档_
```

## HTML Template

Use `assets/schedule_template.html` as the base template. Replace `<!-- SCHEDULE_CONTENT_PLACEHOLDER -->` with generated schedule cards.

### Date Label Logic

When updating HTML, dynamically calculate date labels based on current date:

| Label | Condition | CSS Class |
|-------|-----------|-----------|
| **今天** | Date == Today | `today` |
| **明天** | Date == Tomorrow | `tomorrow` |
| **本周** | Within 7 days from today | `thisweek` |
| **未来** | More than 7 days away | `upcoming` |

Also update the page header month: `<div class="subtitle" id="current-month">2026年3月</div>`

Use `scripts/update_schedule.py` to auto-update month and date labels:

```bash
python3 scripts/update_schedule.py assets/schedule_template.html memory/schedule.html
```

## Screenshot Generation

Use the provided script for high-quality screenshots:

```bash
python3 scripts/generate_screenshot.py /path/to/schedule.html /path/to/output.png
```

This generates a 1200x2400 (2x) resolution screenshot.

## Reminder Setup

Use `openclaw cron add` for reminders:

```bash
openclaw cron add \
  --name "提醒名称" \
  --at "2026-03-13T18:00:00+08:00" \
  --session isolated \
  --message "提醒内容" \
  --deliver \
  --channel qqbot \
  --to "USER_ID" \
  --delete-after-run
```

### Time Formats

- **Relative**: `5m`, `1h`, `2d` (no + sign)
- **Absolute**: `2026-03-13T18:00:00+08:00`

## Event Types & Icons

| Type | Icon | Color | CSS Class |
|------|------|-------|-----------|
| 运动健身 | 🏋️/💪 | Green | `fitness` |
| 医疗健康 | 🏥 | Purple | `health` |
| 工作会议 | 🏢 | Orange | `work` |

## Example User Requests

- "帮我添加3月21日下午2点的面试"
- "把3/14的报税提醒改成前一天晚上6点"
- "删除已经过期的日程"
- "截图给我看看现在的日程"

## Implementation Notes

1. Always update `memory/schedule.md` first as the source of truth
2. **Update date labels dynamically**: Run `scripts/update_schedule.py` to auto-update month and date labels (今天/明天/本周/未来)
3. Use Playwright + Chromium for screenshot generation
4. Set reminders with meaningful content (include time, location, notes)
5. Clean up expired events from both markdown and HTML
6. **Update page month**: Always update `#current-month` element to current year/month
