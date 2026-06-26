<div align="center">

# 🎯 OpenClaw Smartness Eval

**Stop guessing. Start measuring.**

[![Version](https://img.shields.io/badge/version-0.3.0-blue?style=flat-square)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-yellow?style=flat-square)](./scripts/eval.py)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.13+-orange?style=flat-square)](./SKILL.md)
[![CI](https://github.com/xyva-yuangui/smartness-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/xyva-yuangui/smartness-eval/actions)

A **14-dimension** evaluation framework that turns your AI agent's real runtime data into a structured, reproducible intelligence score — with confidence intervals, trend tracking, and anti-gaming probes. Aligned with CLEAR, T-Eval, and Anthropic evaluation standards.

一个 **14 维度**的 AI Agent 智能评估框架，将真实运行数据转化为可量化、可重复、可追踪的智能度评分。对齐 CLEAR、T-Eval、Anthropic 等行业评测标准。

**[English](#overview) · [中文说明](#-中文说明) · [Quick Start](#-quick-start) · [Docs](./docs/)**

</div>

---

## Overview

Most AI agent improvements are anecdotal — _"it feels smarter."_ This project makes capability evolution **measurable and reproducible**.

`smartness-eval` combines three evaluation signals into one score:

| Signal | Description | Example |
|--------|-------------|---------|
| **Task tests** | 34 automated test commands across 14 dimensions | Intent recognition, risk detection, reasoning template availability, hallucination control |
| **Runtime telemetry** | Real logs, latency metrics, error tracker, reasoning DB | P50/P95 latency, error fix rate, pattern library growth |
| **Anti-gaming probes** | Randomized inputs injected at eval time | Prevents overfitting to known test cases |

The result: a single JSON + Markdown report containing overall score, per-dimension breakdown, confidence interval, risk flags, trend delta, and upgrade recommendations.

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/xyva-yuangui/smartness-eval.git
cd smartness-eval

# 2. Health check — verify skill structure
python3 scripts/check.py

# 3. Quick evaluation (~10 tests, 3-day window)
python3 scripts/eval.py --mode quick --no-probes

# 4. Standard evaluation + Markdown report (~25 tests + probes, 7-day window)
python3 scripts/eval.py --mode standard --format markdown

# 5. Deep evaluation with trend comparison (all tests x2, 30-day window)
python3 scripts/eval.py --mode deep --compare-last
```

---

## 📊 The 14 Dimensions

### 7 Main Dimensions / 七大主维度

| # | Dimension | 维度 | Weight | What it measures |
|---|-----------|------|--------|------------------|
| 1 | **Understanding** | 理解 | 9% | Intent recognition, constraint capture, context consistency |
| 2 | **Analysis** | 分析 | 9% | Problem decomposition, dependency identification, structured output |
| 3 | **Thinking** | 思考 | 9% | Risk awareness, self-check, adversarial reasoning |
| 4 | **Reasoning** | 推理 | 13% | Logic chain completeness, evidence support, confidence calibration |
| 5 | **Self-iteration** | 自我迭代 | 9% | Error fix rate, pattern promotion, learning freshness |
| 6 | **Dialogue** | 对话沟通 | 9% | Clarity, completeness, actionability, tone matching |
| 7 | **Responsiveness** | 响应时长 | 5% | P50/P95 latency, timeout rate, API chain health |

### 7 Expanded Dimensions / 七大扩展维度

| # | Dimension | 维度 | Weight | What it measures |
|---|-----------|------|--------|------------------|
| 8 | **Robustness** | 鲁棒性 | 7% | Stability under noise, long context, edge cases |
| 9 | **Generalization** | 泛化能力 | 5% | Cross-domain routing accuracy, intent diversity |
| 10 | **Planning** ⭐ | 规划能力 | 5% | Task decomposition, step ordering, dependency management, workflow execution |
| 11 | **Hallucination Control** ⭐ | 幻觉控制 | 6% | Factual accuracy, grounded responses, refusal when uncertain |
| 12 | **Policy adherence** | 策略遵循 | 5% | AGENTS.md compliance, safety confirmation, operation constraints |
| 13 | **Tool reliability** | 工具可靠性 | 4% | Script availability, cron health, state file integrity |
| 14 | **Calibration** | 校准能力 | 5% | Uncertainty expression, confidence accuracy, high-confidence error rate |

> Each dimension has a detailed **0–5 rubric** with concrete criteria. See [`config/rubrics.json`](./config/rubrics.json).
> 
> ⭐ = New in v0.3.0. Aligned with [CLEAR framework](https://arxiv.org/html/2511.14136v1), [T-Eval (ACL 2024)](https://www.53ai.com/news/LargeLanguageModel/2024071870985.html), and [Anthropic Agent Eval](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) standards.

---

## 📋 Evaluation Modes / 评估模式

| Mode | Tests | Data window | Repeat | Probes | Best for |
|------|-------|-------------|--------|--------|----------|
| `quick` | ~12 | 3 days | 1x | 1 | Daily self-reflection / 每日自省 |
| `standard` | ~30 | 7 days | 1x | 2 | Weekly report / 每周能力周报 |
| `deep` | All | 30 days | 2x | 3 | Monthly audit or post-upgrade / 月度审计 |

---

## 🔧 CLI Reference

```bash
python3 scripts/eval.py [OPTIONS]
```

| Option | Description | 说明 |
|--------|-------------|------|
| `--mode {quick,standard,deep}` | Evaluation depth (default: `standard`) | 评估深度 |
| `--format {json,markdown}` | Output format (default: `json`) | 输出格式 |
| `--compare-last` | Show trend deltas vs previous run | 与上次对比趋势 |
| `--llm-judge` | Enable LLM subjective scoring (needs API key) | LLM 裁判打分 |
| `--no-probes` | Disable anti-gaming probes | 关闭反作弊探针 |

---

## 📈 Example Output / 输出示例

<details>
<summary><b>Click to expand — real evaluation result / 点击展开真实评估结果</b></summary>

```
Overall: 71.36 (B-)
CI: [71.36, 71.36]  |  mode: quick  |  samples: 15

Main dimensions / 主维度:
  understanding        85.00
  analysis             76.31
  thinking             73.50
  reasoning            74.79
  self_iteration       55.56
  dialogue_comm        82.50
  responsiveness       63.05

Expanded dimensions / 扩展维度:
  robustness           62.14
  generalization       70.00
  policy_adherence     77.14
  tool_reliability     72.43
  calibration          60.69

Risk flags / 风险:
  - 仍有 5 个出错中的启用 Cron 任务
  - finalize 闭环样本不足

Top evidence / 关键证据:
  benchmark_pass_rate    100.0%
  p50_latency_ms         5246
  reasoning_store_total  116 entries
  error_fix_rate_pct     0.0%
  cron_error_pct         35.71%

Recommendations / 建议:
  - 修复出错 Cron 任务或将其 thin-script 化
  - 增加 finalize 路径使用，提升 thinking/calibration 可信度
```

</details>

---

## 🗂 Output Artifacts / 输出文件

| File | Path | Purpose / 用途 |
|------|------|----------------|
| **Run JSON** | `state/smartness-eval/runs/<timestamp>.json` | Complete structured result / 完整结构化结果 |
| **Markdown report** | `state/smartness-eval/reports/<date>.md` | Human-readable report / 人类可读报告 |
| **History** | `state/smartness-eval/history.jsonl` | One-line-per-run for longitudinal analysis / 纵向趋势分析 |

---

## 🔒 Security Model / 安全模型

This tool executes test commands via `subprocess`. To prevent abuse, `eval.py` enforces:

| Rule | Detail | 说明 |
|------|--------|------|
| Interpreter whitelist | Only `python3` allowed | 仅允许 python3 |
| No inline execution | `-c` and `exec(` blocked | 禁止内联代码执行 |
| No absolute paths | All paths must be relative | 禁止绝对路径 |
| No path traversal | `..` segments rejected | 禁止路径穿越 |
| Prefix whitelist | Only `scripts/`, `skills/…`, `state/`, `benchmarks/` | 前缀白名单 |
| Network off by default | `--llm-judge` requires explicit opt-in + API key | 网络默认关闭 |

---

## 📂 Repository Structure

```text
smartness-eval/
├── README.md                  ← EN + CN overview (this file)
├── README_CN.md               ← 完整中文文档
├── SKILL.md                   ← OpenClaw skill manifest
├── _meta.json                 ← ClawHub registry metadata
├── LICENSE                    ← MIT No Attribution
├── CHANGELOG.md               ← Version history / 版本历史
├── CONTRIBUTING.md            ← How to contribute / 贡献指南
├── SECURITY.md                ← Security policy / 安全策略
├── CODE_OF_CONDUCT.md         ← Community standards
│
├── config/
│   ├── config.json            ← Weights, modes, thresholds / 权重与模式配置
│   ├── rubrics.json           ← 12-dimension 0–5 rubric scales / 评分量表
│   └── task-suite.json        ← 28 test definitions / 测试定义
│
├── scripts/
│   ├── eval.py                ← Core evaluation engine / 核心评估引擎
│   ├── check.py               ← Skill structure check / 结构健康检查
│   └── state_probe.py         ← Safe local state probes / 安全状态探针
│
├── docs/
│   ├── ARCHITECTURE.md        ← System design & data flow / 架构设计
│   ├── SCORING.md             ← Scoring formulas explained / 评分公式详解
│   ├── ROADMAP.md             ← Future plans / 路线图
│   ├── SHOWCASE.md            ← Real results & sharing guide / 案例与分享
│   ├── FAQ.md                 ← Common questions / 常见问题
│   └── GROWTH.md              ← Community growth playbook / 增长策略
│
└── .github/
    ├── workflows/ci.yml       ← CI: structure check on push/PR
    ├── ISSUE_TEMPLATE/        ← Bug report & feature request
    └── pull_request_template.md
```

---

## 🖥 Compatibility / 兼容性

| Requirement | Version |
|-------------|---------|
| **Python** | 3.9+ |
| **OpenClaw** | 2026.3.13+ |
| **Workspace** | V5.1+ |
| **OS** | macOS, Linux |
| **External deps** | None (stdlib only). `--llm-judge` optionally uses `urllib.request` |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture](./docs/ARCHITECTURE.md) | System design, data flow, safety model |
| [Scoring formulas](./docs/SCORING.md) | How each dimension is computed, with formulas |
| [FAQ](./docs/FAQ.md) | Common questions in English and Chinese |
| [Roadmap](./docs/ROADMAP.md) | Planned features for v0.3 → v1.0 |
| [Showcase](./docs/SHOWCASE.md) | Real results, sharing templates |
| [Changelog](./CHANGELOG.md) | Full version history |

---

<a id="-中文说明"></a>

## 🇨🇳 中文说明

### 这是什么

`smartness-eval` 是一个 AI Agent 智能度评估框架。它解决一个核心问题：**你的 Agent 到底有多聪明？这个数字是涨了还是跌了？**

大多数 Agent 的改进只停留在"感觉好了"。这个项目把能力进化变成 **可测量、可对比、可追溯** 的过程。

### 核心特性

| 特性 | 说明 |
|------|------|
| **14 维度评分** | 理解、分析、思考、推理、自我迭代、对话沟通、响应时长 + 鲁棒性、泛化、**规划能力**、**幻觉控制**、策略遵循、工具可靠性、校准 |
| **34 项自动化测试** | 涵盖意图识别、风险检测、推理模板验证、幻觉控制、任务规划、API 健康检查等 |
| **真实运行数据** | 从延迟指标、错误追踪、推理知识库、Cron 状态等数据源交叉验证 |
| **反作弊探针** | 随机注入测试输入，防止针对已知测试的过拟合 |
| **趋势追踪** | `--compare-last` 对比上一次评估，显示各维度变化和退化告警 |
| **可选 LLM 裁判** | `--llm-judge` 调用大模型做主观可信度打分（默认关闭） |
| **安全执行** | 命令白名单 + 禁止内联代码 + 禁止绝对路径 + 前缀限制 |

### 评分公式概要

每个维度的最终得分 = **任务测试得分** × 权重 + **真实运行指标** × 权重。

例如 `reasoning`（推理）维度：
```
reasoning = task_score × 0.40
           + benchmark_pass_rate × 0.15
           + reasoning_depth × 0.25       # 高置信条目占比
           + reasoning_total × 0.20       # 知识库总量（上限 120 条）
```

完整公式见 [docs/SCORING.md](./docs/SCORING.md)。

### 数据来源

| 数据源 | 路径 | 用途 |
|--------|------|------|
| 响应延迟 | `state/response-latency-metrics.json` | P50/P95 计算 |
| 错误追踪 | `state/error-tracker.json` | 修复率、重复率 |
| 模式库 | `state/pattern-library.json` | 高置信模式数量 |
| Cron 报告 | `state/cron-governor-report.json` | 任务健康度 |
| Benchmark | `state/benchmark-results/history.jsonl` | 通过率 |
| 推理知识库 | `.reasoning/reasoning-store.sqlite` | 推理深度与覆盖 |
| 编排器日志 | `state/v5-orchestrator-log.json` | 管道使用量 |
| 消息分析日志 | `state/message-analyzer-log.json` | 真实交互采样 |
| 反思报告 | `state/reflection-reports/` | 自省数量 |
| 告警日志 | `state/alerts.jsonl` | 告警频率 |

---

## 👤 Author / 作者

**圆规**

- GitHub: [@yh22e](https://github.com/yh22e)
- ClawHub: [yh22e](https://clawhub.com/yh22e)

---

## 🤝 Contributing / 参与贡献

Issues and PRs are welcome! / 欢迎提交 Issue 和 PR！

- 📖 [CONTRIBUTING.md](./CONTRIBUTING.md) — Development setup & PR guidelines
- 🔒 [SECURITY.md](./SECURITY.md) — Security policy
- 🗺 [docs/ROADMAP.md](./docs/ROADMAP.md) — What's planned next

---

## ⭐ Star & Share

If this project helps you understand your AI agent better:

1. **⭐ Star this repo** — it helps others discover the project
2. **🧪 Share your eval result** — post a screenshot of your score
3. **🔁 Post your before/after** — show capability improvement over time
4. **💬 Open a Discussion** — share tips, ask questions, suggest dimensions

> _"The first step to building a smarter agent is knowing exactly how smart it is today."_

