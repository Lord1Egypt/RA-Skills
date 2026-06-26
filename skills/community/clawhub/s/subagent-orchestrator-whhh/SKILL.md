---
name: subagent-orchestrator
description: 将复杂大型任务拆解为多个子任务，通过 Subagent 并行/串行执行，三文件持久化防丢失，独立任务空间管理，Plan 驱动全程，交付包含中间产物与 diff。降低触发阈值——任务步骤超过3步、涉及2个以上来源或平台、context有膨胀迹象时即触发，不等"大型"才拆。触发词：任务分工、子任务编排、多agent协作、上下文溢出、任务分流、context快满了。
metadata: { "openclaw": { "emoji": "🔀", "requires": ["sessions_spawn", "sessions_send", "sessions_list", "write", "read", "exec", "cron", "sessions_yield", "subagents"] }, "version": "2.0.0", "updatedAt": "2026-05-25" }
---

# Subagent Orchestrator Skill

## 版本

- **v2.0.0 (2026-05-25):** 重大升级（参考 Trae Solo / Windsurf Cascade / Devin）
  1. 新增 **Phase 0.5 需求完善**——接需求后主动询问 3-5 个问题，明确后再拆解
  2. 新增 **独立任务空间**——每个任务专属目录，中间文件和最终产物集中管理
  3. 新增 **Plan 驱动机制**——Phase 1 输出完整 Plan，Phase 3 按 Plan 逐项打勾
  4. 改造 **交付清单**——最终交付含中间产物列表 + 相关文件的 diff
  5. 新增 **Checkpoint + Revert**——每步完成后打 checkpoint，支持回退
  6. 新增 **Queued Messages**——执行期间可追加指令，进入队列依次执行
  7. 新增 **实时进度反馈**——每步完成后推送微信，不等最终完成

---

## 核心原则

### 1. 分工原则

| 角色 | 职责 | 不做什么 |
|------|------|----------|
| **Main Agent** | 需求确认、三文件准备、启动 Subagent、监控进度、失败汇总、Queued Messages 路由、最终整合推送微信 | 不亲自执行信息收集/重IO操作 |
| **Subagent** | 执行具体子任务、写数据文件、更新状态、Checkpoint、失败5次即停+报告 | 不做最终决策、不回写任务文件 |

串行：共享资源（浏览器/数据库）；并行：独立资源（web_fetch/不同API）。不确定时默认串行。

### 2. 三文件分离原则

**Token 节流规范：**
- `_任务.md`：Main Agent 写一次，Subagent 启动时只读一次，永不重读
- `_状态.md`：Subagent 增量写，Main Agent 只扫进度，保持 <500字
- `_数据.md`：Subagent 增量写，Main Agent **仅读此文件汇总**
- 失败先写状态文件；同一错误连续失败5次立即停止，不空转

### 3. 独立任务空间原则

每个任务有专属目录，所有产物集中管理：

```
~/.openclaw/workspace/tasks/[任务ID]/
├── _任务.md           # Main Agent 写入，Subagent 只读
├── _状态.md           # Subagent 增量写
├── _数据.md           # Subagent 增量写
├── _交付清单.md       # Phase 4 由 Main Agent 汇总
├── _Plan.md           # 独立 Plan 文件，Subagent 执行前只读此文件（不读 _任务.md）
├── _Checkpoints.md    # Checkpoint 记录，支持回退
├── _MessageQueue.md   # Queued Messages 队列
└── workspace/         # 任务执行时的所有中间文件
    ├── [子任务A]/
    └── ...
```

- **用户可指定空间：** `--workspace /path/to/dir`，则使用用户指定目录
- **命名规则：** `[任务ID]` = `任务名-日期-序号`，如 `ai-research-20260525`

### 4. Plan 驱动原则

Phase 1 的核心产出是 Plan，所有后续执行必须严格按 Plan 推进：

```
## Plan（共 N 步，控制在 3 轮以内）
- [ ] Step 1: [描述]（工具：[预期工具]，产出：[中间/最终产物]）
- [x] Step 2: [描述] ✅ 完成于 10:02（工具：[实际用到的工具]，产出：[实际产出]）
- [ ] Step 3: [描述]
```

- Plan 总步骤数控制在 **3 轮以内**
- Phase 3 每完成一个 Step → 在 Plan 中打 `[x]` 并标注实际工具和产出
- Subagent 发现 Plan 有缺陷 → 写状态文件 + `tag=need_user` → Main Agent 询问用户是否更新

### 5. 需求完善原则（Phase 0.5）

收到任务后，**不立即拆解**，先主动完善需求，询问 3-5 个关键问题：

```
1. 【目标明确化】最终交付物？格式？位置？
2. 【范围界定】包含什么？明确排除什么？
3. 【约束条件】时间/格式/工具限制？参考文件？
4. 【验收标准】怎么算完成？量化指标？
5. 【优先级】必须 vs 可精简？
6. 【背景/上下文】解决什么问题？历史背景？
7. 【工作空间】指定目录 or 默认 tasks/[任务ID]？
```

**跳过条件：** 用户需求已包含完整信息（目标/范围/验收标准/交付位置均有）→ 直接进入 Phase 1

### 6. Checkpoint + Revert 原则

每次 Phase/Step 完成后自动记录 checkpoint，支持回退：

```markdown
## Checkpoint 记录
| ID | 时间戳 | Phase/Step | 状态摘要 | 可回退 |
|-----|---------|-----------|---------|-------|
| ckpt-0 | 10:00 | Phase 1 | Plan已确认，3步子任务 | 是 |
| ckpt-1 | 10:15 | Phase 3 Step1 | 收集阶段完成，10条记录 | 是 |
```

**回退操作步骤（Main Agent 执行）：**
```
1. 确认 ckpt-ID 存在且「可回退」= 是
2. 备份当前 workspace/ → workspace_backup/
3. 从备份中恢复 ckpt-ID 时 workspace/ 内容（覆盖当前）
4. 将 ckpt-ID 时 _数据.md 内容写入（覆盖当前）
5. 新建 checkpoint ckpt-N+1，记录：回退原因、回退到/来自哪个 checkpoint
6. 通知用户回退完成
7. 若 Subagent 未结束，sessions_send 通知从 ckpt-ID 状态继续
```

**不执行回退：** 任务已完成（Phase 4 结束）或 ckpt「可回退」= 否

### 7. Queued Messages 原则

Subagent 执行期间，用户可追加指令，Main Agent 将其追加到 `_MessageQueue.md`，Subagent 每步执行前检查：

```markdown
## Message Queue
| # | 时间戳 | 来源 | 消息内容 | 状态 | 执行时机 |
|---|--------|------|---------|------|---------|
| 1 | 10:05 | 微信 | "加一个 XX 字段" | ⏳ | 下一步执行前 |
| 2 | 10:07 | WebChat | "这个先暂停" | ⏳ | 当前步完成后检查 |
```

**处理规则（按优先级）：**
- 工具调用**执行前**收到暂停/停止 → **立即停止**，状态文件标记 `⏸️ 暂停`，报告 Main Agent
- 工具调用**执行中**收到暂停/停止 → **完成当前调用再停止**（防止半写入文件）
- 追加类消息 → append 到 `_状态.md` 的「用户追加指令」区，继续执行
- Phase 4 整合时清空已处理的队列

### 8. 失败阈值原则

| 类型 | 可自行重试 | 超过5次 → 暂停 |
|------|-----------|----------------|
| 网络临时故障 | 等10秒再试 | 连续5次 → 暂停 |
| 验证码/风控 | 写状态→暂停 | — |
| 信息不足/参数错误 | 修复后重试 | 连续5次 → 暂停 |
| 权限/认证失败 | — | 立即暂停，报告用户 |

### 9. 交付验证原则

```
📤 交付验证（必须全部提供，否则视为未交付）
- 目标渠道：[channel/thread id 或具体位置描述]
- 消息ID：[message_id 或 object_id]
- 人类可查位置：[可验证的链接或描述]
```
缺少任一 → **任务视为未完成**，不得标记 `done`。

### 10. Memory 固化原则（按需写入，不爆炸）

| 条件 | 是否写 memory | 写什么 | 写多少 |
|------|-------------|--------|--------|
| 子任务数 ≥ 3 且正常完成 | 写一行摘要 | 任务目标+关键成果+文件路径 | ~100字 |
| 有失败/异常/阻塞 | 写 | 失败原因+解决建议 | ~50字 |
| 正常完成（子任务数 < 3） | **不写** | — | 0 |
| 发现更好方案/工具 | 写 | 替代方案+使用条件 | ~50字 |
| 用户做了特殊决策 | 写 | 用户偏好（下次自动用） | ~30字 |

### 11. 模型分级原则

| Agent | 简单 | 中等（默认） | 复杂 |
|-------|------|------------|------|
| Claude Code | `claude-haiku-4-5@20251001` | `claude-sonnet-4-6@default` | `claude-opus-4-6@default` |
| OpenCode | `dobest/MiniMaxM2.5` | `dobest/glm-5.1` | `dobest-claude/claude-opus-4-6@default` |
| 信息收集子 Agent | `dobest/MiniMaxM2.1` | `dobest/MiniMaxM2.5` | `dobest/gpt-5.4` |
| 部署子 Agent | `dobest/MiniMaxM2.1` | `dobest/MiniMaxM2.5` | `dobest/glm-5.1` |
| 学习子 Agent | `dobest/MiniMaxM2.1` | `dobest/MiniMaxM2.5` | `Qwen3.5-397B` |

**难度判断标准：**

| 难度 | 判断标准 |
|------|---------|
| **简单** | 一次性任务、常识性输出、不需要深度推理、单步或两步完成 |
| **中等（默认）** | 需要一定上下文、简单推理、多步操作 |
| **复杂** | 多步骤、深度推理、长上下文、跨域知识、需反复迭代 |

### 12. 其他原则

- **资源整合度：** 引用的路径/资源使用前验证可达性（ls 检查目录/文件），不可达则报告用户
- **资源独占：** 共享资源不可并发（浏览器/数据库），独立资源可并发（web_fetch/只读API）
- **数据纯正性：** 不擅自切换来源，每个来源有验证方法，切换需用户同意

---

## 自动触发场景

**满足任一即触发，不只是用户主动要求：**

1. **预估超出上下文**：3+文件、>10轮对话、多轮浏览器操作、单次输出>1500字 → 立即拆分分流
2. **Context 即将 compact**：回复变慢/开始遗忘/大量工具调用 → 紧急落盘三文件 + spawn 接续
3. **单任务天然拆分**：2+独立信息源/平台、分阶段结构 → 按正常流程执行 Phase 0.5-4
4. **执行中途发现上下文不够**：数据量超预期/Subagent 自身快爆 → 三文件分离，嵌套 spawn 需用户确认
5. **任务略复杂（3步以上）**：多步推理/搜索/文件操作组合 → 优先拆分
6. **Subagent 连续失败5次**：停止重试，报告 Main Agent
7. **Queued Messages 包含暂停/停止指令**：立即停止 Subagent，报告 Main Agent

---

## 执行流程

## Phase 0: 拆分必要性预判

| 判断维度 | 是 → 拆分 | 否 → 直接执行 |
|---------|----------|--------------|
| 独立信息源数量 | ≥2个 | 只有1个 |
| 步骤数 | 明确超过3步 | 1-2步可一次性完成 |
| 资源冲突风险 | 有共享资源需串行 | 完全无共享资源 |
| 预期token消耗 | 多来源→拆分收益高 | 单来源→拆分开销大于收益 |

预判结论写入任务文件：
```markdown
## 拆分判断
- 预判结论：[拆分 / 不拆分]
- 理由：[一句话说明]
```

---

## Phase 0.5: 需求完善（Main Agent）

**触发：** 任务需要拆分（Phase 0 判定为拆分），且用户未在需求中提供足够信息

**目的：** 主动询问 3-5 个问题，完善以下维度，避免执行中反复确认

**问题清单（选择性使用，选最关键的 3-5 个问）：**

```
1. 【目标明确化】最终交付物？格式？位置？
2. 【范围界定】包含什么？明确排除什么？
3. 【约束条件】时间/格式/工具限制？参考文件？
4. 【验收标准】怎么算完成？量化指标？
5. 【优先级】必须 vs 可精简？
6. 【背景/上下文】解决什么问题？历史背景？
7. 【工作空间】指定目录 or 默认 ~/.openclaw/workspace/tasks/[任务ID]/？
```

**确认话术示例：**
```
收到，我来帮你做这个调研。
有几个问题先确认一下：
1. 最终交付物是报告还是摘要文档？格式偏好？
2. 需要覆盖哪些平台/来源？
3. 有没有参考的模板或风格要求？
确认后开始执行。
```

**输出：** 收到用户回复 → 综合 Phase 0 判断 → 进入 Phase 1

---

## Phase 1: 任务拆解与准备（Main Agent）

1. **明确目标：** 最终交付物是什么？验收标准？（综合 Phase 0.5 用户回复）
2. **输出 Plan：** 将任务拆分为 **3 轮以内**的可执行步骤，每步标记预期工具/产出
3. **判断串行/并行：** 共享资源串行，独立资源并行
4. **创建任务空间（执行此命令）：**
```bash
mkdir -p ~/.openclaw/workspace/tasks/[任务ID]/workspace/[子任务目录按需创建]
touch ~/.openclaw/workspace/tasks/[任务ID]/_Plan.md
touch ~/.openclaw/workspace/tasks/[任务ID]/_Checkpoints.md
touch ~/.openclaw/workspace/tasks/[任务ID]/_MessageQueue.md
```
> 三文件（_任务.md / _状态.md / _数据.md / _交付清单.md）由 Main Agent 在后续步骤写入。

**Plan 文件模板（_Plan.md）：**
```markdown
# [任务名] Plan

## 基本信息
- 创建时间: [时间戳]
- 最后更新: [时间戳]

## Plan（共 N 步，3 轮以内）
- [ ] Step 1: [描述]（工具：[预期工具]，产出：[中间/最终产物]）
- [ ] Step 2: [描述]（工具：[预期工具]，产出：[中间/最终产物]）
- [ ] Step 3: [描述]（工具：[预期工具]，产出：[中间/最终产物]）

## 进度记录
| Step | 状态 | 开始时间 | 完成时间 | 实际工具 | 实际产出 |
|------|------|---------|---------|---------|---------|
| Step 1 | ⏳ | — | — | — | — |
| Step 2 | ⏳ | — | — | — | — |
| Step 3 | ⏳ | — | — | — | — |
```

**Checkpoint 初始记录（_Checkpoints.md）：**
```markdown
## Checkpoint 记录
| ID | 时间戳 | Phase | 状态摘要 | 可回退 |
|-----|---------|-------|---------|-------|
| ckpt-0 | [时间戳] | Phase 1 | Plan已确认，N步子任务 | 是（Plan确认后） |
```

**状态文件初始内容：**
```markdown
# [任务名] 状态

## 基本信息
- 任务空间: ~/.openclaw/workspace/tasks/[任务ID]/
- Plan 路径: _Plan.md（Subagent 每次执行前只读此文件，不读 _任务.md）

## Plan 进度
- [ ] Step 1: [描述] — ⏳ 等待中
- [ ] Step 2: [描述] — ⏳ 等待中
- [ ] Step 3: [描述] — ⏳ 等待中

## 当前指向
- 当前执行到：Step N
- 下一步：Step N 的具体操作

## Checkpoint
- 最新：ckpt-0（Phase 1 完成）
- 可回退到：[ckpt-0]

## Queued Messages
- 待处理：0 条

## 任务状态
- 状态：⏳ Plan 已就绪（Phase 0.5 需求确认完成）

## 用户追加指令
- （空）

## 待解决问题
- 无
```

---

## Phase 2: 启动 Subagent 前确认（Main Agent）

**⚠️ Spawn 前必须确认：** 向用户展示 Plan + 子任务列表 + 并行/串行策略 + 预计执行顺序，获明确回复后再 spawn。

**确认话术模板：**
```
📋 需求已确认，开始执行：

📝 Plan（共 N 步，3 轮以内）
  Step 1: [描述] → 产出：[文件/数据]
  Step 2: [描述] → 产出：[文件/数据]
  ...

📁 任务空间：~/.openclaw/workspace/tasks/[任务ID]/
  所有中间文件和最终产物都存在这里
  交付时包含所有文件的变更 diff

🔀 执行策略：[A || B 先行] → C 串行
📊 实时进度：每步完成后推送微信，完成后推送完整交付清单
开始执行？
```

**每次 spawn 四必填：**
- ✅ `mode: "session"`
- ✅ `sessionKey: "[任务ID]-[子任务名]"`
- ✅ 完整 `task` 参数（塞满所有细节，包括 Plan、任务空间路径）
- ✅ 三文件路径告知（强调 workspace/ 下的中间文件都存在任务空间里）
- ✅ 交付证明要求（如有外部交付：`proof` 字段说明需要的证明类型）

**最小 spawn 模板：**
```javascript
sessions_spawn({
  label: "[子任务描述]",
  mode: "session",
  sessionKey: "[任务ID]-[子任务名]",
  task: `
目标：[明确、可验收的目标]
只读：_Plan.md（Plan 核心）、_任务.md（仅补充说明）
只写：_状态.md + _数据.md + _Checkpoints.md + workspace/
执行前：读 _MessageQueue.md，检查是否有暂停/停止指令
执行中：每完成一个 Step → 更新 _Plan.md（打[x]） + 写 _数据.md + 打 checkpoint
异常处理：立即写入状态文件并报告
验收标准：[至少N条/包含XX/格式为XX]
`
})
```

---

## Phase 3: Subagent 执行（6 步法 + 实时进度）

**⚠️ 重要执行顺序（按此优先级读文件，不要读 SKILL.md 全文）：**
```
1. 读 _Plan.md → 找到当前 Step（第一个 [ ] 的行）
2. 读 _MessageQueue.md → 检查暂停/停止指令
3. 执行当前 Step（按 Plan 中的工具预期）
4. 完成后写 _数据.md → 更新 _Plan.md（打[x]）→ 打 checkpoint → sessions_send 进度
5. 读 _状态.md → 更新进度字段
6. 重复 1-5，直到所有 Step 完成
```

**速查表（执行中快速对照）：**
| 动作 | 读什么文件 | 写什么文件 |
|------|-----------|-----------|
| 确认当前步骤 | `_Plan.md`（不读 _任务.md） | — |
| 检查暂停指令 | `_MessageQueue.md` | — |
| 记录产出 | — | `_数据.md`（三段式头） |
| 更新进度 | — | `_Plan.md`（打[x]） |
| 打快照 | — | `_Checkpoints.md` |
| 推送进度 | sessions_send → main | `_状态.md` |
| 遇到问题 | — | `_状态.md` + tag=need_user |

**三段式数据头格式：**
```
---

## [子任务] · Plan-Step-N · [时间戳]

[数据类型]
[实际内容]
```

**每完成一个 Step：**
- ✅ 更新 `_Plan.md`（打 `[x]`，填实际工具和产出）
- ✅ append 到 `_数据.md`（带三段式标记头）
- ✅ 打 checkpoint（写 `_Checkpoints.md`）
- ✅ **推送实时进度**（sessions_send 给 Main，根据发起渠道推送，不跨渠道）

**Checkpoint 格式（每步完成后追加到 _Checkpoints.md）：**
```
| ckpt-[N] | [时间戳] | Phase 3 Step N完成 | [workspace 变化描述] | 是 |
```

**实时进度推送（每步完成后）：**
```javascript
sessions_send({
  sessionKey: "main",
  message: `📊 [任务名] 进度
Step N/N 完成：[step 描述]
产出：[简要摘要]
${is_final_step ? '最终完成，推送交付清单...' : '下一步：${next_step}...'}`
})
```

**结构化 Return（写状态文件）：**
```
## Subagent Return
tag: [autopilot | done | partial | blocked | need_user | paused]
task_id: [任务ID]
Plan 进度: Step N/N（共 M 步）
steps_completed: [1, 2, ...]
files_written: [文件路径列表]
checkpoints_created: [ckpt-1, ckpt-2, ...]
next: [下一步]
proof: [外部交付证明 / null]
```

**tag 含义：**
- `autopilot`：本轮完成但任务线未结束（还有未完成的 Step）→ Main Agent 必须派下一跳
- `done`：本任务所有 Plan Step 全部完成 → 进入 Phase 4 整合
- `partial`：部分完成，状态文件已有断点 → 等待接手或用户决定
- `blocked`：被阻塞（验证码/权限/网络持续失败）→ 等待人工介入
- `need_user`：需要用户决策（如 Plan 需要调整）→ 报告给用户
- `paused`：收到暂停/停止指令 → 等待 Main Agent 决定

---

## Phase 3.5: Queued Messages 处理（Main Agent）

Subagent 返回 `tag=paused` 或用户发送追加消息时：
1. 读 `_MessageQueue.md`，按顺序处理
2. 「继续」类 → `sessions_send` 通知 Subagent 继续执行
3. 「修改 Plan」类 → 更新 `_Plan.md`，`sessions_send` 通知 Subagent
4. 「停止/取消」类 → 标记任务为 `❌ 取消`，进入 Phase 5 清理
5. 「追加需求」类 → append 到 `_任务.md` 的「追加需求」区，更新 Plan，`sessions_send` 通知 Subagent

---

## Phase 4: Main Agent 整合（7 步法）

0. **收集中间产物 + 生成 diff（新增步）：**
   - 扫描 `~/.openclaw/workspace/tasks/[任务ID]/workspace/`，列出所有文件
   - 对已存在文件（配置/脚本/文档）用 `git diff` 或文件对比工具提取变更
   - 将 diff 写入 `_交付清单.md` 的「文件 diff」一节

1. **扫状态文件（极小，token≈0）**
   ```bash
   read ~/.openclaw/workspace/tasks/[任务ID]/_状态.md
   ```
   判断：全✅→继续 | 有⚠️/❌→汇总已有+标注 | 有⏳→汇总已完成部分

2. **仅读数据文件（纯成果内容，无冗余）**
   ```bash
   read ~/.openclaw/workspace/tasks/[任务ID]/_数据.md
   ```
   按优先级顺序读，只读数据文件，不读任务文件。

3. **跨数据源交叉统计**
   - 同类项归一（忽略空格/标点差异）
   - 提及/出现次数 +1
   - 每项附加所有来源
   - 按出现次数降序

4. **生成最终交付清单：**
```markdown
# [任务名] 交付清单

## 基本信息
- Plan 执行：N/N 步
- 完成时间：[时间戳]
- 任务空间：~/.openclaw/workspace/tasks/[任务ID]/

## 最终产物（用户明确要求）
| 产物 | 路径/位置 | 格式 | 验证方式 |
|------|---------|------|---------|
| [产物名] | [路径] | [格式] | [验证方式] |

## 中间产物（执行过程中产生）
| 产物 | 路径 | 用途 | 来源 |
|------|------|------|------|
| [中间文件名] | workspace/[path] | [用途] | [Step N 生成] |

## 文件 diff（已存在文件的变更）
| 文件 | 变更类型 | 变更摘要 | diff 关键行 |
|------|---------|---------|-----------|
| [配置文件] | 修改 | [改了什么] | [diff 片段] |
| [脚本] | 新建 | [脚本用途] | 不适用（新建） |

## Checkpoint 记录（可追溯）
| ID | 时间戳 | Phase/Step | 状态 |
|-----|---------|-----------|------|
| ckpt-0 | ... | Phase 1 | Plan完成 |
| ckpt-1 | ... | Phase 3 Step 1 | 收集完成 |

## 数据来源统计
- [子任务A]：[N] 条记录

## 交付验证
- 目标渠道：[channel/thread id]
- 消息ID：[message_id]
- 人类可查位置：[链接/描述]
```

5. **排序与优先级计算**
   - 定义权重维度（来源权重、时间衰减、相关性等）
   - 计算综合优先级分
   - 按分降序排列

6. **输出完成报告：**
```
【任务完成】[任务名] ✅
📊 Plan 执行：N/N 步
📦 最终产物：X 个
🔧 中间产物：X 个
📄 文件 diff：X 处变更（详细见 _交付清单.md）
💾 Checkpoint：N 个（可回退）
📁 任务空间：~/.openclaw/workspace/tasks/[任务ID]/
```

7. **推送最终结果（必须执行）：**
   > ⚠️ 禁止只回聊天，必须同步推送到用户发起需求的渠道，不跨渠道推送。
   ```bash
   openclaw message send --channel [发起渠道ID] --target [用户ID] -m "[完成报告内容]"
   ```

---

## Phase 4.5: sessions_send 路由处理

收到 Subagent 的 `sessions_send` 时：
1. 识别为「进度更新」或「完成通知」
2. **不要**回复 `ANNOUNCE_SKIP` 或空回复
3. 同步推送到用户发起需求的渠道（不跨渠道）

**Anti-Drop Guard：**
每次 subagent 返回 `tag=autopilot` 后，Main Agent 确认：
```
✅ 确认1：任务线还在任务板上（未手动关闭）
✅ 确认2：Plan 尚有未完成 Step
✅ 确认3：下一跳已派发 OR 任务线已显式关闭
→ 任一缺失 → ❌ 立即 spawn 或派给自己
```

---

## Phase 5: 清理（需用户批准）

**触发：** 任务完成 / 失败 / 超7天未动 / 用户主动要求

**流程：**
1. **Memory 固化（按需，见原则10）**
2. 列出 `~/.openclaw/workspace/tasks/[任务ID]/` 下所有文件（含 workspace/）
3. 向用户展示分类（最终产物 / 中间文件 / 保留文件）
4. **强调 `_交付清单.md` 不删除**
5. 未获批准前不执行任何清理
6. 获批后用 `trash`，不用 `rm`

**规则：**
- 只清理中间文件，不删最终产出和交付清单
- 默认保留 72h 内文件
- 交付清单中标记为「最终产物」的文件永不删除

---

## 实时进度推送规则

**时机：** Phase 3 每完成一个 Step → 推送一条进度（不等最终完成）
**渠道：** 推送到用户发起需求的渠道（WebChat/Discord/微信等，不跨渠道推送）

**内容要素：**
```
📊 [任务名] 进度
Step N/N 完成：[step 描述]
产出：[简要摘要]
[下一步提示 / 最终完成预告]
```

**不推送：** 步骤内部的重试、工具调用细节、思考过程

---

## 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 对话太长快撑爆上下文 | 立即执行上下文抢救：落盘三文件 + spawn Subagent 接续 |
| Context compact 后忘了在做什么 | 读 _Plan.md 恢复进度，读 _状态.md 恢复上下文 |
| Subagent 忘了任务 | 检查 task 参数是否完整；恢复优先级：task > 文件 > 记忆 |
| 多个 Subagent 资源冲突 | 串行执行，一个用完再下一个 |
| Gateway 重启导致失败 | Main Agent 重新 spawn，状态文件中有 Plan 断点 |
| 进度卡住 | `subagents list` 检查，kill 后从断点重启 |
| Token 消耗过大 | 确认只读数据文件汇总，不读任务文件和完整状态日志 |
| 临时文件堆积 | Phase 5 清理，必须用户批准 |
| Subagent 连续失败 5 次 | 停止重试，写状态文件❌，向 Main Agent 报告，等待人工介入 |
| Subagent 返回 autopilot 但任务线停了 | 检查 anti-drop guard 三件事 |
| 外部交付任务口头确认"已发送" | 要求提供 delivery-proof，缺一不可标记未完成 |
| Plan 中的 Step 执行遇到意外情况 | 写状态文件 + tag=need_user，报告 Main Agent，等用户确认 |
| 中间文件不知道存哪 | 存到 `workspace/[子任务]/`，交付时统一汇报 |
| 用户在 Subagent 执行期间追加指令 | Main Agent 追加到 `_MessageQueue.md`，Subagent 下一轮读取 |
| 用户要求回退到某 checkpoint | Main Agent 执行回退，恢复 workspace/ + _数据.md 到当时状态 |

---

## 辅助功能（精简）

**每日 Session 清理定时任务：** 配合 `session-cleanup-pro` skill 使用。用户确认需要后，用 `cron add` 创建定时任务（每天凌晨 03:30）。

---

## 适用场景示例

| 场景 | Plan 拆分 | 执行策略 | 中间产物 |
|------|-----------|---------|---------|
| 上下文即将溢出 | 未完成部分拆出 Plan | Subagent 执行，Main 只保留等待 | workspace/ 下中间文件 |
| 多平台攻略抓取 | 按平台分 Step | 浏览器串行，web_fetch并行 | workspace/[平台]/ 数据文件 |
| 配置修改任务 | Step1备份→Step2修改→Step3验证 | 串行，备份优先 | backup/ + diff |
| 代码生成+review | Step 1生成→Step 2 review→Step 3修改 | 串行，review 依赖生成 | workspace/generate/ + workspace/review/ |
| 多数据源调研 | 按来源分 Step | API限流可能需串行 | workspace/[来源]/ 原始数据 |

---

## 设计理念

> **找的范围应该确定性，想的综合应该概率性。**
> 三文件分离的本质是关注点分离：任务是契约，状态是心跳，数据是成果。Plan 驱动让执行有章可循，独立空间让交付有据可查，diff 让变更透明可追溯。