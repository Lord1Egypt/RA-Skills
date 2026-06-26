# 🐝 Swarm Coord — 多 Agent 协作 Skill

> 一个人干太慢？拆成小任务，多个 Agent 同时干，CEO 统筹汇总。

---

## 中文说明

### 这是什么？

你有一个 CEO Agent，还有 coding、secretary、HR 等下属 Agent。但平时都是 CEO 一个人扛所有事。

Swarm Coord 让 CEO 变成真正的**团队领导**：
- 📋 **分析任务**，识别可并行的部分
- 👥 **分配给合适的 Agent**（coding 写代码、secretary 处理文档……）
- ⏱️ **并行执行**，不用排队等
- 📊 **自动汇总**，整合所有结果

### 安装

**通过 ClawHub 安装（推荐）：**

```bash
clawhub install swarm-coord
```

**从 GitHub 克隆：**

```bash
git clone https://github.com/wavmson/openclaw-skill-swarm-coord.git \
  ~/.openclaw/skills/swarm-coord
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 使用方式

直接给 Agent 下达复合型任务即可自动触发：

> "整理这周所有会议纪要 + 更新项目文档 + 发周报"

或主动说触发词：

| 触发词 | 说明 |
|--------|------|
| `协作` | 中文触发 |
| `分工` | 中文触发 |
| `团队任务` | 中文触发 |
| `swarm` | 英文触发 |
| `team work` | 英文触发 |

### 四阶段流程

| 阶段 | 名称 | 说明 |
|------|------|------|
| 1️⃣ | 拆分 | 分析任务，识别可并行的子任务 |
| 2️⃣ | 分发 | 为每个子任务 spawn 独立 Agent session |
| 3️⃣ | 监控 | 跟踪进度，处理失败，转发中间结果 |
| 4️⃣ | 汇总 | 收集所有结果，整合成统一报告 |

### 拆分示例

**用户请求：** "帮我处理这三件事：1) 把昨天会议纪要整理成文档 2) 更新 GitHub README 3) 给团队发个通知"

**Swarm 拆分：**

```
📋 任务拆分方案
━━━━━━━━━━━━

子任务 1 → 🤖 Secretary
  整理会议纪要，写入飞书文档

子任务 2 → 💻 Coding
  更新 GitHub README，commit & push

子任务 3 → 📢 CEO
  通过飞书群发通知

⚡ 执行方式：3 个任务并行执行
⏱️ 预计耗时：约 1 分钟（串行需 3 分钟）
```

### Agent 能力表

| Agent | 擅长 | 常见任务 |
|-------|------|----------|
| 💻 Coding | 编程、技术 | 写代码、调试、Git、部署 |
| 📝 Secretary | 文档、沟通 | 会议纪要、文档编辑、消息 |
| 👤 HR | 人事 | 人员查询、组织架构 |
| 🧠 CEO | 统筹 | 分析、汇总、决策 |

### 汇总报告示例

```
🐝 Swarm 任务完成
━━━━━━━━━━━━━━━

📋 原始任务：处理三件事

👥 执行分工：
├─ 📝 Secretary：整理会议纪要 ✅
├─ 💻 Coding：更新 README ✅
└─ 🧠 CEO：发群通知 ✅

⏱️ 总耗时：58 秒（并行节省 66%）
✅ 全部完成，0 失败
```

### 设计原则

| 原则 | 说明 |
|------|------|
| 📋 先拆后做 | 先展示拆分方案，用户确认再执行 |
| ⚡ 并行优先 | 无依赖的任务同时启动 |
| 🛡️ 容错设计 | 单个子任务失败不影响其他 |
| 📊 进度透明 | 长任务定期汇报进度 |
| 🔄 结果汇总 | 所有完成后统一呈现结果 |
| ⏱️ 超时保护 | 子任务超时自动终止并标记 |

### 与记忆保护链搭配

| Skill | 职责 |
|-------|------|
| **Smart Compact** | 保护对话细节不被压缩丢失 |
| **Session Resume** | 断线后恢复任务进度 |
| **Memory-Dream** | 定期整合日记到长期记忆 |
| **Swarm Coord** | 多 Agent 并行协作提升效率 |

### 常见问题

**Q: 需要预先配置下属 Agent 吗？**
A: 不需要特殊配置。只要 OpenClaw 支持 sessions\_spawn 就能用。Agent 名称在 SKILL.md 中可自定义。

**Q: 子任务之间能传递数据吗？**
A: 可以。CEO 作为 Team Lead 会在子任务之间转发中间结果。

**Q: 子任务失败了怎么办？**
A: 默认重试一次，仍失败则标记跳过，不影响其他任务。

---

## English

### The Problem

Your CEO agent handles everything alone — coding, docs, communication, HR queries. When tasks span multiple domains, it becomes a bottleneck.

### The Solution

Swarm Coord turns your CEO into a real **team leader**:

```
User request → CEO decomposes → spawn parallel agents → monitor → aggregate results
```

Like a project manager who breaks work into tickets, assigns them to specialists, tracks progress, and delivers the final report.

### Install

```bash
clawhub install swarm-coord
```

Or clone from GitHub:

```bash
git clone https://github.com/wavmson/openclaw-skill-swarm-coord.git \
  ~/.openclaw/skills/swarm-coord
```

### The 4 Phases

| Phase | Name | Description |
|-------|------|-------------|
| 1️⃣ | Decompose | Analyze task, identify parallelizable subtasks |
| 2️⃣ | Dispatch | Spawn independent agent sessions for each subtask |
| 3️⃣ | Monitor | Track progress, handle failures, relay intermediate results |
| 4️⃣ | Aggregate | Collect all results into a unified report |

### Design Principles

| Principle | Description |
|-----------|-------------|
| 📋 Plan before act | Show decomposition plan, get user confirmation |
| ⚡ Parallel first | Launch independent tasks simultaneously |
| 🛡️ Fault tolerant | One subtask failure doesn't block others |
| 📊 Transparent | Regular progress updates for long tasks |
| 🔄 Unified output | Single aggregated report when all done |
| ⏱️ Timeout guard | Auto-terminate stuck subtasks |

### FAQ

**Q: Do I need to set up sub-agents first?**
A: No special setup. Works with any OpenClaw installation that supports sessions\_spawn.

**Q: Can subtasks pass data to each other?**
A: Yes. CEO relays intermediate results between subtasks as needed.

**Q: What if a subtask fails?**
A: Retries once, then skips with a warning. Other tasks continue unaffected.

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) with sessions\_spawn support
- At least 2 agent configurations (CEO + 1 sub-agent)

## License

MIT

## Author

[@wavmson](https://github.com/wavmson)
