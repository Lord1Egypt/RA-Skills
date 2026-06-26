---
name: QClaw任务结果查询
description: |
  通过 QClaw 查询 WorkBuddy 任务执行结果。当用户想要：
  - 查看任务是否完成
  - 获取任务执行结果
  - 查任务状态
  - 询问"刚才那个任务怎么样了"
  - "结果出来了吗"
  - 想知道 WorkBuddy 执行了什么
  触发词：任务结果、查结果、看结果、任务完成了吗、结果出来了吗、工作做完了吗、WorkBuddy结果、任务状态
version: 1.0.0
---

# QClaw → WorkBuddy 结果查询

当用户询问任务结果、任务状态时，查询队列并返回结果。

## 核心逻辑

**先列出所有已完成的任务，再获取结果。**

```bash
# 1. 列出所有已完成/有结果的任务
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list --status done

# 2. 获取指定任务ID的详细结果
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py result <task_id>
```

## 使用流程

### 流程 1：用户说"结果出来了吗" → 主动检查

```bash
# 检查是否有已完成的任务（未查询过的）
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list --status done
```

- **有结果** → 拉取最新一个 done 任务的结果，格式化展示给用户
- **没有 done 任务** → 检查是否有 pending/processing 任务，告知当前状态
- **全部为空** → 告知用户还没有已提交的任务

### 流程 2：用户给了任务ID → 直接查

```bash
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py result <task_id>
```

### 流程 3：用户问"之前提交了什么任务" → 历史列表

```bash
# 查看所有任务（不限状态）
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list
```

## 结果展示模板

### 有结果时
```
✅ WorkBuddy 任务已完成

🆔 任务编号: <task_id>
📋 任务描述: <description>
📝 执行结果: <summary>
<details>: <details>
📁 附件: <file_path or "无">

<完整的 result 输出>
```

### 任务进行中时
```
⏳ 任务正在处理中

🆔 任务编号: <task_id>
📋 任务描述: <description>
🔄 当前状态: <status>
📍 位置: WorkBuddy 执行队列

请稍后再来查询结果，预计还需要 5-15 分钟。
```

### 没有任务时
```
📭 暂无已完成的 WorkBuddy 任务

目前队列中没有已执行完毕的任务。
如需提交新任务，请说"帮我把 XXX 交给 WorkBuddy 执行"。
```

## 注意事项

- `result <task_id>` 只对 `status=done` 的任务有效
- 如果任务状态是 `error`，展示错误信息而非结果
- 优先展示最新完成的任务（队列中最后一条 done 记录）
- 不要主动轮询，每用户查询一次就查一次
