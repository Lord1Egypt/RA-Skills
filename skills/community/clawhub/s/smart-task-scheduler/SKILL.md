---
name: smart-task-scheduler
description: 智能任务与排班管理系统，支持多时段工作安排、动态排班和上班时间自适应提醒
metadata: {"openclaw": {"emoji": "⏰", "requires": {"env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"]}, "primaryEnv": "FEISHU_APP_ID"}}
---

# 智能任务与排班管理系统

一个先进的个人任务与排班管理系统，能根据您复杂的多时段工作安排动态调整提醒，支持从表格文件导入排班，并通过自然语言修改排班。

## 核心优势

- **多时段工作支持**：完整支持"早"、"晚"、"早晚"等多种工作时段安排
- **排班自适应提醒**：根据您每天实际的多个工作时段动态计算提醒时间
- **灵活提醒规则**：支持基于特定工作时段开始前/后的提醒
- **表格导入**：支持上传Excel/CSV排班表，自动解析并存储
- **自然语言修改**：可通过对话直接修改排班信息
- **智能时段选择**：为任务自动选择最合适的工作时段

## 功能特性

### 1. 多时段排班管理
- **多时段工作安排**：支持单个时段、多个时段的复杂工作安排
- **排班表格导入**：支持上传Excel/CSV文件，自动解析复杂排班信息
- **自然语言修改**：通过对话直接修改特定日期的上班时间和时段安排
- **时段智能选择**：为任务自动选择最合适的工作时段
- **排班查询**：查询任意日期的排班信息和时段安排

### 2. 智能任务管理
- **动态提醒计算**：根据当天实际工作时段计算提醒时间
- **多时段提醒规则**：
  - `before_shift_start:X`：指定时段开始前X分钟提醒
  - `after_shift_start:X`：指定时段开始后X分钟提醒
  - `between_shifts:X`：两个工作时段之间提前X分钟提醒
  - `fixed_time:HH:MM`：固定时间提醒
- **时段自动匹配**：根据任务描述自动推荐最合适的工作时段

### 3. 智能提醒系统
- **智能体对话提醒**：在适当时间主动发起对话提醒，支持交互操作
- **时段关联提醒**：为同一任务在不同时段设置不同提醒

## 工具接口

### `import_schedule`
**导入排班表**

从Excel或CSV文件导入排班信息。文件格式需包含日期、工作时段等列。

*参数*：
- `file_path`: (字符串) 排班表文件路径
- `format`: (字符串) 文件格式，`excel` 或 `csv`

*示例*：
`/import_schedule /path/to/schedule.xlsx excel`

### `update_schedule`
**更新排班信息**

通过自然语言修改特定日期的排班信息。

*参数*：
- `date`: (字符串) 要修改的日期，格式为 `YYYY-MM-DD` 或自然语言如"明天"、"下周一"
- `change_description`: (字符串) 变更描述，如"明天上早晚班"、"周三晚班"

*示例*：
`/update_schedule 明天 早晚班，9:30-11:30 和 16:00-21:30`

### `show_schedule`
**查看排班**

查看指定日期范围的排班信息。

*参数*：
- `start_date`: (字符串，可选) 开始日期，默认为今天
- `end_date`: (字符串，可选) 结束日期，默认为7天后
- `format`: (字符串，可选) 输出格式，`table`(表格) 或 `list`(列表)

*示例*：
`/show_schedule 2026-04-01 2026-04-07 table`

### `add_smart_task`
**添加智能任务**

添加能根据排班动态调整提醒时间的任务。系统会根据任务类型和时段自动选择最合适的提醒时段。

*参数*：
- `description`: (字符串) 任务描述
- `due_date`: (字符串) 截止日期，格式为 `YYYY-MM-DD` 或自然语言
- `reminder_rule`: (字符串) 提醒规则，支持：
  - `before_first_shift:30` (第一时段开始前30分钟)
  - `after_first_shift_start:15` (第一时段开始后15分钟)
  - `before_second_shift:30` (第二时段开始前30分钟)
  - `between_shifts:60` (两时段之间提前60分钟)
  - `fixed_time:14:00` (固定时间)
- `task_type`: (字符串，可选) 任务类型，帮助系统选择时段，如`morning_task`, `between_shift_task`, `evening_task`
- `priority`: (字符串，可选) 优先级，`high`/`medium`/`low`

*示例*：
`/add_smart_task 买早餐 明天 before_first_shift:20 high morning_task`

### `calculate_reminders`
**计算提醒时间**

为所有任务计算基于排班的实际提醒时间。

*参数*：
- `date`: (字符串，可选) 计算指定日期的提醒，默认为明天

*示例*：
`/calculate_reminders 2026-04-01`

## 配置要求

### 环境变量

飞书应用配置 (必需)

FEISHU_APP_ID=your_app_id

FEISHU_APP_SECRET=your_app_secret

文件路径配置 (可选)

SCHEDULE_FILE_PATH=/path/to/schedule.json

TASKS_FILE_PATH=/path/to/tasks.json

### 定时任务配置
创建以下定时任务以实现自动化：

1. **每日排班同步**（每晚22:00运行，同步明天的排班和任务）：

openclaw cron add \

--name "每日排班同步" \

--cron "0 22 * * *" \

--tz "Asia/Shanghai" \

--session isolated \

--message "请执行以下操作：1. 调用'smart-task-scheduler'技能的'calculate_reminders'功能，为明天的任务计算基于排班的提醒时间。2. 返回执行摘要，格式：[排班同步] 已为X个任务计算提醒时间。明天的工作时段是：Z。" \

--announce \

--agent smart-task-scheduler

2. **时段智能提醒**（根据实际工作时段的开始时间动态触发）：

openclaw cron add \

--name "工作时段提醒" \

--cron "0 7,9,13,15,20 * * 1-5" \

--tz "Asia/Shanghai" \

--session main \

--system-event "请检查当前时间是否需要触发提醒。调用'smart-task-scheduler'技能的'check_shift_reminders'功能，如果当前时间接近任何任务的提醒时间，在对话中提醒我。" \

--wake hourly \

--agent smart-task-scheduler

## 数据结构

### 1. 多时段排班表 (`workspace/work_schedule.json`)

json

{

"schedule": [

{

"date": "2026-04-01",

"work_shifts": [

{

"shift_type": "晚班",

"start": "15:30",

"end": "22:30",

"shift_index": 0

}

],

"notes": "周三晚班",

"tags": ["晚班"]

},

{

"date": "2026-04-02",

"work_shifts": [

{

"shift_type": "早班",

"start": "09:30",

"end": "11:30",

"shift_index": 0

},

{

"shift_type": "晚班",

"start": "16:00",

"end": "21:30",

"shift_index": 1

}

],

"notes": "周四早晚班",

"tags": ["早晚班", "多时段"]

},

{

"date": "2026-04-03",

"work_shifts": [

{

"shift_type": "早班",

"start": "08:00",

"end": "15:30",

"shift_index": 0

}

],

"notes": "周五早班",

"tags": ["早班"]

}

],

"default_schedule": {

"work_shifts": [

{

"shift_type": "标准班",

"start": "09:30",

"end": "18:30",

"shift_index": 0

}

]

},

"shift_types": {

"早班": {"typical_start": "08:00", "typical_end": "16:00"},

"晚班": {"typical_start": "15:00", "typical_end": "23:00"},

"早晚班": {"description": "分早晚两个时段"}

},

"last_updated": "2026-03-31T14:20:00Z"

}

### 2. 智能任务文件 (`workspace/smart_tasks.json`)

json

{

"smart_tasks": [

{

"id": "st_20260401_001",

"description": "上班前买晚餐食材",

"due_date": "2026-04-01",

"reminder_rule": "before_shift_start:60",

"target_shift": 0,

"target_shift_type": "晚班",

"calculated_time": "2026-04-01 14:30",

"priority": "high",

"completed": false,

"notes": "超市17点关门，记得下班前去"

},

{

"id": "st_20260402_001",

"description": "两班之间去银行",

"due_date": "2026-04-02",

"reminder_rule": "between_shifts:30",

"calculated_time": "2026-04-02 11:30",  // 第一时段结束后，第二时段开始前

"priority": "medium",

"completed": false,

"recurring_source": "weekly_bank"

},

{

"id": "st_20260402_002",

"description": "早班后去健身房",

"due_date": "2026-04-02",

"reminder_rule": "after_shift_end:15",

"target_shift": 0,

"calculated_time": "2026-04-02 11:45",

"priority": "medium"

}

],

"recurring_rules": [

{

"id": "weekly_bank",

"description": "每周银行办事",

"cycle": "weekly",

"cycle_config": {"day_of_week": 4},  // 周四

"reminder_rule": "between_shifts:30",

"shift_preference": "between_shifts",

"active": true

}

],

"settings": {

"feishu_reminder_minutes": 10,

"default_shift_type": "标准班",

"timezone": "Asia/Shanghai"

}

}

### 3. Excel/CSV排班表格式
支持多种格式，最推荐格式如下：

**推荐格式**：
| 日期       | 班次类型 | 时段1开始 | 时段1结束 | 时段2开始 | 时段2结束 | 备注       |
|------------|----------|------------|------------|------------|------------|------------|
| 2026-04-01 | 晚班     | 15:30      | 22:30      |            |            | 周三晚班   |
| 2026-04-02 | 早晚班   | 09:30      | 11:30      | 16:00      | 21:30      | 周四早晚班 |
| 2026-04-03 | 早班     | 08:00      | 15:30      |            |            | 周五早班   |

**简化格式**（单时段自动解析）：
| 日期       | 排班描述               | 备注       |
|------------|------------------------|------------|
| 2026-04-01 | 晚（15:30-22:30）      | 周三晚班   |
| 2026-04-02 | 早晚（9:30-11:30 16:00-21:30） | 周四早晚班 |
| 2026-04-03 | 早（8:00-15:30）       | 周五早班   |

**自动解析规则**：
- "早（8:00-15:30）" → 解析为早班，时段：08:00-15:30
- "晚（15:30-22:30）" → 解析为晚班，时段：15:30-22:30
- "早晚（9:30-11:30 16:00-21:30）" → 解析为两个时段：09:30-11:30 和 16:00-21:30

## 使用示例

### 场景一：上传多时段排班表
1. **准备排班表**（Excel格式，使用推荐格式）
2. **上传排班表**：
用户：帮我上传这个月的排班表

（用户发送排班表文件）

技能：/import_schedule /path/to/uploaded/schedule.xlsx excel

（解析并存储排班信息，自动识别多时段）

### 场景二：设置基于不同时段的提醒
1. **晚班前的任务**：

用户：明晚上晚班，下午3点提醒我去超市

技能：检测到明天是晚班（15:30-22:30）。/add_smart_task 去超市采购 明天 before_shift_start:30

（自动计算：15:30前30分钟 = 15:00提醒）

2. **早晚班之间的任务**：

用户：周四早晚班之间提醒我去银行

技能：检测到周四是早晚班（09:30-11:30 和 16:00-21:30）。/add_smart_task 去银行办事 2026-04-02 between_shifts:30

（自动计算：第一时段结束后，第二时段开始前30分钟 = 11:30提醒）

3. **早班后的任务**：

用户：周五早班后提醒我去健身房

技能：检测到周五是早班（08:00-15:30）。/add_smart_task 健身房锻炼 2026-04-03 after_shift_end:15

（自动计算：15:30后15分钟 = 15:45提醒）

### 场景三：自然语言修改多时段排班

用户：下周三改成早晚班

技能：/update_schedule 2026-04-08 早晚班，时段1：9:30-11:30，时段2：16:00-21:30

（更新2026-04-08的work_shifts为两个时段）

用户：下周四的晚班时间改成16:30开始

技能：/update_schedule 2026-04-09 晚班，16:30-23:00

（更新2026-04-09的晚班开始时间）

用户：查看下周排班

技能：/show_schedule 2026-04-06 2026-04-12 table

（以表格形式显示下周排班）

### 场景四：自动时段匹配

用户：添加每周四的午间提醒任务

技能：系统会检查周四的排班：

如果是早晚班：建议在between_shifts时段提醒

如果是单时段班：建议在午休时间（12:00-13:00）提醒

会询问：您希望将提醒设置在哪个时段？

## 提醒计算逻辑

### 1. 时段选择策略
系统根据任务类型和排班自动选择最合适的时段：

| 任务类型/时间 | 单时段（早班） | 单时段（晚班） | 多时段（早晚班） |
|---------------|---------------|---------------|------------------|
| 早晨任务      | before_shift_start | before_shift_start | before_first_shift_start |
| 午间任务      | fixed_time:12:00 | fixed_time:12:00 | between_shifts |
| 晚间任务      | after_shift_end | before_shift_start | before_second_shift_start |
| 休息日任务    | fixed_time:09:00 | fixed_time:09:00 | fixed_time:09:00 |

### 2. 时间计算示例
- **早晚班**（09:30-11:30，16:00-21:30）：
  - `before_first_shift_start:30` → 09:00提醒
  - `between_shifts:60` → 11:30提醒（第一时段结束后，第二时段开始前60分钟）
  - `before_second_shift_start:15` → 15:45提醒
  - `after_second_shift_end:30` → 22:00提醒

- **晚班**（15:30-22:30）：
  - `before_shift_start:45` → 14:45提醒
  - `after_shift_start:60` → 16:30提醒
  - `after_shift_end:30` → 23:00提醒

## 注意事项

1. **多时段处理**：对于早晚班，系统会识别两个时段之间的间隔，`between_shifts`规则会自动在两时段之间设置提醒。
2. **时段索引**：`shift_index`从0开始，0表示第一个工作时段，1表示第二个工作时段。
3. **自动时段选择**：如果不指定具体时段，系统会根据任务描述和时间自动选择最合适的时段。
4. **休息日处理**：如果某天没有排班记录，视为休息日，使用默认的固定时间提醒。
5. **时间冲突检测**：如果计算的提醒时间与工作时间冲突，系统会自动调整。

## 故障排除

- **排班表导入失败**：
  1. 检查文件格式是否为支持的Excel(.xlsx/.xls)或CSV
  2. 确认时间格式为HH:MM（24小时制）
  3. 多时段排班确保时段之间不重叠

- **提醒时间计算错误**：
  1. 检查当天的排班记录是否包含正确的工作时段
  2. 确认提醒规则语法正确
  3. 对于多时段，确保指定了正确的`shift_index`

- **自然语言修改不生效**：
  1. 确保时段描述清晰，如"早晚班"或具体时间"9:30-11:30 16:00-21:30"
  2. 修改后使用`/show_schedule`确认修改已生效
---

*提示：对于多时段工作，建议先用`/show_schedule`查看排班，再根据实际时段设置提醒规则。*
