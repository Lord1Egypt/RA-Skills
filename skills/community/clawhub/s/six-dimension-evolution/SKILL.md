---
name: "six-dimension-evolution"
description: "Six-dimension evolution system for AI agents. Transform from reactive assistant to proactive partner with lessons tracking, success patterns, decision review, preference tracking, skill statistics, and knowledge gap detection. Use when setting up a new agent or when the user wants to implement an evolution/self-improvement system."
version: "1.0.0"
author: "stephonGAO"
created: "2026-03-24"
install_hook: "prompt"  # 安装后主动提示用户
---

# 六维进化体系 (Six-Dimension Evolution System)

从"被动响应"到"主动进化"的完整 AI Agent 自我进化框架。

---

## ⚡ 安装后激活

**重要**：此 skill 需要激活才能生效。Agent 读取此文件后应立即执行以下流程：

### 激活检查流程

```
1. 检查 SKILL_STATS.md 是否存在且有 installed 字段：
   
   → 有 installed 字段 → 已激活，跳过提示
   → 无此文件或无 installed 字段 → 未激活，继续检查

2. 如果未激活，检查 workspace 是否缺少六维进化文件：
   - LESSONS.md, SUCCESSES.md, PREFERENCES.md
   - DECISIONS.md, SKILL_STATS.md, KNOWLEDGE_GAPS.md
   
3. 如果文件不存在：
   → 主动询问用户："检测到六维进化体系尚未激活，是否立即配置生效？"
   
4. 用户确认后：
   → 从 templates/ 复制文件到 workspace
   → 在 SKILL_STATS.md 中写入 installed 时间戳
   → 报告安装结果

5. 如果文件已存在但无 installed 标记：
   → 补充写入 installed 时间戳
   → 提示用户"已检测到现有配置，已标记为激活状态"
```

### 激活命令

当用户确认后，执行以下操作：

```bash
# 1. 复制六维进化文件到 workspace
cp templates/LESSONS.md ~/.openclaw/workspace/
cp templates/SUCCESSES.md ~/.openclaw/workspace/
cp templates/PREFERENCES.md ~/.openclaw/workspace/
cp templates/DECISIONS.md ~/.openclaw/workspace/
cp templates/SKILL_STATS.md ~/.openclaw/workspace/
cp templates/KNOWLEDGE_GAPS.md ~/.openclaw/workspace/

# 2. 复制心跳执行文件
mkdir -p ~/.openclaw/workspace/heartbeat
cp templates/1-session-summary.md ~/.openclaw/workspace/heartbeat/  # 昨日会话总结
cp templates/2-daily-review.md ~/.openclaw/workspace/heartbeat/    # 每日复盘

# 3. 写入激活时间戳（重要：标记已激活）
# 在 SKILL_STATS.md 的 JSON 中设置 installed 字段为当前时间
```

**4. 修改 HEARTBEAT.md（关键步骤）**

激活后必须修改 `HEARTBEAT.md`，确保包含以下调度规则：

```markdown
### 1. ✨ 昨日会话总结
- **时间条件**：当前时间在 0:10 - 01:00 之间（北京时间）
- **时间戳字段**：`lastSessionSummary`
- **执行文件**：`heartbeat/1-session-summary.md`
- **注意**：该功能是核心，永远也不要跳过该流程，如果仔细检查后确认昨日没有任何用户会话就把说明情况保存到文件。

满足时间条件时，读取执行文件并按其内容执行。

---

### 2. 🧠 每日复盘
- **前置依赖**：需要先完成「昨日会话总结」（检查 `lastSessionSummary` 是否为今天）
- **时间条件**：当前时间在 01:10 - 02:00 之间（北京时间）
- **时间戳条件**：距离 `lastDailyReview` 超过 12 小时
- **时间戳字段**：`lastDailyReview`
- **执行文件**：`heartbeat/2-daily-review.md`

满足时间条件且前置依赖完成时，读取执行文件并按其内容执行。
```

**检查方式**：读取 HEARTBEAT.md，如果已包含 `heartbeat/1-session-summary.md` 和 `heartbeat/2-daily-review.md` 的引用则跳过；否则按上述格式添加或更新。

**文件关系**：
```
HEARTBEAT.md (调度入口，定义时间条件)
    ├── heartbeat/1-session-summary.md  ← 生成 memory/YYYY-MM-DD.md
    └── heartbeat/2-daily-review.md     ← 读取 memory/*.md 进行复盘
```

**关键步骤**：
1. 必须在 `SKILL_STATS.md` 中写入 `installed` 时间戳
2. 必须修改 `HEARTBEAT.md` 添加调度入口

否则后续仍会提示激活。

---

## 核心理念

单一教训库不足以支撑 AI Agent 的持续进化。需要六维闭环：
- **教训库**：不重复犯错
- **成功库**：可复制成功
- **决策追踪**：质量闭环
- **偏好追踪**：越来越懂你
- **技能统计**：量化驱动
- **盲区追踪**：主动进化

---

## 快速开始

### 1. 安装文件

将 `templates/` 目录下的文件复制到 workspace 根目录：

```
templates/
├── LESSONS.md              → workspace/LESSONS.md
├── SUCCESSES.md            → workspace/SUCCESSES.md
├── PREFERENCES.md          → workspace/PREFERENCES.md
├── DECISIONS.md            → workspace/DECISIONS.md
├── SKILL_STATS.md          → workspace/SKILL_STATS.md
├── KNOWLEDGE_GAPS.md       → workspace/KNOWLEDGE_GAPS.md
├── 1-session-summary.md    → workspace/heartbeat/1-session-summary.md
└── 2-daily-review.md       → workspace/heartbeat/2-daily-review.md
```

### 2. 配置每日复盘

确保 HEARTBEAT.md 中包含每日复盘任务，引用 `heartbeat/2-daily-review.md`。

### 3. 开始使用

系统会在每日复盘中自动：
- 检查决策验证状态
- 统计 skill 调用效果
- 检测知识盲区
- 更新偏好追踪

---

## 六维架构

```
                         ┌─────────────────┐
                         │   每日复盘       │
                         │  (质量检查中心)  │
                         └────────┬────────┘
                                  │
   ┌─────────┬─────────┬─────────┬┴────────┬─────────┬─────────┐
   ↓         ↓         ↓         ↓         ↓         ↓         ↓
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│LESSONS │ │SUCCESSES│ │DECISIONS│ │PREFERENCES│ │SKILL_STATS│ │KNOWLEDGE│
│  .md   │ │   .md   │ │   .md   │ │    .md    │ │    .md    │ │_GAPS.md │
└────────┘ └────────┘ └────────┘ └──────────┘ └──────────┘ └──────────┘
   ↓          ↓          ↓          ↓            ↓            ↓
"不重复    "可复制    "质量      "越来越      "量化        "主动
 犯错"      成功"      闭环"      懂你"        驱动"        进化"
```

---

## 各维度说明

### 1. 教训库 (LESSONS.md)

**触发条件**：犯错、用户纠正

**核心功能**：记录什么不该做

**格式**：
```markdown
### F001: [教训标题]
- **触发**：什么情况下发生的
- **问题**：具体是什么问题
- **改进**：应该如何改进
- **验证**：[ ] 待验证 / [x] 已验证有效
```

---

### 2. 成功库 (SUCCESSES.md)

**触发条件**：用户感谢、采纳建议、明确满意

**核心功能**：记录什么值得复制

**格式**：
```markdown
### S001: [成功模式标题]
- **触发**：什么场景下成功
- **模式**：可复用的方法
- **效果**：具体效果
- **验证**：[ ] 待验证 / [x] 已验证有效（应用 3+ 次）
```

---

### 3. 决策追踪 (DECISIONS.md)

**触发条件**：提出重要建议、方向性决策

**核心功能**：验证建议效果，形成质量闭环

**状态流转**：
```
[活跃] → 观察7-30天 → 验证效果
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
[成功] → SUCCESSES   [失败] → LESSONS
```

---

### 4. 偏好追踪 (PREFERENCES.md)

**触发条件**：用户明确表达、行为反复体现

**核心功能**：动态适应用户，越来越懂你

**分类**：
- 已确认偏好：明确验证
- 待确认偏好：推测，需询问

---

### 5. 技能统计 (SKILL_STATS.md)

**触发条件**：每次 skill 执行后

**核心功能**：量化 skill 效果，驱动优化

**预警机制**：成功率 < 70% 触发关注

**详细日志**：各 skill 目录下的 `logs.json`

---

### 6. 盲区追踪 (KNOWLEDGE_GAPS.md)

**触发条件**：
- 用户提及陌生概念
- 回答后用户纠正
- Skill 失败率高
- 使用模糊词汇（可能、应该、大概）

**核心功能**：检测盲区，主动学习

---

## 每日复盘整合

每日复盘作为"质量检查中心"，整合六维检查：

| 步骤 | 动作 | 涉及文件 |
|------|------|----------|
| 1-4 | 读取记忆、更新 MEMORY.md | `memory/*.md`, `MEMORY.md` |
| 5 | 决策回顾 | `DECISIONS.md` |
| 6 | 技能统计 | `SKILL_STATS.md` |
| 7 | 知识盲区检查 | `KNOWLEDGE_GAPS.md` |
| 8-11 | 生成报告、推送 | - |

---

## 与其他系统的关系

```
用户交互 → 检测盲区 → KNOWLEDGE_GAPS.md → 主动学习 → 知识库
    ↓
Skill 执行 → SKILL_STATS.md → 发现问题 → LESSONS.md → 优化 Skill
    ↓
提出建议 → DECISIONS.md → 验证效果 → SUCCESSES/LESSONS
    ↓
用户反馈 → PREFERENCES.md → 更新偏好 → 更懂用户
```

---

## 使用场景

### 场景 1：新 Agent 初始化

```
用户：帮我配置一个能自我进化的 Agent

Agent：
1. 复制六维进化体系文件
2. 配置每日复盘
3. 创建初始记忆文件
4. 完成：Agent 已具备自我进化能力
```

### 场景 2：犯错后学习

```
Agent 犯错 → 记录到 LESSONS.md
    ↓
每日复盘检查 → 验证是否改进
    ↓
改进有效 → 标记验证通过
```

### 场景 3：建议效果追踪

```
Agent 提出建议 → 记录到 DECISIONS.md
    ↓
7-30 天后验证 → 成功？
    ↓ 是
复制到 SUCCESSES.md → 可复用模式
```

---

## 文件结构

```
workspace/
├── MEMORY.md          # 长期记忆（含进化架构图）
├── LESSONS.md         # 教训库
├── SUCCESSES.md       # 成功模式库
├── PREFERENCES.md     # 用户偏好追踪
├── DECISIONS.md       # 决策追踪库
├── SKILL_STATS.md     # 技能统计汇总
├── KNOWLEDGE_GAPS.md  # 知识盲区追踪
├── heartbeat/
│   ├── 1-session-summary.md  # 昨日会话总结
│   └── 2-daily-review.md     # 每日复盘流程
└── skills/
    └── <skill-name>/
        └── logs.json  # Skill 详细日志
```

---

## 自定义配置

### 调整预警阈值

在 `SKILL_STATS.md` 中修改：
```markdown
> 成功率 < 70% 的 skill 需要关注
```

### 调整决策验证周期

在 `DECISIONS.md` 中修改：
```markdown
验证周期：7-30天，视决策类型而定
```

### 添加模糊词汇

在 `KNOWLEDGE_GAPS.md` 中添加：
```markdown
模糊词汇列表：可能、应该、大概、或许、我记得、好像、不太确定
```

---

## 版本历史

- v1.0.0 (2026-03-24): 初始版本，完整六维进化体系

---

## 许可证

MIT

---

## 致谢

本技能基于实际 AI Agent 运维经验设计，感谢所有反馈和建议。