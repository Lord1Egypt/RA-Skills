# workday-calendar 反模式

> 本文件以渐进式加载方式提供，详见 `references/antipatterns.md`

## 反模式 1：在 SKILL.md 正文中写完整数据格式说明

**错误做法**：把 `holiday_intervals.json` 和 `schedule_events.json` 的完整字段说明全部写在 SKILL.md 里，导致文件超过 230 行，违反 R-17 规则。

**正确做法**：数据格式说明拆分到 `references/data_format.md`，SKILL.md 只留摘要 + 引用链接。当 SKILL.md 超过 150 行时应主动考虑拆分。

## 反模式 2：触发词过于宽泛导致误触发

**错误做法**：trigger 写成 `日历|calendar`，导致用户说「帮我画一个日历 UI」时也触发本技能，而用户实际想要的是 drawio-diagram 画图。

**正确做法**：触发词须含具体动作或对象（如 `法定假日|工作日|周历|日程管理`），并配合 `trigger_negative: true` 在「不触发」段落排除 UI 设计类意图。

## 反模式 3：直接编辑 data/ 下的 JSON 文件而不备份

**错误做法**：手动用编辑器打开 `data/schedule_events.json` 更新日程，改错后无法恢复，也没有利用系统自带的 .bat 容灾备份机制。

**正确做法**：始终通过 `python scripts/workday_calendar.py add/delete/update` 操作，脚本会自动创建 `.bat` 容灾备份。紧急恢复时双击 `data/backups/schedule_backup_XX.bat` 即可回滚。
