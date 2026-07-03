# Skills Index

> 技术研判系统的所有技能，按 agent-skills 格式组织。
> 每次启动项目对话时，加载本索引 + 当前阶段对应的 Skill。

## Core Skills

| # | Skill | File | Phase | Status |
|---|-------|------|-------|--------|
| 1 | 核心技术分析 | [skills/deep-tech-dd-analysis/SKILL.md](skills/deep-tech-dd-analysis/SKILL.md) | 1st, 2nd | ✅ |
| 2 | BP话术反驳 | [skills/anti-rationalization/SKILL.md](skills/anti-rationalization/SKILL.md) | 1st, 2nd | ✅ |
| 3 | 质疑驱动分析 | [skills/doubt-driven-analysis/SKILL.md](skills/doubt-driven-analysis/SKILL.md) | 1st, 2nd | ✅ |
| 4 | 团队评估 | [skills/team-assessment/SKILL.md](skills/team-assessment/SKILL.md) | 1st, 2nd | ✅ |
| 5 | 供应链审计 | [skills/supply-chain-audit/SKILL.md](skills/supply-chain-audit/SKILL.md) | 2nd, 3rd | ✅ |
| 6 | 独立竞品发现 | [skills/competitor-discovery/SKILL.md](skills/competitor-discovery/SKILL.md) | 1st, 3rd | ✅ |
| 7 | 质量门控 | [skills/quality-gate/SKILL.md](skills/quality-gate/SKILL.md) | all rounds | ✅ |
| 8 | 报告生成 | [skills/report-generation/SKILL.md](skills/report-generation/SKILL.md) | all rounds | ✅ |
| 9 | 反馈采集 | [skills/feedback-collection/SKILL.md](skills/feedback-collection/SKILL.md) | post-delivery | ✅ |
| 10 | Q&A信息融合 | [skills/iteration-merge/SKILL.md](skills/iteration-merge/SKILL.md) | iteration | ✅ |

## Expert Personas

| Persona | File | Purpose |
|---------|------|---------|
| Tech Reviewer | [agents/tech-reviewer.md](agents/tech-reviewer.md) | 独立审查核心技术 claim 物理可行性 |
| Supply Chain Analyst | [agents/supply-chain-analyst.md](agents/supply-chain-analyst.md) | 审查供应链依赖和国产替代 |
| Team Evaluator | [agents/team-evaluator.md](agents/team-evaluator.md) | 评估团队能力匹配度和结构性缺口 |
| Competition Analyst | [agents/competition-analyst.md](agents/competition-analyst.md) | 独立竞品对标分析 |

## References (stubs, await enrichment)

| File | Content | Status |
|------|---------|--------|
| [references/physics-formulas.md](references/physics-formulas.md) | 常见技术方向的物理公式库 | 🏗️ stub |
| [references/supply-chain-framework.md](references/supply-chain-framework.md) | 供应商尽调通用框架 | 🏗️ stub |
| [references/team-assessment-template.md](references/team-assessment-template.md) | 逐人能力匹配度评估模板 | 🏗️ stub |
| [references/competitor-comparison.md](references/competitor-comparison.md) | 定量参数对比框架 | 🏗️ stub |
| [references/README.md](references/README.md) | 知识库使用说明 | ✅ |

## System Files

| File | Purpose |
|------|---------|
| [01-deeptechnic-definition.md](01-deeptechnic-definition.md) | Agent identity, capability scope, dialog rules |
| [02-workflow-rules.md](02-workflow-rules.md) | Four-round DD workflow overview |
| [evaluation-framework.md](evaluation-framework.md) | Project evaluation mind map / criteria |
| [.learnings/LEARNINGS.md](.learnings/LEARNINGS.md) | Cross-session learnings & process records |

## How to Use

1. Start project → load [01-deeptechnic-definition.md Section 3](01-deeptechnic-definition.md#启动协议强制每条新项目对话必须执行)
2. Load [02-workflow-rules.md](02-workflow-rules.md) for phase guidance
3. Load current phase's skill(s) from the Core Skills table
4. Execute using loaded skills
5. Run [quality-gate](skills/quality-gate/SKILL.md) before output
6. Run [feedback-collection](skills/feedback-collection/SKILL.md) after delivery
7. Data accumulates → trigger SkillOpt retraining
