# 模型分级参考

> **价格时效性声明**：本文档定价数据更新于 2026年6月3日。大模型 API 价格变动频繁（月度级别），以下数据仅供参考。
> **使用前务必核实各厂商官方定价页**：
> - Anthropic: https://docs.anthropic.com/en/docs/about-claude/pricing
> - OpenAI: https://openai.com/api/pricing/
> - Google: https://ai.google.dev/pricing
> - DeepSeek: https://api-docs.deepseek.com/quick_start/pricing
> - xAI: https://docs.x.ai/docs/models
> - MiniMax: https://platform.minimaxi.com/docs/guides/pricing-paygo
> - Microsoft MAI: https://microsoft.ai/pricing
>
> 通过 OpenRouter (https://openrouter.ai) 可统一接入 200+ 模型，避免频繁更新各厂商配置。
> 价格单位：美元/百万 Token（$ / MTok）

## 目录
- [Tier 0：极致性价比（路由/分类专用）](#tier-0)
- [Tier 1：轻量级（日常执行）](#tier-1)
- [Tier 2：中端（推理/代码/分析）](#tier-2)
- [Tier 3：旗舰（复杂推理/创造）](#tier-3)
- [按场景推荐矩阵](#场景推荐矩阵)
- [价格趋势观察](#价格趋势观察)

---

## Tier 0：极致性价比

适用于：意图分类、关键词提取、简单格式化、路由决策、二分类

| 模型 | 输入 $/MTok | 输出 $/MTok | 上下文 | 特点 |
|------|-----------|-----------|--------|------|
| GLM-4.7-Flash | $0.07 | $0.40 | 200K | 智谱永久免费（1并发），200K上下文 |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | 1M | 极低价格+超长上下文 |
| GPT-4.1 nano | $0.10 | $0.40 | 128K | OpenAI最低价模型 |
| DeepSeek-V4 Flash | $0.14 | $0.28 | 128K | 中文场景极优，腾讯云降价97.5% |
| GPT-4o-mini | $0.15 | $0.60 | 128K | OpenAI经典性价比王 |
| Grok 4.1 Fast | $0.20 | $0.50 | 128K | xAI轻量快速模型 |
| MAI-Code-1-Flash | $0.75 | $4.50 | 256K | 微软5B编程专用，GitHub Copilot集成 |

**选择建议**：
- 需要超长上下文 → Gemini 2.5 Flash-Lite（1M）
- 中文/分类场景 → DeepSeek-V4 Flash
- OpenAI生态 → GPT-4.1 nano 或 GPT-4o-mini
- 零成本 → GLM-4.7-Flash（永久免费，限1并发）或本地部署 Qwen via Ollama
- 编程辅助 → MAI-Code-1-Flash（Copilot内集成，简单任务token消耗降60%）

---

## Tier 1：轻量级

适用于：摘要、翻译、简单QA、代码补全、结构化输出、数据提取、中等复杂度写作

| 模型 | 输入 $/MTok | 输出 $/MTok | 上下文 | 特点 |
|------|-----------|-----------|--------|------|
| Grok 4.1 | $0.20 | $0.50 | 128K | 极低价格，日常任务首选 |
| DeepSeek-V4 Pro | $0.27 | $1.10 | 128K | 中文综合性价比最高 |
| MiniMax M3 (≤512K) | $0.60 | $2.40 | 1M | 开源，SWE-Bench Pro超GPT-5.5，1M上下文 |
| Claude Haiku 4.5 | $0.80 | $4.00 | 200K | 速度快、质量稳定 |
| Gemini 3.5 Flash | $1.50 | $9.00 | 1M | 超越上代旗舰，速度4x提升，输出289 tok/s |
| Llama 3.3 70B (自托管) | ~$0.05 | ~$0.05 | 128K | 成本可控、数据私有 |

**选择建议**：
- 中文写作/分析 → DeepSeek-V4 Pro
- 需要稳定质量 → Claude Haiku 4.5
- 编程+长上下文 → MiniMax M3（开源，1M上下文，限时五折$0.30/$1.20）
- 速度+性价比 → Gemini 3.5 Flash（超越上代Pro级模型，输出$9仍远低于旗舰）
- 极致省钱 → Grok 4.1
- 数据隐私要求 → Llama 自托管

---

## Tier 2：中端

适用于：代码生成、分析报告、多步推理、文档撰写、复杂数据分析

| 模型 | 输入 $/MTok | 输出 $/MTok | 上下文 | 特点 |
|------|-----------|-----------|--------|------|
| DeepSeek-V4 Pro (高参) | $0.54 | $2.18 | 128K | 同模型高参数版本，性价比极高 |
| Mistral Large | $2.00 | $6.00 | 128K | 欧洲厂商、多语言 |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 200K | 代码质量业界顶级 |
| GPT-5.5 | $5.00 | $30.00 | 128K | Terminal-Bench 82.7%，最强CLI/Agent能力 |
| Qwen 3.7 Max | 待定 | 待定 | 260K | Arena全球第五、国产第一，限时5折 |
| Kimi K2.6 | 待定 | 待定 | 待定 | Agent能力强化，开源，ARR超2亿美元 |

**选择建议**：
- 编程/代码 → Claude Sonnet 4.6
- CLI/终端任务 → GPT-5.5（Terminal-Bench最强）
- 预算有限 → DeepSeek-V4 Pro 高参
- 国产替代 → Qwen 3.7 Max 或 Kimi K2.6
- 多语言/欧洲合规 → Mistral Large

---

## Tier 3：旗舰

适用于：架构设计、创意写作、复杂规划、关键决策、深度推理、安全审计

| 模型 | 输入 $/MTok | 输出 $/MTok | 上下文 | 特点 |
|------|-----------|-----------|--------|------|
| GPT-5.5 Pro | 待定 | 待定 | 128K | OpenAI旗舰，GPT-5.6预计6月8-14日发布 |
| Claude Opus 4.8 | $5.00 | $25.00 | 1M | SWE-Bench Pro 69.2%，最诚实模型，思考力度可控 |
| o3 / o3-pro | $10.00 | $40.00 | 200K | 深度推理专用 |
| Gemini 3.5 Pro | 待定 | 待定 | 2M | 预计6月发布，3.5系列旗舰 |
| MAI-Thinking-1 | 待定 | 待定 | 256K | 微软自研推理模型，35B活跃参数，未蒸馏第三方 |
| MiniMax M3 (>512K) | $8.40 | $33.60 | 1M | 超长上下文旗舰级，开源 |

**选择建议**：
- 复杂编程/架构 → Claude Opus 4.8（SWE-Bench Pro 69.2%领先）
- 深度推理/数学 → o3
- 企业级推理（IP清洁度）→ MAI-Thinking-1（未蒸馏，授权数据训练）
- 综合旗舰 → GPT-5.5 Pro（等6月GPT-5.6发布）
- 超长上下文旗舰 → Gemini 3.5 Pro（等6月发布）
- 开源旗舰+长上下文 → MiniMax M3

---

## 场景推荐矩阵

| 场景 | 推荐模型 | 预估成本/百万Token | 理由 |
|------|---------|-------------------|------|
| 聊天客服 | GPT-4.1 nano | $0.50 | 简单对话无需强模型 |
| 邮件分类 | DeepSeek-V4 Flash | $0.42 | 模式匹配，极低成本 |
| 代码生成 | Claude Sonnet 4.6 | $18.00 | 代码质量领先 |
| 文档分析（超长） | MiniMax M3 | $3.00 | 1M上下文+超越GPT-5.5的编程能力 |
| 中文写作 | DeepSeek-V4 Pro | $1.37 | 中文质量优+价格低 |
| 数据提取 | Gemini 2.5 Flash-Lite | $0.50 | 极低价格+结构化可靠 |
| 架构设计 | Claude Opus 4.8 | $30.00 | SWE-Bench Pro 69.2%领先 |
| 批量处理 | GPT-4o-mini | $0.75 | 高吞吐+低成本 |
| 安全审计 | Claude Opus 4.8 | $30.00 | 零容忍错误+诚实性最强 |
| CLI/终端任务 | GPT-5.5 | $35.00 | Terminal-Bench 82.7%最强 |
| 高速Agent循环 | Gemini 3.5 Flash | $10.50 | 289 tok/s输出+超越上代旗舰 |
| 编程Copilot | MAI-Code-1-Flash | $5.25 | 简单任务token消耗降60% |

## 价格趋势观察（2026年6月）

2026年关键趋势：
1. **国产模型性能爆发**：MiniMax M3 SWE-Bench Pro超GPT-5.5，Qwen 3.7 Max Arena全球第五
2. **价格断崖式下降**：DeepSeek-V4 腾讯云降价97.5%，MiniMax M3 仅为海外旗舰5-10%
3. **Flash超越Pro**：Gemini 3.5 Flash超越上代Gemini 3.1 Pro，"级别"定义正在失效
4. **微软自研加速**：MAI系列从代码到推理全覆盖，去OpenAI化趋势明确
5. **输出/输入价差扩大**：输出价格普遍是输入的 4-8 倍
6. **缓存折扣普及**：Anthropic/OpenAI 缓存命中可降 90%/50%
7. **Batch API 折扣**：各大平台批量调用享 50% 折扣
8. **1M上下文成标配**：MiniMax M3、DeepSeek-V4、Gemini 3.5系列均支持百万级上下文
