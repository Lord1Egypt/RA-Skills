---
name: smart-reminder-companion
slug: smart-reminder-companion
version: 1.0.0
description: 智能提醒小管家，支持定时提醒、情绪联动提醒、场景化提醒。
homepage: https://github.com/786793119/miya-skills
metadata: {"openclaw":{"emoji":"⏰","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# 每日提醒小管家 (Smart Reminder Companion)

你的私人智能提醒管家。

## 功能

- 添加/删除提醒
- 查看所有提醒
- 启用/禁用提醒
- 情绪联动建议
- 天气相关提醒

## 使用示例

```bash
# 添加提醒
python smart-reminder-companion.py add "09:00" "起床啦～" daily

# 查看提醒
python smart-reminder-companion.py list

# 删除提醒
python smart-reminder-companion.py delete <ID>
```

## 数据存储

- 提醒数据: `~/.memory/reminders/reminders.json`

---

*By Miya - 2026*
