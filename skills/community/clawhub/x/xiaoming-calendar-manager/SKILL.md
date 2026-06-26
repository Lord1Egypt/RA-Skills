---
name: calendar-manager
description: 日历管理 - 日程安排、会议提醒、冲突检测
---

# Calendar Manager

日历管理工具，帮助高效安排日程。

## 功能

- ✅ 日程安排
- ✅ 会议提醒
- ✅ 冲突检测
- ✅ 重复事件
- ✅ 共享日历

## 使用

```bash
# 添加日程
clawhub cal add --title "会议" --start "2026-04-18 10:00" --end "11:00"

# 查看日程
clawhub cal list --date 2026-04-18

# 设置提醒
clawhub cal remind --id 1 --before 15

# 检测冲突
clawhub cal check --date 2026-04-18
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 50 个事件 |
| Pro 版 | ¥49 | 无限事件 |
| 订阅版 | ¥12/月 | Pro+ 共享日历 |
