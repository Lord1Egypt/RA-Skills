---
name: self-improvement
version: 1.0.0
description: >
  错误学习闭环：记录失败和纠正 → Pattern-Key 分类 → 定期复盘 → 整合长期记忆 → 防止再犯。
  Use when: (1) 命令/操作意外失败且原因值得记录,
  (2) 用户纠正了错误（"不对"/"Actually..."/"你搞错了"）,
  (3) 用户要求的能力不存在（能力缺口信号）,
  (4) 外部 API/工具故障且需记录规避方案,
  (5) 发现更好的做法可以替代当前方式,
  (6) 开始重大任务前回顾历史教训。
  NOT for: 一次性小错误（typo/手误/用户说"没关系"的）、
  功能性 bug 修复（用 problem-solving）、
  skill 创建/优化（用 skill-creator）、
  日常操作日志（不是每个 tool call 都要记）。
metadata:
---

# Self-Improvement Skill

记录错误和教训，定期复盘整合到长期记忆，持续改进。

> 来源：[ClawHub](https://clawhub.ai) `self-improving-agent@1.0.11`，3/15 融入 v3.0.2 新特性（Pattern-Key / Recurrence / See Also / Simplify & Harden）
> 原始 repo：https://github.com/pskoett/pskoett-ai-skills

## 核心理念

```
犯错 → 立即记录 → 定期复盘 → 整合记忆 → 形成规则 → 避免再犯
```

不只是记错题本，而是一个**学习闭环**。

---

## 一、被动记录（犯错时触发）

### 什么时候记？

| 信号 | 记到哪 |
|------|--------|
| 命令报错、工具失败 | `.learnings/ERRORS.md` |
| 被用户纠正（"不对"、"你搞错了"） | `.learnings/LEARNINGS.md` |
| 发现自己编造了信息 | `.learnings/LEARNINGS.md` |
| 用户要求缺失的功能 | `.learnings/FEATURE_REQUESTS.md` |
| 发现更好的做法 | `.learnings/LEARNINGS.md` |

### 记录格式

**ERRORS.md / LEARNINGS.md：**

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted
**Area**: frontend | backend | infra | config | workflow | content

### Summary
一句话描述

### Details
完整上下文：发生了什么、做错了什么、正确做法是什么

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback | simplify-and-harden
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20260312-001（如有关联条目）
- Pattern-Key: harden.config_validation | simplify.dead_code（可选，用于追踪重复模式）
- Recurrence-Count: 1（可选，同一模式出现几次）
- First-Seen: 2026-03-12（可选）
- Last-Seen: 2026-03-15（可选）

---
```

**FEATURE_REQUESTS.md：**

```markdown
## YYYY-MM-DD: 功能名

**需求**: 用户想做什么
**场景**: 为什么需要
**状态**: pending / resolved
**方案**: （如果有的话）

---
```

### 记录原则

1. **立即记** — 刚犯错时上下文最完整，拖了就忘
2. **写教训不写流水账** — 重点是"下次怎么避免"，不是"事情经过"
3. **一条教训一个行动** — 能转化为具体规则的才有价值
4. **关联已有条目** — 用 `See Also: LRN-xxx` 关联类似问题
5. **追踪重复模式** — 同一类错误用相同的 `Pattern-Key`，`Recurrence-Count` 递增。≥3 次 → 必须 promote 成规则

---

## 二、主动复盘（定期触发）

### 复盘时机

| 时机 | 做什么 |
|------|--------|
| **每次 session 启动** | 扫一眼 `.learnings/` 最近条目，避免重复犯错 |
| **heartbeat 每 2 天一次** | 完整复盘：回顾近期 learnings，整合到 MEMORY.md |
| **大任务开始前** | 搜索相关 learnings，预防已知问题 |
| **同一个错犯了 3 次** | 必须 promote 成永久规则 |

### 复盘流程（heartbeat 触发）

```
1. 读取最近 2-3 天的 .learnings/ 文件
2. 识别有价值的条目（高频、高影响、可泛化）
3. 整合到 MEMORY.md 的「教训与规则」部分
4. 已整合的条目标记为 [已归档]
5. 检查是否有条目需要 promote 到 AGENTS.md / SOUL.md / TOOLS.md
```

### 复盘模板

在 heartbeat 复盘时，用这个框架思考：

```markdown
## 本周复盘 (YYYY-MM-DD)

### 犯了什么错？
- ...

### 学到什么？
- ...

### 哪些该变成规则？
- → promote 到 [目标文件]

### 哪些已经不再相关？
- → 标记 [已归档]
```

---

## 三、记忆整合（learnings → 长期记忆）

### Promote 规则

| 条件 | Promote 到哪 |
|------|-------------|
| 改变我做事方式的教训 | `AGENTS.md`（工作流规则）|
| 改变我说话/行为方式的教训 | `SOUL.md`（人格规则）|
| 工具使用的坑 | `TOOLS.md`（工具笔记）|
| 值得长期记住但不算规则的 | `MEMORY.md`（长期记忆）|
| 同一个错 ≥3 次（Recurrence-Count ≥ 3） | **必须** promote，不能只留在 learnings |

### Simplify & Harden 模式（v3.0 新增）

在日常工作中发现可以简化或加固的重复模式时，用 `Pattern-Key` 追踪：

| 模式类型 | Pattern-Key 前缀 | 例子 |
|---------|-----------------|------|
| **Simplify**（简化冗余） | `simplify.*` | `simplify.dead_code`、`simplify.redundant_check` |
| **Harden**（加固薄弱点） | `harden.*` | `harden.config_validation`、`harden.error_handling` |

**工作流：**
1. 发现重复模式 → 记录到 LEARNINGS.md，设置 `Pattern-Key` 和 `Recurrence-Count: 1`
2. 再次出现 → 更新同一条目的 `Recurrence-Count` 和 `Last-Seen`
3. `Recurrence-Count ≥ 3` → promote 到 AGENTS.md/TOOLS.md 成为永久规则

### Promote 格式

从 learnings 提炼成**短规则**，不是复制粘贴整段：

❌ 不要这样（太长）：
> 2026-03-04 因为在 models.providers 里加了 capabilities 字段导致 Config invalid，
> 然后 restart 后 webchat 崩了，用户被锁 30 分钟……（500 字）

✅ 要这样（短规则）：
> **改 openclaw.json 后必须先 `openclaw status` 校验，确认无 error 再 restart。**

### MEMORY.md 结构建议

```markdown
# MEMORY.md

## 关于老板
（用户偏好、习惯、重要信息）

## 活跃项目
（当前在做的事）

## 教训与规则
（从 learnings promote 上来的重要教训）

## 工具与环境
（环境特定的知识，如 API 配置、设备信息）
```

---

## 四、文件管理

### 目录结构

```
<WORKSPACE>/
├── .learnings/
│   ├── ERRORS.md          # 错误记录
│   ├── LEARNINGS.md       # 教训记录
│   └── FEATURE_REQUESTS.md # 功能需求
├── MEMORY.md              # 长期记忆（整合后的精华）
├── AGENTS.md              # 工作流规则（promote 的硬性规则）
├── SOUL.md                # 人格规则
└── TOOLS.md               # 工具笔记
```

### 文件大小控制

- `.learnings/` 每个文件保持 <5KB
- 超过时归档旧条目到 `.learnings/archive/YYYY-MM.md`
- MEMORY.md <6KB（定期精简）

### 归档规则

条目符合以下任一条件时归档：
- 已 promote 到永久文件
- 超过 30 天且不再相关
- 问题已彻底解决且不会再犯

---

## 五、检测触发词

自动识别这些信号并触发记录：

**用户纠正：**
- "不对"、"你搞错了"、"Actually..."、"No, that's wrong"

**功能请求：**
- "能不能..."、"要是能..."、"Can you..."、"I wish..."

**知识缺口：**
- 用户告诉你不知道的信息
- 文档/API 行为与你理解的不一致

**错误：**
- 命令返回非零退出码
- 异常或堆栈跟踪
- 超时或连接失败
