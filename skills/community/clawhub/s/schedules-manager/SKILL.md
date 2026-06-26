---
name: schedule-manager
description: 管理用户日程与任务安排。用于以下场景：(1) 用户要求"安排日程""规划任务""帮我排日程"；(2) 用户要求"新增日程""添加任务""记住这个日程"；(3) 用户要求"查看日程""今日安排""明天任务""本周日程""下周日程""本月日程""下月日程"；(4) 用户要求"修改日程""改一下DDL""调整优先级"；(5) 用户要求"完成了""删除日程"。
---

# 日程管理

通过脚本管理用户日程。日程数据存储在工作目录下的 `schedules/schedule.csv`。

## 优先级分类

| 优先级 | 含义 | 判断条件 |
|--------|------|---------|
| P0 | 重要且紧急 | 有近期DDL（48h内）且影响重大 |
| P1 | 紧急不重要 | 有时间压力但可委托或影响较小 |
| P2 | 重要不紧急 | 对长期目标有价值但无紧迫DDL |
| P3 | 不重要不紧急 | 无时间压力且影响极小 |

用户未指定优先级时，根据描述自动判断并向用户确认。有DDL且在48h内视为"紧急"，无DDL默认归入P2。

## 脚本调用

所有日程操作通过 Bash 执行。

### 添加日程

```bash
python {baseDir}/scripts/schedule_crud.py add --task "任务名" --deadline "YYYY-MM-DD HH:mm" --priority P0 [--note "备注"]
```

- `--task` 必填，任务描述
- `--deadline` 可选，格式 `YYYY-MM-DD HH:mm` 或 `YYYY-MM-DD`
- `--priority` 必填，P0/P1/P2/P3
- `--note` 可选，备注信息

### 查看日程

```bash
python {baseDir}/scripts/schedule_crud.py list [--today] [--tomorrow] [--week] [--next-week] [--month] [--next-month] [--priority P0]
```

### 更新日程

```bash
python {baseDir}/scripts/schedule_crud.py update --id 1 [--task "..."] [--deadline "..."] [--priority P0] [--reminder Y] [--note "..."]
```

- `--id` 必填，任务ID
- 其余字段可选，按需传入

### 删除日程

```bash
python {baseDir}/scripts/schedule_crud.py delete --id 1
```

## 任务路由

根据用户意图路由到对应分支：

| 用户意图 | 触发词示例 | 分支 | 后续 |
|---------|-----------|------|------|
| 新增日程 | 帮我安排日程、规划任务、新增日程、添加任务、记住这个 | 新增日程 | → 设置提醒 |
| 查看日程 | 查看日程、今日安排、明天任务、本周日程、下周日程、本月日程、下月日程 | 查看日程 | （无） |
| 修改日程 | 修改日程、改一下DDL、调整优先级 | 修改日程 | → 设置提醒 |
| 删除日程 | 完成了XX、删除XX | 删除日程 | （无） |
| 设置提醒 | 帮我设置提醒、提醒我XX | 设置提醒 | — |

## 任务分支

### 新增日程

1. 收集任务信息（名称、DDL、备注）；若用户提供多条任务，一并收集
2. 按优先级分类，向用户确认
3. 逐条执行 `python {baseDir}/scripts/schedule_crud.py add --task "..." --priority P0 [--deadline "..."] [--note "..."]`
4. 执行 `python {baseDir}/scripts/schedule_crud.py list` 获取完整日程
5. 将脚本输出直接作为回复内容发送给用户
6. → 进入「设置提醒」

### 查看日程

1. 根据用户要求执行对应命令：
   - 全部：`python {baseDir}/scripts/schedule_crud.py list`
   - 今日：`python {baseDir}/scripts/schedule_crud.py list --today`
   - 明日：`python {baseDir}/scripts/schedule_crud.py list --tomorrow`
   - 本周：`python {baseDir}/scripts/schedule_crud.py list --week`
   - 下周：`python {baseDir}/scripts/schedule_crud.py list --next-week`
   - 本月：`python {baseDir}/scripts/schedule_crud.py list --month`
   - 下月：`python {baseDir}/scripts/schedule_crud.py list --next-month`
2. 将脚本输出直接作为回复内容发送给用户

### 修改日程

1. 先执行 `python {baseDir}/scripts/schedule_crud.py list` 展示当前日程
2. 确认用户要修改的任务 ID 和修改内容（任务名、DDL、优先级、备注）
3. 执行 `python {baseDir}/scripts/schedule_crud.py update --id X [--task "..."] [--deadline "..."] [--priority P0] [--note "..."]`
4. 将脚本输出作为回复
5. → 进入「设置提醒」

### 删除日程

1. 先执行 `python {baseDir}/scripts/schedule_crud.py list` 展示当前日程
2. 确认用户要删除的任务 ID
3. 执行 `python {baseDir}/scripts/schedule_crud.py delete --id X`
4. 将脚本输出作为回复

## 设置提醒（子流程）

在「新增日程」「修改日程」完成后自动触发，也可由用户直接请求。

1. 问用户：「是否需要为任务设置定时提醒？」
2. 用户拒绝 → 结束
3. 用户确认 → 确认提醒时间（默认DDL前30分钟）
4. 加载 `cron-mastery` skill，用 agentTurn + announce + isolated 模式创建提醒：
   - 消息格式：`DELIVER THIS EXACT MESSAGE TO THE USER WITHOUT MODIFICATION OR COMMENTARY:\n\n日程提醒: [任务名] 将在 [剩余时间] 后截止！`
5. 执行 `python {baseDir}/scripts/schedule_crud.py update --id X --reminder Y` 更新提醒状态
6. 回复：「已为「任务名」设置 [时间] 的定时提醒。」

## 回复纪律

- 脚本输出即回复内容，直接发送，不重新格式化
- 安排/新增/修改后，只追加一句：「是否需要为任务设置定时提醒？」
- 回复格式模板严格遵循 `{baseDir}/references/templates.md`
