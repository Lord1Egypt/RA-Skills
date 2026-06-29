# CLI 命令参考

```bash
# 规则确认（重要！初始化后必须执行，核对配置是否正确）
python scripts/workday_calendar.py rules 2026           # 导出规则确认表

# 工作日计算
python scripts/workday_calendar.py calculate 2026       # 计算年度工日
python scripts/workday_calendar.py calendar 2026        # 生成周历JSON
python scripts/workday_calendar.py sync 2026 2025       # 同步数据

# 轮休管理
python scripts/workday_calendar.py rotation add "A组" 2026-01-05 7 5 --skip
python scripts/workday_calendar.py rotation list
python scripts/workday_calendar.py rotation delete <id>
python scripts/workday_calendar.py rotation generate 2026

# 特殊休息管理（公休/临修）
python scripts/workday_calendar.py special add 公休 --date=2026-03-15 --reason="公司统一调休"
python scripts/workday_calendar.py special add 临修 --start-date=2026-04-10 --end-date=2026-04-12
python scripts/workday_calendar.py special list
python scripts/workday_calendar.py special delete <id>

# 排班时段规则
python scripts/workday_calendar.py sched view
python scripts/workday_calendar.py sched set 0 08:30-11:30:上午班|收银台:张三,李四 13:30-17:30:下午班

# 配置管理
python scripts/workday_calendar.py config
python scripts/workday_calendar.py config set --use-scheduling=true
python scripts/workday_calendar.py config set --auto-complete=true

# 规则模板（标准化 JSON 接口）
python scripts/workday_calendar.py export-rules-template
python scripts/workday_calendar.py import-rules '<json>'

# 日程管理
python scripts/workday_calendar.py add 2026-05-20 09:00 10:00 "晨会"
python scripts/workday_calendar.py list 2026-05-20
python scripts/workday_calendar.py free 2026-05-20 09:00 18:00
python scripts/workday_calendar.py delete <event_id>
python scripts/workday_calendar.py update <event_id> --status=completed
python scripts/workday_calendar.py schedule 7
python scripts/workday_calendar.py today

# HTML 导出
python scripts/workday_calendar.py export-weekly-board [year]
python scripts/workday_calendar.py export-schedule-weekly [year]
python scripts/workday_calendar.py export-schedule-table --mode=week|month --date-from=... --date-to=...

# 定时任务自动化
python scripts/workday_calendar.py auto add "晨间简报" 6 0 3
python scripts/workday_calendar.py auto list
python scripts/workday_calendar.py auto check

# 配置中心（Web 界面）
python scripts/settings.py [port]   # 默认 8765
```

### ⚙️ 配置中心

运行 `python scripts/settings.py 8765` 后在浏览器打开 `http://localhost:8765`，支持：
- **基础周类型切换** - 节假周 / 排班周
- **过期日程自动打标** - 已完成 / 已错过
- **导出规则模板** / **导入规则**
- **导出排班HTML** / **导出日程HTML** / **导出排班表**
- 排班表支持周/月单选 + 日期范围筛选
