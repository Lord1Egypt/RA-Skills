<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">中文</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_FR.md">Français</a> |
  <a href="README_RU.md">Русский</a>
</p>

<p align="center">
  <h1 align="center">Quant Research Lab</h1>
  <p align="center">
    <strong>Multi-Agent Quantitative Strategy R&D Framework</strong>
  </p>
  <p align="center">
    15 Specialized LLM Agents Modeled After Top Quant Firms
  </p>
</p>

<p align="center">
  <a href="https://github.com/anthropics/claude-code" target="_blank"><img alt="Claude Code" src="https://img.shields.io/badge/Claude_Code-Compatible-D97706?logo=anthropic&logoColor=white"/></a>
  <a href="https://hermes.nousresearch.com" target="_blank"><img alt="Hermes Agent" src="https://img.shields.io/badge/Hermes_Agent-Skill-7C3AED?logo=data:image/svg+xml;base64,..." /></a>
  <img alt="Roles" src="https://img.shields.io/badge/Roles-15-blue" />
  <img alt="Pipeline Tracks" src="https://img.shields.io/badge/Pipeline_Tracks-8-green" />
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
</p>

---

> **Quant Research Lab** is an AI-agent skill that brings institutional-grade quantitative strategy research workflow to LLM-powered coding agents. It deploys 15 specialized agents — each modeled after the expertise of a top quant firm (Goldman Sachs, Renaissance Technologies, Two Sigma, Citadel, Jane Street, and more) — to collaboratively design, backtest, risk-manage, and validate quantitative trading strategies.

> ⚠️ **Disclaimer**: This framework is designed for **research and educational purposes** only. It does not constitute financial, investment, or trading advice. Trading performance depends on many factors including model choice, data quality, and market conditions. Always perform your own due diligence.

---

## Table of Contents

- [Framework Overview](#framework-overview)
- [The 15 Roles](#the-15-roles)
- [Pipeline Architecture](#pipeline-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Quality Gates](#quality-gates)
- [State Management](#state-management)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Framework Overview

Quant Research Lab mirrors how real-world quantitative trading firms operate: complex strategy research is decomposed into specialized roles, each bringing domain expertise from a different institutional perspective. The framework orchestrates these roles through two modes:

- **Toolbox Mode** — Invoke any individual role on demand for targeted analysis
- **Pipeline Mode** — Run pre-configured tracks (sequences of roles) for end-to-end strategy research

```
┌─────────────────────────────────────────────────────────────┐
│                    Quant Research Lab                        │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Strategy  │→ │ Backtest │→ │   Risk   │→ │  Alpha   │   │
│  │ Architect │  │  Engine  │  │ Manager  │  │Researcher│   │
│  │ (GS)      │  │ (RenTech)│  │ (Two σ)  │  │ (Citadel)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │             │              │         │
│       ▼              ▼             ▼              ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Execution │  │  Factor  │  │ Stat Arb │  │  Macro   │   │
│  │ Algo     │  │  Model   │  │(D.E.Shaw)│  │(Bridge-  │   │
│  │ (Virtu)  │  │  (AQR)   │  │          │  │ water)   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │             │              │         │
│       ▼              ▼             ▼              ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Data Pipe │  │    ML    │  │Portfolio │  │ Trading  │   │
│  │ (Bloomberg)│ │Researcher│  │Optimizer │  │ System   │   │
│  │          │  │(Point72) │  │(Man Grp) │  │(Millenn.)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │Factor Backtest│  │  Compliance  │                        │
│  │(Dimensional)  │  │    (GS)      │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Quality Gate System                     │   │
│  │  Required Fields │ Numerical Sanity │ Dual Signatures│   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## The 15 Roles

Each agent is backed by a detailed prompt template that defines the agent's persona, expertise, and a structured multi-dimensional task specification. No role is a generic "assistant" — every agent thinks and produces output in the style of its associated institution.

| ID | Role | Institution | Depends On | Complexity | Phase |
|:---|:-----|:------------|:-----------|:-----------|:------|
| 01 | **Strategy Architect** | Goldman Sachs | — | High | 1 |
| 02 | **Backtest Engine** | Renaissance Technologies | 01 | Normal | 1 |
| 03 | **Risk Manager** | Two Sigma | 01 | Normal | 1 |
| 04 | **Alpha Researcher** | Citadel | — | High | 1 |
| 05 | **Market Maker** | Jane Street | 01 | Normal | 3 |
| 06 | **Factor Model Builder** | AQR | 02 | Normal | 2 |
| 07 | **Statistical Arbitrage** | D.E. Shaw | 01 | Normal | 2 |
| 08 | **Macro Strategy** | Bridgewater Associates | 01 | Normal | 3 |
| 09 | **Data Pipeline** | Bloomberg | — | Normal | 2 |
| 10 | **Execution Algorithm** | Virtu Financial | 01 | Normal | 1 |
| 11 | **ML Researcher** | Point72 | 01 | High | 3 |
| 12 | **Portfolio Optimizer** | Man Group | 01,02,03,06 | Normal | 2 |
| 13 | **Trading System** | Millennium Management | 10,12 | Normal | 2 |
| 14 | **Factor Backtester** | Dimensional Fund Advisors | 01 | Normal | 3 |
| 15 | **Compliance Framework** | Goldman Sachs | 13 | Normal | 3 |

### Role Highlights

**Strategy Architect (01)** — Covers 9 dimensions of strategy design: thesis, security selection, signal generation, entry/exit rules, position sizing, risk parameters, and implementation specifications. Every decision backed by mathematical formulas and pseudocode.

**Backtest Engine (02)** — 10-dimension validation framework including data quality, engine architecture, transaction cost modeling (Almgren-Chriss), statistical rigor (Deflated Sharpe Ratio, False Discovery Rate), and walk-forward testing.

**Risk Manager (03)** — Multi-layer risk assessment: market risk (VaR/CVaR), liquidity risk, counterparty risk, tail risk (EVT), with stress testing scenarios drawn from historical crises.

**Alpha Researcher (04)** — Alpha signal discovery pipeline with IC/ICIR analysis, signal decay modeling, and multi-factor orthogonalization.

**Factor Model Builder (06)** — Full Barra-style factor model construction: alpha factors, risk factors, factor covariance estimation, and factor-based attribution.

**ML Researcher (11)** — End-to-end ML pipeline: feature engineering, model selection (XGBoost/LSTM/Transformer), hyperparameter optimization, and production deployment specifications.

---

## Pipeline Architecture

Roles form a **Directed Acyclic Graph (DAG)**, not a linear chain. Different research scenarios use different tracks:

| Track | Trigger Phrase | Role Sequence | Est. Time | Use Case |
|:------|:---------------|:--------------|:----------|:---------|
| **Core** (default) | "启动流水线" / "pipeline" | 01→02→03→04→10 | ~15min | Standard: Design→Backtest→Risk→Alpha→Execute |
| **Factor** | "因子流水线" | 01→02→06→14→12 | ~20min | Factor research: Build→Backtest→Validate→Optimize |
| **Execution** | "执行流水线" | 01→10→13→15 | ~18min | System deployment: Algo→Trading System→Compliance |
| **Macro** | "宏观流水线" | 01→08→03→12 | ~18min | Macro strategy + risk + portfolio allocation |
| **Stat Arb** | "套利流水线" | 01→07→02→10 | ~18min | Pairs trading / cointegration strategies |
| **ML** | "ML流水线" | 01→11→02→03 | ~18min | ML-driven strategy development |
| **Market Making** | "做市流水线" | 01→05→10→13 | ~18min | Market making system design |
| **Full** | "全量流水线" | 01→...→15 | ~40min | Complete end-to-end (use with caution) |

### Pipeline Features

- **Breakpoint Resume** — Pause at any role, resume later from where you left off
- **Re-execution** — Re-run from any role, discarding downstream outputs
- **Custom Tracks** — Define your own role sequences (e.g., "run 01→04→11")
- **Strict Mode** — Halt on quality gate warnings instead of auto-continuing
- **Progress Tracking** — Real-time progress display with quality gate status per role

---

## Installation

### Option 1: One-Line Install (Recommended)

```bash
npx skills add https://github.com/yili1992/quant-research-lab --skill quant-research-lab
```

### Option 2: Paste This to Claude Code

> Install the `quant-research-lab` skill. Follow these steps:
>
> 1. Ensure `.claude/skills/` directory exists in the current project (create if not)
> 2. Run `git clone https://github.com/yili1992/quant-research-lab.git .claude/skills/quant-research-lab`
> 3. Verify: `ls .claude/skills/quant-research-lab/` should show `SKILL.md`, `roles/`, `pipelines/`
> 4. Confirm installation is complete. When I describe quantitative research needs, this skill should activate automatically.

Paste the above into Claude Code — it will handle the full installation.

### Option 3: Manual Command Line

```bash
git clone https://github.com/yili1992/quant-research-lab.git ~/.hermes/skills/quant-research-lab
```

### Option 4: As a Standalone Reference

The role templates in `roles/` can be used independently as high-quality system prompts for any LLM — no framework required. Each `.md` file is self-contained with persona, task specification, and output format requirements.

### Triggers

Once installed, the skill activates automatically when you describe quantitative research needs:

- "Design a funding rate arbitrage strategy" — Triggers Strategy Architect
- "Run a backtest on this strategy" — Triggers Backtest Engine
- "Launch the quant pipeline" — Shows track selection menu
- "Factor research pipeline" — Starts Factor Research track
- "Use the Goldman Sachs role" / "Do a backtest" / "Run risk analysis" — Toolbox mode for specific roles

---

## Usage

### Natural Language Triggers

The skill activates automatically when you describe quantitative research needs:

```
"帮我设计一个费率套利策略"           → Triggers Strategy Architect (01)
"做一下这个策略的回测"               → Triggers Backtest Engine (02)
"启动量化流水线"                     → Shows track selection menu
"因子流水线"                         → Starts Factor track
"从角色 03 恢复"                     → Resumes pipeline from Risk Manager
"用高盛角色" / "做回测" / "风控分析"  → Toolbox mode for specific roles
"流水线进度" / "status"              → Shows current pipeline progress
"重置流水线" / "reset"               → Resets pipeline state
```

### Toolbox Mode

Use individual roles for targeted analysis without running a full pipeline:

1. Say the role name or describe the task
2. The skill matches to the appropriate role, loads its template, and dispatches a subagent
3. Results are saved to `state/research-context.md` with quality gate annotations
4. Downstream roles that depend on this one are suggested as next steps

### Pipeline Mode

Run end-to-end research tracks:

1. Select a track (or let the skill suggest one based on your goal)
2. Review the execution plan: role sequence, estimated time, dependency graph
3. Confirm to start — roles execute sequentially with automatic context passing
4. Monitor progress with `[1/5] 01 Strategy Architect ✅ [QAGATE: PASS]` style output
5. Pause anytime with "暂停", resume later with "从角色 NN 恢复"

---

## Quality Gates

Every role output undergoes automated quality checks before being accepted into the pipeline:

| Check | Scope | What It Catches | On Failure |
|:------|:------|:----------------|:-----------|
| **Required Fields** | All roles | Missing `[QAGATE]` block, empty core conclusion, missing downstream fields | `[输出不完整]` |
| **Numerical Sanity** | Backtest/Risk/Factor roles | Sharpe > 50, MaxDD > -99%, or other implausible values | `[数值极端异常]` |
| **Dual Signatures** | Numerical roles | Missing `method_signature` or `data_signature` | `[缺少签名]` |

The QAGATE block embedded in each role's output serves as a structured quality report:

```
[QAGATE]
core_conclusion: Strategy achieves Sharpe 1.8 with 12% max drawdown
key_params: lookback=20, threshold=2.0σ, rebalance=weekly
downstream_fields: signal_formula, entry_rules, risk_params
method_signature: momentum_zscore_v1
data_signature: binance_btcusdt_perp_2023_2025
[/QAGATE]
```

---

## State Management

Pipeline state is persisted in `state/research-context.md` — a single markdown file with YAML frontmatter:

```yaml
---
pipeline_id: btc-arb-20260504
pipeline_track: "核心流水线"
status: in-progress
current_role_id: "03"
completed_roles: ["01", "02"]
next_recovery: "04"
created_at: 2026-05-04T02:16:00Z
project: btc-arb
---
```

Each role's full output is appended between `<!-- ROLE_OUTPUT_START:{ID} -->` and `<!-- ROLE_OUTPUT_END:{ID} -->` markers, enabling:

- **Resumability** — Close your session, come back later, pick up where you left off
- **Selective re-execution** — Discard outputs from a specific role and re-run it
- **Cross-role context** — Downstream roles automatically receive upstream parameters and conclusions
- **Audit trail** — Full history of every role's output with quality gate results

---

## Project Structure

```
quant-research-lab/
├── SKILL.md                          # Skill definition & orchestration logic
├── README.md                         # This file
├── LICENSE                           # MIT License
├── roles/                            # Role prompt templates
│   ├── 01-gs-strategy-architect.md   # Goldman Sachs Strategy Architect
│   ├── 02-rentec-backtest-engine.md  # Renaissance Technologies Backtest Engine
│   ├── 03-twosigma-risk-manager.md   # Two Sigma Risk Manager
│   ├── 04-citadel-alpha-researcher.md# Citadel Alpha Researcher
│   ├── 05-js-market-maker.md         # Jane Street Market Maker
│   ├── 06-aqr-factor-builder.md      # AQR Factor Model Builder
│   ├── 07-deshaw-stat-arb.md         # D.E. Shaw Statistical Arbitrage
│   ├── 08-bridgewater-macro.md       # Bridgewater Macro Strategy
│   ├── 09-bbg-data-pipeline.md       # Bloomberg Data Pipeline
│   ├── 10-virtu-execution.md         # Virtu Execution Algorithm
│   ├── 11-point72-ml-researcher.md   # Point72 ML Researcher
│   ├── 12-man-portfolio-optimizer.md # Man Group Portfolio Optimizer
│   ├── 13-millennium-trading-system.md # Millennium Trading System
│   ├── 14-dimensional-factor-backtest.md # Dimensional Factor Backtest
│   └── 15-gs-compliance.md           # Goldman Sachs Compliance Framework
├── state/                            # Pipeline state (auto-generated)
│   └── research-context.md
└── docs/                             # Design documents & specs
    └── superpowers/
```

---

## How It Works Under the Hood

1. **Skill Activation** — Natural language matching or explicit `/quant-research-lab` trigger
2. **Context Collection** — Reads role registry, checks for existing pipeline state, collects user inputs (market, capital, focus)
3. **Template Loading** — Reads the target role's `.md` file to get the full prompt template
4. **Placeholder Substitution** — Replaces `{user_market}`, `{user_capital}`, `{user_focus}`, `{upstream_params}`, `{upstream_summary}` with collected values
5. **Subagent Dispatch** — Spawns a dedicated subagent (Opus for high-complexity roles, Sonnet for normal) with the completed prompt
6. **Quality Gate Evaluation** — Parses the QAGATE block, runs 3 automated checks
7. **State Persistence** — Appends output to state file with markers, updates frontmatter
8. **Next Step Suggestion** — Scans the dependency graph and suggests the next logical role

---

## Contributing

Contributions are welcome! Here's how you can help:

### Add a New Role

1. Create `roles/NN-your-role.md` following the existing template structure:
   - **Persona** section: institutional background, expertise domains, working philosophy
   - **Task Description** section: numbered dimensions with concrete quantitative requirements
   - **Output Format** section: structured markdown with tables, formulas, and pseudocode
   - **QAGATE** section: required fields and quality criteria
2. Add the role to the registry table in `SKILL.md`
3. Define `depends_on` relationships and assign a `Phase` (1/2/3)

### Add a New Pipeline Track

1. Define the role sequence based on the dependency DAG
2. Add to the track table in `SKILL.md`
3. Add trigger keywords for natural language matching

### Improve Existing Roles

Each role template is designed to produce institutional-grade output. Improvements welcome in:
- More precise mathematical specifications
- Additional edge case handling
- Better statistical methodology
- Real-world constraint modeling

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

