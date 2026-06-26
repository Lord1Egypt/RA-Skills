# PulseFlow

> A lightweight daily work system where human tasks and AI work converge naturally.

[English](#english) | [中文](#中文)

---

## English

### What is PulseFlow?

**PulseFlow is a lightweight daily work system that brings human tasks and AI work into one operational rhythm.**

It uses one current dashboard (`NOW.md`) for active work, append-only AI logs for execution records, weekly usage visibility for cost awareness, and monthly archives grouped by week for durable history.

PulseFlow is not just a task list and not just an AI log viewer.
It is a small operating layer for day-to-day work:

- humans manage priorities in one place
- agents append finished work as structured logs
- heartbeat rebuilds the live dashboard
- daily rollover archives yesterday and prepares today
- history stays monthly, current state stays simple

### Core promise

PulseFlow solves one practical problem:

> how to keep planning, execution, usage visibility, and history aligned without turning the system into a heavy project manager.

### System model

PulseFlow has four layers:

1. **Current dashboard**
   - `todo/NOW.md`
   - human-facing live state

2. **Execution logs**
   - `reports/<agent>-ai-log-YYYY-MM-DD.jsonl`
   - append-only source of AI work records

3. **Derived live views**
   - `AI USAGE THIS WEEK`
   - `AI DONE TODAY`
   - rebuilt from usage data and agent logs

4. **Monthly history**
   - `todo/history/YYYY-MM.md`
   - stores week-grouped daily history entries plus one weekly usage summary table per visible week block

### Dashboard structure

`NOW.md` contains:

- `AI USAGE THIS WEEK`
- `FOCUS`
- `TODAY`
- `UP NEXT`
- `DONE`
- `AI DONE TODAY`

Design intent:

- top = weekly visibility
- middle = human priorities
- bottom = today's AI execution summary

### Runtime flow

#### 1. Agent completes work
Each agent appends one JSON line to its daily log.

Example:

```json
{"ts":"2026-04-05T14:10:00+08:00","agent":"main","task":"Finish first draft of the backtest module","tokens":0}
```

`tokens` is optional metadata and is **not** the source of truth for dashboard usage totals.

#### 2. Sync / heartbeat runs
`scripts/sync_ai_done.js`:

- reads `config.json`
- reads today's agent logs
- queries OpenClaw usage summary
- rebuilds `AI USAGE THIS WEEK`
- rebuilds `AI DONE TODAY`
- updates `sync-state.json`

#### 3. Previous-day report runs at 00:05, rollover runs at 00:15
`scripts/rollover_now.js`:

- archives completed human work into the month file
- archives yesterday's AI snapshot into the month file
- groups day entries under clipped week sections inside the month file
- updates that week section's `AI Usage Weekly Summary`
- resets `DONE`
- resets `AI DONE TODAY`
- carries unfinished work forward

### Token accounting

PulseFlow intentionally separates:

- **what AI did** → agent logs
- **how much usage happened** → OpenClaw usage summary

Current live usage table uses:

- `Total Tokens = input + output` (fresh tokens)
- `Cache = cacheRead + cacheWrite`
- `Hit Rate = cacheRead / (input + cacheRead)`

This keeps the visible total intuitive while still exposing cache behavior.

### File layout

```text
pulseflow/
  SKILL.md
  README.md
  scripts/
    _common.js
    _agent_log_rules.js
    _usage_panel.js
    append_ai_log.js
    init_system.js
    install_agent_log_rules.js
    install_summary_crons.js
    repair_system.js
    rollover_now.js
    sync_ai_done.js
    validate_system.js
  references/
    agent-integration-template.md
    agent-log-format.md
    config-template.json
    daily-close-template.md
    heartbeat-checklist.md
    history-template.md
    init-checklist.md
    midday-summary-template.md
    now-template.md
    recovery-playbook.md
    release-checklist.md
    rollover-rules.md
    sync-state-template.json
  docs/
    design.md
    file-spec.md
    lifecycle.md
    portability.md
```

### Scripts

- `append_ai_log.js` — append one AI work record
- `install_agent_log_rules.js` — install/update managed logging rules in agent `AGENTS.md`
- `install_summary_crons.js` — optionally install/update template-driven summary cron jobs from config
- `init_system.js` — initialize a new PulseFlow instance
- `repair_system.js` — repair missing runtime files
- `sync_ai_done.js` — rebuild live AI sections
- `rollover_now.js` — daily rollover and monthly archive update
- `validate_system.js` — end-to-end validation in a temporary environment

### Optional summary notifications

PulseFlow can optionally install two template-driven summary cron jobs:

- **15:30 midday summary** — summarize progress so far, judge the day, and suggest the second-half priorities
- **00:05 previous-day report** — generate the previous day's report before rollover, using `NOW.md` as the still-live end-of-day snapshot

These jobs are **not** installed by default during `init_system.js` because delivery targets are deployment-specific.
They also do **not** replace the normal PulseFlow rollover schedule; if you install the previous-day report cron, the actual rollover should still run later (recommended: 00:15).

Configure `notifications.summaryCrons` in `todo/system/config.json`, then run:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js
```

Review first with:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js --dry-run
```

---

## 中文

> 一个让人类任务与 AI 工作自然汇流的日常工作系统。

### PulseFlow 是什么？

**PulseFlow 是一个把人类任务与 AI 工作纳入同一节奏的轻量日常工作系统。**

它用一个当前面板 `NOW.md` 承载活跃工作，用 append-only AI 日志记录执行结果，用周用量面板展示本周消耗，再把历史沉淀进月文件。

它不是传统任务管理器，也不是单纯的 AI 日志查看器。它更像一个小型运行层：

- 人在一个面板里管理优先级
- Agent 完成工作后追加结构化日志
- heartbeat 负责重建实时面板
- 每天 00:05 可先生成前一日日报，00:15 再完成日切
- 当前只看 `NOW.md`，历史只看月文件

### 它解决什么问题？

PulseFlow 解决的是这件事：

> 如何让计划、执行、用量可见性和历史回溯落到同一条稳定流水里，而不是散落在聊天、日志和临时文件中。

### 系统分层

PulseFlow 可以拆成四层：

1. **当前面板**
   - `todo/NOW.md`
   - 给人看的实时工作面

2. **执行日志**
   - `reports/<agent>-ai-log-YYYY-MM-DD.jsonl`
   - AI 工作的原始流水

3. **实时派生视图**
   - `AI USAGE THIS WEEK`
   - `AI DONE TODAY`
   - 由 usage 数据和 agent 日志重建

4. **月度历史**
   - `todo/history/YYYY-MM.md`
   - 按周分组存放日条目，并在每个周块下维护 `AI Usage Weekly Summary`

### 面板结构

`NOW.md` 里有六块：

- `AI USAGE THIS WEEK`
- `FOCUS`
- `TODAY`
- `UP NEXT`
- `DONE`
- `AI DONE TODAY`

设计意图很简单：

- 上面看本周用量
- 中间看人的工作优先级
- 下面看 AI 今天干了什么

### 运行流程

#### 1）Agent 完成工作
每个 Agent 完成一个独立工作单元后，往自己的当日日志里追加一行 JSON。

#### 2）sync / heartbeat 执行
`scripts/sync_ai_done.js` 会：

- 读取 `config.json`
- 读取今日日志
- 查询 OpenClaw usage 汇总
- 重建 `AI USAGE THIS WEEK`
- 重建 `AI DONE TODAY`
- 更新 `sync-state.json`

#### 3）每天 00:05 前一日日报，00:15 日切
`scripts/rollover_now.js` 会：

- 把昨天的人类完成项归档进月文件
- 把昨天的 AI 快照归档进月文件
- 把日条目挂到当月对应的周块下面
- 更新该周块的 `AI Usage Weekly Summary`
- 清空 `DONE`
- 重置 `AI DONE TODAY`
- 把未完成事项带到新一天

### token 统计口径

PulseFlow 故意把这两件事分开：

- **AI 做了什么** → 看 agent logs
- **用了多少 token** → 看 OpenClaw usage 汇总

当前周用量面板里：

- `Total Tokens = input + output`
- `Cache = cacheRead + cacheWrite`
- `Hit Rate = cacheRead / (input + cacheRead)`

这样总量更直观，但缓存情况也不会被藏掉。

### 可选定时总结通知

PulseFlow 可以额外挂两条“模板 + LLM”的总结类 cron：

- **15:30 日间总结** — 汇总当天截至当前的推进，做判断，并给出后半天建议
- **00:05 前一日日报** — 在日切前读取仍然保留昨日收盘快照的 `NOW.md`，生成前一日日报

这两条 cron **不会** 在 `init_system.js` 中默认自动创建，因为通知目标、账号、时区、归档目录都属于部署侧决策。
而且它们**不能替代** PulseFlow 正常的日切；如果启用前一日日报 cron，真正的日切仍应在之后执行（推荐 00:15）。

配置方式：在 `todo/system/config.json` 的 `notifications.summaryCrons` 中填好设置，然后执行：

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js
```

建议先 dry run：

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js --dry-run
```

