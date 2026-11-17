---
name: stata-econ-workflow
description: >
  完整实证研究工作流管理技能。整合 codex-stata-for-economists 的工程化方法论与 Stata-MCP 执行工具。
  使用场景：(1) Stata do-file 编写、调试、执行与优化 (2) 实证研究流水线搭建与项目管理
  (3) 论文结果复现与审查（replication/robustness）(4) 计量经济学方法选择与实现
  (5) 研究日志溯源校验（log verification）(6) 提交前质量审核与评分
  当用户提到以下关键词时触发：stata, do文件, do-file, dofile, dta, 面板数据, panel, did, 双重差分,
  倍分法, 事件研究, event study, rd, 断点回归, iv, 工具变量, psm, 倾向得分, 合成控制, synth, ddml,
  复现, replication, 实证, emprical, 科研, 计量, 计量经济学, 回归, regress, reghdfe, esttab,
  系数, 标准误, p值, 置信区间, clustered SE, 聚类标准误, 固定效应, fixed effect, FE, 效能评估,
  质量评分, quality, verify, log, 日志, 代码审查, study, paper, 模板, template, pipeline, workflow,
  研究流程, 研究框架, do文件, 论文复现, 审稿, 论文发表, 研究设计, 方法选择, 因果推断, causal inference,
  差分法, triple diff, DDD, 三重差分, 平行趋势, parallel trend, 安慰剂检验, placebo
  不用于：与Stata/实证研究/计量经济学分析无关的通用对话。
---

# Stata Econ Workflow Skill

## 概述

本技能整合两套工具：

| 来源 | 内容 | 大小 |
|:-----|:-----|:-----|
| **codex-stata-for-economists** (陈铸/中国农大) | Agent审查规则、工作流规范、质量门禁、复现协议、18条Rule | 核心方法论 |
| **Stata-MCP** (Sepinetam) | Stata CLI执行、包管理、do-file运行、日志读取 | 执行层 |
| **OpenClaw stata-skill** | 基础Stata语法参考与执行指南 | 兼容层 |

### 灵感来源

本技能受 @chenzhu_cau 的 [codex-stata-for-economists](https://github.com/maxwell2732/codex-stata-for-economists) 项目启发。
该仓库提供了一套完整的 **Codex/Claude Agent 驱动Stata实证研究工作流**，
包含日志溯源验证、质量门禁、复现优先协议等工程化方法论。
本技能将其适配为 OpenClaw 技能系统，并与 Stata-MCP 执行工具集成。

---

## 路由表

根据用户实际任务，读取对应文件（每次只读1-3个文件）：

| 用户请求 | 读哪个文件 |
|:---------|:-----------|
| "帮我写个do文件" | `references/stata-coding-convention.md` |
| "搭建研究流水线" | `references/workflow-quickref.md` |
| "复现这篇论文" | `references/replication-first.md` + `references/reproduction-protocol.md` |
| "结果对不对，查一下" | `references/log-verification.md` |
| "质量怎么样，能不能提交" | `references/quality-gates.md` |
| "合并分支" | `references/merge-protocol.md` |
| "帮我审查do文件" | `agents/log-validator.md` 或 `agents/domain-reviewer.md` |
| "数据没进去" | `references/data-protection.md` |
| "总入口怎么做" | `templates/master-do-template.do` |
| "写一个DID分析" | `templates/did-analysis-template.do` |
| "做DDML" | `templates/ddml-analysis-template.do` |
| "帮我跑Stata" | 本SKILL.md中的Stata-MCP执行指引 |
| "有没有Stata语法参考" | 引导查看 `.claude/skills/stata/` 目录或安装 `stata-skill` |
| "质量评分" | `scripts/quality_score.py` |

---

## 核心工作流：LRQR 循环

受 codex-stata-for-economists 启发，所有实证分析遵循四步：

```
[L] LISTEN  → 理解用户的分析问题与数据
[Q] QUESTION → 出研究计划（Plan: 方法+变量+预期结果）
[R] RUN     → 执行do-file + 读取日志
[R] REPORT  → 归纳结果 + 解释系数 + 确认可复现性
```

**关键约束：**
- 没有 `logs/*.log` 或 `output/tables/*` 支撑的数值结论**不陈述**
- 不编造标准误、p值、样本量

---

## Stata-MCP 执行工具（与已有 stata-skill 兼容）

本技能兼容 [Stata-MCP](https://github.com/sepinetam/stata-mcp) 的执行方式：

```bash
# 检查是否可用
uvx stata-mcp --usable

# 执行do-file
uvx stata-mcp tool do dofiles/02_construct/main.do --log-file-name main

# 安装包
uvx stata-mcp tool ado-install reghdfe --source ssc

# 获取日志
uvx stata-mcp tool read-log logs/02_construct_main.log --output-format dict
```

**Stata 命令行直连（Windows）:**
```powershell
Start-Process -FilePath "D:\stata19\StataMP-64.exe" -ArgumentList '/e', 'do', 'dofiles/02_construct/main.do' -PassThru
```

---

## 项目标准结构

```bash
<project_root>/
├── dofiles/
│   ├── 00_master.do          # 流水线总入口
│   ├── 01_clean/             # 原始→清洗
│   ├── 02_construct/         # 变量构造
│   ├── 03_analysis/          # 回归/DiD/IV/DDML
│   └── 04_output/            # 表格+图
├── data/
│   ├── raw/                  # GITIGNORE
│   └── derived/              # GITIGNORE
├── logs/                     # GITIGNORE
├── output/tables/ & figures/
├── explorations/             # 沙盒
├── templates/
├── quality_reports/
│   ├── plans/
│   ├── session_logs/
│   └── merges/
└── scripts/
    ├── run_stata.sh /.bat
    └── quality_score.py
```

---

## 质量门禁速查

| 等级 | 含义 | 动作 |
|:-----|:-----|:-----|
| < 60 | 质量差 | 不提交，彻底重写 |
| 60-79 | 有改进空间 | 修正后重评 |
| 80-89 | **可接受** | ✓ 可以提交 |
| 90+ | **优秀** | ✓ 可以合并PR |

主要扣分项：无文件头(-10)、无日志(-15)、硬编码路径(-10)、缺失set seed(-5)……

---

## 引用

- 工作流方法论：Chen Zhu,「codex-stata-for-economists」, GitHub, 2025.
  https://github.com/maxwell2732/codex-stata-for-economists
- Stata执行工具：Sepinetam,「stata-mcp」, GitHub, 2025.
  https://github.com/sepinetam/stata-mcp
