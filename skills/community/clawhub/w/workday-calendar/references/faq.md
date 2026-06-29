# FAQ — workday-calendar 常见问题

> 本文件以渐进式加载方式提供，详见 `references/faq.md`

Q: 什么时候用工作日计算，什么时候用日程管理？
A: 工作日计算用于查询某年/某月有多少个工作日、是否为假日等；日程管理用于管理个人日程事件（会议、任务等）。两者互不干扰，可以同时使用。

Q: 数据文件存储在哪里？会不会丢失？
A: 所有数据存储在 `skills/.standardization/workday-calendar/data/` 目录下（`holiday_intervals.json`、`compensatory_days.json`、`schedule_events.json` 等）。每次添加日程前系统自动创建 .bat 容灾备份，最多保留 9 个，可一键回滚。

Q: 如何导入新的法定假日数据？
A: 使用 CLI 命令 `python scripts/workday_calendar.py init <year>` 初始化年份数据，然后手动编辑 `data/holiday_intervals_<year>.json` 填入官方假日区间，或使用 AI 批量导入。

Q: 周历和日程有什么区别？
A: 周历（calendar）是按周展示的年度工作日/假日视图，用于查看某周有哪些工作日；日程（schedule）是具体日期上的事件安排，两者属于不同维度，可配合使用。

Q: 为什么计算的工作日数和官方不一致？
A: 请先执行 `python scripts/workday_calendar.py rules <year>` 查看规则确认表，核对假日区间和补班日是否正确配置。配置错误是计算结果偏差的最常见原因。

Q: add_schedule_event() 返回"冲突"怎么办？
A: 该时间段已有日程。先用 `list <date>` 查看现有日程，调整起止时间避开冲突。更新日程时也会重新检测冲突，冲突则自动还原。

Q: 导入规则模板时报 JSON 解析错误？
A: 检查模板 JSON 是否符合 `export_rules_template` 格式（version/year/base_type/rules 字段）。可先用 `export-rules-template` 导出正确格式作为对照。

Q: HTML 导出后页面空白/乱码？
A: 确保使用 UTF-8 编码保存 .html 文件。用浏览器打开时若显示乱码，在浏览器菜单中手动选择 UTF-8 编码。

Q: settings.py 配置中心无法访问？
A: 确认端口 8765 未被占用。如被占用，运行 `python scripts/settings.py <其他端口>` 指定端口。防火墙可能需放行。
