# transcript-crafter

访谈实录转公众号深度长文全流程：10 维度提取 → 人设适配 → 框架 → 5 工具搜索补充 → 重构撰写。

[![版本](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/EdwardWason/transcript-crafter)
[![许可证](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-transcript--crafter-orange)](https://clawhub.ai/EdwardWason/transcript-crafter)

## 功能

- **10 维度提取**：从访谈实录中提取核心观点、行业洞察、数据事实、反常观点、劲爆点等 10 个维度
- **人设适配**：6 种写作人设自动匹配（行业老兵/技术极客/商业分析师/观察者/创业者/学者）
- **5 工具搜索补充**：WebSearch + WebFetch + 竞品分析 + 数据验证 + 背景补充
- **8 步主管道**：输入预处理 → 10 维度提取 → 人设适配 → 框架生成 → 搜索补充 → 撰写 → 质量验证 → 交付
- **3 确认点**：素材确认 → 框架确认 → 补充确认，确保方向正确
- **双通道交付**：本地保存 + 飞书云盘同步

## 快速开始

```bash
npx clawhub@latest install EdwardWason/transcript-crafter
```

## 使用方法

在 TRAE / Claude Code / OpenClaw 中，提供访谈实录文件路径即可触发：

```
请用 transcript-crafter 转写这篇文章：/path/to/transcript.md
```

## 文件结构

```
transcript-crafter/
├── SKILL.md                    # 技能主文件（入口）
└── references/
    ├── anti-ai-rules.md        # 反 AI 味写作规则
    ├── extraction-guide.md     # 10 维度提取指南
    ├── fact-check-guide.md     # 事实核查指南
    ├── interview-personas.yaml # 6 种写作人设配置
    ├── pipeline-detail.md      # 8 步管道详细说明
    ├── quality-checklist.md    # 质量验证清单
    ├── tool-router.md          # 5 工具搜索路由
    └── wechat-format-guide.md  # 公众号排版规范
```

## 文档

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 技能主文件，8 步管道+10 维度+人设适配 |
| [references/extraction-guide.md](references/extraction-guide.md) | 10 维度提取详细说明 |
| [references/pipeline-detail.md](references/pipeline-detail.md) | 8 步管道每步的输入/输出/规则 |
| [references/quality-checklist.md](references/quality-checklist.md) | 质量验证清单 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

License: MIT-0

---

# transcript-crafter

Full pipeline for converting interview/meeting transcripts into in-depth WeChat Official Account articles: 10-dimension extraction → persona matching → framework → 5-tool search supplement → reconstruction writing.

[![version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/EdwardWason/transcript-crafter)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-transcript--crafter-orange)](https://clawhub.ai/EdwardWason/transcript-crafter)

## Features

- **10-Dimension Extraction**: Extract core views, industry insights, data facts, contrarian views, explosive points, and 5 more dimensions from transcripts
- **Persona Matching**: 6 writing personas auto-matched (Industry Veteran / Tech Geek / Business Analyst / Observer / Entrepreneur / Scholar)
- **5-Tool Search Supplement**: WebSearch + WebFetch + competitor analysis + data verification + background supplement
- **8-Step Pipeline**: Input preprocessing → 10-dim extraction → persona matching → framework → search supplement → writing → quality check → delivery
- **3 Checkpoints**: Material confirmation → Framework confirmation → Supplement confirmation
- **Dual Delivery**: Local save + Feishu cloud drive sync

## Quick Start

```bash
npx clawhub@latest install EdwardWason/transcript-crafter
```

## Usage

In TRAE / Claude Code / OpenClaw, provide a transcript file path to trigger:

```
Please use transcript-crafter to convert this transcript: /path/to/transcript.md
```

## File Structure

```
transcript-crafter/
├── SKILL.md                    # Main skill file (entry point)
└── references/
    ├── anti-ai-rules.md        # Anti-AI-tone writing rules
    ├── extraction-guide.md     # 10-dimension extraction guide
    ├── fact-check-guide.md     # Fact-checking guide
    ├── interview-personas.yaml # 6 writing persona configs
    ├── pipeline-detail.md      # 8-step pipeline details
    ├── quality-checklist.md    # Quality verification checklist
    ├── tool-router.md          # 5-tool search router
    └── wechat-format-guide.md  # WeChat formatting guide
```

## Documentation

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Main skill file, 8-step pipeline + 10 dimensions + persona matching |
| [references/extraction-guide.md](references/extraction-guide.md) | 10-dimension extraction details |
| [references/pipeline-detail.md](references/pipeline-detail.md) | 8-step pipeline input/output/rules |
| [references/quality-checklist.md](references/quality-checklist.md) | Quality verification checklist |
| [CHANGELOG.md](CHANGELOG.md) | Version change log |

License: MIT-0
