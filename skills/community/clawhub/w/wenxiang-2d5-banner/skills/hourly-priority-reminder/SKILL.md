# Hourly Priority Reminder - V1.7 (Weekend Mode)

## 更新记录

### V1.7 (2026-03-08 15:48) - 周末模式
- **新增**: 周六/周日不读取项目知识库待办事项
- **原因**: 周末不推送项目级任务，只推送日常任务
- **逻辑**: 检测 `DayOfWeek`，如果是 Saturday 或 Sunday，跳过项目任务读取

### V1.6 (2026-03-08) - HTML 链接优化
- 显示完整 `<title>` 标签内容
- 添加 `[📄 查看]` 链接

### V1.5 (2026-03-08) - Worklog 自动更新
- 每小时自动记录完成情况到 worklog.txt

---

## 核心逻辑

```powershell
# 周末检测
$dayOfWeek = (Get-Date).DayOfWeek
$isWeekend = ($dayOfWeek -eq "Saturday" -or $dayOfWeek -eq "Sunday")

if ($isWeekend) {
    # 跳过项目任务
} else {
    # 正常读取 active-tasks.md
}
```

---

## 触发词

- "每小时优先级提醒"
- "优先级播报"
- "任务提醒"

---

## 三线同步

- **MD**: `scripts/hourly-priority-reminder.ps1` (脚本本身)
- **TXT**: `skills/README.md` (技能列表)
- **飞书**: 原子动作清单 - 动态更新文档

---

## 测试验证

- [ ] 工作日运行：包含项目任务
- [ ] 周末运行：仅日常任务
- [ ] 语音流程正常
- [ ] Worklog 自动更新
