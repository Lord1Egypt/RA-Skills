# Task Dispatch Skill

任务调度技能，让 Agent 能够自动检查任务看板、派发任务给 subagent 执行、验收结果并更新状态。

---

## 功能特性

| 特性 | 说明 |
|------|------|
| **自动调度** | 定时检查任务看板，派发可执行任务 |
| **连续派发** | 一次触发执行到底，不等待下次 cron |
| **结构化上下文** | 使用模板确保 subagent 收到完整信息 |
| **状态追踪** | 自动更新任务状态（todo → in-progress → review → done） |
| **失败处理** | 记录失败原因，清理无效占用，不静默失败 |

---

## 快速开始

### 1. 安装技能

```bash
# 从 ClawHub 安装
clawhub install task-dispatch

# 或手动安装
cp task-dispatch.skill /path/to/agent/skills/
cd /path/to/agent/skills/
unzip task-dispatch.skill
```

### 2. 配置环境

```bash
# 设置任务看板 API 地址
export TASKBOARD_API_URL=http://127.0.0.1:3000

# 设置 API 访问令牌
export TASKBOARD_ACCESS_TOKEN=your-token-here
```

### 3. 部署任务看板

本技能需要任务看板 API 支持，推荐使用 [ClawBoard](https://github.com/your-org/clawboard)：

```bash
git clone <clawboard-repo>
cd ClawBoard
npm install
npm start  # 默认端口 3000
```

### 4. 启用调度

告诉 Agent：
```
"设置每5分钟自动检查任务看板"
```

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    调度循环                                  │
│                                                              │
│  1. 检查可派发任务                                           │
│     ├─ 有 → 继续步骤 2                                       │
│     └─ 无 → 结束本轮 (HEARTBEAT_OK)                         │
│                                                              │
│  2. 填充派发模板，创建 subagent                              │
│                                                              │
│  3. 等待 subagent 完成                                       │
│                                                              │
│  4. 验收交付物                                               │
│     ├─ 成功 → status: review                                 │
│     └─ 失败 → status: failed                                 │
│                                                              │
│  5. 【立即回到步骤 1】，继续下一个任务                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 任务要求

要被自动派发，任务需满足：

| 条件 | 要求 |
|------|------|
| `executionMode` | `"auto"` |
| `status` | `"todo"` 或无人认领的 `"in-progress"` |
| `assignee` | 为空 |
| `claimedBy` | 为空 |
| `dependencies` | 全部已完成 |

### 创建可自动派发的任务

```bash
curl -X POST http://127.0.0.1:3000/api/tasks/projects/{projectId}/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "创建 API 文档",
    "description": "为项目创建 API 说明文档",
    "status": "todo",
    "executionMode": "auto",
    "priority": "P2",
    "deliverables": ["docs/api.md"],
    "acceptanceCriteria": [
      "文件已创建",
      "包含至少 3 个 API 端点说明"
    ]
  }'
```

---

## 技能文件结构

```
task-dispatch/
├── SKILL.md                      # 主指令文件
├── scripts/
│   └── setup_cron.py            # Cron 配置生成脚本
└── references/
    ├── config.md                # 配置参考
    └── dispatch-template.md     # Subagent 派发模板
```

### SKILL.md

核心指令文件，包含：
- Agent 角色定位
- 数据真源定义
- 调度逻辑
- API 调用方式
- 状态转换规则
- 失败处理

### scripts/setup_cron.py

生成 cron 配置：

```bash
python setup_cron.py --interval 600000 --channel feishu --to "chat_id"
```

输出：
```json
{
  "name": "Task Dispatch",
  "schedule": { "kind": "every", "everyMs": 600000 },
  "payload": { "kind": "agentTurn", "message": "执行 task-dispatch 调度检查..." },
  "sessionTarget": "isolated"
}
```

### references/dispatch-template.md

Subagent 派发模板，确保任务上下文完整：

```markdown
# Task Dispatch

## Task Identity
- project: <projectName> (<projectId>)
- task_id: <taskId>
- title: <taskTitle>
- priority: <P0|P1|P2|P3>

## Goal
<一句话目标>

## Hard Constraints
- 只处理当前任务，不修改无关内容
- ...

## Deliverables
- <交付物路径>

## Acceptance Criteria
- <验收标准>

## Output Format (Required)
```completion_signal
task_id: <taskId>
status: done | blocked
summary: <一句话总结>
deliverables: <结果路径>
next_step: <N/A 或阻塞原因>
```
```

---

## 状态流转

```
todo ──────→ in-progress ──────→ review ──────→ done
                │                   │
                ↓                   ↓
              failed              failed
```

| 状态 | 含义 |
|------|------|
| `todo` | 待处理 |
| `in-progress` | 执行中（subagent 正在工作） |
| `review` | 待审核（subagent 完成，等待验收） |
| `done` | 已完成（验收通过） |
| `failed` | 失败（执行出错或被阻塞） |

---

## 配置选项

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TASKBOARD_API_URL` | 任务看板 API 地址 | `http://127.0.0.1:3000` |
| `TASKBOARD_ACCESS_TOKEN` | API 访问令牌 | (必填) |
| `TASK_DISPATCH_INTERVAL_MS` | 调度间隔 | `300000` (5分钟) |

详见 [references/config.md](references/config.md)

---

## API 要求

任务看板 API 需提供以下端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/tasks/projects` | GET | 获取项目列表 |
| `/api/tasks/projects/{projectId}/tasks` | GET | 获取项目任务列表 |
| `/api/tasks/projects/{projectId}/tasks/{taskId}` | PUT | 更新任务状态 |

---

## 使用示例

### 手动触发调度
```
"检查任务看板，派发所有待执行任务"
```

### 设置定时调度
```
"设置每10分钟自动检查任务"
```

### 查看调度状态
```
"查看当前任务调度状态"
```

### 创建测试任务
```
"创建一个测试项目，包含3个自动执行的任务"
```

---

## 与其他系统集成

本技能支持任何兼容 API 的任务看板系统。要适配其他系统：

1. 实现 API 端点（projects, tasks, updateTask）
2. 或修改 `references/config.md` 中的适配器配置

---

## 故障排查

### 任务不被派发

检查任务是否满足条件：
- `executionMode` 是否为 `"auto"`
- `status` 是否为 `"todo"`
- `assignee` 和 `claimedBy` 是否为空
- `dependencies` 是否全部完成

### Subagent 超时

增加超时时间：
```json
{
  "timeoutSeconds": 600
}
```

### API 认证失败

检查 `TASKBOARD_ACCESS_TOKEN` 是否正确：
```bash
curl -H "Authorization: Bearer $TASKBOARD_ACCESS_TOKEN" \
  $TASKBOARD_API_URL/api/tasks/projects
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-25 | 初始版本：自动调度、连续派发、模板派发 |

---

## 许可证

MIT License