---
name: team-tasks
summary: 面向任意团队的任务协作技能，支持创建、提醒、查询、统计与导出
description: |
  Team-Tasks 是一个通用的团队任务协调技能，通过 JSON 文件存储任务数据，
  支持自然语言创建任务、多频次提醒、逾期升级、统计分析和多格式导出。
  设计哲学：提醒的是事，不是人；记录的是过程，不是权力关系。
tags: [task, team, collaboration, reminder, productivity]
---

# Team-Tasks

## 适用范围

用于任意团队的共享任务管理场景。这个 skill 应保持平台无关、组织无关，不应硬编码具体人名、部门、群组 ID、节假日维护人或单一聊天平台字段。

## 设计哲学

- 提醒的是事，不是人
- 记录的是过程，不是权力关系
- 鼓励成员自驱记录和更新任务
- 允许团队透明查看进展

## 数据目录

运行时数据默认放在 `workspace/data/team-tasks/`：

```text
workspace/data/team-tasks/
├── team-tasks.json
├── team-tasks.json.bak
└── team-tasks-archive-YYYY-MM.json
```

## 写入保护

所有写操作强制执行以下流程：

```text
1. 读取 team-tasks.json 到内存
2. 修改内存数据
3. 写入 team-tasks.json.bak 作为备份
4. 写入 team-tasks.json 作为正式结果
5. 成功后删除 .bak
6. 失败时保留 .bak 并报告恢复建议
```

如果启动时发现 `.bak` 仍存在，优先从备份恢复，并在当前执行上下文中报告异常，不要假定固定通知对象。

## 数据模型

顶层结构：

```json
{
  "version": "1.0",
  "updatedAt": "2026-03-23T10:00:00+08:00",
  "tasks": []
}
```

任务对象：

```json
{
  "id": "T-260323-003",
  "title": "完成资产盘点报告",
  "description": "详细描述，保留关键上下文",
  "priority": "high",
  "isBlocking": false,
  "tags": ["资产", "盘点"],
  "status": "pending",

  "assignee": "Alex",
  "assigneeId": "user-123",
  "creator": "Robin",
  "creatorId": "user-456",

  "createdAt": "2026-03-23T10:00:00+08:00",
  "dueDate": "2026-04-07",
  "dueTime": "18:00",
  "completedAt": null,
  "cancelledAt": null,

  "sourceType": "direct",
  "sourceId": "conversation-001",
  "notifyTargetId": null,

  "lastReminded": null,
  "lastRemindedSlot": null,
  "reminderCount": 0,
  "snoozedUntil": null,
  "lastProgressAt": null,

  "comments": [],
  "history": []
}
```

字段约定：

| 字段 | 说明 |
|------|------|
| `id` | `T-YYMMDD-NNN` |
| `priority` | 任务本身的重要性，建议 `critical / high / medium / low` |
| `isBlocking` | 是否阻塞其他任务、流程或他人工作 |
| `status` | `pending / done / cancelled` |
| `dueDate` | `YYYY-MM-DD / "none" / null` |
| `lastProgressAt` | 最近一次有效进展更新时间 |
| `notifyTargetId` | 手动覆盖通知目标；平台无关 |
| `sourceType` | 如 `direct / group / api`，按接入平台映射 |
| `comments` | `{ at, from, content }[]` |
| `history` | `{ at, action, by, detail }[]` |

不要在通用 skill 中写死 `Slack`、`飞书`、`钉钉` 等平台字段名。若接入层已有特定平台元数据，应在适配层做映射，再写入通用字段。

`urgency` 和 `attentionLevel` 是运行时派生值，不建议直接写死在存储层，以免随时间推移变旧。

## 任务 ID

格式：`T-YYMMDD-NNN`

生成逻辑：

```text
1. 读取 team-tasks.json 和当月归档文件
2. 找出所有同一天前缀的任务 ID
3. 取最大序号
4. 新任务使用 MAX + 1
5. 当天无历史任务则从 001 开始
```

生成 ID 时必须扫描归档文件，避免月度归档后序号碰撞。

## 触发规则

当用户消息包含下列意图时，可启动任务管理：

`任务` / `todo` / `待办` / `task` / `记下` / `提醒我` / `帮我跟进`

也可以直接识别自然语言任务表达，例如“下周三前完成巡检报告”。

## 重要性、紧急度与关注度

不要把“离截止时间近”直接等同于“优先级高”。通用 skill 应拆成三层：

- `priority`：任务本身的重要性
- `urgency`：时间压力
- `attentionLevel`：提醒引擎使用的综合关注度

### priority

`priority` 只表达业务重要性，不随时间自动变化。

判断链：

```text
手动指定 > 关键词推断 > 默认 medium
```

建议枚举：

| 值 | 含义 |
|----|------|
| `critical` | 关键任务，失误成本很高 |
| `high` | 重要任务，需要优先保障 |
| `medium` | 常规任务 |
| `low` | 低重要性任务 |

关键词推断：

| 识别词 | priority |
|--------|----------|
| 核心、关键、必须完成、P0、阻塞发布 | `critical` |
| 重要、优先、尽快处理 | `high` |
| 不急、有空再做、低优先 | `low` |
| 无特殊词 | `medium` |

### urgency

`urgency` 由截止时间动态计算，不覆盖 `priority`。

建议枚举：

| 条件 | urgency |
|------|---------|
| 已逾期 | `overdue` |
| 今天到期或剩余 ≤ 24h | `today` |
| 剩余 ≤ 72h | `soon` |
| 剩余 > 72h | `normal` |
| 无截止时间 | `none` |

### attentionLevel

`attentionLevel` 用于决定提醒频率，建议按以下因素综合计算：

```text
priority
+ urgency
+ isBlocking
+ 最近是否长期无进展
- snooze
```

推荐规则：

1. `urgency = overdue` 时，至少为 `high`
2. `urgency = today` 且 `priority` 为 `high/critical` 时，升为 `critical`
3. `isBlocking = true` 时，上调一档，最高到 `critical`
4. 连续多个工作日无进展时，上调一档
5. `snoozedUntil` 未过期时，不发送提醒

创建确认时应同时展示 `priority`、`urgency` 和主要推断依据，允许用户立刻纠正 `priority`。

## 创建任务

命令式示例：

```text
task add "完成资产盘点报告" --assign Alex --due 2026-04-01 --priority high --blocking false --tags 资产,盘点
```

自然语言也应支持直接创建。

标准流程：

1. 读取 `data/team-tasks/team-tasks.json`
2. 生成新任务 ID
3. 从上下文提取 `sourceType` 和 `sourceId`
4. 写入任务
5. 回复确认
6. 若负责人不是创建人，则发送分配通知

创建确认建议包含：

- `priority`：业务重要性
- `urgency`：当前时间压力
- `attentionLevel`：当前提醒强度

任务记录规则：

| 字段 | 要求 |
|------|------|
| `title` | 动词开头，一句话概括核心任务 |
| `description` | 保留关键细节，结构化整理 |

## 负责人识别

优先级：

1. 直接识别显式用户引用
2. 识别名字或别名并通过团队成员映射解析
3. 从自然语言中的“让 XX 做”或“由 XX 负责”中提取负责人

不要把消息接收者默认当成负责人。负责人必须来自明确语义或可靠映射。

## 批量拆分

唯一拆分条件：负责人不同。

| 场景 | 处理 |
|------|------|
| 同一负责人下的多个子步骤 | 不拆分 |
| 同一事项的多个执行步骤 | 不拆分 |
| 多个负责人共同出现 | 视为多任务，必要时确认 |

如果是否拆分存在歧义，应主动确认。

## 状态操作

| 指令 | 动作 |
|------|------|
| `task done T-xxx` | 标记完成 |
| `task cancel T-xxx` | 标记取消 |
| `task reopen T-xxx` | 恢复为 pending |
| `task snooze T-xxx 2h` | 暂停提醒 |

默认权限建议：

- 完成任务：所有成员可操作
- 取消任务：负责人、创建人或团队管理员可操作
- 转交任务：负责人、创建人或团队管理员可操作

团队管理员必须由外部配置或运行上下文注入，不要在 skill 中写死具体人员。

`snoozedUntil` 上限：

```text
min(now + 指定时长, now + 7 天, dueDate - 1 天)
```

归档任务重开时，应自动从归档文件中检索并移回活动文件。

## 转交任务

示例：

```text
task reassign T-260323-003 --to Jordan
```

流程：

1. 更新 `assignee` 和 `assigneeId`
2. 写入 `history`
3. 通知新负责人、原负责人和创建人
4. 去重合并相同接收者

## 查询与搜索

支持：

- `task list`
- `task list --all`
- `task list --assign <name>`
- `task list --priority high`
- `task list --urgency overdue`
- `task list --blocking true`
- `task list --tags <tag>`
- `task list --status done`
- `task overdue`
- `task search "关键词"`
- `task view T-xxx`

默认 `task list` 返回当前用户相关的 pending 任务。

## 修改与进展

支持：

```text
task update T-xxx --due 2026-04-10
task update T-xxx --priority high
task update T-xxx --blocking true
task comment T-xxx "已联系供应商，预计下周到货"
```

更新后把变更写入 `history`，评论追加到 `comments`，并通知相关成员。

## 统计与导出

支持：

- `task stats`
- `task stats --all`
- `task export --format json|csv|txt`
- `task export --filter pending`
- `task export --include-archive`
- `task export --month YYYY-MM`

CSV 默认列顺序：

`id, title, priority, urgency, attentionLevel, isBlocking, status, assignee, dueDate, dueTime, tags, createdAt, completedAt`

## 提醒引擎

提醒频率由 `attentionLevel` 主导，而不是由 `priority` 单独决定。

建议模式：

| attentionLevel | 适用任务 | 触发时间 |
|----------------|---------|---------|
| `critical` | 已逾期，或今天到期且高重要性/阻塞 | 每个工作日 10:00 / 14:00 / 18:00 |
| `high` | 临近到期，或高重要性阻塞任务 | 每个工作日 10:00 / 18:00 |
| `medium` | 常规任务 | 每个工作日 09:00 |
| `low` | 低重要性且不紧急 | 每 2 个工作日 09:00 |

分类规则：

```text
1. snoozedUntil 未过期则跳过
2. 先计算 urgency
3. 再结合 priority、isBlocking、lastProgressAt 计算 attentionLevel
4. 按 attentionLevel 选择提醒频率
5. 无截止日期任务默认不进入高频提醒，除非它阻塞其他工作
```

每个时间槽用 `lastRemindedSlot` 防重复。

所有提醒可在触发后增加 1 到 15 分钟随机延迟，避免集中发送。

## 工作日与节假日

是否跳过提醒、如何识别节假日，不应在通用 skill 中写死某个国家或地区的法定日历。

要求：

- 工作日和节假日规则来自外部配置
- 若没有节假日配置，则至少按本地周一到周五执行
- 若团队所在地区不同，由接入方提供地区化日历

## 通知路由

通知位置优先级：

```text
1. notifyTargetId 显式指定
2. 原始群组会话
3. 原始私聊会话
4. 团队默认通知通道（若外部配置提供）
```

不要在 skill 中硬编码固定群组 ID。

## 消息模板

所有模板保持平台中性。使用抽象占位符而不是具体用户 ID。

分配通知示例：

```text
[待处理任务]
{assignee}，你有一项待处理工作：

[{id}] {title}
截止：{due}
重要性：{priority}
紧急度：{urgency}
```

提醒示例：

```text
[任务提醒]
[{id}] {title}
截止：{due}
重要性：{priority}
紧急度：{urgency}
关注度：{attentionLevel}
剩余时间：{remaining}
最新进展：{latestComment}
```

变更通知示例：

```text
[任务变更]
[{id}] {title}
变更项：{field}
变更前：{before}
变更后：{after}
```

逾期提醒示例：

```text
[逾期提醒]
[{id}] {title} 已逾期 {overdueDays} 天。
```

## 变更通知规则

| 变更类型 | 通知对象 |
|---------|---------|
| 修改截止时间 | 创建人 + 负责人，排除操作人 |
| 修改优先级 | 创建人 + 负责人，排除操作人 |
| 修改标题或描述 | 创建人 + 负责人，排除操作人 |
| 完成任务 | 创建人，排除操作人 |
| 取消任务 | 创建人 + 负责人，排除操作人 |
| 转交任务 | 新负责人 + 原负责人 + 创建人，排除操作人 |
| 添加评论 | 创建人 + 负责人，排除操作人 |

同一人身兼多个角色时只发一条。

## 权限边界

通用默认值：

| 操作 | 建议权限 |
|------|---------|
| 创建任务 | 所有成员 |
| 查看任务 | 团队成员 |
| 完成任务 | 所有成员 |
| 取消任务 | 负责人 / 创建人 / 团队管理员 |
| 修改任务 | 团队成员，必要时可由接入方收紧 |
| 转交任务 | 负责人 / 创建人 / 团队管理员 |
| 评论任务 | 所有成员 |
| 导出任务 | 团队成员 |

如果团队有更严格权限模型，应由接入层覆盖。

## 归档

- 频率：每月 1 日执行
- 条件：`done` 或 `cancelled` 且状态变化时间在上月及以前
- 目标文件：`team-tasks-archive-YYYY-MM.json`
- 归档也走 `.bak` 保护流程

## 接入要求

接入任意聊天平台或自动化系统时，应提供以下能力：

- 当前操作者身份
- 团队成员映射或目录服务
- 消息来源会话 ID
- 可选的默认通知通道
- 可选的地区化工作日日历

如果接入的是特定平台，应在适配层完成平台字段到通用字段的转换，不要把平台细节写进通用 skill。

## 注意事项

1. 记录任务意味着立即落盘，不是仅保留在上下文里
2. 生成 ID 时必须扫描归档文件
3. 提醒执行后不要发送内部执行日志
4. 任何组织特定配置都应外置，不要写进 skill 正文
5. 若后续需要平台专版，应在此通用 skill 之上再做派生版本
