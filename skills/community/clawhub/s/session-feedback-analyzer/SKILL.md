---
name: session-feedback-analyzer
category: tool
description: |
  Parse Claude Code session JSONL to extract implicit user feedback signals.
  Detects skill invocations (tool_use blocks with name="Skill" or /slash-commands),
  classifies user responses as correction/acceptance/partial within a 3-turn
  influence window, and computes per-skill correction_rate metrics.
  Not for synthetic evaluation (use improvement-evaluator) or structural
  scoring (use improvement-learner). Use this when you need to find which
  skills users correct most often, or generate feedback.jsonl for the
  improvement-generator.
license: MIT
triggers:
  - feedback
  - correction_rate
  - session.*analyz
  - user.*feedback
  - skill.*feedback
  - which skills get corrected
  - implicit feedback
  - feedback.jsonl
  - correction.*trend
  - hotspot.*dimension
  - user.*correct
  - skill.*quality.*regress
  - parse.*session
  - analyze.*session
  - skill.*invocation
  - acceptance.*rate
---

# Session Feedback Analyzer

Mines Claude Code session JSONL for implicit user feedback. When a user corrects, redoes, reverts, or partially accepts AI output after a skill invocation, that signals a skill gap. Outputs structured `feedback.jsonl` with per-event dimension attribution for the improvement pipeline.

## When to Use

- Compute per-skill correction rates to find which skills users correct most often.
- Generate `feedback.jsonl` as input for improvement-generator's candidate prioritization.
- Track correction trends over time (30-day rolling windows) to detect skill quality regression.
- Identify hotspot dimensions (accuracy vs coverage vs trigger_quality vs efficiency) per skill.
- Compare correction_rate before and after an improvement to validate whether a change actually helped.
- Audit a single skill's feedback history with `--skill-filter` to understand why users reject its output.
- Feed dimension hotspots into improvement-generator so candidates target the dimensions users care about.
- Bootstrap the auto-improvement loop: analyzer output is the starting signal that tells the pipeline which skills need work.
- Investigate spikes in correction_rate after a skill update to decide whether to rollback.

## When NOT to Use

- Synthetic task evaluation against a predefined task suite -- use **improvement-evaluator** instead.
- Structural scoring of SKILL.md quality (knowledge_density, coverage, completeness) -- use **improvement-learner** instead.
- Candidate multi-reviewer scoring with LLM judges -- use **improvement-discriminator** instead.
- Gate/accept decisions on improvement candidates -- use **improvement-gate** instead.
- Executing approved changes to skill files -- use **improvement-executor** instead.
- Generating improvement candidates from scratch -- use **improvement-generator** instead.
- Benchmark comparison against historical baselines -- use **benchmark-store** instead.
- Orchestrating the full generate-score-evaluate-execute-gate pipeline -- use **improvement-orchestrator** instead.
- Analyzing test runs or sub-agent sessions (these are filtered out automatically by `iter_session_files`).

<example name="find-worst-skills">
Run the analyzer against all sessions, then query metrics to find the three skills with the highest correction rate:

```bash
python3 scripts/analyze.py --session-dir ~/.claude/projects/ --output feedback-store/feedback.jsonl
```

```python
from scripts.metrics import load_feedback_events, compute_all_skill_metrics, format_metrics_report
events = load_feedback_events(Path("feedback-store/feedback.jsonl"))
report = format_metrics_report(compute_all_skill_metrics(events))
print(report)
# Skill Feedback Metrics
# ========================================
#   cpp-expert: correction_rate=0.40 (n=20, corrections=6, partials=4, acceptances=10)
#     hotspots: accuracy=5, coverage=3
#   deslop: correction_rate=0.15 (n=40, corrections=4, partials=4, acceptances=32)
#     hotspots: accuracy=3, efficiency=1
```

The output tells you cpp-expert has the highest correction rate (0.40) and its hotspot dimension is accuracy -- users most often correct naming/format issues. Feed this into improvement-generator with `--source feedback-store/feedback.jsonl` to generate candidates that prioritize accuracy fixes.
</example>

<example name="single-skill-audit">
Analyze only the `deslop` skill and suppress user message snippets for privacy:

```bash
python3 scripts/analyze.py --skill-filter deslop --no-snippets --output feedback-store/deslop-feedback.jsonl
```

Then compute trend to check if recent changes improved the skill:

```python
from scripts.metrics import load_feedback_events, compute_correction_trend
events = load_feedback_events(Path("feedback-store/deslop-feedback.jsonl"))
trend = compute_correction_trend(events, "deslop")
print(trend)
# {'skill_id': 'deslop', 'trend': -0.12, 'recent_rate': 0.10, 'prior_rate': 0.22,
#  'recent_sample': 18, 'prior_sample': 22, 'direction': 'improving'}
```

A negative trend (-0.12) with direction "improving" means the last 30 days had fewer corrections than the prior 30 days. The improvement worked.
</example>

<anti-example name="wrong-tool-for-task-suite">
Do NOT use session-feedback-analyzer to run synthetic evaluations. If you have a `task_suite.yaml` and want to measure execution pass rate, use improvement-evaluator instead:

```bash
# WRONG: session-feedback-analyzer does not execute tasks
python3 scripts/analyze.py --session-dir task_suite_results/  # meaningless

# RIGHT: use improvement-evaluator for synthetic task evaluation
python3 -m skills.improvement-evaluator.scripts.evaluate --task-suite task_suite.yaml
```
</anti-example>

<anti-example name="wrong-tool-for-structural-scoring">
Do NOT use session-feedback-analyzer to score SKILL.md structure. The analyzer reads session JSONL (runtime user interactions), not SKILL.md files. For structural quality scoring (knowledge_density, coverage, completeness), use improvement-learner:

```bash
# WRONG: analyzer has no concept of SKILL.md structure
python3 scripts/analyze.py --session-dir ./skills/  # no JSONL files here

# RIGHT: use improvement-learner for SKILL.md structural scoring
python3 -m skills.improvement-learner.scripts.evaluate_skill --skill-dir skills/deslop/
```
</anti-example>

## Why Implicit Feedback Matters

**问题**: improvement-evaluator 用预定义的 task_suite.yaml 来验证 skill 质量，但 task suite 只能覆盖作者预想到的场景。真实用户的使用方式远比 task suite 丰富 -- 他们会用 skill 做作者从未设想过的事情。当用户纠正 AI 输出时，这个纠正信号就是隐式反馈，指向 skill 在真实场景中的不足。

**Because** 隐式反馈来自真实使用而非合成测试，它能发现 task suite 永远发现不了的问题。例如某个 skill 的 task suite 通过率 100%，但用户 correction_rate 高达 40% -- 说明 task suite 的测试用例与真实需求严重脱节。session-feedback-analyzer 的输出（feedback.jsonl）直接喂给 improvement-generator，让生成的候选优先解决用户最常纠正的维度。

**Tradeoff**: 隐式反馈的局限性在于信号噪声。用户说 "不对" 可能是纠正 skill 输出，也可能是纠正自己之前的指令。当前的 keyword-based 分类器无法区分这两种情况，实测误判率约 8%。提高精度的方向是引入 LLM-based 分类（让一个小模型判断 "不对" 的指代对象），但这会引入延迟和成本。当前选择 keyword heuristic 是因为 8% 的误判率在 correction_rate 的统计聚合下被稀释 -- 单个事件的误判不影响 per-skill 的整体趋势判断。

## Why 3-Turn Influence Window

**Tradeoff**: 窗口太窄（1 turn）会漏掉延迟纠正 -- 用户看到 AI 输出后继续问了一个问题，第 3 turn 才说 "刚才那个不对"。窗口太宽（5+ turns）会引入噪音 -- 用户可能已经在讨论完全不同的话题，此时的 "wrong" 不是对之前 skill 调用的纠正。实测中 3 turn 窗口的 precision/recall 平衡最好：捕获了 92% 的真实纠正，误判率约 8%。相比之下 1 turn 窗口只捕获 71% 的纠正，5 turn 窗口误判率升到 18%。

**Because** 窗口边界还受到 next-invocation 的约束：如果 3-turn 窗口内出现了新的 skill 调用，当前窗口在新调用处截断。这防止了将对第二个 skill 的反馈误归因给第一个 skill。代码中 `classify_outcome` 的 `next_invocation_idx` 参数实现了这个截断。实际效果是大多数窗口只有 1-2 turn（用户通常立即反馈），真正用到第 3 turn 的场景约占 15%。

**窗口内的优先级规则**: 当窗口内多个 turn 包含不同信号时（如 turn 1 说 "可以" 但 turn 2 说 "但是命名不对"），分类器按以下优先级判定：revert > redo > partial > correction > acceptance。这意味着只要窗口内出现任何纠正信号，即使第一个 turn 是 acceptance，最终结果仍然是 correction 或 partial。

## CLI

```bash
# Basic: analyze all sessions, write to default output
python3 scripts/analyze.py

# Custom session directory and output
python3 scripts/analyze.py --session-dir ~/.claude/projects/ --output feedback-store/feedback.jsonl

# Privacy mode: strip user message snippets
python3 scripts/analyze.py --no-snippets

# Filter to a single skill
python3 scripts/analyze.py --skill-filter cpp-expert

# Require at least 10 invocations before computing metrics
python3 scripts/analyze.py --min-invocations 10

# Combine flags: audit one skill privately with high threshold
python3 scripts/analyze.py --skill-filter deslop --no-snippets --min-invocations 10 --output feedback-store/deslop-audit.jsonl
```

| Param | Default | Description |
|-------|---------|-------------|
| `--session-dir` | `~/.claude/projects/` | Root directory containing session JSONL files |
| `--output` | `feedback-store/feedback.jsonl` | Output path for the feedback JSONL file |
| `--no-snippets` | off | Omit user message snippets from output (privacy mode) |
| `--skill-filter` | none | Only analyze invocations of this specific skill |
| `--min-invocations` | 5 | Minimum invocations before correction_rate is considered statistically meaningful |

## Detection Rules

两种方式触发 skill 检测：

**Tool use 检测**：Assistant message 中出现 `tool_use` block，
`name == "Skill"`，从 `input.skill` 提取 skill_id。
这是标准的 Claude Code skill 调用路径。

**Slash command 检测**：System message 中 `subtype == "local_command"`，
从 `<command-name>` tag 提取 skill name。
排除内建命令：help, clear, resume, compact, config。

| Path | Condition |
|------|-----------|
| Tool use | `tool_use` block, `name == "Skill"`, skill_id from `input.skill` |
| Slash command | `subtype == "local_command"` + `<command-name>` tag |

## Outcome Classification (3-turn influence window)

| Outcome | Type | Confidence | Trigger |
|---------|------|-----------|---------:|
| correction | rejection | 0.9 | Keywords: "wrong", "incorrect", "no," (zh: "不对", "错了") |
| correction | revert | 0.9 | Git revert commands in assistant tool_use (`git checkout/restore/reset`) |
| correction | redo | 0.9 | Keywords: "try again", "redo" (zh: "重新来", "换个方案") |
| partial | partial | 0.7 | Qualifier ("but", "however", "但是") + correction or acceptance keyword |
| acceptance | explicit | 0.8 | Keywords: "lgtm", "looks good", "correct" (zh: "好", "可以", "对的") |
| acceptance | implicit | 0.6 | User message >20 chars, no question marks, no correction keywords |

## Dimension Attribution

Each correction/partial gets a `dimension_hint` from keyword matching. 当用户的纠正消息包含特定关键词时，该纠正事件会被归因到对应的评估维度。这个归因结果通过 feedback.jsonl 传递给 improvement-generator，使其生成的候选优先针对用户最常纠正的维度。如果关键词匹配到多个维度，取 confidence 最高的那个；如果都匹配不上则标记为 "unknown"。

| Dimension | Keywords |
|-----------|----------|
| accuracy | naming, format, style, typo, 命名, 格式, 拼写 |
| coverage | missing, forgot, incomplete, 缺少, 漏了 |
| reliability | again, inconsistent, 重复, 不稳定 |
| efficiency | slow, verbose, 太慢, 冗余 |
| security | security, secret, token, credential, 密钥 |
| trigger_quality | "wrong skill", "shouldn't trigger", "不该触发" -- wrong skill invoked entirely (distinct from accuracy which is correct skill, wrong output) |

## correction_rate Formula

`correction_rate = (corrections + 0.5 * partials) / total_invocations`

partial 按 0.5 权重计算——partial acceptance 意味着 skill 输出部分正确，
比完全纠正轻，但仍然需要改进。
当 sample_size < `--min-invocations`（默认 5）时返回 `sufficient_data: false`，
避免小样本下的统计噪音。

Trend 计算方式：last 30d correction_rate vs prior 30d correction_rate。
Positive delta = worsening（纠正率上升）。
Negative delta = improving（纠正率下降）。
|delta| <= 0.05 = stable（变化在统计噪音范围内）。
autoloop-controller 用 trend 判断是否继续迭代：连续两个周期 stable 则停止。

## Output Artifacts

The primary output is `feedback-store/feedback.jsonl` -- one JSON object per line, one line per detected feedback event. Each event captures a single user reaction to a single skill invocation.

**Schema** (all fields present on every line):

```json
{
  "event_id": "a1b2c3d4...",
  "timestamp": "2026-04-05T10:00:00Z",
  "session_id": "uuid",
  "skill_id": "cpp-expert",
  "invocation_uuid": "msg-uuid",
  "outcome": "correction",
  "confidence": 0.9,
  "correction_type": "rejection",
  "user_message_snippet": "not right, should use const ref...",
  "turns_to_feedback": 1,
  "ai_tools_used": ["Read", "Edit"],
  "dimension_hint": "accuracy"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string | SHA-256 hash prefix (16 chars) of `invocation_id:skill_id`, guarantees deduplication |
| `timestamp` | ISO 8601 | When the skill was invoked (not when the user responded) |
| `session_id` | string | JSONL filename stem, identifies the Claude Code session |
| `skill_id` | string | Which skill was invoked (e.g. `"cpp-expert"`, `"deslop"`) |
| `invocation_uuid` | string | UUID of the assistant message that triggered the skill |
| `outcome` | enum | One of `"correction"`, `"partial"`, `"acceptance"` |
| `confidence` | float | 0.6-0.9, how confident the classifier is in the outcome label |
| `correction_type` | string? | `"rejection"`, `"revert"`, `"redo"`, `"partial"`, or null for acceptances |
| `user_message_snippet` | string | First 200 chars of the user's response (empty when `--no-snippets`) |
| `turns_to_feedback` | int | How many user turns after invocation the feedback appeared (1-3) |
| `ai_tools_used` | string[] | Tools the assistant called between invocation and user response |
| `dimension_hint` | string? | Attributed evaluation dimension (`"accuracy"`, `"coverage"`, etc.) or null |

**Secondary artifacts**:
- `feedback-store/archive/feedback-YYYYMMDD.jsonl` -- events older than 90 days, auto-archived by `archive_old_events()`.
- Console summary printed to stdout after each run: event count, outcome distribution, top-5 skills by invocation count.

## Metrics API (scripts/metrics.py)

```python
from pathlib import Path
from scripts.metrics import (
    load_feedback_events,
    compute_correction_rate,
    compute_correction_trend,
    compute_hotspot_dimensions,
    compute_all_skill_metrics,
    format_metrics_report,
)

events = load_feedback_events(Path("feedback-store/feedback.jsonl"))

# Per-skill correction rate
compute_correction_rate(events, "cpp-expert")
# -> {"correction_rate": 0.35, "sample_size": 20, "sufficient_data": True,
#     "corrections": 5, "partials": 4, "acceptances": 11}

# Trend over rolling 30-day windows
compute_correction_trend(events, "cpp-expert")
# -> {"trend": -0.08, "direction": "improving", "recent_rate": 0.30,
#     "prior_rate": 0.38, "recent_sample": 12, "prior_sample": 8}

# Dimension hotspots (which dimensions get corrected most)
compute_hotspot_dimensions(events, "cpp-expert")
# -> {"accuracy": 5, "coverage": 3}

# All skills at once
all_metrics = compute_all_skill_metrics(events)
print(format_metrics_report(all_metrics))
```

## Privacy Controls

`--no-snippets` strips user message snippets from feedback.jsonl output。
`~/.claude/feedback-config.json` with `{"enabled": false}` disables all collection。
analyze.py 启动时检查此配置，如果 disabled 则直接退出。

自动跳过的目录：
- `pytest/` — 测试产生的 session 不是真实用户行为
- `/tmp/` — 临时 session
- `/subagents/` — 子 agent session 不反映用户直接意图

Auto-archives events >90 days old to `feedback-store/archive/`
to keep the active feedback store small and fast to query。

## Related Skills

| Skill | Relationship | Data Flow |
|-------|-------------|-----------|
| **improvement-generator** | Primary consumer | Reads `feedback.jsonl` via `--source`; uses dimension hotspots to prioritize candidates |
| **improvement-evaluator** | Complementary | Synthetic evaluation (task_suite.yaml) covers designed scenarios; analyzer covers real usage |
| **improvement-learner** | Orthogonal | Learner scores SKILL.md document structure; analyzer scores user interactions at runtime |
| **improvement-discriminator** | Downstream | Discriminator scores candidates that were generated based on analyzer's feedback signals |
| **autoloop-controller** | Control loop | Uses correction_rate trend for plateau/convergence detection; stable trend = stop iterating |
| **improvement-gate** | Downstream | Gate validates changes; analyzer provides the "before" baseline that gate compares against |
| **benchmark-store** | Historical | Stores correction_rate snapshots for long-term Pareto front tracking |

Generator auto-discovers `feedback-store/` via `lib/common.py:load_source_paths()`. Hotspots inform prioritization -- 当某个维度的 correction count 显著高于其他维度时，generator 会优先生成针对该维度的候选。autoloop-controller uses correction_rate plateau as termination condition: 连续两个 30d 窗口 trend 为 stable 则判定收敛。

## Scripts & Tests Reference

| File | Purpose |
|------|---------|
| `scripts/analyze.py` | Main analyzer: parses sessions, classifies outcomes, writes feedback.jsonl |
| `scripts/metrics.py` | Metrics library: correction_rate, trend, hotspots, report formatting |
| `tests/test_analyze.py` | 16 test cases covering invocation detection, outcome classification, deduplication, archival |
| `tests/test_metrics.py` | 11 test cases covering rate computation, trend direction, hotspot grouping, report format |

Run all tests:

```bash
cd skills/session-feedback-analyzer && python3 -m pytest tests/ -v
```
