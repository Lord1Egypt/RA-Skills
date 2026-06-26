<div align="center">

# 🎯 OpenClaw Smartness Eval — 完整中文文档

**别靠感觉，用数据说话。**

[![Version](https://img.shields.io/badge/版本-0.2.1-blue?style=flat-square)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/协议-MIT--0-green?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-yellow?style=flat-square)](./scripts/eval.py)

</div>

---

## 目录

- [项目简介](#项目简介)
- [为什么需要这个项目](#为什么需要这个项目)
- [快速开始](#快速开始)
- [12 维度详解](#12-维度详解)
- [评估模式](#评估模式)
- [命令行参考](#命令行参考)
- [评分公式](#评分公式)
- [数据来源](#数据来源)
- [输出文件](#输出文件)
- [安全模型](#安全模型)
- [目录结构](#目录结构)
- [真实评估示例](#真实评估示例)
- [常见问题](#常见问题)
- [作者](#作者)
- [参与贡献](#参与贡献)

---

## 项目简介

`smartness-eval` 是一个面向 AI Agent 的智能度评估框架。

它通过 **28 项自动化测试 + 多数据源交叉验证 + 反作弊探针**，在 12 个维度上量化 Agent 的能力水平，输出结构化评分、置信区间、风险告警和升级建议。

**一句话定位**：用于回答 _"我的 Agent 到底有多聪明？这周比上周进步了吗？"_ 的评估工具。

---

## 为什么需要这个项目

| 传统做法 | 本项目 |
|----------|--------|
| "感觉变聪明了" | 12 维度量化评分 |
| 单次对话判断 | 28 项可重复测试 |
| 没有历史数据 | 纵向趋势追踪 + 退化告警 |
| 容易自欺 | 反作弊随机探针 |
| 没有证据链 | 多数据源交叉验证 |
| 纯主观 | 客观评分 + 可选 LLM 裁判 |

---

## 快速开始

### 前置条件

- Python 3.9+
- OpenClaw 2026.3.13+ (推荐)
- macOS 或 Linux

### 安装与运行

```bash
# 克隆仓库
git clone https://github.com/xyva-yuangui/smartness-eval.git
cd smartness-eval

# 检查技能结构完整性
python3 scripts/check.py

# 快速评估（约 10 项测试，3 天数据窗口）
python3 scripts/eval.py --mode quick

# 标准评估 + Markdown 报告（约 25 项测试 + 2 个探针，7 天窗口）
python3 scripts/eval.py --mode standard --format markdown

# 深度评估 + 趋势对比（全部测试 x2，30 天窗口）
python3 scripts/eval.py --mode deep --compare-last

# 可选：LLM 裁判主观评分（需设置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY）
python3 scripts/eval.py --mode standard --llm-judge
```

### ClawHub 安装

```bash
clawhub install openclaw-smartness-eval
```

---

## 12 维度详解

### 七大主维度

| # | 维度 | 英文 | 权重 | 评估内容 | 数据来源 |
|---|------|------|------|----------|----------|
| 1 | **理解** | Understanding | 10% | 意图识别、约束捕获、上下文一致性 | message-analyzer 测试 + benchmark |
| 2 | **分析** | Analysis | 10% | 问题拆解、依赖识别、结构化输出 | 推理库深度 + 回归指标 |
| 3 | **思考** | Thinking | 10% | 风险意识、自检、反面论证 | 安全审计 + 质量门控 + finalize 闭环 |
| 4 | **推理** | Reasoning | 15% | 逻辑链完整性、证据支持、置信度校准 | 推理知识库 + benchmark + 模板可用性 |
| 5 | **自我迭代** | Self-iteration | 10% | 错误修复率、模式推广、学习新鲜度 | error-tracker + pattern-library + reflection |
| 6 | **对话沟通** | Dialogue | 10% | 表达清晰度、需求覆盖、可操作性 | 真实交互采样 + benchmark |
| 7 | **响应时长** | Responsiveness | 5% | P50/P95 延迟、超时率 | latency-metrics + API fallback |

### 五大扩展维度

| # | 维度 | 英文 | 权重 | 评估内容 | 数据来源 |
|---|------|------|------|----------|----------|
| 8 | **鲁棒性** | Robustness | 8% | 噪声/长上下文/模糊指令下的稳定性 | benchmark + 重复错误 + 告警 |
| 9 | **泛化能力** | Generalization | 5% | 跨域路由准确性、意图多样性 | 意图分布 + orchestrator 日志 |
| 10 | **策略遵循** | Policy adherence | 7% | AGENTS.md 合规、安全确认、操作约束 | Cron 健康 + 高风险交互检测 |
| 11 | **工具可靠性** | Tool reliability | 5% | 脚本可用、Cron 健康、状态文件完整 | Cron 报告 + benchmark + 规则候选 |
| 12 | **校准能力** | Calibration | 5% | 不确定性表达、置信度准确性 | 推理深度 + finalize 审批率 + 高优错误 |

每个维度都有 0–5 分的详细评分量表，包含具体评判标准。完整量表见 [`config/rubrics.json`](./config/rubrics.json)。

---

## 评估模式

| 模式 | 测试数 | 数据窗口 | 重复次数 | 探针数 | 适用场景 |
|------|--------|----------|----------|--------|----------|
| `quick` | ~10 | 3 天 | 1 次 | 1 个 | 每日自省，快速检查 |
| `standard` | ~25 | 7 天 | 1 次 | 2 个 | 每周能力周报 |
| `deep` | 全部 | 30 天 | 2 次 (pass@k) | 3 个 | 月度审计、版本升级回归 |

---

## 命令行参考

```bash
python3 scripts/eval.py [选项]
```

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--mode {quick,standard,deep}` | `standard` | 评估深度 |
| `--format {json,markdown}` | `json` | 输出格式 |
| `--compare-last` | 关闭 | 与上一次评估对比，显示趋势变化 |
| `--llm-judge` | 关闭 | 启用 LLM 主观评分（需要 API Key） |
| `--no-probes` | 关闭 | 禁用反作弊探针（调试用） |

### 辅助命令

```bash
# 技能结构健康检查
python3 scripts/check.py

# 状态探针（独立安全检测）
python3 scripts/state_probe.py --probe quality-gate-prompt
python3 scripts/state_probe.py --probe latency-state-count
python3 scripts/state_probe.py --probe rule-candidates
```

---

## 评分公式

### 总分计算

```
overall_score = Σ(dimension_score × weight) / Σ(weights)
```

总权重 = 100%（主维度 70% + 扩展维度 30%）。

### 单维度计算示例

以 **推理（Reasoning）** 维度为例：

```
reasoning = task_score × 0.40           # 测试通过率
          + benchmark_pass_rate × 0.15  # 核心 benchmark 结果
          + reasoning_depth × 0.25      # 推理库高置信条目占比
          + reasoning_total × 0.20      # 推理库总量（上限 120 条归一化）
```

以 **响应时长（Responsiveness）** 维度为例（非线性惩罚）：

```
score = 100
if p50 > 1500ms: score -= min(25, ((p50-1500)/1000)^1.5 × 5)
if p95 > 5000ms: score -= min(35, ((p95-5000)/2000)^1.4 × 8)
score -= min(20, timeout_rate × 100)
```

完整 12 个维度的公式详解见 [docs/SCORING.md](./docs/SCORING.md)。

### 等级划分

| 等级 | 分数范围 | 含义 |
|------|----------|------|
| A+ | ≥ 92 | 卓越 |
| A | ≥ 88 | 优秀 |
| A- | ≥ 84 | 良好偏上 |
| B+ | ≥ 80 | 良好 |
| B | ≥ 76 | 中等偏上 |
| B- | ≥ 72 | 中等 |
| C+ | ≥ 68 | 中等偏下 |
| C | ≥ 64 | 及格 |
| D | < 64 | 需要改进 |

---

## 数据来源

| 数据源 | 文件路径 | 用途 |
|--------|----------|------|
| 响应延迟指标 | `state/response-latency-metrics.json` | P50/P95 延迟计算 |
| 错误追踪 | `state/error-tracker.json` | 修复率、验证率、重复率 |
| 模式库 | `state/pattern-library.json` | 高置信模式数量、推广率 |
| Cron 报告 | `state/cron-governor-report.json` | 启用任务、出错率、thin-script 率 |
| Benchmark 历史 | `state/benchmark-results/history.jsonl` | 核心测试通过率 |
| 编排器日志 | `state/v5-orchestrator-log.json` | V5 管道使用量 |
| Finalize 日志 | `state/v5-finalize-log.json` | 闭环审批率 |
| 推理知识库 | `.reasoning/reasoning-store.sqlite` | 推理深度、置信度分布 |
| 消息分析日志 | `state/message-analyzer-log.json` | 真实交互意图分布 |
| 反思报告 | `state/reflection-reports/` | 自省报告数量 |
| 告警日志 | `state/alerts.jsonl` | 窗口内告警频率 |
| 规则候选 | `state/rule-candidates.json` | 自动生成的规则数量 |
| 回归指标 | `scripts/regression-metrics-report.py` | 重复回复率、调度延迟 |

> 缺少某些数据源时，评估不会崩溃，对应维度会使用 fallback 默认值。

---

## 输出文件

每次评估生成三个文件：

| 文件 | 路径 | 内容 |
|------|------|------|
| **评估 JSON** | `state/smartness-eval/runs/<时间戳>.json` | 完整结构化结果：所有维度分数、证据、风险、建议、元数据 |
| **Markdown 报告** | `state/smartness-eval/reports/<日期>.md` | 人类可读报告：表格、趋势箭头、风险标记 |
| **历史日志** | `state/smartness-eval/history.jsonl` | 每次运行追加一行，用于纵向分析 |

### JSON 输出字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `overall_score` | float | 加权总分 (0–100) |
| `grade` | string | 等级 (A+ ~ D) |
| `dimension_scores` | object | 七大主维度分数 |
| `expanded_scores` | object | 五大扩展维度分数 |
| `confidence_interval` | [float, float] | 95% 置信区间 |
| `dimension_spread` | float | 维度间离散度（方差） |
| `evidence` | array | 关键证据指标列表 |
| `risk_flags` | array | 风险告警 |
| `upgrade_recommendations` | array | 升级建议 |
| `trend_vs_last` | object/null | 趋势对比（需 `--compare-last`） |
| `pass_at_k` | object/null | 测试可靠性（deep 模式） |
| `llm_judge` | object/null | LLM 裁判评分（需 `--llm-judge`） |

---

## 安全模型

`eval.py` 通过 `subprocess` 执行测试命令，为防止滥用实施了多层防护：

| 安全规则 | 具体措施 |
|----------|----------|
| 解释器白名单 | 仅允许 `python3` |
| 禁止内联执行 | 屏蔽 `-c` 参数和 `exec(` 模式 |
| 禁止绝对路径 | 所有路径必须是相对路径 |
| 禁止路径穿越 | 拒绝包含 `..` 的路径 |
| 前缀白名单 | 仅允许 `scripts/`、`skills/openclaw-smartness-eval/`、`state/`、`benchmarks/` |
| 网络默认关闭 | `--llm-judge` 需显式启用 + API Key |

---

## 目录结构

```text
smartness-eval/
├── README.md                  ← 英文 + 中文概览
├── README_CN.md               ← 完整中文文档（本文件）
├── SKILL.md                   ← OpenClaw 技能清单
├── _meta.json                 ← ClawHub 注册元数据
├── LICENSE                    ← MIT No Attribution 协议
├── CHANGELOG.md               ← 版本变更日志
├── CONTRIBUTING.md            ← 贡献指南
├── SECURITY.md                ← 安全策略
├── CODE_OF_CONDUCT.md         ← 行为准则
│
├── config/
│   ├── config.json            ← 权重、模式、阈值配置
│   ├── rubrics.json           ← 12 维度 0–5 评分量表
│   └── task-suite.json        ← 28 项测试定义
│
├── scripts/
│   ├── eval.py                ← 核心评估引擎（~960 行）
│   ├── check.py               ← 技能结构健康检查
│   └── state_probe.py         ← 安全状态探针
│
└── docs/
    ├── ARCHITECTURE.md        ← 架构设计与数据流
    ├── SCORING.md             ← 评分公式详解
    ├── ROADMAP.md             ← 路线图
    ├── SHOWCASE.md            ← 案例展示与分享指南
    └── FAQ.md                 ← 常见问题
```

---

## 真实评估示例

以下是一次真实的 `quick` 模式评估结果摘要：

```
🎯 Overall: 71.36 (B-)
📊 CI: [71.36, 71.36]  |  mode: quick  |  samples: 15

📈 维度得分:
  理解 (understanding)       85.00   ████████░░  强
  对话 (dialogue)            82.50   ████████░░  强
  策略 (policy_adherence)    77.14   ███████░░░
  分析 (analysis)            76.31   ███████░░░
  推理 (reasoning)           74.79   ███████░░░
  思考 (thinking)            73.50   ███████░░░
  工具 (tool_reliability)    72.43   ███████░░░
  泛化 (generalization)      70.00   ███████░░░
  响应 (responsiveness)      63.05   ██████░░░░
  鲁棒 (robustness)          62.14   ██████░░░░
  校准 (calibration)         60.69   ██████░░░░  弱
  迭代 (self_iteration)      55.56   █████░░░░░  弱

🚨 风险告警:
  - 仍有 5 个出错中的 Cron 任务
  - finalize 闭环样本不足

💡 升级建议:
  - 修复出错 Cron 任务或将其 thin-script 化
  - 增加 finalize 路径使用量
```

---

## 常见问题

**Q: 不用 OpenClaw 也能用吗？**
A: 核心评估引擎（eval.py）依赖 OpenClaw 的工作区脚本和状态文件。如果你只想参考评估框架的设计思路，可以阅读 `config/rubrics.json` 和 `docs/SCORING.md`。

**Q: --llm-judge 会发送什么数据？**
A: 仅发送评估维度分数摘要、关键证据指标和风险标记（无原始日志或用户数据）。默认关闭，需显式启用。

**Q: 测试命令安全吗？**
A: 所有测试命令在执行前经过 `validate_command()` 安全校验，禁止内联代码、绝对路径和路径穿越。详见 [安全模型](#安全模型)。

**Q: 如何添加自定义维度？**
A: 当前版本不支持自定义维度插件。v1.0 计划支持。你可以通过修改 `config/rubrics.json` 和 `config/config.json` 的权重来调整现有维度。

**Q: 分数波动正常吗？**
A: 是的。由于数据窗口（3/7/30 天）和反作弊探针的随机性，每次评分会有小幅波动。`deep` 模式通过重复运行 + pass@k 来降低方差。

---

## 作者

**圆规**

- GitHub: [@yh22e](https://github.com/yh22e)

---

## 参与贡献

欢迎提交 Issue 和 PR！详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

**可以贡献的方向**：
- 评分公式改进
- 新的测试用例
- 报告可视化
- 文档翻译

---

<div align="center">

_"进步的第一步，是精确知道自己现在站在哪里。"_

⭐ 如果这个项目对你有帮助，请 Star 本仓库

</div>
