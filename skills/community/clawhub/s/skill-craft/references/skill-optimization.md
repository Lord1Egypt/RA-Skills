# Skill Optimization Guide

基于同行评审研究（ACL/NeurIPS/EMNLP 2023-2025）、AI 厂商官方指南（Anthropic/Google/Microsoft）和生产级工程实践（Claude Code/Cursor/Windsurf 社区）的技能优化框架。AI agent 读取后即可立即对技能进行针对性优化。

## Table of Contents

1. [诊断优先原则](#1-诊断优先原则)
2. [9 大优化维度](#2-9-大优化维度)
   - [D1: 触发描述质量](#d1-触发描述质量-trigger-precision)
   - [D2: 上下文效率](#d2-上下文效率-token-economy)
   - [D3: 结构化指令](#d3-结构化指令-visual-separation)
   - [D4: 步骤分解](#d4-步骤分解-actionable-sequences)
   - [D5: 正向约束](#d5-正向约束-affirmative-framing)
   - [D6: 示例设计](#d6-示例设计-concrete-demonstrations)
   - [D7: 验证机制](#d7-验证机制-quality-gates)
   - [D8: 自由度校准](#d8-自由度校准-specificity-matching)
   - [D9: 渐进式加载](#d9-渐进式加载-context-architecture)
3. [按技能类型的优化优先级](#3-按技能类型的优化优先级)
4. [反模式目录](#4-反模式目录)
5. [证据来源](#5-证据来源)

---

## 1. 诊断优先原则

在修改任何内容之前，先完整读取技能文件并诊断哪些维度存在问题。并非每个技能都需要在所有维度上优化。

### 快速诊断问题

对每个维度回答诊断问题。如果答案是"否"或"不确定"，则该维度需要优化。

| # | 维度 | 诊断问题 |
|---|------|---------|
| D1 | 触发描述质量 | 遮住 SKILL.md 正文，只看 name + description，能判断何时触发吗？ |
| D2 | 上下文效率 | 逐行审计——"删掉这行 agent 会犯错吗？"——每行都通过了吗？ |
| D3 | 结构化指令 | 不同类型的内容（工作流、约束、示例）是否用视觉分隔？ |
| D4 | 步骤分解 | 复杂的多步骤流程是否被分解为编号的、有序的步骤？ |
| D5 | 正向约束 | 规则是用"做 X"而非"不要做 Y"来表达的？ |
| D6 | 示例设计 | 是否包含至少一个具体的"用户请求 → 期望行为"示例？ |
| D7 | 验证机制 | 技能是否告诉 agent 如何验证其输出是否正确？ |
| D8 | 自由度校准 | 具体程度是否匹配任务脆弱性（脆弱任务用严格步骤，创意任务用灵活指导）？ |
| D9 | 渐进式加载 | SKILL.md 是否精简，详细信息是否推迟到 `references/`？ |

### 诊断输出

诊断后，生成一个按预期影响排序的、需要优化的维度排名列表。首先关注前 3-4 个问题。

---

## 2. 9 大优化维度

### D1: 触发描述质量 (Trigger Precision)

#### 为什么这样做

`description` 字段是**唯一始终加载到上下文中**的内容。无论 agent 当前在做什么任务，description 都会被扫描以判断是否触发该技能。如果 description 无法让 agent 正确识别触发时机，技能即使存在也不会被调用。

Claude Code Issue #9716（69+ 👍）明确记录了这一现象：安装在 `.claude/skills/` 中的技能因为 description 缺少触发短语而**完全不被识别**。这意味着无论 SKILL.md 写得多好，如果 description 不合格，整个技能等于不存在。

**核心原理**：description 的作用是"路由器"——它决定技能是否被激活，而非说明技能如何工作。工作细节属于 SKILL.md 的职责。

#### 诊断方法

1. **遮罩测试**：用纸遮住 SKILL.md 全文，只看技能的 `name` 和 `description`
2. 问自己：如果 agent 当前正在处理任务 X，它能仅凭这两个字段判断"我需要加载这个技能"吗？
3. 如果答案是"不确定"或"不能"，description 需要重写

#### 优化操作：三步公式

1. **能力描述**：一句话说明技能做什么（25词以内）
2. **触发场景编号列表**：用 `(1)...(2)...(3)...` 列出具体使用场景
3. **具体触发关键词**：列出用户可能使用的短语/关键词

#### Before/After 对比示例

**示例 1：PDF 处理技能**

```yaml
# ❌ BEFORE: 无触发短语，无具体场景
name: pdf-helper
description: Helps with PDF operations and document processing.

# ✅ AFTER: 能力 + 场景 + 关键词
name: pdf-helper
description: >
  Create, edit, and analyze PDF documents. Use when working with .pdf
  files for: (1) Extracting text or form data, (2) Rotating or merging
  pages, (3) Filling form fields, (4) Converting PDFs to images.
  Trigger: "pdf", "rotate pdf", "merge pdf", "extract text", "fill form"
```

**示例 2：数据库操作技能**

```yaml
# ❌ BEFORE: 只描述功能，不描述触发时机
name: db-toolkit
description: Provides database operation capabilities for multiple database types.

# ✅ AFTER: 明确列出触发场景和关键词
name: db-toolkit
description: >
  轻量级多数据库操作工具，支持 MySQL/PostgreSQL/SQLite 的 DDL/DML 操作。
  触发场景：(1) 连接/测试数据库 (2) 查看表结构/列出所有表 (3) 执行 SQL 查询
  (4) 创建/修改/删除表 (5) 增删改数据。
  触发词："连接数据库"、"查看表结构"、"执行SQL"、"创建表"
```

**示例 3：前端设计技能**

```yaml
# ❌ BEFORE: 抽象描述，缺乏可操作性
name: ui-design
description: Senior UI/UX engineering guidance for building better interfaces.

# ✅ AFTER: 具体场景 + 明确触发词
name: design-taste-frontend
description: >
  Senior UI/UX Engineer. Enforces metric-based rules, strict component
  architecture, CSS hardware acceleration, and balanced design engineering.
  Use when: (1) Building new UI components (2) Reviewing CSS/HTML quality
  (3) Deciding layout or animation approaches (4) Optimizing rendering
  performance. Trigger: "design", "UI", "CSS", "component", "layout",
  "animation", "responsive"
```

#### 检查清单

- [ ] Description 包含技能做什么（能力）
- [ ] Description 包含何时使用（触发场景，编号列表）
- [ ] Description 包含具体关键词/短语
- [ ] Description 在 1024 字符以内
- [ ] Description 中无尖括号（破坏 YAML 解析）
- [ ] 遮罩测试通过：仅凭 name+description 能判断触发时机

---

### D2: 上下文效率 (Token Economy)

#### 为什么这样做

上下文窗口是最稀缺的资源。过载的技能不仅自身被忽略，还会**拖累所有已加载技能的性能**。

Claude Code Issue #2544（39+ 👍）证明：当 CLAUDE.md（与 SKILL.md 机制相同）超过 200 行时，规则开始被系统性地忽略。Issue #6354（27+ 👍）进一步证明：在上下文压缩（compaction）后，长文件的规则会被遗忘。

CFPO 论文（Liu et al., Fudan/Microsoft, 2025）提供了定量证据：仅通过格式优化（不改变内容）即可带来 **5-38%** 的性能提升。这证明**信息密度**本身就是一个独立的优化维度。

Anthropic 最佳实践总结为一条原则："大多数最佳实践源于一个约束：上下文很快就会填满。"

#### 诊断方法

1. **逐行审计**：对 SKILL.md 中的每一行问"如果删掉这行，agent 会犯错吗？"
2. 如果答案是"不会"或"大概率不会"，该行应删除或移至 references
3. **重复检测**：SKILL.md 和 references 之间是否有信息重复？
4. **已知知识检测**：是否有内容是 LLM 已经知道的通用知识？

#### 优化操作：三步精简法

1. **删除已知知识**：移除 LLM 已知的通用概念（"Python 是一种编程语言"、"REST API 使用 HTTP 方法"等）
2. **用示例替代段落**：一个具体示例胜过三段文字解释
3. **细节移入 references**：边缘情况、完整 API 文档、高级用法 → `references/`

#### Before/After 对比示例

**示例 1：冗长解释 → 精简指令**

```markdown
# ❌ BEFORE: 30+ tokens，包含已知知识
When you encounter a PDF file that has fillable form fields, you should
use the pdfplumber library to first identify what fields exist in the
document, and then fill them using the fill_form_fields.py script located
in the scripts directory of the project.

# ✅ AFTER: 20 tokens，直接指令 + 引用
Fill PDF forms: Run `scripts/fill_form_fields.py <pdf_path>` to list
and fill form fields. See [PDF-FORMS.md](references/pdf-forms.md) for
field types and advanced options.
```

**示例 2：重复信息 → 单一来源**

```markdown
# ❌ BEFORE: SKILL.md 中重复了 references 的内容
## API Endpoints
- GET /api/users — List all users (returns User[])
- GET /api/users/:id — Get user by ID (returns User)
- POST /api/users — Create user (body: CreateUserDTO, returns User)
- PUT /api/users/:id — Update user (body: UpdateUserDTO, returns User)
- DELETE /api/users/:id — Delete user (returns void)
See references/api.md for more details.

# ✅ AFTER: SKILL.md 只保留摘要，详情在 references
## API Endpoints
CRUD operations on `/api/users`. See [API.md](references/api.md) when
you need specific endpoint signatures, request/response types, or
authentication headers.
```

**示例 3：段落解释 → 具体示例**

```markdown
# ❌ BEFORE: 解释"为什么"，agent 不需要
Before running the migration, it is important to back up the database
because migrations can sometimes fail and leave the database in an
inconsistent state. We use a custom backup script that creates a
timestamped snapshot, which allows us to restore to any point in time.

# ✅ AFTER: 直接指令 + 示例
## Pre-migration
Always backup before migrating:
  `scripts/backup.sh`  # Creates timestamped snapshot at backups/
Verify backup exists before proceeding.
```

#### 检查清单

- [ ] SKILL.md 正文在 500 行以内（硬性上限）
- [ ] 目标长度：200-300 行
- [ ] 每行都通过"删掉会犯错吗？"测试
- [ ] 无 SKILL.md 和 references 之间的信息重复
- [ ] 无 LLM 已知的通用知识解释
- [ ] 边缘情况和详细信息已移至 `references/`

---

### D3: 结构化指令 (Visual Separation)

#### 为什么这样做

LLM 解析结构化内容的可靠性显著高于混合格式的内容块。当不同类型的内容（工作流、约束、示例）混在一起时，指令会"模糊化"——agent 难以区分哪些是必须遵守的规则、哪些是参考信息、哪些是示例。

CFPO 论文（Liu et al., 2025）提供了关键发现：**联合优化内容和格式**优于分别优化（GSM8K: 63.38% vs 各自优化之和）。这意味着结构本身就是一种"指令"——告诉 agent 如何理解内容的格式。

Anthropic、Google 和 Microsoft 三家独立推荐使用 XML 标签或 Markdown 分隔来组织提示词：
- Anthropic：推荐 `<instructions>`、`<example>`、`<constraints>` 等 XML 标签
- Google Gemini 3 指南："Use XML tags or Markdown headings to clearly separate prompt sections"
- Microsoft：将提示词分解为 Instructions / Content / Examples / Cue 四个组件

#### 诊断方法

1. 扫描 SKILL.md：不同类型的内容是否有视觉分隔？
2. 约束条件是否被埋在段落中间？
3. 工作流步骤是否和说明注释混在一起？

#### 优化操作

1. 用 `###` 标题分隔不同类型的内容（工作流、约束、示例、验证）
2. 用 `---` 分隔符创建视觉边界
3. 用代码块（` ``` `）包裹代码和命令
4. 关键规则用加粗或列表强调

#### Before/After 对比示例

**示例 1：无结构 → 有结构**

```markdown
# ❌ BEFORE: 所有内容混在一起
This skill helps you deploy applications. First you need to check if
all tests pass by running npm test. If tests pass, build the project
with npm run build. Then deploy to staging using the deploy script.
Make sure you never deploy to production without staging approval.
Also remember to update the changelog. Here's an example: when the
user says "deploy v2.3", run tests, build, deploy to staging, then
ask for approval. If the user says "deploy to prod", verify staging
is approved first.

# ✅ AFTER: 结构化分隔
## Workflow

1. **Test**: Run `npm test` — all tests must pass
2. **Build**: Run `npm run build`
3. **Stage**: Run `scripts/deploy.sh staging`
4. **Verify**: Confirm staging deployment is healthy

---

## Constraints

- Always update `CHANGELOG.md` before deploying
- Production deploy requires explicit staging approval

---

## Examples

### User: "deploy v2.3"
→ 1. Run tests  2. Build  3. Deploy to staging  4. Ask for prod approval

### User: "deploy to prod"
→ 1. Verify staging is approved  2. If yes, deploy  3. If no, STOP and inform
```

**示例 2：约束埋在段落中 → 独立约束区**

```markdown
# ❌ BEFORE: 约束分散在说明文本中
When generating API documentation, you should always include the endpoint
URL, HTTP method, request parameters, and response format. Don't include
internal implementation details. Also make sure the examples use realistic
data, not placeholder text like "foo" or "bar".

# ✅ AFTER: 独立约束区，视觉清晰
## Constraints

- Include for every endpoint: URL, HTTP method, parameters, response format
- Use realistic data in examples (never "foo", "bar", "test")
- Omit internal implementation details
```

#### 检查清单

- [ ] 指令、约束和示例在不同区域
- [ ] 每个区域有清晰的 Markdown 标题
- [ ] 复杂区域使用子标题增强可扫描性
- [ ] 没有超过 5 行的段落没有视觉分隔
- [ ] 代码和命令用代码块包裹

---

### D4: 步骤分解 (Actionable Sequences)

#### 为什么这样做

逐步指令产生的 agent 行为质量显著优于自由格式描述。这是因为编号步骤为 agent 提供了明确的执行顺序和进度追踪能力。

**Chain of Methodologies（CoM, Liu et al., ACL 2025）** 证明：结构化的逐步推理在复杂任务上优于非结构化方法。关键机制是"方法论链"——每个步骤都是可验证的、有明确输入输出的单元。

**Watch Every Step（Xiong et al., EMNLP 2024）** 证明：步骤级指导显著增强 agent 效率。具体而言，当 agent 知道"下一步做什么"时，减少了无效的探索和回溯。

**Read Before You Think（2025）** 补充证明：将推理分解为显式步骤比自由推理更有效，因为每个步骤可以被独立验证。

Cursor 最佳实践中的 "Plan-and-Act" 模式也体现了同一原理：先规划（步骤列表），再执行。

#### 诊断方法

1. 工作流是否用编号步骤描述？
2. 每个步骤是否是单一、可执行的指令？
3. 是否有决策分支（if X → do Y, else → do Z）？
4. 是否有错误处理（步骤失败时怎么办）？

#### 优化操作

1. **段落 → 编号列表**：将流程描述转换为编号步骤
2. **添加决策点**：在关键分支处添加 if/else 条件
3. **添加错误处理**：每个可能失败的步骤都有失败处理路径

#### Before/After 对比示例

**示例 1：段落 → 编号步骤**

```markdown
# ❌ BEFORE: 自由格式描述
Process the document by extracting key fields, validating them against
the schema, and then generating a report. Handle errors gracefully and
make sure all required fields are present before generating the report.

# ✅ AFTER: 编号步骤 + 决策点 + 错误处理
## Workflow

1. **Extract**: Read document, extract fields listed in `references/schema.md`
2. **Validate**: Check each field against schema rules
   - If validation passes → proceed to step 3
   - If validation fails → report specific errors with line numbers, suggest fixes, STOP
3. **Transform**: Run `scripts/transform.py --input <extracted.json>`
   - If script fails → capture stderr, check `references/troubleshooting.md`, report
4. **Report**: Generate output using `assets/report-template.md`
5. **Verify**: Confirm output contains all required sections (summary, details, metadata)
   - If any section missing → regenerate from step 4
```

**示例 2：无决策分支 → 有决策分支**

```markdown
# ❌ BEFORE: 线性描述，缺少分支处理
Run the migration script and then verify the database. If something
goes wrong, fix it and try again.

# ✅ AFTER: 明确决策分支和失败处理
## Migration Workflow

1. **Backup**: Run `scripts/backup.sh` → verify `backups/` has new snapshot
2. **Dry-run**: Run `scripts/migrate.py --dry-run`
   - If dry-run succeeds → proceed to step 3
   - If dry-run shows conflicts → STOP, report conflicts, ask user to resolve
3. **Migrate**: Run `scripts/migrate.py`
   - If migration succeeds → proceed to step 4
   - If migration fails → run `scripts/rollback.sh`, report error, STOP
4. **Verify**: Run `scripts/verify-migration.py`
   - If verify passes → report success
   - If verify fails → run `scripts/rollback.sh`, escalate to user
```

#### 检查清单

- [ ] 多步骤流程使用编号列表
- [ ] 每个步骤是单一、可执行的指令
- [ ] 决策点包含清晰的分支（if X → do Y）
- [ ] 错误处理是显式的（失败时做什么）
- [ ] 工作流末尾有验证步骤

---

### D5: 正向约束 (Affirmative Framing)

#### 为什么这样做

LLM 遵循正向约束（"做 X"）的可靠性显著高于负向约束（"不要做 Y"）。这不是"风格偏好"，而是已被定量研究证实的能力边界。

**Inverse IFEval（Zhang et al., ByteDance/NJU/PKU, 2025）** 系统测试了所有主流 LLM 在正向约束和负向约束上的表现，结论明确：**所有 LLM 在负向/非常规约束上的表现都显著差于正向约束**。这是跨模型的普遍现象，不是某个模型的特有问题。

**Constraint Decomposition（Paunova, 2025）** 提供了更精确的数据：将复杂约束分解为单条简单约束，可将 prompt 级别的准确率从 **41.2% 提升到 73.8%**（+32.6 个百分点）。这意味着"不要做 X 且不要做 Y 且不要做 Z"远不如分别表达为三个独立的正向规则。

Anthropic 最佳实践明确建议："Instead of 'don't use markdown', say 'use flowing prose paragraphs'."

#### 诊断方法

1. 扫描技能文件中的 "don't"、"never"、"avoid"、"no"、"without" 等否定词
2. 每个否定约束是否有对应的正面表述？
3. 是否有"不要做 X 且不要做 Y"这种复合否定？

#### 优化操作

1. **负约束 → 正约束**：将"不要做 Y"改写为"做 X"
2. **安全关键负约束保留但配正面替代**：涉及安全/不可逆操作的否定约束可以保留，但必须同时给出正面替代
3. **复杂约束分解为单条**：一个约束只表达一个规则

#### Before/After 对比示例

**示例 1：基本否定 → 肯定**

```markdown
# ❌ BEFORE
Don't write functions longer than 20 lines.

# ✅ AFTER
Keep every function under 20 lines. If logic is complex, extract helper functions.
```

**示例 2：复合否定 → 分解的肯定**

```markdown
# ❌ BEFORE: 三条否定约束堆叠
Never modify files outside the project directory. Don't use deprecated APIs.
Avoid adding new dependencies without approval.

# ✅ AFTER: 三条独立正向约束
- Only modify files within the project directory
- Use the latest stable API version from `references/api.md`
- Request user approval before adding new dependencies (list the package and reason)
```

**示例 3：安全关键场景**

```markdown
# ❌ BEFORE: 纯否定，agent 不知道该做什么
CRITICAL: Never delete files without asking the user first. Don't modify
production configuration files.

# ✅ AFTER: 保留安全否定 + 给出正面替代
## Safety Rules
- CRITICAL: Ask user confirmation before deleting any file
- CRITICAL: Only modify production configs after explicit user approval
- When in doubt about a destructive action: STOP, describe the action, ask for confirmation
```

**示例 4：模糊否定 → 具体肯定**

```markdown
# ❌ BEFORE: "avoid" 是最弱的否定词
Avoid using global variables in your code.

# ✅ AFTER: 具体的正向替代方案
Pass state as function parameters or use dependency injection. If shared
state is necessary, use a module-level singleton with clear access patterns.
```

#### 检查清单

- [ ] 规则用"做 X"而非"不要做 Y"表达
- [ ] 安全关键的否定约束配有正面替代
- [ ] 约束是具体可测量的（"20 行以内"而非"简短"）
- [ ] 复杂约束集分解为独立规则
- [ ] 无 "avoid" 这类模糊否定词

---

### D6: 示例设计 (Concrete Demonstrations)

#### 为什么这样做

示例是控制 LLM 输出行为的**最可靠机制**。这不是"锦上添花"，而是与指令同等重要的核心组件。

Cursor 官方数据：Good/Bad 示例使规则效果提升 **3 倍**。注意不是 30%，而是 300%——这意味着一个带示例的规则比三个不带示例的规则更有效。

**1-shot CoT Distillation（Chen et al., ACL 2025）** 证明：1-shot（一个示例）是灵活性和结构之间的最优平衡点。更多示例的边际收益递减，但 0 个示例则完全没有结构引导。

Google Gemini 指南："We recommend to always include few-shot examples"——"always" 这个词在官方文档中很少见，表明示例的重要性。

Anthropic 推荐 3-5 个精心设计的示例，并使用 `<example>` 标签包裹。

#### 诊断方法

1. 技能中是否有"用户请求 → agent 行为"格式的示例？
2. 示例是否使用了真实场景（而非占位符如 "process a file"）？
3. 示例是否覆盖了最常见的使用场景？

#### 优化操作

1. 添加 1-3 个具体示例
2. 格式：`### User: "..." → 1. ... 2. ... 3. ...`
3. 简单技能 1-2 个，中等技能 3-5 个，复杂技能 3-5 个核心 + references 中的详细示例

#### 好示例 vs 坏示例

```markdown
# ❌ BAD: 抽象示例，无具体输入输出
Use the transform script to convert between formats. For example,
you might process a CSV file and convert it to JSON format.

# ✅ GOOD: 具体的用户请求 → 期望的 agent 行为
## Examples

### User: "Convert this CSV to JSON"
→ 1. Run `scripts/transform.py data.csv --output data.json`
→ 2. Verify the JSON has expected keys: `name`, `date`, `amount`
→ 3. Report: "Converted 150 records from CSV to JSON"

### User: "The output has wrong date format"
→ 1. Check current date format in output
→ 2. Add `--date-format ISO8601` flag to transform command
→ 3. Re-run and verify dates match `YYYY-MM-DD`

### User: "Merge these two PDFs"
→ 1. Run `scripts/pdf-merge.py input1.pdf input2.pdf --output merged.pdf`
→ 2. Verify page count: original1 + original2 = merged
→ 3. Report: "Merged into N pages"
```

**为什么好示例有效**：好示例同时展示了三件事——(1) agent 应该执行什么命令 (2) 如何验证结果 (3) 如何向用户报告。坏示例只展示了"做什么"，遗漏了验证和沟通。

#### 检查清单

- [ ] 至少 1 个具体的"用户请求 → agent 行为"示例
- [ ] 示例使用真实的用户输入（非占位符）
- [ ] 示例覆盖最常见使用场景
- [ ] 错误/边缘情况示例（如适用）
- [ ] SKILL.md 中不超过 5 个示例（多余的放入 references）

---

### D7: 验证机制 (Quality Gates)

#### 为什么这样做

没有验证标准的 agent 会产出"看起来正确"但实际错误的结果。这不是偶发问题，而是 agent 的系统性倾向。

Claude Code Issue #42796（**1781 👍**，是该仓库最高赞 issue 之一）提供了定量分析：agent 的 Read:Edit 比率下降了 70%——意味着 agent 在修改文件前越来越少地先读取文件，直接跳过验证步骤导致错误。Issue 标题直指问题本质："Claude rushes to completion"（Claude 急于完成任务）。

Anthropic 最佳实践明确要求："Always provide validation criteria"（始终提供验证标准）。

生产级模式 Plan → Act → Verify 被 Cursor、Aider 和 Claude Code 一致采用，因为这是唯一能确保输出质量的方法。

#### 诊断方法

1. 工作流最后是否有验证步骤？
2. 是否有可测试的成功标准？（不是"确保质量好"，而是"运行 `npm test` 且全部通过"）
3. 验证失败时 agent 知道该怎么做吗？

#### 优化操作

1. **添加验证步骤**：每个工作流末尾添加明确的验证环节
2. **定义可测试标准**：标准必须是机器可验证的（命令输出、文件存在性、断言）
3. **失败时的处理流程**：验证失败 → 诊断 → 修复 → 重新验证

#### Before/After 对比示例

**示例 1：无验证 → 有验证**

```markdown
# ❌ BEFORE: 无验证步骤
## Deployment
1. Build the project
2. Deploy to staging
3. Inform the user

# ✅ AFTER: 完整验证链
## Deployment
1. Build: `npm run build` — confirm exit code 0
2. Deploy: `scripts/deploy.sh staging`
3. **Verify**:
   - Run `curl -f https://staging.example.com/health` — expect 200
   - Run `scripts/smoke-test.sh` — all tests pass
4. Report results to user
5. If any verification fails → capture logs, diagnose, fix, re-deploy, re-verify
```

**示例 2：模糊成功标准 → 可测试标准**

```markdown
# ❌ BEFORE: 不可测试的标准
After generating the report, make sure it looks good and contains
all the necessary information.

# ✅ AFTER: 可测试的验证标准
## Verification

After generating the report, verify all checks pass:

1. **File exists**: `ls -la reports/<report-name>.md`
2. **Sections complete**: Report contains `## Summary`, `## Details`, `## Metadata`
3. **Data accurate**: Run `scripts/validate-report.py reports/<report-name>.md`
4. **No regressions**: `npm test` — all existing tests pass

If any check fails: diagnose the specific failure, fix the report, re-verify.
Do NOT inform the user of success until all 4 checks pass.
```

#### 检查清单

- [ ] 工作流包含显式验证步骤
- [ ] 成功标准是具体可测试的
- [ ] agent 知道验证失败时做什么
- [ ] 尽可能引用自动化检查（测试命令、脚本）
- [ ] 验证失败时不会向用户报告"完成"

---

### D8: 自由度校准 (Specificity Matching)

#### 为什么这样做

过度约束创意任务会不必要地限制模型；约束不足的脆弱任务会导致错误。这不是"一刀切"的问题，而是需要根据任务类型精确校准。

**NeurIPS 2024 论文 "Teach Better or Show Smarter?"** 证明：教学（指令优化）vs 示例（模仿学习）的效果取决于任务类型。对于需要精确遵循步骤的任务（如数学证明），显式指令更有效；对于需要创造力的任务（如写作），示例更有效。

Claude Code 的设计原则形象地描述了这一思想："Think of Codex exploring a path — a narrow bridge needs guardrails, an open field allows many routes"（想象 Codex 在探索路径——窄桥需要护栏，开阔田野允许多条路线）。

#### 诊断方法

1. 脆弱任务（部署、数据库迁移）的指令是否足够具体？
2. 创意任务（写作、设计）是否过度约束？
3. 同一技能中是否存在矛盾的 specificity 信号？

#### 优化操作

按任务类型校准自由度：

| 任务类型 | 自由度 | 信号词 | 优化策略 |
|---------|--------|-------|---------|
| 脆弱序列（部署、DB 迁移） | **低** | "必须"、"精确"、"按顺序" | 编号步骤、具体命令、脚本 |
| 模式化任务（代码生成、API 调用） | **中** | "优先"、"通常"、"默认" | 首选模式 + 允许的替代方案 |
| 创意/开放式（写作、头脑风暴） | **高** | "考虑"、"可以"、"探索" | 原则 + 示例，少量硬规则 |

#### 低/中/高自由度的典型示例

**低自由度（数据库迁移）**：
```markdown
## Migration Workflow
1. Run `scripts/backup.sh` to create DB backup
2. Run `scripts/migrate.py --dry-run` and verify output
3. ONLY if dry-run succeeds: run `scripts/migrate.py`
4. Run `scripts/verify-migration.py` to confirm data integrity
```
→ 每步都是具体命令，无解释，无替代方案。

**中等自由度（API 客户端生成）**：
```markdown
## Code Generation
- Prefer typed request/response interfaces (TypeScript/zod)
- Use fetch with proper error handling; axios is acceptable if already in project
- Follow existing project patterns in `src/api/` for consistency
```
→ 有偏好但不强制，允许合理的替代方案。

**高自由度（技术博客写作）**：
```markdown
## Writing Guidelines
- Match the brand voice described in `references/brand-voice.md`
- Target length: 500-800 words
- Structure: Lead with the key insight, then expand with evidence
- Include at least one code example if the topic is technical
```
→ 原则而非规则，给 agent 充分的创作空间。

#### 检查清单

- [ ] 自由度级别匹配任务脆弱性
- [ ] 脆弱任务有编号的具体步骤（可能包含脚本）
- [ ] 创意任务有原则，而非死板的规则
- [ ] 同一区域中无矛盾的 specificity 信号

---

### D9: 渐进式加载 (Context Architecture)

#### 为什么这样做

一次性加载所有内容会浪费上下文空间——agent 在当前任务中并不需要所有信息。

不同平台的加载机制不同，但原则一致：**只在需要时加载需要的内容**。

- **Claude Code**：三层加载机制——Metadata（~100 词，始终加载）→ SKILL.md（<5k 词，触发时加载）→ Resources（按需加载）
- **Cursor**：.mdc 模式，按文件路径触发规则，只有匹配路径时才加载对应规则
- **Windsurf**：**6000 字符硬限制**，强制要求激进的上下文管理

#### 诊断方法

1. SKILL.md 是否在 500 行以内？
2. references/ 是否从 SKILL.md 链接？
3. 链接是否说明了**何时**读取？（不是"更多信息见 X"，而是"当用户要求 Y 时，读取 X"）
4. references 是否嵌套超过 1 层？

#### 优化操作

1. **核心工作流留在 SKILL.md**：处理 80% 场景的最小工作流
2. **详细信息移到 references**：边缘情况、完整 API 文档、高级用法
3. **每个链接说明 WHEN**：明确告诉 agent 在什么条件下读取 reference

#### Before/After 对比示例

**示例 1：所有内容塞进 SKILL.md → 渐进式加载**

```markdown
# ❌ BEFORE: SKILL.md 600+ 行，包含所有内容
## API Endpoints
[50 行完整 API 文档]

## Error Codes
[30 行错误码列表]

## Authentication
[20 行认证说明]

## Rate Limiting
[15 行限流说明]

## Examples
[40 行示例]

## Troubleshooting
[50 行排错指南]
[总计：205+ 行，仅 API 相关]

# ✅ AFTER: SKILL.md 只保留核心 + 引用
## API Usage
Base URL: `https://api.example.com/v2`
Auth: Bearer token in `Authorization` header

For endpoint details, read the relevant reference:
- **CRUD operations**: See [API.md](references/api.md) when working with users/orders endpoints
- **Authentication**: See [API.md](references/api.md#auth) when configuring auth
- **Error handling**: See [ERRORS.md](references/errors.md) when API returns 4xx/5xx
[总计：6 行 + 3 行引用]
```

**示例 2：模糊引用 → 条件化引用**

```markdown
# ❌ BEFORE: 引用但不说何时读取
For more details, see references/advanced.md.

# ✅ AFTER: 明确的触发条件
- **Custom schemas**: Read [SCHEMAS.md](references/schemas.md) when user provides non-standard input formats
- **Error handling**: Read [TROUBLESHOOTING.md](references/troubleshooting.md) when any script exits with non-zero code
- **Performance tuning**: Read [PERFORMANCE.md](references/performance.md) when user mentions "slow", "timeout", or "optimize"
```

#### 检查清单

- [ ] SKILL.md 正文在 500 行以内
- [ ] 详情移至 `references/`，有从 SKILL.md 的清晰链接
- [ ] 每个引用链接说明了**何时**读取
- [ ] 引用深度为 1 层（无嵌套引用）
- [ ] 大型引用文件（>100 行）有目录

---

## 3. 按技能类型的优化优先级

不同技能类型有不同的优化优先级。使用此矩阵聚焦优化努力。

| 技能类型 | 优先级排序（高→低） | 典型优化操作 |
|---------|-------------------|-------------|
| **工作流技能**（顺序流程） | D4 步骤 > D7 验证 > D2 效率 | 编号步骤、验证检查点、边缘情况移入 references |
| **工具集成技能**（API/CLI 封装） | D1 描述 > D8 自由度 > D6 示例 | 触发词包含工具/API 名、校准具体度、添加使用示例 |
| **知识/参考技能**（schema、策略、标准） | D9 渐进 > D2 效率 > D3 结构 | 激进地将详情移至 references、SKILL.md 只留导航、结构化分区 |
| **创意/生成技能**（写作、设计、头脑风暴） | D5 正向 > D8 自由度 > D6 示例 | 表达为原则而非规则、高自由度、用示例设定质量标杆 |
| **调试/分析技能**（排错、调查） | D4 步骤 > D7 验证 > D5 正向 | 诊断流程逐步化、内置验证、正向表达修复方案 |

### 优先级矩阵

```
              D1  D2  D3  D4  D5  D6  D7  D8  D9
工作流          ●   ●   ○   ★   ○   ○   ★   ○   ●
工具集成        ★   ○   ●   ●   ○   ★   ○   ★   ●
知识/参考       ○   ★   ★   ○   ○   ○   ○   ○   ★
创意/生成       ●   ●   ○   ○   ★   ★   ○   ★   ●
调试/分析       ●   ●   ○   ★   ★   ●   ★   ○   ●

★ = 最高优先级  ● = 重要  ○ = 可选
```

---

## 4. 反模式目录

已知会降低技能性能的模式。优化时检查这些反模式。

### AP-1: Kitchen Sink（大杂烩）

**症状**：SKILL.md > 500 行，涵盖过多主题，什么都想说
**根因**：害怕遗漏信息，把所有内容都塞进 SKILL.md
**修复**：核心工作流留在 SKILL.md，其余移至 `references/`
**证据**：Issue #2544 — 规则超过 200 行开始被忽略

### AP-2: Invisible Skill（隐形技能）

**症状**：技能已安装但从不触发
**根因**：description 缺少触发短语和场景
**修复**：用三步公式重写 description（能力 + 场景 + 关键词）
**证据**：Issue #9716 — 技能因缺少触发词而不被识别

### AP-3: Vague Guardrails（模糊护栏）

**症状**："Write clean code"、"Be helpful"、"Ensure quality"
**根因**：规则不可操作、不可测量
**修复**：替换为具体、可测量的规则（"函数 < 20 行"、"运行 `npm test` 且全部通过"）
**证据**：Anthropic — "Delete lines Claude could infer"

### AP-4: Negative-Only Rules（纯否定规则）

**症状**：满篇 "Don't do X"、"Never Y"、"Avoid Z"
**根因**：人类思维习惯用否定表达禁止，但 LLM 遵循负约束的能力差
**修复**：转换为正向表达（"Don't write long functions" → "Keep functions under 20 lines"）
**证据**：Inverse IFEval — 所有 LLM 在负约束上表现差

### AP-5: Missing Exit Condition（缺失退出条件）

**症状**：Agent 不断工作，不确定何时完成；或过早宣布完成
**根因**：没有定义"成功"的具体标准
**修复**：添加可测试的成功标准和显式的验证步骤
**证据**：Issue #42796（1781👍）— Agent 跳过验证导致错误

### AP-6: Flat Structure（扁平结构）

**症状**：所有内容在一个块中，无标题层级
**根因**：快速编写技能时忽略了结构
**修复**：添加 Markdown 层级（`##`、`###`）和 `---` 分隔符
**证据**：CFPO — 结构优化可带来 +5-38% 提升

### AP-7: Zombie References（僵尸引用）

**症状**：references/ 中有文件，但 SKILL.md 中没有链接
**根因**：创建了引用文件但忘记在 SKILL.md 中添加链接
**修复**：在 SKILL.md 中添加 "See [X](Y) when..." 的条件化引用
**证据**：Claude Code — 未链接的引用不会被 agent 发现和读取

### AP-8: Over-Specified Creative（过度约束创意任务）

**症状**：创意任务有 20 条死板规则（"精确 3 段"、"每段以...开头"）
**根因**：对创意任务使用了脆弱任务的约束策略
**修复**：减少为原则 + 示例，给 agent 创作空间
**证据**：NeurIPS 2024 — 任务类型决定最优方法

---

## 5. 证据来源

### 同行评审研究

| 论文 | 发表 venue | 核心发现 |
|------|-----------|---------|
| CFPO (Liu et al.) | arXiv 2025 | 内容+格式联合优化：相比基线 +5-38% |
| Inverse IFEval (Zhang et al.) | arXiv 2025 | 所有主流 LLM 在负约束上表现显著差于正约束 |
| Constraint Decomposition (Paunova) | Optimization Online 2025 | 约束分解：41.2% → 73.8% 准确率 |
| Chain of Methodologies (Liu et al.) | Findings of ACL 2025 | 结构化逐步推理优于自由格式 |
| Watch Every Step (Xiong et al.) | EMNLP 2024 | 步骤级指导增强 agent 效率 |
| What's in a Prompt (Atreja et al.) | ICWSM 2025 | 提示词结构因素显著影响输出质量 |
| Teach Better or Show Smarter | NeurIPS 2024 | 指令 vs 示例的有效性取决于任务类型 |
| 1-shot CoT Distillation (Chen et al.) | Findings of ACL 2025 | 1-shot 是灵活性和结构的最优平衡 |

### 官方指南

| 来源 | 核心建议 |
|------|---------|
| Anthropic | XML 标签、3-5 个示例、正向表达、"golden rule" 测试 |
| Google Gemini | "始终包含 few-shot 示例"、关键指令放最前 |
| Microsoft | 将提示词分解为 Instructions / Content / Examples / Cue |
| Brex | 命令语法、假设隐藏提示词可见 |

### 社区证据

| 来源 | 核心发现 |
|------|---------|
| Claude Code Issue #2544 (39+) | CLAUDE.md 规则在过长时被忽略 |
| Claude Code Issue #6354 (27+) | 上下文压缩后规则被遗忘 |
| Claude Code Issue #9716 (69+) | 技能因缺少触发词而不被识别 |
| Claude Code Issue #42796 (1781+) | Agent 跳过验证导致错误 |
| Cursor 官方博客 | Good/Bad 示例使规则效果提升约 3 倍 |

> **详细数据和完整引用**见 [evidence-database.md](evidence-database.md)
