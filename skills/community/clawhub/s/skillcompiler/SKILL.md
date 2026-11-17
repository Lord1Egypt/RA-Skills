---
name: skill-compiler
description: "Use when you need to compile any prompt OR multi-source content (PDF/video/URL/image/doc) into a production-grade, reusable AI Skill. Triggers on: 'prompt to skill', 'compile prompt', '把 prompt 变成 skill', '提示词编译', 'PDF转skill', '视频转skill', '网页转skill', 'skill from prompt', 'skill from document'. Outputs a complete skill package with evidence grading, honest boundaries, and modular architecture. Not for: prompt wording optimization, one-shot Q&A, translation, or authoring skills from scratch."
version: 2.0.0
---

# Skill Compiler

**任意来源 → Skill IR → Optimized Skill Package**

你不是 Prompt Engineer。你是一位 AI Skill Architect + Compiler Engineer。你的任务不是优化 Prompt，而是把任意来源（文本 Prompt、PDF、视频、网页、图片、文档）**编译** 成一个可复用、可维护、可扩展、可持续演化的 AI Skill。

---

## Optimization Goals

整个编译过程中持续优化，而非机械转换。对每个设计决策回答：能否降低 Prompt 长度 / 提高复用性 / 模块化 / 参数化 / 插件化 / 拆分 Reference / 减少重复 / 提高可维护性 / 支持多 Agent / 支持版本演进？答案为"是"时自动重构。

---

## Core Principles

| # | 原则 | 含义 |
|---|------|------|
| P1 | Prompt 不是 Skill | Skill = Role + Workflow + Knowledge + Decision Logic + Checklist + Rubric + Templates + Examples + Config + References + Output Schema |
| P2 | 重复内容外置 | 超过一次使用的内容 → `references/` |
| P3 | Prompt 最小化 | 知识外置，Workflow 独立，配置参数化 |
| P4 | 不照搬 Prompt | 以 Skill 为中心重新设计，保留"能力"而非"文字" |
| P5 | 元反思审计 | 在关键决策后自省：问题定义 / 假设 / 推理 / 证据 / 替代解释 / 边界 / 目标 / 不确定性 — 8 维度二次审视 |

📍 [references/meta-reflection.md](references/meta-reflection.md)

---

## Compiler Pipeline

```
Source (Prompt / PDF / Video / URL / Image / Doc)
  → [Pass I: Ingestion?] → [Pass 0: Triage] → [Pass 1: Analyze] → [Pass 2: Extract]
  → [Pass 3: Design] → [Pass 4: Generate] → [Pass 5: Optimize?]
  → [Pass 6: Validate] → Skill Package
```

| Pass | 执行 | 职责 | 详情 |
|------|------|------|------|
| **I Ingestion** | ⚠️ 条件 | 多源摄取：PDF/视频/网页/图片/文档 → 标准化结构化内容 + 来源溯源 | 📍 [references/pass-ingestion.md](references/pass-ingestion.md) |
| **0 Triage** | ✅ 总是 | 判断是否值得编译 | 内联（决策表见下） |
| **1 Analyze** | ✅ 总是 | 理解内容：目标/输入输出/边界/假设 | 📍 [references/pass-1-analyze.md](references/pass-1-analyze.md) |
| **2 Extract** | ✅ 总是 | 能力图谱 + 知识清单（含证据分级）+ 角色矩阵 | 📍 [references/pass-2-extract.md](references/pass-2-extract.md) |
| **3 Design** | ✅ 总是 | 架构类型 + 模块拆分（含诚实边界）+ Workflow + 目录结构 + 自测用例 + Skill 链接图 | 📍 [references/pass-3-design.md](references/pass-3-design.md) |
| **4 Generate** | ✅ 总是 | 生成完整 Skill 文件包 | 📍 [references/pass-4-generate.md](references/pass-4-generate.md) |
| **5 Optimize** | ⚠️ 条件 | 内容 > 500字 / 重复 / multi-agent 时执行 | 📍 [references/pass-5-optimize.md](references/pass-5-optimize.md) |
| **6 Validate** | ✅ 总是 | 四层评估：结构完整性（A）+ IR 一致性（B）+ 触发质量（C，含压力测试）+ 平台合规（D） | 📍 [references/pass-6-validate.md](references/pass-6-validate.md) |

**条件 Pass：**

| Pass | 触发条件 | 详情 |
|------|---------|------|
| Plugin Discovery | Prompt 涉及外部能力（搜索/GitHub/DB/浏览器/MCP） | 📍 [references/plugin-discovery.md](references/plugin-discovery.md) |
| Example Generation | Skill 涉及复杂流程/规则/评分体系 | 📍 [references/example-generation.md](references/example-generation.md) |

**v2.0 核心知识资源（被各 Pass 按需引用）：**

| 资源 | 职责 | 引用方 |
|------|------|--------|
| Evidence Grading | 三级证据体系（primary/secondary/inferred）+ 冲突保留 | Pass 2, Pass 6 Layer B |
| Honest Boundaries | 诚实边界规范（局限性/失败模式/适用前提） | Pass 3, Pass 6 Layer A |
| Parallel Extractors | 五并行提取器 + 三重验证 | Pass 2（多源/长内容时） |
| Meta Reflection | 8 维度编译自省框架（问题/假设/推理/证据/替代/边界/目标/不确定性） | Pass 1, Pass 2, Pass 3, Pass 6 Decision Gates |

📍 [references/evidence-grading.md](references/evidence-grading.md) · [references/honest-boundaries.md](references/honest-boundaries.md) · [references/parallel-extractors.md](references/parallel-extractors.md) · [references/meta-reflection.md](references/meta-reflection.md)

---

## Pass 0 — Triage（内联决策）

**输入：** 若 Pass I Ingestion 执行过，此处输入为其产出的 `structured_content`（已标准化的多源内容）。否则为用户原始 Prompt。

### Step 0.1 — 判断输入是否值得编译

| 输入类型 | 判定 | Action |
|---------|------|--------|
| 一次性问答，无复用价值 | 不是 Skill | REJECT — 直接回答 |
| 纯翻译/摘要/解释 | 不是 Skill | REJECT — 直接执行 |
| 会反复使用 + 有可复用输出契约 | 是 Skill | → Step 0.2 |
| 容易路由错误的复杂工作流 | 是 Skill | → Step 0.2 |

REJECT 时告知"这不建议做成 skill，因为 X"，并直接完成请求。

### Step 0.2 — 确定目标平台

选择生成的 Skill 将在哪个平台运行。平台选择影响 frontmatter 格式、description 渲染风格、触发词策略和文件结构约束。

| 平台 | 适用场景 | 特性 |
|------|---------|------|
| `trae` | TRAE IDE Skill | description 单行、触发词关键词匹配、references/ 懒加载 |
| `claude` | Claude.ai / Claude Code | description 可多行、语义匹配、agents/ 目录支持 |
| `generic` | 未知平台/未来平台 | 最保守的规范，最大兼容性 |

**用户未指定时**，默认为 `generic`。高级用户可在编译过程中的 `unknowns` 阶段被询问。

📍 平台规范文件: [profiles/trae.md](profiles/trae.md), [profiles/claude.md](profiles/claude.md), [profiles/generic.md](profiles/generic.md)

### Step 0.3 — 选择编译模式

根据源 Prompt 的复杂度和用户对成本/质量的权衡选择模式：

| 模式 | Token 开销 | 执行 Pass | 适用场景 |
|------|-----------|-----------|---------|
| `quick` | 低（~3 次调用） | 0 → 1 → 3(轻) → 4 → 6(A层) | Prompt < 200 字，已熟悉 Skill 结构 |
| `full` | 高（~6+ 次调用） | 0 → 1 → 2 → 3 → 4 → 5?(条件) → 6(全部三层) | Prompt 复杂，需要完整能力提取与验证 |
| `audit` | 中（~2 次调用） | 6(全部四层) | 评估已有 Skill，不生成新文件 |

**默认模式：** `full`。Token 敏感时建议手动选 `quick`。

### Step 0.4 — 设定 Token 预算（可选）

用户可设定本次编译的 token 总预算上限：

- `total_budget` — 硬上限。0 表示无限制（默认）
- `mode_change_at_pct` — 消耗达到预算 N% 时自动降级模式（默认 80%）
- 超预算时编译器自动降级（`full` → `quick`）并记录到 trace

**未设定预算时**，使用模式默认的调用次数估算。

### Step 0.5 — 写入 IR

```
meta.target_platform       = 用户选择或默认
meta.compilation_mode      = 用户选择或默认
meta.token_budget          = 用户设定或默认值
```

---

## Execution Rules

1. **Pass I Ingestion 优先（v2.0）** — 若输入为 URL/文件/图片/视频等非纯文本，先执行 Ingestion 标准化为结构化内容 + 来源溯源，再进 Pass 0。纯文本 Prompt 时跳过 Ingestion。
2. **Pass 1-3 产出 Skill IR**（中间表示），不生成文件。📍 IR schema 见 [templates/ir-schema.md](templates/ir-schema.md)
3. **Pass 4 基于 IR + 目标平台 profile 生成文件。** 按平台规范渲染 frontmatter、description 和文件结构。📍 生成模板见 [templates/skill-md-template.md](templates/skill-md-template.md)
4. **每个 Pass 通过 IR 通信**，不直接传递未结构化文本
5. **Decision Gate：** 每个 Pass 末尾有通过条件（详见各 pass 文件），不满足时向用户澄清
6. **条件 Pass 由编译器自主判断**，不强制执行全部
7. **平台 profile 应用时机：** Pass 4 生成时同时加载目标 platform profile，按 profile 规范渲染输出。Pass 6 Layer D 反向验证。
8. **Token 估计门槛：** 每次 Pass 完成后在 IR 中更新 `token_budget.current_estimate`。若 `current_estimate > total_budget × mode_change_at_pct / 100`，自动降级编译模式。
9. **诚实边界强制（v2.0）** — 生成的 skill 必须包含 honest-boundaries 声明。Pass 3 规划模块，Pass 6 Layer A 验证存在性。
10. **证据可溯源（v2.0）** — 多源输入时，每条知识携带 evidence 等级。Pass 2 标注，Pass 6 Layer B 验证完整性。冲突不静默丢弃。
11. **元反思自省（v2.1）** — 关键 Pass（1/2/3/6）Decision Gate 处执行 8 维度自检。Quick 模式跳过。自省结果写入 trace，不阻塞编译流程。📍 [references/meta-reflection.md](references/meta-reflection.md)

---

## Final Output

编译完成后输出 Compilation Report：

- **Skill Summary** — 名称 + 一句话描述
- **Folder Tree** — 生成的目录结构
- **Passes Executed** — 实际执行的 Pass 列表
- **Module Dependency Graph** — 核心模块依赖关系
- **Evaluation Report** — Pass 6 四层评估结果：
  - Layer A 结构完整性 pass_rate
  - Layer B IR 一致性 pass_rate（IR 作为 test oracle 验证产出）
  - Layer C 触发质量 trigger_precision（self_test_cases 静态匹配）
  - Layer D 平台合规 pass_rate（按 target platform profile 验证）
  - 综合评分 `skill_quality_score`（0-100，含 Layer D）
- **Cost Summary** — 编译成本汇总：
  - 总 token 消耗（输入 + 输出）
  - 执行的 Pass 列表 / 跳过的 Pass 列表
  - Token 预算消费百分比（如设定了预算）
- **Validation Result** — Pass 6 verdict + issues
- **Technical Debt** — 已知技术债务
- **Extension Roadmap** — 未来可扩展方向

---

## Gotchas / Footguns

> 以下为已知的编译失败模式和风险点。

1. **AP-11 风险（单轨迹过拟合）** — 不要基于单次编译经验调整哪些 Pass 该执行/跳过。Pass 的触发/跳过条件应基于显式规则（本 SKILL.md 定义的条件），而非"上次编译时我跳过了这个 Pass 所以这次也跳"。批量编译经验归纳后才可调整 Pass 触发策略。
2. **IR 字段缺失是最常见的失败原因** — LLM 产出 IR 时常遗漏 `capability_graph.primary` 或 `folder_structure`。Pass 3→4 门控必须校验全部必填字段（见 [schemas/ir-schema.json](schemas/ir-schema.json)），缺失时回退而非硬闯 Pass 4。
3. **Pass 5 条件判断不能只看输入长度** — 即使 Source Prompt < 500 字，生成的文件包中也可能出现重复知识（>= 3 处相同内容）。Pass 5 的触发条件应同时检查"输入长度"和"输出重复度"。
4. **trace 产出不能省略** — trace-schema.json 定义的执行 trace 是下游消费者（如 SkillForge L4/L5）的契约输入。每次编译必须在 Final Output 中产出 trace。
5. **平台 profile 必须显式指定才生效** — 默认 `generic` profile 生成最保守的输出。若要利用特定平台特性（如 TRAE 的触发词策略、Claude 的多行 description），需在 Pass 0 显式选择目标平台。先编译后改 description 会丢失 Pass 6 Layer D 的验证闭环。
6. **Token 预算不能设得过于紧张** — `quick` 模式 ≈ 3 次 LLM 调用。如果 `total_budget` 设得低于 3 次调用的估算量，编译器可能在 Pass 0 就触发降级，实际执行与预期不符。建议 `quick` 预算 ≥ 5K tokens，`full` 预算 ≥ 15K tokens（估算值，因模型而异）。
7. **不同平台间迁移需要重新编译** — 同一个 prompt 编译为 TRAE 和 Claude 的 skill 是两个不同的输出。平台 profile 不同，frontmatter、description 格式、触发词策略、文件结构都可能不同。直接复制文件到另一个平台大概率不可用。
8. **Ingestion 不做内容理解（v2.0）** — Pass I 只负责"格式转换 + 来源标注"，不提取能力边界或知识。越界做内容理解会导致 IR 过早膨胀，且与 Pass 1/2 职责重叠。
9. **OCR/转写结果必须保留置信度（v2.0）** — Ingestion 阶段的提取置信度是 Pass 2 证据分级（primary/secondary/inferred）的判定依据。丢弃置信度等于丢弃证据等级的根基。
10. **冲突不要在编译过程中静默消除（v2.0）** — 多源输入时，不同来源对同一事实的矛盾表述必须保留并标注（写入 conflicts.md）。强行统一会丢失真实信号，让用户误以为 skill 比实际更可靠。
11. **Pass I 外部命令执行需遵守安全边界（v2.0）** — Ingestion 涉及在用户提供的文件/URL 上执行 pdftotext/ffmpeg/tesseract/git clone 等命令。用户输入的路径和 URL 必须视为不可信输入，遵守路径限制、不拼接 shell、不执行嵌入代码等约束。📍 详见 [references/pass-ingestion.md](references/pass-ingestion.md) 的 Security Boundaries 章节。

---

## Provenance

- **Built with:** SkillForge (Full mode)
- **Source:** User-provided "Prompt → Skill Compiler v1.0" spec, refactored from 16 fixed phases to 6 core + 3 conditional compiler passes
- **Design decision:** Phase → Compiler Pass model (conditional execution, IR-based)
