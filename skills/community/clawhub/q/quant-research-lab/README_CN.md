<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">中文</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_FR.md">Français</a> |
  <a href="README_RU.md">Русский</a>
</p>

<p align="center">
  <h1 align="center">量化策略研发实验室</h1>
  <p align="center">
    <strong>多智能体量化策略研发框架</strong>
  </p>
  <p align="center">
    15 个专业化 LLM 智能体，对标顶级量化机构
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

> **量化策略研发实验室** 是一项 AI 智能体技能，将机构级量化策略研究工作流带给由 LLM 驱动的编程智能体。它部署了 15 个专业化智能体——每个都对标顶级量化机构（Goldman Sachs、Renaissance Technologies、Two Sigma、Citadel、Jane Street 等）的专业能力——协同完成量化交易策略的设计、回测、风控管理与验证。

> ⚠️ **免责声明**：本框架仅用于**研究和教育目的**，不构成金融、投资或交易建议。交易表现取决于多种因素，包括模型选择、数据质量和市场条件。请务必自行进行尽职调查。

---

## 目录

- [框架概述](#框架概述)
- [15 个角色](#15-个角色)
- [流水线架构](#流水线架构)
- [安装](#安装)
- [使用方法](#使用方法)
- [质量门控](#质量门控)
- [状态管理](#状态管理)
- [项目结构](#项目结构)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 框架概述

量化策略研发实验室镜像了现实世界量化交易公司的运作方式：复杂的策略研究被分解为专业化角色，每个角色从不同机构视角带来领域专长。本框架通过两种模式编排这些角色：

- **工具箱模式** — 按需调用任意单个角色进行针对性分析
- **流水线模式** — 运行预配置的轨迹（角色序列）进行端到端策略研究

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

## 15 个角色

每个智能体都由详细的提示词模板支撑，定义了智能体的人设、专业领域和结构化的多维度任务规格。没有哪个角色是泛用的"助手"——每个智能体都以其所属机构的风格进行思考和产出。

| ID | 角色 | 机构 | 依赖 | 复杂度 | 阶段 |
|:---|:-----|:-----|:-----|:-------|:-----|
| 01 | **策略架构师** | Goldman Sachs | — | 高 | 1 |
| 02 | **回测引擎** | Renaissance Technologies | 01 | 普通 | 1 |
| 03 | **风控经理** | Two Sigma | 01 | 普通 | 1 |
| 04 | **Alpha 研究员** | Citadel | — | 高 | 1 |
| 05 | **做市商** | Jane Street | 01 | 普通 | 3 |
| 06 | **因子模型构建师** | AQR | 02 | 普通 | 2 |
| 07 | **统计套利** | D.E. Shaw | 01 | 普通 | 2 |
| 08 | **宏观策略** | Bridgewater Associates | 01 | 普通 | 3 |
| 09 | **数据管道** | Bloomberg | — | 普通 | 2 |
| 10 | **执行算法** | Virtu Financial | 01 | 普通 | 1 |
| 11 | **ML 研究员** | Point72 | 01 | 高 | 3 |
| 12 | **组合优化器** | Man Group | 01,02,03,06 | 普通 | 2 |
| 13 | **交易系统** | Millennium Management | 10,12 | 普通 | 2 |
| 14 | **因子回测器** | Dimensional Fund Advisors | 01 | 普通 | 3 |
| 15 | **合规框架** | Goldman Sachs | 13 | 普通 | 3 |

### 角色亮点

**策略架构师 (01)** — 涵盖策略设计的 9 个维度：论题、标的筛选、信号生成、入场/出场规则、仓位管理、风险参数和实施规格。每个决策都有数学公式和伪代码支撑。

**回测引擎 (02)** — 10 维验证框架，包括数据质量、引擎架构、交易成本建模（Almgren-Chriss）、统计严谨性（缩尾夏普比率、错误发现率）和滚动前瞻测试。

**风控经理 (03)** — 多层风险评估：市场风险（VaR/CVaR）、流动性风险、对手方风险、尾部风险（极值理论），并提供源自历史危机的压力测试情景。

**Alpha 研究员 (04)** — Alpha 信号发现流水线，配备 IC/ICIR 分析、信号衰减建模和多因子正交化。

**因子模型构建师 (06)** — 完整的 Barra 风格因子模型构建：Alpha 因子、风险因子、因子协方差估计和基于因子的归因分析。

**ML 研究员 (11)** — 端到端机器学习流水线：特征工程、模型选择（XGBoost/LSTM/Transformer）、超参数优化和生产部署规格。

---

## 流水线架构

角色组成一个**有向无环图（DAG）**，而非线性链。不同的研究场景使用不同的轨迹：

| 轨迹 | 触发短语 | 角色序列 | 预计时间 | 使用场景 |
|:-----|:---------|:---------|:---------|:---------|
| **核心**（默认） | "启动流水线" / "pipeline" | 01→02→03→04→10 | ~15分钟 | 标准：设计→回测→风控→Alpha→执行 |
| **因子** | "因子流水线" | 01→02→06→14→12 | ~20分钟 | 因子研究：构建→回测→验证→优化 |
| **执行** | "执行流水线" | 01→10→13→15 | ~18分钟 | 系统部署：算法→交易系统→合规 |
| **宏观** | "宏观流水线" | 01→08→03→12 | ~18分钟 | 宏观策略 + 风控 + 组合配置 |
| **统计套利** | "套利流水线" | 01→07→02→10 | ~18分钟 | 配对交易 / 协整策略 |
| **ML** | "ML流水线" | 01→11→02→03 | ~18分钟 | ML 驱动的策略开发 |
| **做市** | "做市流水线" | 01→05→10→13 | ~18分钟 | 做市系统设计 |
| **全量** | "全量流水线" | 01→...→15 | ~40分钟 | 完整端到端（谨慎使用） |

### 流水线功能

- **断点续传** — 在任意角色处暂停，稍后从中断处继续
- **重新执行** — 从任意角色重新运行，丢弃下游输出
- **自定义轨迹** — 定义自己的角色序列（例如"运行 01→04→11"）
- **严格模式** — 遇到质量门控警告时暂停而非自动继续
- **进度追踪** — 实时进度显示，每个角色带有质量门控状态

---

## 安装

### 方式一：一行命令安装（推荐）

```bash
npx skills add https://github.com/yili1992/quant-research-lab --skill quant-research-lab
```

### 方式二：把下面这段话直接发给 Claude Code

> 帮我安装 `quant-research-lab` 这个技能。请按下面步骤做：
>
> 1. 确保当前项目的 `.claude/skills/` 目录存在（不存在就创建）
> 2. 执行 `git clone https://github.com/yili1992/quant-research-lab.git .claude/skills/quant-research-lab`
> 3. 验证：`ls .claude/skills/quant-research-lab/` 应该看到 `SKILL.md`、`roles/`、`pipelines/` 三项
> 4. 告诉我安装好了，之后我说"做一下回测"之类的话就会触发这个技能

把这段话复制粘贴给 Claude Code，它会自动完成安装。

### 方式三：手动命令行

```bash
git clone https://github.com/yili1992/quant-research-lab.git ~/.hermes/skills/quant-research-lab
```

### 方式四：作为独立参考

`roles/` 目录中的角色模板可以独立使用，作为任何 LLM 的高质量系统提示词——无需框架。每个 `.md` 文件都是自包含的，包含人设、任务规格和输出格式要求。

### 触发方式

装好后，当你描述量化研究需求时，技能会自动激活：

- "帮我设计一个费率套利策略" → 触发策略架构师
- "做一下这个策略的回测" → 触发回测引擎
- "启动量化流水线" → 显示流水线选择菜单
- "因子流水线" → 启动因子研究流水线
- "run a quant pipeline" / "backtest this strategy" → 英文触发
- "用高盛角色" / "做回测" / "风控分析" → 工具箱模式

---

## 使用方法

### 自然语言触发

当你描述量化研究需求时，技能会自动激活：

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

### 工具箱模式

无需运行完整流水线，即可使用单个角色进行针对性分析：

1. 说出角色名称或描述任务
2. 技能匹配到合适的角色，加载其模板，并调度一个子智能体
3. 结果保存到 `state/research-context.md`，带有质量门控标注
4. 建议执行依赖该角色的下游角色作为下一步

### 流水线模式

运行端到端的研究轨迹：

1. 选择一条轨迹（或让技能根据你的目标推荐）
2. 审查执行计划：角色序列、预计时间、依赖图
3. 确认开始——角色依次执行，自动传递上下文
4. 以 `[1/5] 01 Strategy Architect ✅ [QAGATE: PASS]` 风格输出监控进度
5. 随时用"暂停"暂停，稍后用"从角色 NN 恢复"继续

---

## 质量门控

每个角色的输出在被接受进入流水线之前，都会经过自动化质量检查：

| 检查项 | 范围 | 捕获问题 | 失败时 |
|:-------|:-----|:---------|:-------|
| **必填字段** | 所有角色 | 缺失 `[QAGATE]` 块、核心结论为空、缺少下游字段 | `[输出不完整]` |
| **数值合理性** | 回测/风控/因子角色 | 夏普比率 > 50、最大回撤 > -99%，或其他不合理的值 | `[数值极端异常]` |
| **双重签名** | 数值类角色 | 缺失 `method_signature` 或 `data_signature` | `[缺少签名]` |

每个角色输出中嵌入的 QAGATE 块作为结构化的质量报告：

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

## 状态管理

流水线状态持久化存储在 `state/research-context.md` 中——一个带有 YAML 前置元数据的单一 markdown 文件：

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

每个角色的完整输出追加在 `<!-- ROLE_OUTPUT_START:{ID} -->` 和 `<!-- ROLE_OUTPUT_END:{ID} -->` 标记之间，支持：

- **可恢复性** — 关闭会话，稍后回来，从中断处继续
- **选择性重新执行** — 丢弃特定角色的输出并重新运行
- **跨角色上下文** — 下游角色自动接收上游参数和结论
- **审计跟踪** — 每个角色输出的完整历史，包含质量门控结果

---

## 项目结构

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

## 底层工作原理

1. **技能激活** — 自然语言匹配或显式 `/quant-research-lab` 触发
2. **上下文收集** — 读取角色注册表，检查现有流水线状态，收集用户输入（市场、资金、关注点）
3. **模板加载** — 读取目标角色的 `.md` 文件获取完整提示词模板
4. **占位符替换** — 将 `{user_market}`、`{user_capital}`、`{user_focus}`、`{upstream_params}`、`{upstream_summary}` 替换为收集到的值
5. **子智能体调度** — 使用完成后的提示词生成一个专用子智能体（高复杂度角色使用 Opus，普通角色使用 Sonnet）
6. **质量门控评估** — 解析 QAGATE 块，运行 3 项自动化检查
7. **状态持久化** — 将输出追加到状态文件并附带标记，更新前置元数据
8. **下一步建议** — 扫描依赖图，建议下一个逻辑角色

---

## 贡献指南

欢迎贡献！以下是你能提供帮助的方式：

### 添加新角色

1. 按照现有模板结构创建 `roles/NN-your-role.md`：
   - **人设**部分：机构背景、专业领域、工作理念
   - **任务描述**部分：编号维度，包含具体量化要求
   - **输出格式**部分：结构化 markdown，含表格、公式和伪代码
   - **QAGATE**部分：必填字段和质量标准
2. 将角色添加到 `SKILL.md` 中的注册表
3. 定义 `depends_on` 依赖关系并分配 `Phase`（1/2/3）

### 添加新流水线轨迹

1. 基于依赖 DAG 定义角色序列
2. 添加到 `SKILL.md` 中的轨迹表
3. 添加用于自然语言匹配的触发关键词

### 改进现有角色

每个角色模板旨在产出机构级输出。欢迎在以下方面进行改进：
- 更精确的数学规格
- 更多边界情况处理
- 更好的统计方法论
- 现实约束建模

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

