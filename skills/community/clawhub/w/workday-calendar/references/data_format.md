# 智能周历系统 - 数据格式规范

## 概述

本系统使用 JSON 格式存储数据，支持 AI/智能体 格式化导入导出。

---

## 1. 法定假日区间 (Holiday Intervals)

**文件名**: `holiday_intervals_{年份}.json`

### 完整格式

```json
{
  "year": 2026,
  "intervals": [
    {
      "name": "元旦",
      "start": "2026-01-01",
      "end": "2026-01-01",
      "note": "新年第一天"
    },
    {
      "name": "春节",
      "start": "2026-01-28",
      "end": "2026-02-04",
      "note": "农历新年假期"
    }
  ],
  "updated_at": "2025-12-01T10:30:00"
}
```

### AI导入格式（简化）

```json
[
  {"name": "元旦", "start": "2026-01-01", "end": "2026-01-01"},
  {"name": "春节", "start": "2026-01-28", "end": "2026-02-04"},
  {"name": "清明节", "start": "2026-04-04", "end": "2026-04-06"},
  {"name": "劳动节", "start": "2026-05-01", "end": "2026-05-05"},
  {"name": "端午节", "start": "2026-06-20", "end": "2026-06-22"},
  {"name": "中秋节", "start": "2026-10-06", "end": "2026-10-08"},
  {"name": "国庆节", "start": "2026-10-01", "end": "2026-10-07"}
]
```

---

## 2. 补班日期 (Compensatory Days)

**文件名**: `compensatory_days_{年份}.json`

### 完整格式

```json
{
  "year": 2026,
  "days": [
    {"date": "2026-01-25", "note": "春节前调休"},
    {"date": "2026-02-08", "note": "春节后补班"}
  ],
  "updated_at": "2025-12-01T10:30:00"
}
```

### AI导入格式（简化）

```json
[
  {"date": "2026-01-25"},
  {"date": "2026-02-08", "note": "春节调休"}
]
```

---

## 3. 周末规则配置 (Weekend Config)

**文件名**: `weekend_config.json`

```json
{
  "weekends": [0, 6],
  "updated_at": "2025-12-01T10:30:00"
}
```

### 周末数值对照

| 数值 | 星期 |
|------|------|
| 0 | 周日 |
| 1 | 周一 |
| 2 | 周二 |
| 3 | 周三 |
| 4 | 周四 |
| 5 | 周五 |
| 6 | 周六 |

---

## 4. 日程事件 (Schedule Events)

**文件名**: `schedule_events.json`

### 完整格式

```json
{
  "events": [
    {
      "id": "d008b885",
      "title": "团队会议",
      "date": "2026-05-20",
      "start_time": "14:00",
      "end_time": "15:00",
      "description": "项目进度讨论",
      "category": "会议",
      "status": "pending",
      "created_at": "2026-05-19T22:00:00",
      "updated_at": "2026-05-19T22:00:00"
    }
  ],
  "updated_at": "2026-05-19T22:00:00"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✅ | 唯一标识符（自动生成） |
| title | string | ✅ | 日程标题 |
| date | string | ✅ | 日期 (YYYY-MM-DD) |
| start_time | string | ✅ | 开始时间 (HH:MM) |
| end_time | string | ✅ | 结束时间 (HH:MM) |
| description | string | ❌ | 描述说明 |
| category | string | ❌ | 分类（工作/个人/会议/其他） |
| status | string | ❌ | 状态（pending/completed/cancelled） |
| created_at | string | ✅ | 创建时间 |
| updated_at | string | ✅ | 更新时间 |

### 分类选项

| 值 | 说明 |
|----|------|
| 工作 | 工作相关事务 |
| 个人 | 个人事务 |
| 会议 | 会议安排 |
| 其他 | 其他类型 |

### 状态选项

| 值 | 说明 |
|----|------|
| pending | 待完成（默认） |
| completed | 已完成 |
| cancelled | 已取消 |

---

## 5. 年度汇总导出 (Year Summary)

```json
{
  "year": 2026,
  "total_workdays": 247,
  "total_holidays": 118,
  "total_days": 365,
  "holiday_count": 28,
  "compensatory_count": 5,
  "weekend_config": {"weekends": [0, 6]},
  "holiday_intervals": [...],
  "compensatory_days": [...]
}
```

---

## 6. 周历导出 (Weekly Calendar)

```json
[
  {
    "week_number": 1,
    "week_start": "2026-01-01",
    "week_end": "2026-01-03",
    "week_workdays": 2,
    "week_holidays": 5,
    "days": [
      {
        "date": "2026-01-01",
        "weekday": 3,
        "weekday_name": "周四",
        "day_type": "假日",
        "is_workday": false,
        "holiday_name": "元旦",
        "month": 1,
        "day": 1
      }
    ]
  }
]
```

---

## 7. 空闲时段查询 (Free Slots)

```json
[
  {"start": "10:00", "end": "14:00", "duration": 240},
  {"start": "15:30", "end": "18:00", "duration": 150}
]
```

---

## AI调用示例

### 场景1：导入法定假日数据

```python
import_holidays_from_ai(2026, [
    {"name": "元旦", "start": "2026-01-01", "end": "2026-01-01"},
    {"name": "春节", "start": "2026-01-28", "end": "2026-02-04"},
    # ...
])
```

### 场景2：添加日程

```python
event, msg = add_schedule_event(
    title="团队会议",
    date="2026-05-20",
    start_time="14:00",
    end_time="15:00",
    description="项目进度讨论",
    category="会议"
)
```

### 场景3：查询空闲时间

```python
slots = find_free_slots(
    date="2026-05-20",
    start_search="09:00",
    end_search="18:00"
)
```

### 场景4：生成日程列表

```python
schedule = generate_today_schedule()
# 输出:
# 📅 2026-05-19 (周二) - 无安排
# 📅 2026-05-20 (周三)
#   🔄 09:00-10:00 晨会
#   🔄 14:00-15:30 项目评审
```

### 场景5：删除日程

```python
msg = delete_schedule_event("d008b885")
# 输出: "已删除日程: 晨会"
```

### 场景6：更新日程状态

```python
msg = update_schedule_event(
    "d008b885",
    status="completed"
)
```
