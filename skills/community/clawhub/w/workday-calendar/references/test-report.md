## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | workday-calendar |
| 测试时间 | 2026-06-22 14:00 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| D1-D6 功能测试 | 187 | 72 | 0 | 38% |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\settings.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\workday_calendar | PASS | :0 |  |
| D1 | WARN | 启动失败: scripts\settings.py | FAIL | scripts\settings.py:0 | exit code 1: -calendar\scripts\settings.py", line  |
| D1 | WARN | 启动失败: scripts\workday_calendar | FAIL | scripts\workday_calendar.py:0 | exit code 1:  |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\settings.py → webbrowser |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\settings.py → http.server.HTTPServer |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\settings.py → http.server.BaseHTTPRequestH |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.loa |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.sav |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.exp |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.imp |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.gen |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.gen |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.exp |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.cal |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.get |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\settings.py → scripts.workday_calendar.dat |
| D2 | INFO | 外部依赖: urllib | PASS | :0 | scripts\settings.py → urllib.parse.urlparse |
| D2 | INFO | 外部依赖: urllib | PASS | :0 | scripts\settings.py → urllib.parse.parse_qs |
| D2 | INFO | 外部依赖: uuid | PASS | :0 | scripts\workday_calendar.py → uuid |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\settings.py:451 | print("按 Ctrl+C 停止服务器") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\settings.py:456 | print("\n服务器已停止") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3002 | print("用法: python workday_calendar.py <command> [o |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3003 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3004 | print("规则确认:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3005 | print("  rules [year]               - 导出规则确认表（请在初始 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3006 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3007 | print("工作日计算:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3008 | print("  calculate <year>           - 计算年度总工日") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3009 | print("  calendar <year>            - 生成周历") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3010 | print("  sync <year> [source_year]  - 同步数据到目标年份") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3011 | print("  init <year>                - 初始化年度数据") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3012 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3013 | print("日程管理:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3014 | print("  add <date> <start> <end> <title> [desc] [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3015 | print("  list [date]                - 列出日程") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3016 | print("  delete <id>                - 删除日程") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3017 | print("  update <id> [options]      - 更新日程") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3018 | print("  free <date> [start] [end]  - 查找空闲时间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3019 | print("  schedule [days]            - 生成日程列表(默认7天) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3020 | print("  today                      - 生成今天及后续7天日程" |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3021 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3022 | print("轮休管理:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3023 | print("  rotation add <name> <start> <cycle> <work |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3024 | print("                               - 添加轮休配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3025 | print("  rotation list              - 列出轮休配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3026 | print("  rotation delete <id>       - 删除轮休配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3027 | print("  rotation generate [year]   - 生成轮休日并缓存") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3028 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3029 | print("特殊休息管理:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3030 | print("  special add 公休|临修 --date=<d> [--reason=<r |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3031 | print("  special add 公休|临修 --start-date=<d> --end- |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3032 | print("  special list [公休|临修]    - 列出特殊休息") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3033 | print("  special list [公休|临修]    - 列出特殊休息") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3034 | print("  special delete <id>        - 删除特殊休息") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3035 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3036 | print("排版规则管理(B层):") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3037 | print("  sched view                  - 查看当前排班规则") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3038 | print("  sched set <weekday> <slots> - 配置某天规则") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3039 | print("     时段格式: start-end:label[:position[:perso |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3040 | print("     例: sched set 0 00:00-08:30:休息 08:30-11 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3041 | print("                   11:30-13:30:午休 13:30-17: |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3042 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3043 | print("自动化(定时任务):") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3044 | print("  auto check               - 检查并执行到时的定时任务") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3045 | print("  auto add <name> <hour> <min> <days> [--no |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3046 | print("  auto list                - 列出定时任务") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3047 | print("  auto delete <id>         - 删除定时任务") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3048 | print("  auto preview <days> [--nosched] [--noshif |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3049 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3050 | print("HTML 导出:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3051 | print("  export-weekly-board [year] [output] - 导出排 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3052 | print("  export-schedule-weekly [year] [output] -  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3053 | print("  export-schedule-table --mode=<week|month> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3054 | print("     例: export-schedule-table --mode=week   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3055 | print("         export-schedule-table --mode=month |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3056 | print("  export-schedule [output]     - 导出现有日程 HTM |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3064 | print(export_rules_table(year)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3069 | print("用法: add <date> <start> <end> <title> [descr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3079 | print(json.dumps(event.to_dict(), ensure_ascii=Fal |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3080 | print(msg) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3096 | print("用法: delete <event_id>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3098 | print(delete_schedule_event(sys.argv[2])) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3102 | print("用法: update <event_id> [options]") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3103 | print("选项: --title, --date, --start, --end, --desc |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3122 | print(update_schedule_event(event_id, **kwargs)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3138 | print(generate_daily_schedule(datetime.now().strft |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3141 | print(generate_today_schedule()) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3147 | print(json.dumps(summary, ensure_ascii=False, inde |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3152 | print(json.dumps(cal, ensure_ascii=False, indent=2 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3158 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3169 | print("用法: rotation <add|list|delete|generate> [op |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3176 | print("用法: rotation add <name> <start_date> <cycle |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3189 | print(json.dumps(config.to_dict(), ensure_ascii=Fa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3190 | print(msg) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3193 | print(list_rotation_configs()) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3197 | print("用法: rotation delete <id>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3199 | print(delete_rotation_config(sys.argv[3])) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3203 | print(rotate_generate(year)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3211 | print("用法: special <add|list|delete> [options]") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3218 | print("用法: special add 公休|临修 --date=... [--reason= |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3236 | print(json.dumps(rest.to_dict(), ensure_ascii=Fals |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3237 | print(msg) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3241 | print(list_special_rests(filter_type)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3245 | print("用法: special delete <id>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3247 | print(delete_special_rest(sys.argv[3])) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3255 | print("用法: sched <view|set> ...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3262 | print("当前无自定义排版规则（使用默认）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3270 | print("用法: sched set <weekday(0-6)> <start-end:lab |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3271 | print("  weekday: 0=周一 1=周二 ... 6=周日") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3317 | print(json.dumps(cfg, ensure_ascii=False, indent=2 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3320 | print(json.dumps(cfg, ensure_ascii=False, indent=2 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3326 | print(json.dumps(template, ensure_ascii=False, ind |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3330 | print("用法: import-rules '<json_string>'") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3331 | print("  或: import-rules --file=<path>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3340 | print(result) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3345 | print("用法: auto <check|add|list|delete|preview> .. |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3351 | print(result) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3353 | print("当前无匹配的自动化规则") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3355 | print(list_auto_rules()) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3360 | print(generate_schedule_markdown(days, show_shifts |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3363 | print("用法: auto add <name> <hour> <min> <days> [-- |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3377 | print(msg) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3379 | print(msg) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3382 | print("用法: auto delete <id>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3384 | print(delete_auto_rule(sys.argv[3])) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3398 | print(html) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3409 | print(html) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3419 | print(html) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\workday_calendar.py:3444 | print(html) |
| D5 | INFO | 发现 1 个验证函数 | PASS | :0 | check_automations |
| D5 | INFO | 发现 2 个计算函数 | PASS | :0 |  |
| D5 | WARN | 模块加载异常: scripts\settings | FAIL | scripts\settings.py:0 | invalid literal for int() with base 10: 'C:/Users/ |
| D5 | INFO | 模块可加载: scripts\workday_calenda | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_skill_data_dir() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: get_weekend_config_file | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: get_rotation_config_fil | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: get_special_rests_file( | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: get_scheduling_rules_fi | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: load_scheduling_rules() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: get_auto_config_file() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: load_auto_configs() | PASS | :0 | 返回值类型: list |
| D5 | INFO | 函数可运行: list_auto_rules() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: check_automations() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: get_config_file() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: load_config() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: load_weekend_config() | PASS | :0 | 返回值类型: WeekendConfig |
| D5 | INFO | 函数可运行: load_rotation_configs() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: load_special_rests() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: get_schedule_file() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: load_schedule_events() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: generate_today_schedule | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: list_rotation_configs() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: generate_schedule_html( | PASS | :0 | 返回值类型: str |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:86 | get_rotation_days_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:332 | save_scheduling_rules() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:379 | get_slot_color_for_time() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:508 | generate_schedule_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:597 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:723 | save_weekend_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:744 | save_rotation_configs() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:768 | save_rotation_days() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:799 | save_special_rests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:909 | save_schedule_events() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:920 | auto_update_event_statuses() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:992 | get_all_dates_of_year() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1024 | generate_holiday_set() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1039 | generate_compensatory_set() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1044 | generate_rotation_days_for_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1135 | get_special_rest_dates() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1568 | get_schedule_by_date() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1574 | get_schedules_by_date_range() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1687 | delete_rotation_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1841 | import_holidays_from_ai() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1854 | import_compensatory_from_ai() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1865 | export_year_summary() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:1936 | import_rules_from_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:101 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:116 | from_dict() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:127 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:164 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:195 | from_dict() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:260 | from_dict() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:313 | from_dict() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\workday_calendar.py:668 | overlaps() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\settings.py:0 | scripts\settings.py: 1 个 except / 462 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\workday_calendar.py:0 | scripts\workday_calendar.py: 6 个 except / 3449 行 |
