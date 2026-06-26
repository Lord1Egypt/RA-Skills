# Tech Trend Radar

`tech-trend-radar` 是一个 Codex/OpenClaw skill，用于根据最新行业信号生成技术与市场趋势报告。它重点关注来源质量、AI 模型排名变化、GitHub 热度、公司策略变化、商业影响和可执行建议。

## 能力范围

- 跟踪 `1w`、`1m`、`3m` 三个窗口，用来区分短期热点和持续趋势。
- 监控 LMArena/Text Arena、Artificial Analysis、LiveBench、SWE-bench、OpenRouter 等模型榜单。
- 月报和季报必须包含当前 Top 10 模型排名表。
- 跟踪 OpenAI、Anthropic、Alibaba Qwen/通义千问、Zhipu GLM/智谱、Google Gemini/Gemma、Microsoft/GitHub、Meta、xAI 等 AI 公司策略变化。
- 捕捉 GitHub Trending 热度，包括 stars、forks、release、issue 活跃度和贡献者变化。
- 覆盖 AI/ML、Agent Platform Ecosystem、开发者工具、SaaS、云基础设施、安全、创业公司、融资和监管。
- 生成包含执行摘要、Top Signals、Company Strategy Watch、行动项、分类深挖、来源和观察清单的结构化报告。

## 使用示例

可以用类似下面的提示触发：

```text
Write this week's AI trend report
Show current top 10 AI models and ranking changes
Track Claude managed agents and agent teams updates
Generate a trend radar for developer tools
Summarize GitHub Trending for AI agents this month
What changed in SaaS and AI this week?
```

## 研究来源

优先使用一手、高信号来源：

- 官方博客、release notes、changelog、价格页
- Anthropic news、Claude docs、Claude Code docs、API changelog、企业管理文档
- GitHub releases、GitHub Trending、仓库活跃度、RFC
- 模型榜单与评测：LMArena/Text Arena、Artificial Analysis、LiveBench、SWE-bench、OpenRouter
- 公司策略来源：OpenAI、Anthropic、Alibaba/Tongyi Qianwen/Qwen、Zhipu AI/GLM、Google Gemini/Gemma、Microsoft/GitHub、Meta、xAI、Mistral、DeepSeek 官方新闻和文档
- 融资公告、并购、财报电话会、监管文件
- 可信行业媒体和社区信号；社区信号只作为辅助证据

## 报告质量规则

- 每次生成都要刷新最新来源，即使同一主题之前已经报告过。
- 月报和季报必须包含完整 Top 10 模型排名表。
- 月报必须包含 OpenAI、Anthropic、Alibaba Qwen、Zhipu AI 的策略更新；如果没有重大公开变化，也要明确写出已检查且未发现重大新动向。
- 模型排名部分需要在相关时检查 open-weight 和国内模型，例如 Gemma、Llama、Qwen/通义千问、GLM/智谱、DeepSeek、Kimi、ERNIE/文心、Hunyuan/混元、Doubao/豆包。
- 每个重要信号应包含事实、日期、证据链接、相比上一期的核心变化和建议动作。

## 报告输出

默认报告路径：

```text
memory/research/tech-trend-radar-YYYY-WXX.md
```

指定范围的报告示例：

```text
memory/research/tech-trend-radar-ai-agents-YYYY-WXX.md
memory/research/tech-trend-radar-ai-agents-1m-YYYY-MM.md
memory/research/tech-trend-radar-ai-agents-3m-YYYY-QN.md
```

## Skill 文件

```text
tech-trend-radar/
├── README.md
└── SKILL.md
```

`SKILL.md` 包含实际的 skill 指令，包括研究流程、报告模板、事件 payload 和关键词配置。

## 维护

保持 `SKILL.md` frontmatter 简洁有效：

```yaml
---
name: tech-trend-radar
description: Use when generating current technology, AI model ranking, product, startup, funding, regulation, or market trend reports from recent industry updates
author: Chad Liu
---
```

提交前检查文档：

```bash
sed -n '1,80p' tech-trend-radar/SKILL.md
sed -n '1,120p' tech-trend-radar/README.md
git status --short
```
