# 🔄 Session Resume — 会话恢复 Skill

> 断线不怕，重启不慌。让你的 AI Agent 拥有"断点续传"能力。

---

## 中文说明

### 这是什么？

OpenClaw Agent 执行长时间任务时最怕的事：

- 🔌 **Gateway 重启**：任务进度全部丢失
- 📦 **Session 被压缩**：上下文被浓缩，细节丢失
- 🌐 **网络中断**：对话断开，无法继续
- 😵 **用户忘了**：第二天回来不记得昨天在干什么

**Session Resume 就像游戏的"存档/读档"功能** —— Agent 执行任务时定期保存进度，断线后自动恢复，告诉你"之前在干什么、做到哪了、还剩什么"。

### 安装

**通过 ClawHub 安装（推荐）：**

```bash
clawhub install session-resume
```

**从 GitHub 克隆：**

```bash
git clone https://github.com/wavmson/openclaw-skill-session-resume.git \
  ~/.openclaw/skills/session-resume
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 工作原理

#### 保存（执行任务时）

Agent 执行多步骤任务时，每完成一个关键步骤自动保存进度到 `.task-state.json`：

```
步骤1 ✅ → 保存 → 步骤2 ✅ → 保存 → 步骤3 ⏳ → [断线]
```

#### 恢复（新 session 启动时）

```
新 session → 检测到 .task-state.json → 解析进度 → 汇报用户 → 等待确认 → 继续执行
```

### 四阶段流程

| 阶段 | 名称 | 说明 |
|------|------|------|
| 1️⃣ | 检测 | 检查 `.task-state.json` 是否存在 |
| 2️⃣ | 恢复 | 解析任务描述、已完成步骤、待完成项 |
| 3️⃣ | 汇报 | 向用户发送恢复报告 |
| 4️⃣ | 继续 | 用户确认后从断点继续执行 |

### 恢复报告示例

```
🔄 任务恢复
━━━━━━━━━

📋 之前的任务：
部署新版本到生产环境

✅ 已完成（3/6）：
- 代码拉取和构建
- 单元测试通过
- Docker 镜像构建完成

⏳ 待完成（3/6）：
- 推送镜像到仓库
- 更新配置
- 执行滚动更新

⏱️ 中断时间：2 小时前
💡 是否继续执行？
```

### 任务状态文件

位置：`~/.openclaw/workspace-main/.task-state.json`

包含字段：
- **taskId**：任务唯一标识
- **description**：用户原始请求
- **steps**：步骤列表及完成状态
- **context**：关键中间数据
- **lastCheckpoint**：最后保存点

任务完成后自动清理此文件。

### 设计原则

| 原则 | 说明 |
|------|------|
| 📖 只读不猜 | 只恢复文件中明确记录的信息，不猜测进度 |
| 🗣️ 先报后做 | 恢复后先告知用户，等确认再继续 |
| 💾 及时保存 | 每个关键步骤完成后都更新状态文件 |
| 🧹 完成即清 | 任务全部完成后删除状态文件 |
| 🔇 无感启动 | 没有待恢复任务时，完全不影响正常流程 |

### 与其他 Skill 搭配

Session Resume 是记忆保护链的第三环：

| Skill | 职责 | 保护对象 |
|-------|------|----------|
| **Smart Compact** | 压缩前抢救信息 | 对话上下文中的细节 |
| **Session Resume** | 断线后恢复任务 | 多步骤任务的执行进度 |
| **Memory-Dream** | 定期整合日记 | 长期记忆的准确性 |

三者形成完整的**记忆保护链**：

```
对话中 ──→ Smart Compact 保护细节
                    ↓
断线时 ──→ Session Resume 保存进度
                    ↓
凌晨时 ──→ Memory-Dream 整合记忆
```

### 常见问题

**Q: 每次 session 启动都会检测吗？**
A: 是的，但如果没有 `.task-state.json` 文件，检测瞬间完成，不影响启动速度。

**Q: 什么样的任务需要保存状态？**
A: 超过 3 个步骤的多步骤任务建议保存。简单的问答不需要。

**Q: 状态文件会越来越大吗？**
A: 不会。任务完成后自动删除，同一时间只保存一个活跃任务。

**Q: 能同时恢复多个任务吗？**
A: 当前版本支持一个活跃任务。未来版本可能支持任务队列。

---

## English

### The Problem

Long-running agent tasks are fragile:

- 🔌 **Gateway restarts** wipe all task progress
- 📦 **Session compaction** loses step-by-step context
- 🌐 **Network disconnects** break the conversation
- 😵 **User forgets** what was happening yesterday

### The Solution

Session Resume adds "save/load" functionality to your agent — like game checkpoints. The agent periodically saves task progress to a file, and automatically restores it when a new session starts.

```
Task running → save checkpoint → [disconnect] → new session → detect checkpoint → restore → report → continue
```

### Install

**Option A (recommended): Via ClawHub**

```bash
clawhub install session-resume
```

**Option B: Clone from GitHub**

```bash
git clone https://github.com/wavmson/openclaw-skill-session-resume.git \
  ~/.openclaw/skills/session-resume
```

Then restart Gateway:

```bash
openclaw gateway restart
```

### The 4 Phases

| Phase | Name | Description |
|-------|------|-------------|
| 1️⃣ | Detect | Check if `.task-state.json` exists |
| 2️⃣ | Restore | Parse task description, completed steps, pending items |
| 3️⃣ | Report | Send recovery report to user |
| 4️⃣ | Resume | Continue from checkpoint after user confirms |

### Recovery Report Example

```
🔄 Task Recovery
━━━━━━━━━━━━━━

📋 Previous task:
Deploy new version to production

✅ Completed (3/6):
- Code pull and build
- Unit tests passed
- Container image built

⏳ Remaining (3/6):
- Push image to registry
- Update configuration
- Execute rolling update

⏱️ Interrupted: 2 hours ago
💡 Continue execution?
```

### Design Principles

| Principle | Description |
|-----------|-------------|
| 📖 Read, don't guess | Only restore explicitly saved information |
| 🗣️ Report first | Always inform user before resuming |
| 💾 Save often | Update state file after each key step |
| 🧹 Clean on complete | Delete state file when task finishes |
| 🔇 Silent when idle | Zero overhead when no task to restore |

### Works with Other Skills

| Skill | Role | Protects |
|-------|------|----------|
| **Smart Compact** | Pre-compaction rescue | Conversation details |
| **Session Resume** | Post-disconnect recovery | Multi-step task progress |
| **Memory-Dream** | Periodic consolidation | Long-term memory accuracy |

### FAQ

**Q: Does it check on every session start?**
A: Yes, but detection is instant when no state file exists — zero overhead.

**Q: What tasks should save state?**
A: Multi-step tasks (3+ steps). Simple Q&A doesn't need it.

**Q: Will the state file grow large?**
A: No. It's deleted on task completion. Only one active task at a time.

### Notes

- Works with any model (no model-specific features)
- State file is JSON, human-readable for debugging
- Follows the same workspace layout as standard OpenClaw

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) (any version with Skill support)
- Standard workspace with `~/.openclaw/workspace-main/`

## License

MIT

## Author

[@wavmson](https://github.com/wavmson)
