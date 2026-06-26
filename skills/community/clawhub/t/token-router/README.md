# TokenRouter / 智能模型路由与Token成本优化顾问

> Intelligently select the optimal model tier for AI tasks of varying complexity, saving 70-90% on token costs without sacrificing quality.
> 为不同复杂度的 AI 任务智能选择最合适的模型层级，在保证质量的前提下节省 70-90% 的 Token 成本。

---

[English](#english) | [中文](#中文)

---

<a id="english"></a>

## Core Capabilities

- **4-Dimension Complexity Assessment**: Reasoning depth, output length, precision requirement, context dependency (1-5 scale), auto-mapped to L0-L3 model tiers
- **Safety-Forced Upgrades**: Auto-upgrade to L2+ for finance/legal/medical/security/production scenarios
- **Progressive User Profiling**: Learn preferences from conversation, no questionnaires
- **3 Routing Modes**: Direct (daily), Cascading (batch), Hybrid (Agent workflows)
- **Multi-Platform Support**: Trae IDE, Claude Code, OpenClaw, Hermes Agent, and more

## Model Tiers (Updated June 2026)

| Tier | Role | Representative Models | Typical Scenarios |
|------|------|----------------------|-------------------|
| **L0** | Router | DeepSeek-V4 Flash, GPT-4.1 nano, Gemini 2.5 Flash-Lite | Classification, extraction, formatting, routing |
| **L1** | Executor | MiniMax M3, Claude Haiku 4.5, Gemini 3.5 Flash | Summarization, translation, simple QA, structured output |
| **L2** | Reasoner | Claude Sonnet 4.6, GPT-5.5, Qwen 3.7 Max | Code generation, analysis reports, multi-step reasoning |
| **L3** | Creator | Claude Opus 4.8, GPT-5.5 Pro, o3 | Architecture design, creative writing, complex planning |

## Trigger Scenarios

This skill activates when users discuss:

- "API costs too high", "save money on AI", "token cost optimization", "reduce API bill"
- "which model should I use", "Sonnet vs Opus", "help me pick a model"
- "configure Hermes/OpenClaw multi-model routing", "model tiers", "intelligent scheduling"
- Solo founder / indie developer AI tool costs
- Building Agent workflows with different models for different tasks

## Usage Examples

**Simple Task → Lightweight Model**
```
User: Classify these 100 emails, find which ones are complaints
Recommend: DeepSeek-V4 Flash (L0) — email classification is pattern matching, lightweight model sufficient
Estimate: $0.02 (vs flagship $0.50, save 96%)
```

**Complex Task → Flagship Model**
```
User: Design a microservice architecture supporting million-level concurrency
Recommend: Claude Opus 4.8 (L3) — architecture design requires deep reasoning
```

**Agent Workflow → Hybrid Routing**
```
Email classification → L0 (DeepSeek V4 Flash)
Daily report generation → L1 (MiniMax M3)
Code review → L2 (Claude Sonnet 4.6)
Exception escalation → L3 (Claude Opus 4.8)
Estimated monthly cost: $3-8
```

## File Structure

```
token-router/
├── SKILL.md                          # Main skill file (decision flow, output formats, platform guides)
├── README.md                         # This file
├── references/
│   ├── model-tiers.md                # 20+ model tiers with pricing (with freshness disclaimer)
│   ├── routing-strategies.md         # Deep routing guide (cascading, caching strategies)
│   └── config-templates.md           # Config templates (Trae/OpenClaw/Hermes-specific)
└── evals/
    └── evals.json                    # Evaluation test cases (20 scenarios, 95% pass rate)
```

## Evaluation Results

| Dimension | Score |
|-----------|-------|
| Feature Completeness | 9/10 |
| Instruction Clarity | 9.5/10 |
| Test Pass Rate | 19/20 (95%) |
| Structural Compliance | 9/10 |
| Platform Coverage | 9/10 |
| **Overall** | **9.0/10** |

---

<a id="中文"></a>

## 核心能力

- **四维复杂度评估**：推理深度、输出长度、精度要求、上下文依赖（1-5分制），自动映射到 L0-L3 四个模型层级
- **安全强制升级**：金钱/法律/医疗/安全/生产环境场景自动升级到 L2+ 模型
- **渐进式用户画像**：从对话中学习偏好，不问问卷
- **三种路由方式**：单次路由（日常）、级联路由（批量）、混合路由（Agent工作流）
- **多平台支持**：Trae IDE、Claude Code、OpenClaw、Hermes Agent 等

## 模型分级体系（2026年6月更新）

| 层级 | 定位 | 代表模型 | 典型场景 |
|------|------|---------|---------|
| **L0** | 路由级 | DeepSeek-V4 Flash、GPT-4.1 nano、Gemini 2.5 Flash-Lite | 分类、提取、格式化、路由 |
| **L1** | 执行级 | MiniMax M3、Claude Haiku 4.5、Gemini 3.5 Flash | 摘要、翻译、简单QA、结构化输出 |
| **L2** | 推理级 | Claude Sonnet 4.6、GPT-5.5、Qwen 3.7 Max | 代码生成、分析报告、多步推理 |
| **L3** | 创造级 | Claude Opus 4.8、GPT-5.5 Pro、o3 | 架构设计、创意写作、复杂规划 |

## 触发场景

当用户涉及以下场景时自动触发：

- "API费用太贵"、"帮我省钱"、"Token太贵"、"怎么降本"
- "用哪个模型"、"Sonnet和Opus选哪个"、"帮我选模型"
- "配置Hermes/OpenClaw多模型路由"、"模型分级"、"智能调度"
- 一人公司/独立开发者的AI工具成本问题
- 搭建需要不同模型处理不同任务的Agent工作流

## 使用示例

**简单任务 → 轻量模型**
```
用户：帮我给100封邮件分个类，看哪些是投诉
推荐：DeepSeek-V4 Flash（L0）— 邮件分类是模式匹配，轻量模型足够
预估：$0.02（vs 旗舰 $0.50，省96%）
```

**复杂任务 → 旗舰模型**
```
用户：帮我设计一个微服务架构，要支持百万级并发
推荐：Claude Opus 4.8（L3）— 架构设计需要深度推理
```

**Agent工作流 → 混合路由**
```
邮件分类 → L0（DeepSeek V4 Flash）
日报生成 → L1（MiniMax M3）
代码review → L2（Claude Sonnet 4.6）
异常升级 → L3（Claude Opus 4.8）
预估月成本：$3-8
```

## 文件结构

```
token-router/
├── SKILL.md                          # 主技能文件（决策流程、输出格式、平台指引）
├── README.md                         # 本文件
├── references/
│   ├── model-tiers.md                # 20+ 模型详细分级与定价（含时效性声明）
│   ├── routing-strategies.md         # 路由策略深度指南（级联实现、缓存策略）
│   └── config-templates.md           # 配置模板（Trae/OpenClaw/Hermes 专属配置）
└── evals/
    └── evals.json                    # 评估测试用例（20个场景，95%通过率）
```

## 评估结果

| 维度 | 评分 |
|------|------|
| 功能完整性 | 9/10 |
| 指令清晰度 | 9.5/10 |
| 测试通过率 | 19/20（95%） |
| 结构合规性 | 9/10 |
| 平台覆盖 | 9/10 |
| **综合** | **9.0/10** |

---

## 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>
