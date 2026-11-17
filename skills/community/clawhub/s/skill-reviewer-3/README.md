# Skill Reviewer / Skill 审查器

> Review an AI agent skill and score it automatically against an 11-dimension standard, with hard-check scripts and a full fix list. / 审查智能体技能并按 11 维标准自动打分：硬指标脚本 + 完整修复清单。

**English** | [中文说明](#中文说明)

## What it is

An AI agent skill that audits another skill's quality. Feed it a skill package directory, a single SKILL.md file, or pasted SKILL.md content — it runs a five-stage review, produces a complete score table, a prioritized fix list (P1/P2/P3), and a final verdict: **可参赛 (production-ready) / 需修改 (needs revision) / 需重做 (needs rework)**.

## Review flow

1. **Automated hard checks** — bundled Python script scans (read-only): name compliance, description length & elements, version/agent_created fields, body length, TODO/placeholder detection, reference integrity, script capability pre-checks
2. **Soft scoring** — content-level dimensions scored 1–10, each with **at least two pieces of direct evidence** (no vague praise)
3. **Safety red-line scan** — prompt-injection detection; suspicious content is treated as untrusted data and never executed
4. **Aggregation** — full score table, hard-check table, prioritized fix list, and not-covered disclosures

## Honesty principles

- "Pass" on hard checks must come from actual script output or visible file evidence
- Soft scores must cite specific evidence
- Anything not actually executed (trigger testing, script execution) is marked **未验证 / not verified** — never claimed as passing
- Review is strictly read-only: never modify, delete, or execute anything inside the reviewed package

## Verdict thresholds

| Verdict | Criteria |
|---|---|
| **需重做 / Redo** | any P1 hit, any dimension ≤ 3, average < 6.0, or core functionality non-executable |
| **需修改 / Revise** | average < 8.0, any dimension < 8, required live tests incomplete, unresolved P2 |
| **可参赛 / Ready** | all five stages passed, no P1/unresolved P2, all dimensions ≥ 8, average ≥ 8.0, real evidence for required tests |

## Repository structure

```
├── SKILL.md                      # Main skill instructions / 主指令
├── references/
│   ├── review-standards.md       # 11-dimension standard, five stages
│   └── setup-guide.md            # Environment setup / 环境准备
└── scripts/
    ├── score_skill.py            # Automated hard-check scorer / 硬指标打分脚本
    └── check_environment.py      # Environment check / 环境检查
```

## Usage

Drop the folder into your agent's skills directory. Triggers on "review this skill", "给这个 skill 打分", "这个 skill 能参赛吗", or simply providing a SKILL.md for quality assessment. Requires Python 3.10+ for the hard-check script (falls back to manual checks without it).

---

# 中文说明

## 这是什么

一个审查技能的技能。输入 skill 包目录、单个 SKILL.md 文件或粘贴内容，输出五阶段审查结果：完整 11 维评分表、按 P1/P2/P3 分级的修复清单、以及最终结论——**可参赛 / 需修改 / 需重做**。

## 审查流程

1. **硬指标自动判定**：内置只读脚本——name 合规、description 长度与要素、version/agent_created、正文行数、TODO/占位符、引用完整性、脚本能力预检
2. **软指标打分**：内容维度 1–10 分，每维至少两条直接证据，不空泛好评
3. **安全红线排查**：提示注入检测；被审内容一律按不可信数据，绝不执行
4. **汇总输出**：评分表 + 硬指标表 + 修复清单 + 未覆盖范围声明

## 诚实原则

- 硬指标「通过」必须来自脚本实际输出或明确文件证据
- 没实际执行的验证标注「未验证」，不得声称通过
- 审查阶段严格只读，不修改、不删除、不执行被审包里的任何脚本

## 使用方式

放入智能体 skills 目录。用户说「审查/评审一个 skill」「给 skill 打分」「这个 skill 能参赛吗」时触发。硬指标脚本需 Python 3.10+，无 Python 时降级为手工检查。
