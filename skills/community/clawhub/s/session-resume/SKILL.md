---
name: session-resume
description: "会话恢复。Gateway 重启或 session 中断后，自动恢复任务上下文并向用户汇报进度。通过 .task-state.json 持久化任务状态，确保长时间任务不会因断线而丢失。触发词：恢复任务、resume、任务状态、断线恢复、session resume。也可在每次 session 启动时自动检测。"
---

# Session Resume — 会话恢复

Gateway 重启、网络断线、session 压缩后，自动恢复任务上下文。

## 什么时候用

- 每次新 session 启动时（自动检测）
- 用户说"恢复任务"、"resume"、"断线恢复"
- Gateway 重启后的第一次对话
- 长时间任务中途被中断

## 核心理念

AI Agent 执行长时间任务时最怕断线——Gateway 重启、session 被压缩、网络中断，
任务进度全部丢失，用户不得不重新描述需求。

Session Resume 通过**任务状态持久化**解决这个问题：
- 执行任务时定期保存进度到文件
- 新 session 启动时自动读取并恢复
- 向用户汇报：之前在做什么、做到哪了、还剩什么

## 执行流程

### Phase 1 — 检测（Detect）

新 session 启动时检查：

1. 读取 `~/.openclaw/workspace-main/.task-state.json`
2. 如果文件存在且内容有效，说明有未完成的任务
3. 如果文件不存在或为空，说明没有待恢复的任务（跳过后续步骤）

### Phase 2 — 恢复（Restore）

解析任务状态文件，提取：

- **任务描述**：用户原始请求是什么
- **当前进度**：已完成的步骤
- **未完成项**：还剩哪些步骤
- **关键上下文**：文件路径、配置值、中间结果等
- **中断原因**：如果能判断的话（压缩/重启/超时）

### Phase 3 — 汇报（Report）

向用户发送恢复报告：

```
🔄 任务恢复
━━━━━━━━━

📋 之前的任务：
部署新版本到生产环境

✅ 已完成：
- 代码拉取和构建
- 单元测试通过
- Docker 镜像构建完成

⏳ 待完成：
- 推送镜像到仓库
- 更新 K8s 配置
- 执行滚动更新

💡 是否继续执行？
```

### Phase 4 — 继续或放弃（Resume / Abandon）

- 用户说"继续" → 从断点处继续执行
- 用户说"放弃"或"不用了" → 清理状态文件，开始新任务
- 用户不回应 → 保持状态文件不动，下次再问

## 任务状态文件格式

文件路径：`~/.openclaw/workspace-main/.task-state.json`

```json
{
  "version": 1,
  "taskId": "uuid-here",
  "createdAt": "2026-04-02T10:30:00+08:00",
  "updatedAt": "2026-04-02T11:15:00+08:00",
  "description": "用户的原始任务描述",
  "status": "in_progress",
  "steps": [
    {"name": "步骤1", "status": "done", "result": "简要结果"},
    {"name": "步骤2", "status": "done", "result": "简要结果"},
    {"name": "步骤3", "status": "pending"},
    {"name": "步骤4", "status": "pending"}
  ],
  "context": {
    "key1": "value1",
    "key2": "value2"
  },
  "lastCheckpoint": "步骤2完成后"
}
```

## 使用规范

### 保存任务状态（执行长时间任务时）

在执行多步骤任务时，每完成一个关键步骤后更新状态文件：

1. 任务开始时创建 `.task-state.json`
2. 每完成一个步骤，更新对应 step 的 status 和 result
3. 任务全部完成后删除状态文件

### 自动检测（session 启动时）

建议在 AGENTS.md 的启动序列中加入：

```
5. 检查 .task-state.json 是否存在，如有则执行 session-resume skill 恢复任务
```

## 规则

- **只读取，不猜测**：只恢复文件中明确记录的信息，不猜测未记录的进度
- **先汇报，后执行**：恢复后先告知用户，等用户确认再继续
- **及时更新**：每个关键步骤完成后都要更新状态文件
- **任务完成即清理**：全部完成后删除状态文件，避免下次误恢复
- **不影响正常流程**：没有状态文件时，完全不影响正常的 session 启动

## 与其他 Skill 的配合

- **Smart Compact**：压缩前先保存任务状态，压缩后自动恢复
- **Memory-Dream**：任务状态是临时的（完成即删），长期信息由 Dream 整合到 MEMORY.md
