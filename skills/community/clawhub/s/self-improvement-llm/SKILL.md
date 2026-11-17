---
name: self-improvement-llm
description: Autonomous memory and self-learning system for AI agents. Continuously collects experience, manages memory (daily logs, user preferences, knowledge extraction), builds knowledge graphs connecting events→lessons→principles, extracts principles, auto-adjusts behavior, and verifies improvements. Proposes actionable changes for user review before applying. Use when: (1) Agent needs to learn from past sessions, (2) User asks "improve yourself" or "learn from this", (3) Periodic self-evaluation is needed, (4) Agent needs to auto-correct recurring mistakes, (5) Updating AGENTS.md/SOUL.md/MEMORY.md/TOOLS.md based on experience, (6) Extracting universal principles from episodic experiences, (7) Processing user feedback to permanently adapt behavior, (8) Managing daily memory logs, user preferences, or knowledge retention.
---

# Self-Learning System

A continuous learning loop that automatically captures learnings, tracks improvements, and verifies their effectiveness.

**Inspiration:** This skill fuses the structured recording format and detection triggers from [pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) (6.1k installs) with a verification/hypothesis loop that most agent learning systems lack.

## 🤖 Agent: What You Must Do (Not Optional)

These are **required behaviors**, not suggestions. Execute them during conversation without being told.

### During Every Conversation

1. **Detect learning opportunities in real-time.** After every user message or tool result, mentally check:
   - Did the user correct me? → run `python3 scripts/reflect.py --detect "USER_MESSAGE"`
   - Did a tool fail? → log to `.learning-trail.json` immediately
   - Did I learn something new? → log to `.learning-trail.json` immediately

2. **Log corrections immediately.** When the user says "不对", "错了", "no", "actually", etc.:
   ```bash
   python3 scripts/learn.py --log correction "具体纠正了什么"
   ```
   Set pattern_key for dedup: `--log correction "message" --area behavior --priority high`

3. **Log errors automatically.** When a tool call fails or returns unexpected output:
   ```bash
   python3 scripts/learn.py --log error "工具名: 错误简述" --area tooling --priority medium
   ```

4. **After significant tasks,** append to today's daily log:
   ```bash
   python3 scripts/reflect.py --log "完成了什么"
   ```

### At Session Start

5. **Check `.hook-context.txt`** (written by plugin hook at gateway startup):
   Use `read(path="memory/.hook-context.txt")` to check it.
   If it shows pending verifications or patterns ready for promotion, act on them.

6. **Run a quick status check:**
   ```bash
   python3 scripts/learn.py --status
   ```

### During Daily Cycle (via cron, 3AM)

7. The full cycle runs automatically: `python3 scripts/learn.py --cycle`
   - **🌙 Dream:** Distills recent daily logs into MEMORY.md (dedup + compress)
   - Auto-promotes patterns (≥2 occurrences across ≥2 sessions)
   - Auto-generates session summaries (L1)
   - Auto-triggers skill generation (via `skillgen.py --auto`)
   - Records `record_change` for verification tracking
   - Checks for overdue verifications

### ⚠️ Mandatory: Read Before Edit

**CRITICAL RULE — 任何文件编辑前必须先 read 获取当前内容。**

```bash
# ❌ 错误：凭记忆构造 oldText
edit(path="MEMORY.md", oldText="我印象中的内容", newText="新内容")

# ✅ 正确：先读文件，拿到实际内容
read(path="MEMORY.md")
# 然后用实际内容构造 oldText
edit(path="MEMORY.md", oldText="从 read 结果中复制的精确文本", newText="新内容")
```

**为什么：** edit 工具要求 oldText 与文件内容**逐字符匹配**（含空白和换行）。凭记忆构造几乎必然失败，导致 cron 假性 error。

**适用场景：** 编辑 MEMORY.md、TOOLS.md、USER.md、AGENTS.md、SOUL.md 等任何文件。

### Record Changes for Verification

8. **When you modify any core file** (MEMORY.md, TOOLS.md, SOUL.md, AGENTS.md):
   ```bash
   python3 scripts/learn.py --record-change MEMORY.md "what was changed" "why this should help"
   ```
   This populates the verification loop so 7 days later the system checks if it helped.

### Score Conversations

9. **At the end of significant conversations,** rate yourself:
   ```bash
   python3 scripts/learn.py --score 8 7 9 8 7 "brief justification"
   ```
   (accuracy, usefulness, efficiency, tone, proactiveness, 0-10 each)

## Learning Loop

```
Session / Task
    ↓
  [DETECT]     ← Automatic triggers: corrections, errors, feature requests
    ↓
  [LOG]        ← Structured entries with IDs, priorities, categories
    ↓
  [EXTRACT]    ← Distill patterns from repeated entries
    ↓
  [PROMOTE]    ← To AGENTS.md / SOUL.md / TOOLS.md / MEMORY.md
    ↓
  [VERIFY]     ← 7-day check: did this change actually help?
    ↓
  [ADAPT]      ← Reinforce success, revert failure
    ↓
  (back to detect on next interaction)
```

## Memory Management

The skill also manages the agent's memory system — daily logs, user preferences, and knowledge retention.

### Memory Architecture (三层)

| Layer | Store | Content |
|-------|-------|--------|
| **L1** Session Context | `memory/sessions/*.md` | 会话摘要 |
| **L2** Persistent Store | `MEMORY.md`, `memory/*.md`, `memory/skills/` | 蒸馏知识、经验教训 |
| **L3** User Model | `memory/preferences.json`, `USER.md` | 用户偏好、沟通风格 |

Inspired by Nous Research [Hermes Agent](https://github.com/NousResearch/hermes-agent).

### Auto-Daily-Log

At the end of each session or significant task, write a summary to `memory/YYYY-MM-DD.md`. Do NOT log individual micro-events (corrections, errors, tool failures) here — those go to `.learning-trail.json` only.

```markdown
### 📝 Session summary
Completed tasks, user requests, decisions, key outcomes.
```

Keep entries concise (3-5 lines per session).

### Memory Types

| Type | Layer | Where | Example |
|------|-------|-------|---------|
| **Session summaries** | L1 | `memory/sessions/*.md` | "2026-05-27 搜了苏超、装了 SearXNG" |
| **Daily logs** | L2 | `memory/YYYY-MM-DD.md` | "10:30 创建 self-improvement skill" |
| **Distilled principles** | L2 | `MEMORY.md` | "Simple before powerful" |
| **Auto-generated skills** | L2 | `memory/skills/*.md` | "SearXNG 部署流程" |
| **User preferences** | L3 | `memory/preferences.json` | "直接回答，不要解释" |
| **User profile** | L3 | `USER.md` | "技术背景强，中文沟通" |
| **Structured learning** | — | `.learning-trail.json` | 所有 LRN/ERR/FEAT 条目 |

### Memory Retention

| Memory | Retention | Action |
|--------|-----------|--------|
| Daily logs | Keep forever | Append-only, never delete |
| Learning entries | 90 days | Auto-resolve pending items after 90d |
| Verified principles | Keep forever | Part of long-term knowledge |
| User preferences | Keep until changed | Update when user says otherwise |
| Tool notes | Keep until outdated | Update when tools change |

### Memory Search

When user asks "之前说过什么" or "帮我回忆一下":

1. First check `MEMORY.md` (distilled knowledge)
2. Then check `USER.md` (preferences)
3. Then check `.learning-trail.json` for structured entries
4. Then `grep` recent `memory/*.md` files

### Memory Flow

```
会话中
  → 检测到用户偏好 / 知识 / 错误
  → 仅写入 .learning-trail.json（结构化）

会话结束（每次对话结束）
  → 自动生成 L1 会话摘要到 memory/sessions/YYYY-MM-DD-NNN.md
  → 摘要包含：做了什么任务、学到了什么、用户反馈、生成了哪些技能
  → 追加概要到 memory/YYYY-MM-DD.md
  
心跳/空闲
  → 读取 .learning-trail.json 的 patterns
  → 达到阈值的晋升为 MEMORY.md 原则或 memory/preferences.json 偏好
  → 检查是否有值得生成技能的任务（8+ 工具调用且含写操作/脚本执行）
  
新会话开始
  → MEMORY.md 自动注入上下文
  → .learning-trail.json 的 watchlist 提醒我注意
```

## Auto-Trigger Points

### Detection Triggers

Automatically log when you notice:

**Corrections** → log to `.learning-trail.json` (category: correction)
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's outdated..."
- User explicitly correcting your output

**Feature Requests** → log to `.learning-trail.json`
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."
- "Why can't you..."

**Knowledge Gaps** → log to `.learning-trail.json` (category: knowledge_gap)
- User provides info you didn't know
- Documentation you referenced is outdated
- API behavior differs from your understanding

**Errors** → log to `.learning-trail.json`
- Command returns non-zero exit code
- Exception or stack trace
- Timeout or connection failure

**Successes** → log to `.learning-trail.json` (category: best_practice)
- Found a better approach
- Quicker way to do something
- Cleaner pattern emerged

### Scheduled Triggers

| Trigger | When | Action |
|---------|------|--------|
| **Session end** | After completion | Auto-log summary to memory/YYYY-MM-DD.md + memory/sessions/ L1 summary |
| **Skill gen check** | After complex task | Auto-generate skill if 8+ tool calls (with write/exec/workflow) or user says "记住" |
| **Heartbeat** | Idle time | Run learn.py --cycle: check verifications, promote patterns |
| **Improve yourself** | On demand | Full cycle + report |
| **Hook** | Session start | If hook installed, review pending learnings |

## Session Summary (L1)

每次会话/任务完成后，自动生成会话摘要到 `memory/sessions/YYYY-MM-DD-NNN.md`：

```markdown
# Session Summary: 2026-05-27-001

## Tasks Completed
- [任务名称] 做了什么，结果是什么

## Learnings
- [学到了什么]

## Skills Generated
- [生成了哪些技能文件]

## User Feedback
- [用户说了什么重要反馈]

## Open Items
- [未完成的或待确认的]
```

**生成时机：** 一个完整的任务流程结束后（如装完 SearXNG、搜完新闻等）

## Auto Skill Generation

当完成一个复杂度达标的任务后，自动生成标准化技能文件。

**生成条件（满足任意一个）：**
- 任务涉及 **8+ 工具调用且包含写操作/脚本执行/链式工作流**（纯查询类跳过）
- 用户明确要求"记住这个"或"记下来"
- 重复做过类似任务 ≥ 2 次
- 发现了新的工作流或最佳实践

**自动检测机制：**
1. 任务完成后，检查是否满足以上条件
2. 满足则生成技能文件，以短横线命名：`memory/skills/<task-slug>.md`
3. 先检查是否已存在类似技能（grep memory/skills/ 目录），有则更新而非新建

## Structured Log Format

All entries use `TYPE-YYYYMMDD-XXX` IDs (LRN/ERR/FEAT) and go into `memory/.learning-trail.json`. Full entry formats: [references/cli_ref.md](references/cli_ref.md).

## Recurring Pattern Detection

When logging something that might already exist:

1. Search `.learning-trail.json` for matching Pattern-Key
2. If found: increment Recurrence-Count, update Last-Seen
3. If not found: create new entry with Recurrence-Count: 1

### Promotion Rule

Promote a pattern to workspace core files when **all** are true:
- Recurrence-Count >= 3
- Seen across at least 2 distinct sessions
- Occurred within a 30-day window

**Promotion targets:**

| Entry Type | Promote To | Example |
|-----------|-----------|---------|
| Behavioral pattern | SOUL.md | "Be concise, skip disclaimers" |
| Workflow improvement | AGENTS.md | "Spawn sub-agents for long tasks" |
| Tool gotcha | TOOLS.md | "Git push needs auth configured" |
| User preference | USER.md / preferences.json | "User prefers direct answers" |
| Universal principle | MEMORY.md | "Simple before powerful" |
| Reusable procedure | memory/skills/*.md | "SearXNG 部署流程" |

**技能复用流程：**
1. 新任务到来 → 搜索 `memory/skills/` 目录匹配关键词
2. 找到匹配 → 读取技能文件，从 Procedure 开始执行
3. 未找到 → 从头推理，完成后生成新技能文件

Auto-generated skill template: [references/cli_ref.md](references/cli_ref.md).

## Verification Loop

`learn.py --cycle` checks after 7 days if the change helped. Verification API and outcomes: [references/cli_ref.md](references/cli_ref.md).

## CLI Commands

```bash
python3 scripts/learn.py --cycle     # Full cycle: check verifications + promote patterns
python3 scripts/learn.py --verify    # Only check pending verifications
python3 scripts/learn.py --status    # Show learning stats
python3 scripts/learn.py --log learning "message" --area behavior --priority high
```

CLI params reference: [references/cli_ref.md](references/cli_ref.md).

## Hook Integration (Session Start)

For automatic reminders at session start, install the hook:

```bash
# Copy hook files (HOOK.md + handler.js) to OpenClaw hooks directory
cp skills/self-improvement/hooks/openclaw/HOOK.md ~/.openclaw/hooks/self-improvement/HOOK.md
cp skills/self-improvement/hooks/openclaw/handler.js ~/.openclaw/hooks/self-improvement/handler.js

# Enable it
openclaw hooks enable self-improvement

# Verify
openclaw hooks list
```

> **Important:** OpenClaw hooks require `HOOK.md` + `handler.js` at the top level of the hook directory. Shell scripts (`hook.sh`) are not supported.

The hook checks `.learning-trail.json` on session start for:
- Pending high-priority items
- Verifications due for review
- Patterns ready for promotion

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learning-trail.json` |
| User corrects you | Log to `.learning-trail.json` (correction) |
| User wants missing feature | Log to `.learning-trail.json` |
| API/external tool fails | Log to `.learning-trail.json` |
| Knowledge was outdated | Log to `.learning-trail.json` (knowledge_gap) |
| Found better approach | Log to `.learning-trail.json` (best_practice) |
| Same error 3x across sessions | Promote to core file |
| Change applied 7+ days ago | Run verification check |

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| **critical** | Blocks core functionality, data loss risk, security issue |
| **high** | Significant impact, affects common workflows, recurring issue |
| **medium** | Moderate impact, workaround exists |
| **low** | Minor inconvenience, nice-to-have |

## Conflict Resolution

Priority scoring when principles contradict: [references/cli_ref.md](references/cli_ref.md).

## Forgetting & Auto-Revert

- 30d without reinforcement → priority demoted; 60d → stale; 90d → `wont_fix`
- Verification overdue 21+ days → auto-revert
- Details: [references/cli_ref.md](references/cli_ref.md).

## Proposal Workflow

When the learning system detects a pattern ready for promotion or a change that needs verification, it generates a **proposal** for user review:

```
Pattern detected (≥3x across ≥2 sessions)
    ↓
Generate proposal: what to change, why, risk level
    ↓
Present to user for approval
    ↓
User says "approve N" or "skip N"
    ↓
Apply approved changes, track for verification
```

### Proposal Format

Each proposal includes:
- **Type**: promotion / verification / critical_fix
- **Target**: Which file to change (TOOLS.md, MEMORY.md, SOUL.md, AGENTS.md)
- **Change**: Specific text to add/modify
- **Motivation**: Why this change (pattern evidence)
- **Risk**: Low (adds info) / Medium (changes behavior)
- **Effort**: low / medium / high
- **Impact**: low / medium / high

### Auto-apply vs Propose

| Change Type | Action | Example |
|-----------|--------|---------|
| Add note to TOOLS.md | ✅ Auto-apply | "QWeather needs custom host" |
| Add principle to MEMORY.md | ✅ Auto-apply | "Simple before powerful" |
| Add preference to USER.md | ✅ Auto-apply | "User prefers direct answers" |
| Add guideline to SOUL.md | ⚠️ Propose | "Be concise, skip disclaimers" |
| Add rule to AGENTS.md | ⚠️ Propose | "Spawn sub-agents for long tasks" |
| Create new skill | ❌ Always ask | New skill for recurring task |

### Usage

```bash
python3 scripts/learn.py --propose    # Generate proposals for review
```

The agent will present proposals and wait for your approval before applying.

## Conversation Scoring

After each significant interaction, score the response on 5 dimensions (0-10):

| Dimension | What it measures |
|-----------|-----------------|
| **Accuracy** | Was the output factually correct? |
| **Usefulness** | Did it solve the user's actual problem? |
| **Efficiency** | Were tool calls optimal? |
| **Tone** | Matched SOUL.md persona? |
| **Proactiveness** | Anticipated needs? |

### Usage

```bash
python3 scripts/learn.py --score 8 9 7 8 6    # Score last conversation
python3 scripts/learn.py --trends 7            # Show 7-day trend
```

### Trend Tracking

Example in [references/cli_ref.md](references/cli_ref.md).

## Dynamic Memory Injection

Build topic index → detect conversation topic → inject relevant memories.
```bash
python3 scripts/learn.py --build-index
python3 scripts/learn.py --query-memory weather
```
Topics list: [references/cli_ref.md](references/cli_ref.md). Index rebuilt during `--cycle`.

## Knowledge Graph

Connects 事件 → 教训 → 原则. Node types, edge types, and CLI usage: [references/cli_ref.md](references/cli_ref.md).

## Key Principles

1. **Learn automatically.** The system should work without being told.
2. **Verify or it didn't happen.** Every change must be checked later.
3. **Reversible first.** Always track old state so changes can be undone.
4. **Patterns over anecdotes.** One error is noise. Three identical errors are a pattern.
5. **Structured over freeform.** Standardized IDs and categories make learnings searchable.
6. **Don't log secrets.** Never write tokens, keys, or full source files.
7. **Don't learn from noise.** Not every interaction is a learning opportunity.
8. **Connect memories.** Events → lessons → principles form a network, not isolated notes.

## References

- [reflection_frameworks.md](references/reflection_frameworks.md) — Detailed frameworks and patterns
- [scripts/learn.py](scripts/learn.py) — Learning cycle engine
- [scripts/reflect.py](scripts/reflect.py) — Session data collector + auto-log
- [hooks/](hooks/) — OpenClaw session-start hook template

## 更新与迁移

### 更新流程
1. 备份 `memory/` 目录和 `.learning-trail.json`
2. 安装新版本
3. 运行迁移检查：`python3 scripts/migrate.py`
4. 如有问题，运行迁移：`python3 scripts/migrate.py --migrate`

### 版本兼容性
- V2.x → V2.2.0：数据格式兼容，无需迁移
- V1.x → V2.2.0：需要迁移，运行 `python3 scripts/migrate.py --migrate`

### 回滚
如更新后出问题：
1. 恢复备份的 `memory/` 目录
2. 恢复备份的 `.learning-trail.json`
3. 降级到之前的版本

### ⚠️ Windows 已知问题

在 Windows 上，`openclaw skills update` 可能失败，报 `EPERM: operation not permitted`。

**原因：** OpenClaw Gateway（Node.js）运行时持有技能目录的文件句柄，导致 update 流程中的 rename 操作被操作系统拒绝。

**解决方法：**
1. 手动删除旧目录：`cmd /c rmdir /s /q "<skills路径>\self-improvement-llm"`
2. 重新安装：`openclaw skills install self-improvement-llm`

**Linux/macOS 不受影响**，目录在被读取时仍可 rename。

## 备份与同步

### 导出数据
```bash
python3 scripts/sync.py export                    # 导出到当前目录
python3 scripts/sync.py export /path/to/backup.zip  # 导出到指定路径
```

导出内容：
- `memory/MEMORY.md` — 长期记忆
- `memory/.learning-trail.json` — 结构化学习数据
- `memory/.memory-index.json` — 记忆索引
- `memory/preferences.json` — 用户偏好
- `memory/sessions/` — 会话摘要
- `memory/skills/` — 自动生成的技能
- `memory/.dreams/` — 梦境蒸馏数据
- `memory/*.md` — 日常日志

### 导入数据
```bash
python3 scripts/sync.py import /path/to/backup.zip  # 导入（不覆盖已有）
python3 scripts/sync.py import /path/to/backup.zip --overwrite  # 覆盖导入
```

### 多服务器同步
1. 服务器 A：`python3 scripts/sync.py export`
2. 传输 zip 到服务器 B
3. 服务器 B：`python3 scripts/sync.py import backup.zip`

### 查看状态
```bash
python3 scripts/sync.py status
```
