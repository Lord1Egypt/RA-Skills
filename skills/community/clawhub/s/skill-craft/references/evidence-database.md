# Evidence Database for Skill Optimization

Complete research findings from 25+ peer-reviewed papers (ACL/NeurIPS/EMNLP/ICWSM 2023-2025), 6 official AI vendor guidelines (Anthropic/Google/Microsoft/Brex/DAIR.AI/Lilian Weng), and production-grade engineering practices from Claude Code/Cursor/Windsurf/Aider communities.

## Table of Contents

- [D1: Trigger Description Quality](#d1-trigger-description-quality)
- [D2: Context Efficiency](#d2-context-efficiency)
- [D3: Structured Instructions](#d3-structured-instructions)
- [D4: Step Decomposition](#d4-step-decomposition)
- [D5: Positive Constraints](#d5-positive-constraints)
- [D6: Example Design](#d6-example-design)
- [D7: Verification Mechanisms](#d7-verification-mechanisms)
- [D8: Freedom Calibration](#d8-freedom-calibration)
- [D9: Progressive Loading](#d9-progressive-loading)
- [Cross-Dimension Studies](#cross-dimension-studies)
- [Official Guidelines Comparison](#official-guidelines-comparison)
- [Community Evidence](#community-evidence)

---

## D1: Trigger Description Quality

> 触发描述是 skill 能否被正确激活的关键入口。描述质量直接决定 LLM 在意图匹配阶段是否选择加载该 skill。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| Meta-analysis of prompt quality (Do et al., ACL 2025) | 单一属性优化（如描述精确度）往往产生最大影响；触发匹配属于"首次交互"维度，错误率在此阶段最高 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic Official | description 是首要触发机制；将 "when to use" 信息放在描述中，而非 body 内部 |
| Claude Code plugin-dev SKILL.md 模式 | 使用第三人称，包含具体触发短语，如 "create a hook"、"add a PreToolUse hook" |

### Community Evidence

| Issue | 投票数 | 关键发现 |
|---|---|---|
| Claude Code Issue #9716 | 69👍 | Skill "shadcn-components" 已存在于 `.claude/skills/` 但未被识别。原因是 description 缺少具体组件名和触发短语 |
| Claude Code Issue #18192 | 40👍 | 社区请求递归 skill 发现 — 子目录中的 skill 未被找到 |

### Design Implications

1. **必含触发短语**：描述中必须包含用户可能使用的自然语言短语
2. **具体而非笼统**：`"创建 OpenClaw 插件（hook/tool/provider/channel 任意类型）"` 优于 `"帮助开发插件"`
3. **场景枚举**：列出所有适用的触发场景，用编号或无序列表
4. **第三人称**：与 Claude Code 的 skill 匹配机制保持一致

---

## D2: Context Efficiency

> 上下文窗口是稀缺资源。skill 加载的每一行都在与其他指令、代码、对话历史竞争注意力。效率即性能。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| **CFPO** (Liu et al., Fudan University & Microsoft Research Asia, 2025, arXiv) | 首个系统性研究 content + format 联合优化。GSM8K 数学推理：LLaMA-3.1-8B baseline 50.03% → CFPO 63.38% (+13.35pp)；Big-Bench 分类：Mistral-7B baseline 56.00% → CFPO 94.00% (+38pp!)。消融实验：content-only (58.07%) + format-only (52.46%) < joint (63.38%) — 证明内容与格式相互依赖 |
| **LinguaShrink** (Liang et al., IEEE Access 2024) | 心理语言学提示压缩可在维持性能的同时减少 token 数量 |
| **SCOPE** (Zhang et al., arXiv 2025) | 过度压缩会丢失关键约束。需要在压缩率与信息保留之间取得平衡 |
| **What's in a Prompt** (Atreja et al., ICWSM 2025) | 16 条件析因实验，跨 4 个模型。精简提示降低成本，但可能在某些任务上降低准确率 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic Best Practices | "Most best practices derive from one constraint: context fills fast, performance degrades as it fills."（大多数最佳实践源于一个约束：上下文填满快，性能随填充而下降） |
| Anthropic on Multi-Context Windows | 首个窗口构建框架（测试、setup 脚本）；后续窗口迭代 todo-list；优先使用新鲜上下文而非压缩 |

### Community Evidence

| Issue | 投票数 | 关键发现 |
|---|---|---|
| Claude Code Issue #2544 | 39👍 | CLAUDE.md 规则在文件超过 ~200 行时被一致性地忽略 |
| Claude Code Issue #6354 | 27👍 | CLAUDE.md 内容在上下文压缩后被遗忘 |
| Claude Code Issue #41279 | New | Compaction-Protected Rulebook 提案 — 三层分离：Skills（任务流程）、Rulebook（持久规则，压缩保护）、CLAUDE.md（项目上下文） |

### Design Implications

1. **Skill body 限制在 <5k 词**：Claude Code 的三级加载机制已证明此阈值有效
2. **首 100 词决定命运**：metadata 层（~100 词）始终加载，必须包含最关键信息
3. **用结构化格式替代冗长描述**：表格、列表、流程图比散文更高效
4. **避免与 CLAUDE.md 重复**：重复内容浪费上下文且在压缩后产生不一致

---

## D3: Structured Instructions

> 结构化指令通过清晰的分区和格式约定，显著提升 LLM 对复杂指令的遵从度。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| **CFPO** (Liu et al., 2025) | Format + content 联合优化显著优于单独任一维度。不同 LLM 有截然不同的格式偏好 — 没有通用的"最佳格式"，模型特定格式优化至关重要 |
| **Structured Outputs in Prompt Engineering** (Ye et al., ACL 2025 Workshop) | 结构化 I/O 显著提升 LLM 对反直觉指令的遵从度 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic | 推荐 XML 标签（`<instructions>`、`<example>`、`<constraints>`）进行清晰分区。嵌套标签用于层级内容：`<documents>` > `<document>`。长文档放提示词顶部，查询放末尾 → 质量提升可达 30%。引用锚定：要求模型在回答前引用相关文档段落 |
| Google Gemini 3 Guide | "Use XML tags or Markdown headings to clearly separate prompt sections." 关键指令放在 System Instruction 首位。具体查询放在 user prompt 末尾。使用 "Based on the information above..." 锚定上下文 |
| Microsoft | 将提示词分解为 4 组件：Instructions、Primary Content、Examples、Cue。GPT 本质上是补全引擎 — "answer" 只是给定问题输入的最可能补全。提示短语（如 "Key Points:"）可控制输出格式 |

### Community Evidence

Claude Code 的 SKILL.md 模式广泛使用 Markdown 标题 + 列表 + 表格 + 代码块的结构化格式，社区反馈表明此模式显著优于无结构散文。

### Design Implications

1. **每个 skill 使用一致的章节结构**：触发场景 → 核心原则 → 步骤 → 示例 → 约束 → 验证
2. **XML 标签用于动态内容**：需要 LLM 填充或引用的部分使用 `<placeholder>` 标签
3. **关键信息首尾放置**：利用 primacy 和 recency 效应
4. **层级嵌套不超过 3 层**：过深嵌套降低可读性

---

## D4: Step Decomposition

> 将复杂任务分解为明确步骤可提升推理质量和执行可靠性，但并非所有任务都需要同等程度的分解。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| **Chain of Methodologies** (Liu et al., Findings of ACL 2025) | 将方法论洞察注入结构化推理过程的迭代提示框架。在复杂推理上优于竞争基线，无需训练 |
| **Watch Every Step** (Xiong et al., EMNLP 2024) | 迭代步骤级过程细化。步骤级指导显著提升 agent 训练效率。使用蒙特卡洛估计进行步骤级奖励评估 |
| **Read Before You Think** (Han et al., arXiv 2025) | 引导 LLM 在思考前逐步阅读的结构化提示族。即使系统提示为空，结构化阅读指导也能显著改善复杂理解 |
| **Think or Step-by-step** (Gohani Sadr, Brock University, 2025) | "Let's think step by step" vs "Let's think" 产生显著不同的内部推理行为。"Step by step" 并非普遍有益 — 取决于任务和模型 |
| **Guiding LLMs via Directional Stimulus Prompting** (Li et al., NeurIPS 2023) | "Let's think step by step using our creative brains" 产生比简单 "think step by step" 更高质量的推理。需要任务特定的刺激短语 |
| **What Should We Engineer in Prompts** (Ma et al., ACM TOCHI 2025) | 30 名提示工程新手的对照实验。结构化提示工程训练导致更具迭代性、结构化的提示行为 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic | Claude 4.6 Adaptive Thinking — "Think thoroughly" 通常优于手写逐步计划。但对于 skill 设计，显式步骤仍优先，因为 skill 需要确定性指导 |

### Community Evidence

| 来源 | 关键发现 |
|---|---|
| Cursor Best Practices | Plan-and-Act 策略 — 执行前始终展示包含文件路径的详细实现计划。计划保存至 `.cursor/plans/` |

### Design Implications

1. **步骤数量与任务复杂度匹配**：简单任务 2-3 步，复杂任务 5-8 步
2. **每步一个可验证的输出**：步骤终点应有明确的完成标准
3. **步骤间依赖关系显式声明**：使用"前置条件"/"后续步骤"标注
4. **避免过度分解**：每增加一步都增加上下文消耗和出错概率

---

## D5: Positive Constraints

> 正面约束（"使用 X"）比负面约束（"不要使用 Y"）更可靠地被遵循，这是经过大规模基准测试验证的结论。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| **Inverse IFEval** (Zhang et al., ByteDance Seed / Nanjing University / Peking University, arXiv 2025) | 首个反直觉指令大规模基准。1012 个高质量中英文问题，23 个领域，8 种反直觉指令类型。**所有主流 LLM 在反直觉指令上的表现显著差于常规指令**。"反常规格式"（如"不要使用列表格式"）是最难的类型。思考模型（Qwen3-235B-Thinking）远优于非思考模型 — 反思有助于克服 SFT 偏差 |
| **Compact Constraint Encoding** (Tang, arXiv 2026) | 正面约束（"use X"）比负面约束（"don't use Y"）更可靠地被遵循。编码紧凑性与遵从率之间存在权衡 |
| **Constraint Decomposition** (Paunova, Optimization Online 2025) | 将多目标约束分解后，IFEval 基线的 prompt 级准确率从 41.2% 提升至 73.8%（+32.6pp）。消融实验确认约束分解是改进的主要来源 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic | "Instead of 'don't use markdown', say 'use flowing prose paragraphs'" |
| Google | "Be precise and direct — avoid unnecessary or overly persuasive language" |

### Design Implications

1. **所有约束转化为正面表述**：`"不要使用 emojis"` → `"使用纯文本，不含 emoji 字符"`
2. **约束分解**：`"遵循代码规范"` → `"使用 TypeScript strict mode"、"函数不超过 20 行"、"所有公共 API 必须有 JSDoc"`
3. **约束分级**：MUST / SHOULD / MAY 区分优先级
4. **反直觉约束需加解释**：当约束违反模型训练偏好时，说明"为什么"

---

## D6: Example Design

> 精心设计的示例是控制 LLM 输出最可靠的机制，但数量并非越多越好——质量和多样性更为关键。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| **ACL 2025 Distillation Study** (Chen et al., Findings of ACL 2025) | 1-shot 在灵活性与结构之间取得最佳平衡。更多示例不一定有帮助。教师模型多样性比准确率更重要 |
| **Effect of Prompt Strategy on Code Generation** (Wang, University of Gothenburg, 2025) | 从 zero-shot → few-shot → CoT + role 呈渐进式改进。示例的质量和多样性比数量更重要 |
| **Are Prompts All You Need** (Binkhonain & Alfayez, Requirements Engineering, Springer, 2025) | 最优 few-shot 示例数量因任务复杂度而异。简单任务：1-2 个，复杂任务：5-8 个 |
| **Heart Team Simulation** (Garin et al., European Heart Journal, 2025) | 超过最优数量后，额外示例导致性能下降，原因是注意力稀释 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic | 推荐 3-5 个精心设计的示例。使用 `<example>` 标签。示例应相关、多样、结构化 |
| Google Gemini Guide | "We recommend to always include few-shot examples." 即使 2 个示例也能逆转模型偏好 |
| Microsoft | 示例可以展示模型在训练中从未见过的模式。Few-shot 是最可靠的输出控制机制 |

### Community Evidence

| 来源 | 关键发现 |
|---|---|
| Cursor Official Blog (2026-01) | 在 .mdc 文件中包含 Good vs. Bad 示例块，使规则有效性提升约 3 倍 |

### Design Implications

1. **使用 Good/Bad 对照示例**：正反对比比单一正面示例有效 3 倍
2. **示例数量因任务而异**：skill 核心流程 2-3 个，边界情况 1-2 个
3. **示例必须来自真实场景**：合成示例容易被模型识别为"模板"而降低遵从度
4. **示例多样性**：覆盖不同输入类型、不同复杂度级别

---

## D7: Verification Mechanisms

> 没有验证标准的 agent 会产生"看起来对但实际不工作"的输出。验证机制是生产级 AI 工程的基石。

### Academic Evidence

当前维度主要依赖社区实证数据和生产实践证据，学术界尚未有直接针对"agent 内置验证"的大规模研究。以下间接相关：

| 来源 | 关键发现 |
|---|---|
| **Watch Every Step** (Xiong et al., EMNLP 2024) | 步骤级奖励评估 + 蒙特卡洛估计 — 为验证机制提供了理论基础 |
| **Self-Supervised Prompt Optimization** (Xiang et al., arXiv 2025) | LLM 可通过成对输出比较有效评估任务遵从度，无需外部参考。成本仅为现有方法的 1.1%-5.6% |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Anthropic Best Practices | 始终提供验证标准。没有验证标准的 agent 会产生"looks right but doesn't work"的输出 |

### Community Evidence

| Issue | 投票数 | 关键发现 |
|---|---|---|
| Claude Code Issue #42796 | **1,781👍** | "Rush to completion" 定量分析（6,852 sessions, 234,760 tool calls）：Read:Edit 比率从 6.6 降至 2.0（-70%）；每编辑读取率从 93.8% 降至 66.3%；"Simplest" 词频（每千次调用）：2.7 → 6.3（+133%）；过早停止/逃避：0 → 173。根因：(1) Adaptive thinking 分配不足 (2) 默认 effort 降至 medium (3) 系统提示简洁性偏差（~5:1 比例偏好"简单"方案） |

### Production Patterns

| 工具 | 验证模式 |
|---|---|
| Cursor | Plan Mode — 执行前必须展示实现计划（含文件路径），计划保存至 `.cursor/plans/` |
| Aider | 复杂变更以 `/ask` 开始，先讨论计划再编码 |
| Claude Code | Hooks — 可在工具调用前后注入自定义验证逻辑 |

### Design Implications

1. **每个 skill 必须包含验证步骤**：不能只有"做什么"，还要有"怎么确认做对了"
2. **验证标准可自动化**：提供具体的命令或检查清单
3. **防"rush to completion"**：显式要求"完成前必须运行验证"
4. **Read:Edit 比率监控**：设计步骤时确保每步修改前有充分的读取

---

## D8: Freedom Calibration

> 不同任务需要不同程度的自主性。过于严格的约束扼杀创造性，过于宽松的约束导致不可预测的输出。

### Academic Evidence

| 来源 | 关键发现 |
|---|---|
| **NeurIPS 2024 "Teach Better or Show Smarter"** (Wan et al.) | 系统性比较指令优化 vs 示例模仿在自动提示优化中的效果。每种策略的有效性取决于任务类型 — 没有通用赢家 |
| **LLMFacility Framework** (Aslam et al., SSRN 2025) | 核心提示元素的定量评估。角色定义和约束规范显著提升输出质量 |
| **Prompt Patterns for Agile** (Sainio et al., ICSOB 2023/2024) | 清晰的角色定义有助于克服常见项目痛点。输出格式模板进一步收紧输出控制 |

### Official Guidelines

| 来源 | 指导原则 |
|---|---|
| Claude Code Skill Design | "Think of Codex exploring a path: narrow bridge with cliffs needs guardrails (low freedom), open field allows many routes (high freedom)."（想象 Codex 探索路径：悬崖边的窄桥需要护栏（低自由度），开阔原野允许多条路线（高自由度）） |

### Design Implications

1. **按任务类型校准自由度**：
   - 代码生成（确定性高）：低自由度，详细步骤
   - 架构设计（创造性高）：高自由度，原则指导
   - Bug 修复（分析性）：中等自由度，验证优先
2. **用 "MUST/SHOULD/MAY" 分级**：明确哪些是硬约束，哪些是软建议
3. **为创造性任务提供"探索空间"**：使用 "consider"、"evaluate options" 而非 "always do X"

---

## D9: Progressive Loading

> 并非所有指令都需要同时加载。渐进式加载策略可以在保证指令完整性的同时最小化上下文消耗。

### Academic Evidence

当前维度主要基于工程实践，学术界直接相关研究较少。以下间接支撑：

| 来源 | 关键发现 |
|---|---|
| **CFPO** (Liu et al., 2025) | 内容与格式联合优化证明：信息呈现的时机和方式与信息本身同等重要 |
| **LinguaShrink** (Liang et al., 2024) | 心理语言学压缩证明：信息分层呈现可减少认知负担 |

### Community Evidence — Tool Loading Strategies

| 工具 | 核心文件 | 加载策略 | 上下文限制 | 关键模式 |
|---|---|---|---|---|
| **Claude Code** | SKILL.md | 三级渐进：Metadata (~100词, 始终加载) → SKILL.md body (<5k词, 触发时加载) → Bundled resources (无限, 按需加载, 脚本可执行无需上下文加载) | body <5k词 | Two-Phase Retrieval |
| **Cursor** | .mdc files | Glob-scoped rules: Global Rules → Project Rules → Scoped Rules (glob-triggered). 使用 `@include` 跨文件共享 | 无明确限制 | Plan-and-Act, Good/Bad examples |
| **Windsurf** | .windsurfrules | 始终加载。双层：global_rules.md + workspace .windsurfrules | **6000 字符硬限制** | 强制上下文纪律 |
| **Aider** | CONVENTIONS.md | 手动 `/read`。利用 prompt caching。仅添加 1-2 个高相关文件。使用 Repository Map 进行代码库概览，无需手动添加文件 | Prompt caching | Repository Map |
| **Continue.dev** | .continue/rules/ | 自动检测 + Hub | Per agent/chat/edit | Local + Hub rules |

### Community Evidence — Standardization Trend

| Issue | 投票数 | 关键发现 |
|---|---|---|
| Claude Code Issue #41279 | New | 三层分离提案：Skills（任务流程，按需加载）→ Rulebook（持久行为规则，始终活跃，压缩保护）→ CLAUDE.md（项目上下文和偏好，初始加载，压缩后重新注入） |

### Design Implications

1. **三级加载是业界共识**：Metadata → Body → Resources
2. **Metadata 必须自包含**：~100 词内让 LLM 决定是否加载完整 skill
3. **Bundled resources 延迟加载**：大文件、参考文档、脚本不应在触发时全部加载
4. **压缩保护关键规则**：使用 Rulebook 层或 Hooks 确保核心规则在上下文压缩后仍然生效

---

## Cross-Dimension Studies

> 跨维度研究揭示 prompt 工程的整体规律，为 skill 设计提供宏观指导。

### What Makes a Good Natural Language Prompt (Do et al., ACL 2025 Long Paper)

- **规模**：Meta-analysis of 150+ prompt-related papers (2022-2024)
- **贡献**：提出 21 个属性、6 个维度的提示质量评估框架
- **关键发现**：
  - 模型和任务之间在属性支持上存在显著不平衡
  - **单一属性增强往往产生最大影响**（与 D1 触发描述质量直接相关）
  - 没有万能的最佳提示格式 — 任务和模型特定优化至关重要

### Why Prompt Design Matters and Works (Zhang et al., ACL 2025 Long Paper)

- **贡献**：解释为什么某些提示有效而另一些失败的理论框架
- **关键发现**：
  - 提示作为选择器，从隐藏状态中提取任务特定信息
  - 每个提示在答案空间中定义唯一轨迹 — **轨迹选择至关重要**
  - **朴素 CoT ("think step by step") 可能严重损害性能**
  - 最优提示搜索可在推理任务上产生 **>50% 的改进**

### Self-Supervised Prompt Optimization (Xiang et al., arXiv 2025)

- **贡献**：无需外部参考（ground truth 或人工标注）的提示优化
- **关键发现**：
  - LLM 可通过成对输出比较有效评估任务遵从度
  - **成本仅为现有方法的 1.1%-5.6%**
  - 仅需 3 个样本即可匹配/超越 SOTA

### Adaptive Prompt Structure Factorization (Liu et al., arXiv 2026)

- **贡献**：将提示分解为语义因子，使用 Architect 模型发现任务特定的提示结构
- **关键发现**：
  - 干预式单因子评分估计每个因子的边际贡献
  - 错误引导的因子选择将更新路由到当前主要失败源
  - **平均改进 +2.16pp，优化成本降低 45%-87%**

---

## Official Guidelines Comparison

> 六大 AI 供应商的官方提示工程指南对比，揭示行业共识与差异。

| 原则 | Anthropic | Google Gemini | Microsoft | Brex | DAIR.AI |
|---|---|---|---|---|---|
| 清晰/具体 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ |
| 使用示例 | 3-5 个示例，`<example>` 标签 | "Always include few-shot" | 示例可展示未见过的模式 | 嵌入数据 + 引用 | 20+ 提示技术 |
| 结构化提示 | XML 标签分区 | XML 或 Markdown 标题 | 4 组件模型 | 命令语法 | 完整技术目录 |
| 任务分解 | Prompt chaining | Chain/parallel prompts | N/A | ReAct pattern | Prompt chaining |
| 正面表述 | 说 "do X" 而非 "don't Y" | "Be precise and direct" | N/A | N/A | N/A |
| 角色设定 | 即使 1 句话也有帮助 | 放在 system instruction 中 | N/A | N/A | N/A |
| 输出控制 | 格式匹配 | 繁简/语调参数 | Cue phrases | 编程化消费 | 结构化输出 |
| 位置效应 | 关键指令放首尾 | 指令放首位，查询放末尾 | N/A | N/A | N/A |
| 安全性 | 假设隐藏提示可见 | N/A | N/A | 意识越狱/泄露 | N/A |
| 思考模型 | Adaptive Thinking, effort 参数 | N/A | "推理模型不需要" | N/A | CoT, ToT, ReAct |

### 跨指南共识（所有 5+ 指南一致同意）

1. **清晰具体** — 模糊指令产生模糊输出
2. **使用示例** — 少量高质量示例胜过大量低质量示例
3. **结构化** — 清晰分区提升遵从度
4. **任务分解** — 复杂任务需要分解为可管理的步骤

---

## Community Evidence

> 来自生产环境的实证数据，包括高影响力 GitHub Issues 和跨工具对比。

### High-Impact GitHub Issues (Claude Code)

| Issue | 投票数 | 关键发现 |
|---|---|---|
| #6235 - AGENTS.md 标准化 | **3,580👍**, 269💬 | 社区希望跨工具通用 agent 指令格式 |
| #42796 - 复杂工程退化 | **1,781👍** | 定量证明：agent 性能退化（Read:Edit -70%，简洁性偏差 +133%） |
| #45596 - Bring Back Buddy | 654👍 | 社区怀念早期更谨慎的 agent 行为 |
| #3382 - 谄媚行为 | 874👍, 179💬 | Claude 对所有内容都说 "You're absolutely right!"，甚至对 "Yes please" |
| #9716 - Skills 未被识别 | 69👍 | 因 description 缺少触发短语导致 skill 未触发 |
| #18192 - 递归 skill 发现 | 40👍 | 子目录中的 skill 未被找到 |
| #2544 - CLAUDE.md 规则被忽略 | 39👍 | 文件过长时规则被忽略 |
| #41279 - Compaction-Protected Rulebook | New | 三层分离提案：Skills / Rulebook / CLAUDE.md |
| #6354 - 压缩后遗忘 | 27👍 | 关键指令在上下文压缩后丢失 |

### Production-Grade Tool Comparisons

| 工具 | 核心文件 | 加载策略 | 上下文限制 | 关键模式 |
|---|---|---|---|---|
| Claude Code | SKILL.md | 三级渐进 | <5k words body | Two-Phase Retrieval |
| Cursor | .mdc files | Glob-scoped rules | 无明确限制 | Plan-and-Act, Good/Bad examples |
| Windsurf | .windsurfrules | 始终加载 | 6000 chars 硬限制 | Global + Workspace 双层 |
| Aider | CONVENTIONS.md | 手动 /read | Prompt caching | Repository Map |
| Continue.dev | .continue/rules/ | 自动检测 + Hub | Per agent/chat/edit | Local + Hub rules |

### Cross-Tool Standardization Trend

- **SKILL.md 正成为事实标准**：12+ 工具采用（Claude Code, Codex CLI, Gemini CLI, Cursor, OpenClaw, Hermes Agent, Kimi 等）
- **AGENTS.md 运动**（Issue #6235, 3580👍）推动通用格式
- **Anthropic 响应**：在 CLAUDE.md 中使用 `@AGENTS.md` 导入

---

*Last updated: 2025-04-14. Sources verified against original papers, official documentation, and GitHub issue threads.*
