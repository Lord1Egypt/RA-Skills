---
name: token-saver
description: >
  Five-phase token audit & optimization framework for OpenClaw:
  Discover → Prioritize (3D matrix) → Optimize (9 category techniques)
  → Validate → Monitor. Universal; adapt via appendix.
  Trigger: "省点 token", "token 优化", "token saver",
  "token audit", "检查 token 消耗"
  Version history:
  v1.0 (2026-05-03) — 初始框架, 6 categories
  v1.5 (2026-05-04) — +G Provider Caching, +H Behavioral Discipline
  v2.0 (2026-05-12) — +I Context Engineering
  v2.1 (2026-05-14) — +J Intelligent Model Routing (OpenSquilla)
                        + Quick Start guide, +Category Decision Tree
                        + Monitor phase checkpoints
---

# Token Saver

> Universal token audit & optimization framework for OpenClaw agents.
> Based on real-world practice (2026-05-04).

## Core Principles

1. **Tier your model usage** — Simple tasks use cheap models; complex reasoning
   uses expensive ones. Don't mix the two.
2. **Prompts say *what*, not *why*** — Background rationale and philosophy are
   noise to an agent. Strip them.
3. **Batch > Serial** — One call for 10 results costs marginally more than
   three calls for 3+3+4 results. Combine.
4. **Context = Cost** — Every file loaded at session start, every tool schema
   registered, every past message injected — all have a token price.
5. **Idle = Zero burn** — Nighttime, weekends, and idle periods should run
   nothing. Configure active hours.

## Output

After each full execution, write a report (`token-audit-report-YYYY-MM-DD.md`)
containing: before/after comparison table, estimated weekly savings per change,
items deferred and why, recommended next step.

---

## Quick Start

Not every audit needs the full Phase 1-5 treatment. Use these shortcuts
based on your goal:

### 🚀 Express Audit (15 min)
Trigger: "快速 token 审计"
1. Run **Phase 1A** (enumerate cron tasks) + **Phase 1D** (model tier map)
2. Skip directly to **Phase 3** category table and pick the lowest-hanging fruit
3. Apply **Safe** techniques only, no user confirmation needed
4. Skip Phase 4 and Phase 5 — just log the changes

### 🎯 Quick Wins (<5 min)
Trigger: "快速省 token"
Go straight to these high-impact, zero-risk techniques:
1. **A3** (constrain output — add conciseness instruction)
2. **B1** (right-size each task — cheapest viable model)
3. **G1** (fixed prefix first — static prefix + dynamic suffix)
4. **H1/H2** (default to working path, fail once and switch)

Apply directly without audit preamble.

### 🔄 When to run full audit
| Indicator | Action |
|-----------|--------|
| First time using this skill | **Full Phase 1-5** — establish baseline |
| Cron tasks changed significantly | **Phase 1-3** — re-discover + re-optimize |
| New provider/API added | **Phase 1B + 3** — check config + optimize |
| >30 days since last audit | **Phase 1-2** — measure drift, then re-optimize |
| Just want a quick check | **Quick Wins** or **Express Audit** |

---

## Phase 1: DISCOVER — Map the Full Token Landscape

### 1A Enumerate All Automated Tasks

Read your cron/scheduled task configuration (e.g. `~/.openclaw/cron/jobs.json`).

For each task record:
- `name`
- `model` (or "default" if unset)
- `message` / `prompt` length in chars
- `schedule` frequency (daily / weekly / other)
- `delivery.mode` (announce / none)
- `sessionTarget` (isolated / main)

### 1B Analyze Agent Configuration

Inspect your gateway config (e.g. `openclaw.json`):

- `agents.defaults.heartbeat.*` — interval, active hours, isolated session,
  light context flag
- `agents.defaults.compaction.mode` — message retention aggressiveness
- `agents.list[].tools.profile` — full, coding, or custom
- `agents.list[].model` — per-agent model override

### 1C Measure Context Load

List every file that is injected at session start (typically files in the
workspace root directory). Measure each in chars and estimate token cost
(~3 chars per token for CJK-heavy text, ~4 for English-heavy).

If LCM (Lossless Context Management) is active, note the number and average
size of compacted summary blocks injected per turn.

If tool schemas are accessible, estimate total schema chars:
(count of registered tools × average schema size in chars).

### 1D Map Models to Tiers

Categorize all available models into three tiers based on capability and cost:

- **🏆 Premium** (strong reasoning, high cost): e.g. deepseek-v4-pro, gpt-5.x
- **🟡 Standard** (balanced): e.g. deepseek-v4-flash, minimax-m2.7
- **🟢 Economy** (lightweight): e.g. minimax-m2.7-highspeed, ollama local

Map each task from 1A to its current model tier.

> ⚠️ **Checkpoint**: Before moving to Phase 2, present your Phase 1 findings
> (task inventory, file sizes, model tier map) to the user.
> Confirm that the inventory is complete and the measurements are correct.
> This prevents optimizing the wrong things.

---

## Phase 2: PRIORITIZE — Build Your Decision Matrix

Score each finding from Phase 1 along three independent dimensions:

| Dimension | Scale | Assessment |
|-----------|-------|------------|
| **Token Impact** 🎯 | High / Med / Low | Tokens per occurrence × occurrences per period |
| **Risk** ⚠️ | Safe / Moderate / High | Can you undo it? Does it affect core function? |
| **Effort** 🔧 | Easy / Med / Hard | Single config change? Multi-file edit? Needs research? |

### How to Score

Compute a relative priority for each finding by inverting Risk and Effort:

```
Priority = ImpactWeight × (1 / RiskWeight) × (1 / EffortWeight)
```

Where each dimension maps to a simple numeric weight:
- Impact: High=3, Med=2, Low=1
- Risk: Safe=1, Moderate=2, High=3
- Effort: Easy=1, Med=2, Hard=3

Focus on items scoring ≥ 1.5 first. Skip items < 1.0 unless they are
trivially easy (effort=1) and safe (risk=1).

### Common High-Impact Patterns

These patterns tend to score high across most deployments:

| Pattern | Typical Impact | Typical Risk | Typical Effort |
|---------|---------------|-------------|----------------|
| Overly verbose task prompts | High | Safe | Easy |
| Heavy models on simple tasks | High | Safe | Easy |
| No active hours on heartbeat | Med-High | Safe | Easy |
| Duplicated content across bootstrap files | Med-High | Safe | Easy-Med |
| Full tool profile on task-specific agents | High | Moderate | Easy |
| Idle-time session not configured | Med | Safe | Easy |
| Outdated tool/plugin configs still loaded | Low-Med | Safe | Easy |

> ⚠️ **Checkpoint**: Show your top-3 priority items to the user.
> Confirm direction before starting optimization.
> If the highest-score items seem wrong, revisit Phase 1 measurements.

---

## Phase 3: OPTIMIZE — Apply Categorical Techniques

> ⚠️ **User confirmation gate**: Techniques marked **Moderate** or **High** risk
> involve config changes, profile switches, or task merging. Before applying them,
> present the proposed change using this template and get explicit approval:
>
> ```
> ## Proposed Change
> **Technique**: [category/technique name]
> **Target**: [file/config path]
> **Before**: [current state, chars/tokens if measurable]
> **After**: [proposed state, estimated savings]
> **Risk**: [Moderate/High]
> **Rollback**: [how to undo]
> ```
>
> Techniques marked **Safe** can be applied directly.

Each category below contains a set of techniques. Apply them in priority
order from Phase 2 — start with the highest-score items first, regardless
of which category they fall into.

### Failure Recovery

If a technique causes a problem:
- **Config change**: Restore the backed-up config file and reload.
- **Cron merge broken**: Restore the old separate cron job from version control
  or re-create it from the original prompt.
- **Profile switch issue**: Revert to "full" profile, report the missing tool.
- **Prompt compression over-aggressive**: Restore from the diff backup (keep
  pre-optimization prompt versions in a `prompts/backup/` directory).

### Category Selection Guide

Match your Phase 2 findings to the best starting category:

| Finding | Start With |
|---------|-----------|
| Verbose task prompts (background context, philosophy) | **A** Prompt Simplicity |
| Heavy models on simple automation tasks | **B** Model Tiering |
| Bootstrap files >2K chars each, duplicated content | **C** Context Slimming |
| Full tool profile, rarely-used tools registered | **D** Tool Profile Optimization |
| Verbose agent output, too many turns per task | **E** Output Discipline |
| No active hours, co-located tasks running separately | **F** Session Lifecycle |
| Repeated system prompts without caching structure | **G** Provider-Side Caching |
| Agent retries failed approaches instead of switching | **H** Behavioral Discipline |
| Simple/complex tasks both use premium model | **J** Intelligent Model Routing |

### Category Decision Tree

If you're not sure which category to start with, follow this tree from top
to bottom — the first match tells you your likely best starting category:

```
1. Is the main session slow or expensive?
   → Check B (tiering) and J (routing)
   → Also check D (too many tools loaded?)

2. Are cron jobs consuming more than expected?
   → Check A (prompts too wordy?), then B (wrong model?)
   → If F (same-tier jobs not batched?)

3. Is context getting cut off mid-task?
   → Check C (bootstrap too large?) → I (progressive disclosure?)
   → Then J3 (incremental delivery?)

4. Are agent outputs too verbose?
   → Check E (output discipline) → H (behavioral discipline)

5. Is the same heavy prompt repeated across tasks?
   → Check G (provider-side caching: fixed prefix first?)

6. Are you seeing the same errors repeatedly?
   → Check H2 (fail once, switch) → H4 (fix root cause)

7. Default (no obvious symptom):
   Run Phase 1 from scratch → Phase 2 will tell you where to go
```

> **Pro tip**: Start with G (Provider-Side Caching) if you use DeepSeek.
> Cache pricing is 0.83% of uncached — fixing prefix structure alone
> can cut token costs by 90%+.

### A. Prompt Simplicity

| Technique | Description | Risk |
|-----------|-------------|------|
| **A1** Strip preamble | Remove background/rationale paragraphs from task prompts. Keep only: trigger, action, output format.
  *Before:* "你是系统监控助手。每天检查服务器状态：CPU使用率>80%告警、内存>90%告警、磁盘>85%告警、SSL证书<30天告警。每个告警按严重程度分别处理：严重→立即通知值班、一般→发运维邮件、提示→记录日志。"
  *After:* "系统监控。检查：CPU(>80%) Mem(>90%) Disk(>85%) SSL(<30d)。告警：严重→立即、一般→邮件、提示→日志。" (360→110 chars, -69%) | Safe |
| **A2** Bullet points > prose | Replace multi-sentence descriptions with keyword checklists. | Safe |
| **A3** Constrain output | Add "Answer concisely in ≤3 lines" or equivalent to reduce generated tokens. | Safe |
| **A4** Remove redundancy | Delete "What NOT to do" sections — proper instructions make negatives implicit. | Safe |
| **A5** Reference > inline | Replace full instructions for sub-tasks with file references ("See X.md") when the referenced file is always loaded. | Safe |

### B. Model Tiering

| Technique | Description | Risk |
|-----------|-------------|------|
| **B1** Right-size each task | Map every automated task to the cheapest model that can do it adequately. Test borderline cases. | Safe |
| **B2** Define tier boundaries | Document which model(s) belong to each tier so new tasks are assigned correctly. | Safe |
| **B3** Batch same-tier runs | Schedule same-tier tasks back-to-back to reuse the same session (single context load). | Moderate |

### C. Context Slimming

| Technique | Description | Risk |
|-----------|-------------|------|
| **C1** Measure every boot file | List all files loaded at session start and identify those > 2K chars for potential trimming. | Safe |
| **C2** Cross-reference dedup | When the same content appears in 2+ files (e.g. "Core Principles" in SOUL.md and IDENTITY.md), keep it in one authoritative file and replace the others with a `详见 <file>` reference. | Safe |
| **C3** Archive aged-out content | Move old diary entries, superseded milestones, and historical promoted entries to a dedicated archive directory. | Safe |
| **C4** Trim to one-liner | Convert verbose descriptions to single-line summaries.
  *Before:* "This project's coding conventions were established after three code reviews revealed inconsistent patterns: use 2-space indent for HTML/CSS, 4-space for Python, tabs for Go. Prefix private methods with underscore. No Hungarian notation. Import order: stdlib, third-party, local."
  *After:* "Coding conventions (see CONTRIBUTING.md) — 6 rules, numbered."
  Actionable instructions stay; background context goes. | Safe |

### D. Tool Profile Optimization

| Technique | Description | Risk |
|-----------|-------------|------|
| **D1** Size your tool schema | Count all registered tools and estimate total schema chars. This is typically the single largest per-turn overhead. | Safe (measure only) |
| **D2** Switch profile per agent | Use "coding" profile for sub-agents/cron jobs (excludes browser, canvas, media generation, feishu tools). Use "full" only where those tools are actually needed. | Moderate (test on sub-agents first) |
| **D3** Disable unused tools | If you have disabled skills or orphaned plugin tools still registering schemas, disable or remove them from the registry. Check `skills.entries` and `plugins.load.paths`. | Safe |
| **D4** Create custom profile | If neither "full" nor "coding" fits, define a custom profile with exactly the 15-25 tools your use-case needs. Requires config reload. | High |

### E. Output Discipline

| Technique | Description | Risk |
|-----------|-------------|------|
| **E1** No operation narration | Remove "I'll...", "Let me check..." patterns. Do the action directly. | Safe (behavioral) |
| **E2** Lead with conclusion | Put the answer first. Add explanation only when needed. | Safe (behavioral) |
| **E3** Batch turns | Read → plan → apply all changes in as few turns as possible, instead of read→think→edit→think→verify per-item. Each extra turn adds LCM context overhead. | Safe (behavioral) |
| **E4** Sub-agent conciseness | When spawning sub-agents, specify a concise return format. Their full output is injected into context if returned. | Safe |

### F. Session Lifecycle

| Technique | Description | Risk |
|-----------|-------------|------|
| **F1** Set active hours | Configure `heartbeat.activeHours` so no work runs during idle time (overnight, weekends). | Safe |
| **F2** Isolated sessions | Set `heartbeat.isolatedSession: true` so periodic checks don't accumulate in the main session. | Safe |
| **F3** Light context | Set `heartbeat.lightContext: true` to skip loading all bootstrap files — only HEARTBEAT.md is injected. | Safe |
| **F4** Merge co-located tasks | If two cron jobs run within minutes of each other (e.g. both at 23:xx), merge them into one session with a combined prompt. Copy both prompts into one job's `message` field separated by a blank line, then remove the later job. Saves one full startup context per day. | Moderate |
| **F5** Merge example | Before: Job A at 23:00 (System health check), Job B at 23:10 (Log cleanup). After: Single job at 23:00 with prompt "Do A then B.~A: ...~B: ..." | Moderate |
| **F6** Configure queue | If the platform supports message queue settings (debounce, collect), tune them to prevent rapid-turn accumulation during tool execution. | Safe |

### G. Provider-Side Caching

> **Impact is 10× any other category.** DeepSeek V4 Pro cached price is 0.83% of
> uncached. Cache hit rates of 91-96% are achievable with proper prompt structure.

| Technique | Description | Risk |
|-----------|-------------|------|
| **G1** Fixed prefix first | Design all prompts as `[static prefix] + [dynamic suffix]`. Static prefix includes system instructions, bootstrap summary, and tool schemas. Dynamic suffix includes runtime instruction. This maximizes KV cache hits on the provider side.
  *Wrong:* "Analyze this code for memory leaks...你是代码审查助手，审查规则如下：..."
  *Right:* "你是代码审查助手，审查规则如下：...现在分析这段代码的内存泄漏：..." | Safe |
| **G2** Session contiguity | Don't insert unrelated messages between consecutive calls to the same model — this breaks the KV cache prefix. Batch related calls into a single turn instead. | Safe |
| **G3** Monitor cache rate | Check provider dashboards for cache hit rate. If <80%, your prefix structure likely has variability. Fix it. | Safe |
| **G4** Route to best caching provider | Different providers have wildly different cached prices. DeepSeek V4 Pro: 0.83% of uncached. MiniMax: ~20%. Route routine tasks to the provider with the best cache economics. | Moderate |

### H. Behavioral Discipline

> These are zero-config, zero-cost techniques. The savings come from how you use
> the system, not how it's configured.

| Technique | Description | Risk |
|-----------|-------------|------|
| **H1** Default to working path | Use known-working tools before alternatives. Don't retry tools known to be broken in the current deployment — each retry is a wasted tool call + error response.
  *Bad:* web_search (broken) → error → web_search again → error → baidu-search → works
  *Good:* baidu-search → works (first attempt) | Safe |
| **H2** Fail once, switch | If a method fails, switch immediately to a known alternative. Don't retry the same approach with slightly different parameters. Each retry costs full tool-call tokens. | Safe |
| **H3** Batch > Poll | Gather all data before acting instead of incrementally. One `exec` or `read` call that returns 10 results costs less than 5 separate calls returning 2 each. | Safe |
| **H4** Fix root cause | If a tool works inconsistently due to a known config issue (API key expired, wrong provider), fix the config. Working around it each time costs more in accumulated failed calls. | Safe |

### I. Context Engineering (2026-05-12 新增)

> Context Engineering 是 2026 年从 Prompt Engineering 演进出的上层方法论。
> 核心原则：渐进式披露 (Progressive Disclosure) — 仅在任务需要时加载特定模块。
> 北京大学论文《Meta Context Engineering via Agentic Skill Evolution》实测：
> Token 消耗降低 60%，任务成功率提升 45%。

| Technique | Description | Risk |
|-----------|-------------|------|
| **I1** Progressive disclosure | 按任务类型分级加载系统能力描述。不需要的技能说明不加载。与 token-saver 的 C1-C4 互补：C 系列负责文件级裁剪，I1 负责能力级裁剪。
  Wrong: Agent 启动时加载全部技能描述
  Right: Agent 启动时按任务类型加载对应技能（搜索类任务只加载搜索相关技能描述） | Safe |
| **I2** Semantic context scoring | 用语义重要性评分代替固定滑动窗口。计算历史交互与当前 query 的语义相似度，只保留 top-3 + 最近 1 轮。
  推荐实现：Sentence-BERT 计算余弦相似度，按得分排序裁剪到 token budget。
  参考开源项目：Agent Skills for Context Engineering | Safe |
| **I3** Fixed prefix pattern | 设计所有 prompt 为「static prefix + dynamic suffix」。静态前缀包括系统指令、bootstrap 摘要、工具 schema 描述。动态后缀包括本次运行指令。最大化 provider 端 KV cache 命中。
  Wrong: 每次运行时先写任务指令再补系统描述
  Right: 系统描述在前，任务指令在后 | Safe |
| **I4** Tool call circuit breaking | 在调用高成本外部工具（SQL 查询、图像生成、文件写入）前增加预检代理。校验参数合法性 + 资源预估。超限或非法直接拒绝，不触发实际调用。
  适用场景：web_fetch 超长 URL、exec 高风险命令、文件写入大文件。 | Safe |
| **I5** Cost-aware context pruning | 按 taskType 和 budget tokens 动态决定上下文精度。简单任务用精简 prompt，复杂任务才加载完整能力描述。
  实现：在 cron payload 中嵌入 task_type 字段，根据该字段调度上下文模板。 | Safe |

### J. Intelligent Model Routing (2026-05-14 新增)

> 基于 OpenSquilla（开源 Token 优化引擎）方案。
> Core insight: 路由决策本身不消耗 Token — 在本地判定任务复杂度后决定走哪个模型。
> 与 B 系列（Model Tiering）的区别：B 说"每个任务应该固定分配一个 tier"，
> J 说"同一个任务的每一次调用动态判断走哪个 tier"。

| Technique | Description | Risk |
|-----------|-------------|------|
| **J1** Dynamic inbound grading | 对每次入站请求做轻量复杂度判定（prompt length + expected reasoning depth + tool count），自动路由到对应 tier 的模型。
  判定规则示例：
  - 🟢 Economy: 简单信息查询（token 消耗 < 1K，无推理要求）→ sensenova-6.7-flash-lite / minimax-m2.7
  - 🟡 Standard: 一般分析任务（1K-5K，轻度推理）→ deepseek-v4-flash
  - 🏆 Premium: 深度推理（>5K，复杂推理/多工具）→ deepseek-v4-pro
  实现：在 cron/子代理 payload 中嵌入 `model` 字段，或使用中间路由代理做分类。
  *Before:* 所有每日 cron 统一用 deepseek-v4-pro，包括简单版本检查
  *After:* 版本检查→sensenova-6.7-flash-lite，领域探针→deepseek-v4-flash，
           深度分析→deepseek-v4-pro。按任务特征分级，非一刀切。 | Safe |
| **J2** Local routing decision | 路由判定在本地完成（不需要发 request 到远程判断路由）。
  方案：在任务 payload 中预置 `routing_hint` 字段（economy/standard/premium），
  由编排层基于任务特征（prompt length、任务类型、预期工具调用数）决定。
  *Bad:* 每次调用先发一个轻量请求问"这个走哪个模型？"（浪费 Token）
  *Good:* 任务描述本身包含路由线索，编排层本地匹配 | Safe |
| **J3** Incremental context delivery | OpenSquilla 核心方案之一：先发送最小必要上下文，不足时增量补充。
  与 C 系列（Context Slimming）区别：C 是文件级裁剪（减少启动加载量），
  J3 是调用级递进（先发主干，模型需要时再发细节）。
  实现：prompt 中先给出高度压缩的摘要版本，后面用"如需详情请见"标记展开点。
  结合 OpenClaw 的 lossless-claw 机制：LCM 摘要本身已经是一个渐进式实现。 | Safe |
| **J4** Cache-aware routing | 统计各 provider 的 KV cache 命中率，优先路由到命中率高的 provider。
  当前已知：DeepSeek V4 Pro cache price = 0.83% of uncached。
  如果命中了缓存的 prompt prefix（含 bootstrap + 技能描述），成本降低 99%+。
  实现：在路由时优先选择上次使用同一模型+同一 prefix 结构的 provider。 | Moderate |
| **J5** Fallback chain | 当分配的路由模型不可用（API 超时/限流/报错），自动降级到备用模型。
  与 H2（Fail once, switch）的区别：H2 是行为纪律（失败了就换方法），
  J5 是配置级的自动 failover 链。
  示例 Fallback Chain：
  1️⃣ deepseek-v4-pro → 2️⃣ deepseek-v4-flash → 3️⃣ sensenova-6.7-flash-lite
  实现：在 cron/子代理 payload 中使用 `fallbacks` 字段配置降级顺序。
  *Before:* cron job 用 minimax-m2.7，卡死后无降级 → 任务永远失败
  *After:* 同一 cron 配置 `fallbacks: ["deepseek-v4-flash", "deepseek-v4-pro"]` →
           minimax 卡死后自动切到 deepseek-v4-flash 执行 | Safe |

> **权衡**：智能路由的收益上限取决于任务复杂度分布。如果 80% 的任务是简单查询，
> 智能路由的 Token 节省可达 60-80%。如果大部分任务已经是标准/经济 tier，
> 额外收益有限。建议做一次任务复杂度分布扫描后再选择启用哪些 J 技术。

---

## Phase 4: VALIDATE — Confirm Results

### 4A Prompt Length Delta

Before/after comparison of all modified prompts and files. Include total
chars and estimated tokens saved.

### 4B Config Integrity

After editing JSON configuration files, validate:

```bash
python3 -c "import json; json.load(open('<config-path>')); print('OK')"
```

### 4C Functional Test

- Verify cron tasks still start correctly (check `cron action=runs` or next
  scheduled trigger)
- Verify heartbeat runs in configured active window
- Read through compressed cron prompts to ensure key instructions survive

### 4D Generate Report

Write `token-audit-report-YYYY-MM-DD.md` summarizing:
- Changes made and per-change token savings
- Total estimated weekly token reduction
- Items deferred and why
- Recommended next optimization

Log each optimization cycle in `results.tsv` (see skill directory for
format reference). This creates an audit trail for the quarterly deep audit (5B).

---

## Phase 5: MONITOR — Guard Against Regrowth

### 5A Periodic Token Watch (Optional)

Optionally create a weekly cron (cheapest available model) that checks
prompt lengths haven't crept back:

```json
{
  "name": "token-watch-weekly",
  "schedule": { "kind": "cron", "expr": "0 10 * * 1", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "model": "<cheapest-model>",
    "message": "Check all cron prompt lengths. Flag any that grew >20% since last baseline.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

### 5B Quarterly Deep Audit

Run the full Phase 1-4 cycle every quarter using the cheapest available
model. Compare results against previous reports to spot regrowth trends.

The quarterly audit MUST include:
- Compare each cron's prompt length against last audit baseline
- Check if unused categories crept back (complacency regrowth)
- Verify all J routing hints still reflect actual task complexity
- Re-run the Priority Matrix from Phase 2 to catch new high-impact items

### 5C Real-Time Drift Alerts (Optional)

When token consumption suddenly spikes, it's usually one of three causes.
Know which one:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| A specific cron doubled in token count | Prompt crept back (someone added preamble) | A1 Strip preamble |
| All crons increased proportionally | Model changed (e.g. dev switched back to pro from flash) | B1 Right-size, check default model |
| Session-level spikes, not cron | Tool profile expanded / new plugin registered | D1 Size tool schemas, check profile |
| Intermittent spikes | Prefix changed → KV cache missed | G1 Fixed prefix, check for variation |

If you have access to provider dashboards:
- **Monitor cache hit rate** — DeepSeek dashboard shows prefix cache stats
- **If hit rate drops below 80%** -> inspect recent prompt changes for prefix variation
- **Track per-model token consumption weekly** — a 2× week-over-week jump is a red flag

---

## Safety Boundaries

### Configs That Need Gateway Restart

Some configuration paths require a gateway restart to take effect:
- `agents.defaults.heartbeat.*` (edit config file + restart)
- `agents.list[].tools.profile`
- `gateway.*`, `auth.*`
- `plugins.*` — certain sub-fields

### What NOT to Compress

These core mechanisms must be preserved even in an aggressive token budget:
- Error detection logic (consecutive errors, failure alerts)
- Essential signal handling (high-priority alerts → auto-escalation)
- Drift detection for recurring tasks

### External References

- OpenClaw Cron Jobs: https://docs.openclaw.ai/automation/cron.md
- OpenClaw Standing Orders: https://docs.openclaw.ai/automation/standing-orders.md
- OpenClaw Gateway Config: `openclaw gateway config` CLI
- OpenClaw Agent Profiles: `agents.list[].tools.profile` in openclaw.json
- Test Prompts: `test-prompts.json` in skill directory
- Results Log: `results.tsv` in skill directory

---

## Appendix: Local Deployment Configuration

This section is populated by the first execution of the Token Saver in a
specific deployment. Replace the example values below with real ones.

### Configuration Paths

| Item | Example Path |
|------|-------------|
| Cron jobs | `~/.openclaw/cron/jobs.json` |
| Gateway config | `~/.openclaw/openclaw.json` |
| Workspace root | `~/.openclaw/workspace/` |
| Bootstrap files | AGENTS.md, SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, IDENTITY.md, TOOLS.md, STANDING-ORDERS.md |

### Baseline Measurements (example: Wave 2026-05-04)

| File | Initial Size | After First Pass | Reduction | Techniques Used |
|------|-------------|------------------|-----------|----------------|
| SOUL.md | 7,034 | 3,521 | -50% | C2 (cross-ref), C4 (one-liner), A2 |
| STANDING-ORDERS.md | 10,960 | 3,816 | -65% | C2 (cross-ref), A4 (remove redundancy) |
| IDENTITY.md | 6,228 | 4,313 | -31% | C2 (dedup with SOUL.md), C4 |
| AGENTS.md | 5,072 | 2,691 | -47% | C2 (ref to STANDING-ORDERS), C4 |
| TOOLS.md | 8,893 | 7,488 | -16% | C4 (remove stale entries) |
| MEMORY.md | 30,224 | 26,420 | -13% | C3 (archive promoted entries) |
| **Total** | **68,411** | **48,249** | **-29%** | — |

Per-session token savings from bootstrap compression: ~6,720 tokens.

### Benchmark: Compression by File Type

| File Type | Typical Savings | Best Technique |
|-----------|----------------|----------------|
| Program/Protocol (STANDING-ORDERS.md) | 55-65% | A4 (remove boilerplate sections) |
| Guide/Identity (SOUL.md, IDENTITY.md) | 30-50% | C2 (cross-reference dedup) |
| Instructions (AGENTS.md) | 40-50% | C2 (replace lists with file refs) |
| Knowledge base (MEMORY.md) | 10-20% | C3 (archive old entries only) |
| Config/state table (TOOLS.md) | 10-20% | C4 (remove stale entries only) |

### Task-to-Model Map

| Task | Model Tier | Model |
|------|-----------|-------|
| Version check | Economy | minimax-m2.7 |
| Demand scanning | Standard | deepseek-v4-pro (needs search) |
| Domain probe | Economy | minimax-m2.7 |
| Dreaming (memory integration) | Economy | minimax-m2.7 |
| Doc maintenance | Economy | minimax-m2.7 |
| WaveCap daily expansion | Standard | deepseek-v4-pro (needs reasoning) |
| Weekly review | Premium | deepseek-v4-pro |
| Friday topic selection | Premium | deepseek-v4-pro |
| Main session | Standard | deepseek-v4-flash |

### Deferred Items

| Item | Reason | Condition to Revisit |
|------|--------|---------------------|
| Tool profile for main agent | High risk (may break unexpected features) | After sub-agent coding profile proven in production for 1 week |
| Cron task merging | Needs user confirmation; may affect reliability | Next token audit cycle |
| Compaction mode change (safeguard→normal) | Needs config reload | When gateway restarted for other reasons |

### Deployment-Specific Constraints

- **Network**: GFW blocks chatgpt.com, api.openai.com. All OpenAI/Codex models unavailable.
- **Models available**: deepseek-v4-pro (premium), deepseek-v4-flash (standard),
  minimax-m2.7 (economy).
- **File paths**: Standard OpenClaw paths under `~/.openclaw/`.
- **Git**: Workspace is a git repository; all changes version-controlled.
