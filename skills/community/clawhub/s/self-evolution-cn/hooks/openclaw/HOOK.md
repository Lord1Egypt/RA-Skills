---
name: self-evolution-cn
description: "自动识别并记录学习、错误和功能需求，支持多 agent 统计和自动提升"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap","message:received","tool:after"]}}
---

# Self-Evolution-CN Hook

自动识别并记录学习、错误和功能需求。

## 功能

### 1. 自动识别触发条件

**用户纠正（自动记录到 LEARNINGS.md）：**
- 检测到关键词："不对"、"错了"、"错误"、"不是这样"、"应该是"、"你为什么"、"我记得是"、"提醒你"、"更正一下"
- 检测到纠正性表达："No, that's wrong"、"Actually"、"should be"
- **动作**：自动记录到 LEARNINGS.md，类别为 correction
- **Pattern-Key**：user.correction
- **Area**：行为准则

**命令失败（自动记录到 ERRORS.md）：**
- 检测到工具执行失败（非零退出码）
- 检测到错误信息：error、Error、ERROR、failed、FAILED
- 检测到系统级错误：command not found、No such file、Permission denied、fatal
- **动作**：自动记录到 ERRORS.md

**知识缺口（自动记录到 LEARNINGS.md）：**
- 检测到用户提供新信息
- 检测到关键词："我不知道"、"查不到"、"不知道"、"无法找到"、"找不到"、"记下来"、"记住"、"你记好"、"别忘了"、"不清楚"、"不确定"
- 检测到英文表达："I don't know"、"can't find"、"not sure"
- **动作**：自动记录到 LEARNINGS.md，类别为 knowledge_gap
- **Pattern-Key**：knowledge.gap
- **Area**：工作流

**发现更好的方法（自动记录到 LEARNINGS.md）：**
- 检测到关键词："更好的方法"、"更简单"、"优化"、"改进"、"更好的"
- 检测到英文表达："better way"、"simpler"、"optimize"、"improve"
- **动作**：自动记录到 LEARNINGS.md，类别为 best_practice
- **Pattern-Key**：better.method
- **Area**：工作流改进

### 2. 自动记录格式

**学习记录：**
```markdown
## [LRN-YYYYMMDD-XXX] 类别

- Agent: <agent_id>
- Logged: 当前时间
- Priority: medium
- Status: pending
- Area: 根据上下文判断

### 摘要
一句话描述

### 详情
完整上下文

### 建议行动
具体修复或改进

### 元数据
- Source: conversation
- Pattern-Key: 自动生成
- Recurrence-Count: 1
```

**错误记录：**
```markdown
## [ERR-YYYYMMDD-XXX] 技能或命令名称

- Agent: <agent_id>
- Logged: 当前时间
- Priority: high
- Status: pending
- Area: 根据上下文判断

### 摘要
简要描述

### 错误
```
错误信息
```

### 上下文
- 尝试的命令/操作
- 使用的输入或参数

### 建议修复
如果可识别，如何解决

### 元数据
- Reproducible: yes
```

### 3. 记录后回复

记录完成后，会自动回复：
- "已记录到 LEARNINGS.md"（学习记录）
- "已记录到 ERRORS.md"（错误记录）
- "已记录到 FEATURE_REQUESTS.md"（功能需求记录）

### 4. 提升规则

**多 Agent 统计：**
- 所有 agent 共享学习目录
- 按 `Pattern-Key` 累计 `Recurrence-Count`
- 累计次数 >= 3 时自动提升到 SOUL.md

**提升格式：**
```markdown
### 一句话总结
一句话建议行动

---
```

**提升位置：**
- 根据 `Area` 字段自动映射到对应的二级标题
- 如果二级标题不存在，自动创建

**Area 映射规则：**
- `行为准则`|`行为模式`|`交互规范` → `## Core Truths（核心准则）`
- `工作流`|`工作流改进`|`任务分发` → `## 工作流程`
- `工具`|`配置`|`工具问题` → `## 工具使用`
- `边界`|`安全` → `## Boundaries（边界）`
- `风格`|`气质` → `## Vibe（风格气质）`
- `连续性`|`偏好` → `## Continuity（连续性）`
- 其他 → `## 其他`

## 事件结构

Hook 监听以下 OpenClaw 事件：

| 事件 | 读取字段 | 说明 |
|------|----------|------|
| `message:received` | `event.context.content` | 用户发送的消息内容 |
| `tool:after` | `event.context.output` | 工具执行输出 |
| `agent:bootstrap` | `event.context.bootstrapFiles` | 注入引导文件 |

**兼容性：** Hook 同时支持 `event.message` 和 `event.toolOutput` 旧格式，确保向后兼容。

## 配置

无需配置。使用以下命令启用：

```bash
openclaw hooks enable self-evolution-cn
```

## 多 Agent 支持

此 hook 支持多 agent 共享学习目录。所有 agent 的学习记录将存储在共享目录中，并按 `Pattern-Key` 累计 `Recurrence-Count`。

### 学习目录检测逻辑

Hook 会自动检测工作区的 `.learnings` 文件夹：

1. **如果工作区有 `.learnings` 软连接指向共享目录** → 使用共享目录
   - 示例：`/root/.openclaw/workspace-agent1/.learnings -> /root/.openclaw/shared-learning`
   - 学习目录：`/root/.openclaw/shared-learning`

2. **如果工作区有独立的 `.learnings` 文件夹** → 使用工作区的 `.learnings`
   - 示例：`/root/.openclaw/workspace-agent2/.learnings/`（独立文件夹）
   - 学习目录：`/root/.openclaw/workspace-agent2/.learnings`

3. **如果工作区没有 `.learnings`** → 使用共享目录
   - 学习目录：`/root/.openclaw/shared-learning`

## 环境变量

### SHARED_LEARNING_DIR

指定共享学习目录路径。

```bash
export SHARED_LEARNING_DIR="/root/.openclaw/shared-learning"
```

### AGENT_ID

指定当前 agent ID。

```bash
export AGENT_ID="main"
```

## 执行状态和日志

### 状态文件

**位置**：`$SHARED_LEARNING_DIR/heartbeat-state.json`

### 日志文件

**位置**：`$SHARED_LEARNING_DIR/logs/heartbeat-daily.log`

### 查看 Agent 状态

**查看所有 agent 状态：**
```bash
cat $SHARED_LEARNING_DIR/heartbeat-state.json
```

**查看特定 agent 状态：**
```bash
jq '.agents.agent1' $SHARED_LEARNING_DIR/heartbeat-state.json
```

**查看特定 agent 日志：**
```bash
grep 'Processing agent: agent1' $SHARED_LEARNING_DIR/logs/heartbeat-daily.log
```
