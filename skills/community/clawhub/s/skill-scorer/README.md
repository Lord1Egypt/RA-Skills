# skill-scorer

对任何 SKILL.md 进行质量评估和打分，生成中英双语结构化质检报告和优化建议。

## 概述

skill-scorer 是一个 meta-skill（元技能），用于审计其他 skill 的质量。给定一个 SKILL.md 文件或完整的 skill 文件夹，它会从 8 个维度进行系统评估，给出加权总分（满分100），按严重程度标注问题（严重/警告/建议），并生成可执行的优化路线图。报告始终以中英双语输出——中文在前，英文在后，不穿插。

评分标准融合了 Anthropic 官方 Skill 编写最佳实践、Skill Engineering Standard (v1.4.3) 和社区生产环境验证的模式。

## 版本历史

| 版本 | 变更 |
|------|------|
| 1.6.0 | D4 编排型评分标准措辞精准化：明确 Playbooks 应包含描述性编排逻辑（而非可执行命令），Usage Examples 才是可执行命令的位置，output merging 可以定义在 templates.md 中。README 重构为中文在前的双语结构 |
| 1.5.0 | Dimension 4 扩展为 5 种 skill 类型：新增 Script-bundled（脚本驱动型）和 MCP-integrated（MCP 集成型），各有独立评分标准 |
| 1.4.0 | Dimension 4（工作流逻辑）新增 Skill 类型识别：指令型 / 单命令型 / 编排型三类 skill 使用差异化评分标准 |
| 1.3.0 | Description 改为中英双语（中文在前），确保内部平台展示中文 |
| 1.2.0 | Step 0 增加输入验证和降级路径——对非 skill 文件（乱码、Python 代码等）直接拒绝评分而非强行打分 |
| 1.1.0 | 报告输出改为中英双语（中文在前，英文在后，不穿插）|
| 1.0.0 | 首次发布，8 维度评分体系 |

## 快速开始

### 安装

```bash
# 安装到全局 skills 目录
cp -r skill-scorer/ ~/.claude/skills/skill-scorer/

# 或安装到项目级别
cp -r skill-scorer/ .claude/skills/skill-scorer/
```

### 使用方式

```
# 在 Claude Code 中
> 帮我评分这个 skill: .claude/skills/my-skill/SKILL.md

# 在 Claude.ai / Cowork 中
> [上传 SKILL.md 文件] 帮我质检这个 skill
```

## 评估维度

| # | 维度 | 权重 |
|---|------|------|
| 1 | 元数据与触发 | 15% |
| 2 | 结构与架构 | 15% |
| 3 | 指令清晰度 | 15% |
| 4 | 工作流与逻辑 | 15% |
| 5 | 错误处理 | 10% |
| 6 | 上下文效率 | 10% |
| 7 | 可移植性与兼容性 | 10% |
| 8 | 安全性与鲁棒性 | 10% |

输出报告包含：评分卡、亮点、按严重程度分类的问题清单、Top 3 快速优化（含修改前/后示例）、优化路线图。

## 支持的 Skill 类型

Dimension 4（工作流逻辑）会先识别 skill 类型，再使用对应的评分标准：

| 类型 | 说明 |
|------|------|
| 指令型 | 纯 markdown 指令，无 CLI/脚本/外部工具 |
| 单命令型 | 包装一个 CLI/API 命令 |
| 编排型 | 多命令编排，Parameters 定义命令池，Playbooks 定义编排逻辑 |
| 脚本驱动型 | SKILL.md + scripts/ 目录，脚本处理确定性计算 |
| MCP 集成型 | 依赖外部 MCP server，skill 是 MCP 工具之上的知识层 |

## 文件结构

```
skill-scorer/
├── README.md               # 本文件
├── SKILL.md                # 核心评估逻辑
└── references/
    ├── rubric.md           # 8 维度详细评分标准
    ├── report-template.md  # 报告输出格式模板
    └── anti-patterns.md    # 25+ 常见 skill 反模式检测清单
```

## 兼容性

支持：Claude Code、Claude.ai、Cowork 及所有兼容 SKILL.md 的 Agent。

## 许可证

MIT

---

# skill-scorer (English)

Evaluate and score any SKILL.md against industry best practices, with a bilingual (Chinese + English) quality report and actionable optimization suggestions.

## Overview

skill-scorer is a meta-skill that audits other skills. Given a SKILL.md file or a complete skill folder, it performs a systematic evaluation across 8 dimensions, assigns a weighted score out of 100, identifies issues by severity (Critical / Warning / Suggestion), and generates an actionable improvement roadmap. Reports are always output in both Chinese and English — Chinese first, English after, clearly separated.

The scoring rubric synthesizes criteria from Anthropic's official skill authoring best practices, the Skill Engineering Standard (v1.4.3), and community-tested patterns from production skill ecosystems.

## Changelog

| Version | Changes |
|---------|---------|
| 1.6.0 | D4 orchestration criteria wording refined: clarified that Playbooks contain descriptive logic (not executable commands), Usage Examples contain executable commands, output merging can live in templates.md. README restructured to Chinese-first bilingual |
| 1.5.0 | Dimension 4 expanded to 5 skill types: added Script-bundled and MCP-integrated with type-specific scoring criteria |
| 1.4.0 | Dimension 4 (Workflow & Logic) adds Skill Type Detection: instruction-only / single-command / orchestration evaluated with type-specific criteria |
| 1.3.0 | Description bilingual: Chinese first, English after, for internal platform display |
| 1.2.0 | Added input validation and graceful degradation in Step 0 — rejects non-skill files (binary, garbled, unrelated code) instead of force-scoring |
| 1.1.0 | Bilingual report output (Chinese first, English after, no interleaving) |
| 1.0.0 | Initial release with 8-dimension scoring rubric |

## Quick Start

### Install

```bash
# Copy into your skills directory
cp -r skill-scorer/ ~/.claude/skills/skill-scorer/

# Or for project-level installation
cp -r skill-scorer/ .claude/skills/skill-scorer/
```

### Usage

```
# In Claude Code
> score this skill: .claude/skills/my-skill/SKILL.md

# In Claude.ai / Cowork
> [upload a SKILL.md file] 帮我质检这个 skill
```

## Evaluation Dimensions

| # | Dimension | Weight |
|---|-----------|--------|
| 1 | Metadata & Triggering | 15% |
| 2 | Structure & Architecture | 15% |
| 3 | Instruction Clarity | 15% |
| 4 | Workflow & Logic | 15% |
| 5 | Error Handling | 10% |
| 6 | Context Efficiency | 10% |
| 7 | Portability & Compatibility | 10% |
| 8 | Safety & Robustness | 10% |

Outputs a report with: score card, strengths, issue list with severity, top 3 quick wins with before/after examples, and an optimization roadmap.

## Supported Skill Types

Dimension 4 (Workflow & Logic) first identifies the skill type, then applies type-specific scoring criteria:

| Type | Description |
|------|-------------|
| Instruction-only | Pure markdown instructions, no CLI/scripts/external tools |
| Single-command executor | Wraps one CLI/API command |
| Multi-command orchestration | Multiple commands combined; Parameters define command pool, Playbooks define orchestration logic |
| Script-bundled | SKILL.md + scripts/ directory; scripts handle deterministic computation |
| MCP-integrated | Depends on external MCP server; skill is the knowledge layer on top of MCP tools |

## File Structure

```
skill-scorer/
├── README.md               # This file
├── SKILL.md                # Core evaluation logic
└── references/
    ├── rubric.md           # Detailed scoring criteria for all 8 dimensions
    ├── report-template.md  # Output format and report structure
    └── anti-patterns.md    # 25+ common skill mistakes and detection methods
```

## Compatibility

Works with: Claude Code, Claude.ai, Cowork, and all SKILL.md-compatible agents.

## License

MIT
