# Architecture / 架构设计

## Overview / 概述

`smartness-eval` is a four-layer evaluation pipeline that transforms raw runtime data and test outcomes into a single structured intelligence score.

`smartness-eval` 是一个四层评估管道，将原始运行数据和测试结果转化为结构化的智能度评分。

---

## Data Flow / 数据流

```
┌─────────────────────────────────────────────────────────────────┐
│                      config/task-suite.json                     │
│                   (28 test definitions + probes)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Layer 1: Test Execution / 测试执行层                │
│                                                                 │
│  select_tests() ──► validate_command() ──► subprocess.run()     │
│                                                                 │
│  • Selects tests by mode tags (quick/standard/deep)             │
│  • Validates command safety (whitelist, no -c, no abs path)     │
│  • Injects random anti-gaming probes                            │
│  • Captures stdout/stderr/exit code per test                    │
│  • Supports repeated runs for pass@k reliability (deep mode)   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ test results[]
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Layer 2: Metric Ingestion / 指标采集层              │
│                                                                 │
│  collect_metrics(window_days)                                   │
│                                                                 │
│  Reads from:                                                    │
│  ┌──────────────────────┬────────────────────────────────┐      │
│  │ state/*.json         │ latency, errors, cron, alerts  │      │
│  │ .reasoning/*.sqlite  │ reasoning store (SQLite)       │      │
│  │ state/reflection-*   │ reflection report count        │      │
│  │ state/benchmark-*    │ benchmark pass rate history    │      │
│  │ state/message-*      │ real interaction log sampling  │      │
│  │ regression-metrics   │ duplicate rate, dispatch P95   │      │
│  └──────────────────────┴────────────────────────────────┘      │
│                                                                 │
│  All reads are time-window filtered (3/7/30 days by mode)       │
│  Missing files → graceful fallback defaults, never crash        │
└──────────────────────────┬──────────────────────────────────────┘
                           │ metrics{}
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Layer 3: Scoring / 评分合成层                       │
│                                                                 │
│  compute_task_scores()  →  per-dimension task pass rate          │
│  merge_scores()         →  blend task + metrics per dimension   │
│  weighted_overall()     →  single 0–100 score                   │
│  compute_ci()           →  95% confidence interval              │
│  compute_trend()        →  delta vs previous run                │
│  dim_spread()           →  variance across dimensions           │
│                                                                 │
│  Formula per dimension:                                         │
│    score = Σ(task_weight × task_pass + metric_weight × metric)  │
│                                                                 │
│  See docs/SCORING.md for all 12 formulas.                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ result{}
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Layer 4: Output / 输出层                            │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  JSON run file     → runs/<timestamp>.json             │     │
│  │  Markdown report   → reports/<date>.md                 │     │
│  │  History append    → history.jsonl                     │     │
│  │  stdout            → JSON or Markdown (--format)       │     │
│  │  LLM judge (opt)   → external API → judge_score        │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Components / 核心组件

### eval.py (~960 lines)

| Function | Purpose / 用途 |
|----------|----------------|
| `validate_command()` | Security gate: whitelist check before any subprocess call / 安全门控 |
| `run_cmd()` | Execute command with timeout and capture / 执行命令 |
| `evaluate_test()` | Run one test, parse output by type (json_path, stdout_contains, exit_code) / 单测试执行 |
| `select_tests()` | Filter tests by mode tags / 按模式筛选测试 |
| `generate_probe_tests()` | Create random anti-gaming probes / 生成反作弊探针 |
| `collect_metrics()` | Read all state files within time window / 采集运行指标 |
| `query_reasoning_store()` | SQLite query for reasoning depth stats / 查询推理知识库 |
| `merge_scores()` | Blend task scores + metrics into 14 dimension scores (incl. planning, hallucination_control) / 合成维度分数 |
| `weighted_overall()` | Weighted sum → single score / 加权总分 |
| `compute_ci()` | 95% confidence interval from repeated runs / 置信区间 |
| `compute_trend()` | Delta comparison with previous run / 趋势对比 |
| `llm_judge()` | Optional: call external LLM for subjective scoring / LLM 裁判 |
| `build_markdown()` | Generate human-readable Markdown report / 生成报告 |

### state_probe.py

Lightweight script that replaces inline `python -c` commands with safe, auditable probes:

| Probe | What it checks / 检测内容 |
|-------|--------------------------|
| `quality-gate-prompt` | Verifies thought-quality-gate script contains required prompt dimensions / 质量门控结构 |
| `latency-state-count` | Counts records in latency metrics file / 延迟记录数 |
| `rule-candidates` | Reads auto-generated rule candidate count / 规则候选数量 |

### check.py

Verifies that all required skill files exist (SKILL.md, _meta.json, config/, scripts/).
用于验证技能目录结构完整性。

---

## Security Architecture / 安全架构

```
User config                       eval.py runtime
─────────────                     ──────────────────
task-suite.json                   validate_command()
  "command": [                      ├─ only python3?
    "python3",                      ├─ no -c flag?
    "scripts/foo.py",               ├─ no exec() pattern?
    "--arg"                         ├─ no absolute path?
  ]                                 ├─ no .. traversal?
                                    └─ path prefix in whitelist?
                                         │
                                    allowed? ──► subprocess.run(cwd=WORKSPACE)
                                    blocked? ──► BLOCKED_UNSAFE_COMMAND result
```

**Allowed path prefixes / 允许的路径前缀:**
- `scripts/`
- `skills/openclaw-smartness-eval/`
- `state/`
- `benchmarks/`

**Network access / 网络访问:**
- Default: **none** / 默认无网络
- `--llm-judge`: sends dimension summary + evidence to LLM API (no raw logs or user data) / 仅发送摘要

---

## Design Decisions / 设计决策

| Decision | Rationale / 原因 |
|----------|------------------|
| Subprocess for tests | Tests need to invoke real workspace scripts, not mock them / 测试需调用真实脚本 |
| Time-window filtering | Recent data is more relevant than historical noise / 近期数据更有代表性 |
| Non-linear latency scoring | Small latency increases matter less than large spikes / 大延迟惩罚更重 |
| Anti-gaming probes | Prevents overfitting eval to known test inputs / 防止针对已知测试过拟合 |
| pass@k in deep mode | Single-run noise is high; repeated runs give reliability estimate / 重复运行降低方差 |
| Graceful fallback | Missing data files → default values, never crash / 缺数据不崩溃 |
| No external deps | Stdlib only (except optional urllib for LLM judge) / 仅标准库 |
