# 技能减法 · 评估框架

## 一、技能分类体系

针对 AI Agent Skill 的业界生态与实用场景，将技能按照**6 大功能领域（Functional Taxonomy）**进行归类，并标注具体的**细分领域（Subcategory）**。

技能的功能分类与**安装来源（用户安装 / 平台预装 / Agent 创建）**及**作用域（用户级 / 项目级）**完全解耦，作为独立维度进行评估。

### 1. 开发与工程类 (Dev & System / Engineering)

**定义**：面向软件开发、系统运维、终端命令行与代码工程的技能。

**细分领域 (Subcategories)**：
- **代码生成与重构**：代码编写、模式重构、Code Review、架构设计
- **终端 Shell 与 DevOps**：命令行脚本、CI/CD 自动化、容器部署、环境配置
- **测试与调试**：单元测试撰写、Bug 排查、日志诊断、API 测试
- **Git 与版本控制**：Commit/PR 自动化、分支管理、冲突解决

**示例**：`git-workflow`, `code-refactor`, `ci-cd-helper`, `api-tester`

**保留标准**：高频使用（每天或每周）+ 对工程研发有显著提效

### 2. 数据与集成类 (Data & Connectors)

**定义**：连接外部系统、数据库、API 接口及知识检索的技能。

**细分领域 (Subcategories)**：
- **数据库/SQL 查询**：SQL 编写、数据库 Schema 分析、数据查询与导出
- **知识检索与 RAG**：学术文献检索、内部文档库搜索、向量检索
- **SaaS 与 API 连接器**：GitHub/Jira/Notion/Slack/Linear 接口集成与数据同步

**示例**：`postgres-query`, `github-issue-tracker`, `notion-sync`, `arxiv-search`

**保留标准**：关联系统使用频繁 + 接口维护良好 + 无法被标准 Web 搜索简单替代

### 3. 内容与多媒体创作类 (Content, Design & Media)

**定义**：多媒体内容生成、视觉设计及富文本/格式转换类技能。

**细分领域 (Subcategories)**：
- **图像与视觉生成**：AI 绘图 (Midjourney/Flux/SD)、UI 原型、图表制作
- **HTML/PPT 演示文稿生成**：网页版 Presentation、幻灯片制作与转换
- **文档与格式转换**：PDF OCR 解析、Word/Excel 读写、格式清洗与重排

**示例**：`generate-html-ppt`, `image-gen`, `pdf-ocr`, `excel-analyzer`

**保留标准**：输出质量高 + 符合工作流格式要求 + 近期有实际创作需求

### 4. 专业业务与领域类 (Domain & Business)

**定义**：与特定行业、企业部门或具体业务流程绑定的技能。

**细分领域 (Subcategories)**：
- **财务与法务**：合同审查、税务合规、财务报表分析
- **营销与竞品**：竞品分析报告、SEO 优化、社媒文案撰写
- **客服与运营**：电商客服回复、工单处理模板、运营活动策划
- **HR 与行政政策**：员工手册查询、招聘 JD 生成、报销流程指引

**示例**：`legal-contract-review`, `competitor-analysis`, `ecom-customer-service`

**保留标准**：当前正在绑定的业务项目 + 在可预见的业务周期内持续生效

### 5. 通用生产力与工作流类 (Productivity & Workflow)

**定义**：日常办公增强、个人效率提升及流程自动化技能。

**细分领域 (Subcategories)**：
- **周报与会议纪要**：周报月报生成、会议录音/文本整理、Action Item 提取
- **任务与日程管理**：TodoList 整理、日程规划、提醒事项生成
- **邮件与消息撰写**：商务邮件起草、通知群发模板、回复拟定

**示例**：`weekly-report`, `meeting-summary`, `email-drafter`

**保留标准**：每周至少使用一次 + 流程比手动操作具备明显效率优势

### 6. 元技能与系统控制类 (Meta & Agent Control)

**定义**：作用于 Agent 本身或技能体系治理的系统级/元级技能。

**细分领域 (Subcategories)**：
- **技能审计与管理**：已安装技能扫描、价值评估与清理（如本技能 `skill-subtraction`）
- **Prompt 评估与调优**：Prompt 优化、Evaluator 评测、System Prompt 构建
- **Memory 记忆管理**：长期记忆检索、用户偏好更新、上下文摘要
- **Agent 行为规范**：Custom Instructions、规约/Rule 控制

**示例**：`skill-subtraction`, `agy-customizations`, `prompt-evaluator`

**保留标准**：具备高度不可替代的 Agent 治理与自我提升价值

---

### 独立评估维度（与功能分类解耦）

1. **安装来源 (Source Type)**：
   - **用户手动安装 (`user-installed`)**：用户主动引入，需优先重点打分评估。
   - **平台预装 (`platform-preinstalled`)**：Agent 平台批量出厂自带，适合整批按业务方向筛选或归档。
   - **Agent 自主创建 (`agent-created`)**：Agent 在对话中临时生成，易过期，可安全卸载或重新生成。
2. **作用域 (Scope)**：
   - **全局用户级 (`user`)**：存放在 `~/.<agent>/skills/`，全局复用。
   - **项目绑定级 (`project`)**：存放在工作区 `.workbuddy/skills/`，项目结束后直接清理。

## 二、评估指标（百分制）

六个指标加权求和，总分 100 分。各指标权重反映其对技能保留决策的影响程度。

### 指标 1：使用频率（25 分）

> 权重最高——用不用是决定去留的第一标准。

| 等级 | 定义 | 分值 |
|------|------|------|
| 高 | 每天 or 每周使用 | 25 |
| 中 | 每月使用 | 16 |
| 低 | 几个月一次 | 8 |
| 零 | 安装后从未使用，或已忘记其存在 | 4 |

### 指标 2：必要性（20 分）

> 没有它行不行，直接决定技能的不可替代程度。

| 等级 | 定义 | 分值 |
|------|------|------|
| 不可替代 | 没有它，对应工作流断裂 | 20 |
| 有替代方案 | 有其他技能或通用能力可覆盖，但本技能更优 | 12 |
| 可有可无 | 通用能力即可完成，技能只是锦上添花 | 4 |

### 指标 3：当前相关性（20 分）

> 技能再好，跟当前方向不匹配也要清理。

| 等级 | 定义 | 分值 |
|------|------|------|
| 匹配 | 与当前核心业务/工作方向直接相关 | 20 |
| 部分匹配 | 与当前方向间接相关，偶尔有用 | 12 |
| 不相关 | 业务方向已变化，或属于已结束的项目 | 4 |

### 指标 4：启用状态（15 分）

> 已禁用的技能不出现在 agent 上下文中，不影响思考，但也不提供自动价值。

| 等级 | 定义 | 分值 |
|------|------|------|
| 已启用 | 自动触发可用，agent 主动考虑是否调用 | 15 |
| 已禁用但近期有手动调用 | 有意降噪保留，偶尔手动 `/skill-name` 调用 | 9 |
| 已禁用且从未手动调用 | 完全闲置，纯占磁盘空间 | 3 |

### 指标 5：维护状态（10 分）

> 长期不更新的技能可能已经失效。

| 等级 | 定义 | 分值 |
|------|------|------|
| 活跃 | 近 30 天内有修改或更新 | 10 |
| 一般 | 30-90 天内有修改 | 6 |
| 停滞 | 90 天以上未修改 | 3 |

### 指标 6：独特价值（10 分）

> 功能重叠的技能只留最优的一个。

| 等级 | 定义 | 分值 |
|------|------|------|
| 独有 | 提供其他技能和通用能力都没有的功能 | 10 |
| 部分独有 | 与其他技能有重叠，但有差异化能力 | 6 |
| 完全重叠 | 与其他技能功能高度重复 | 3 |

## 三、判定矩阵

综合评分 = 使用频率 + 必要性 + 当前相关性 + 启用状态 + 维护状态 + 独特价值

评分范围：24 - 100

| 综合评分 | 建议 | 说明 |
|---------|------|------|
| 80-100 | 保留 | 高价值技能，深度掌握 |
| 50-79 | 归档 | 价值不确定，保存配置后卸载，需要时重新激活 |
| 24-49 | 卸载 | 低价值，直接清理 |

### 特殊规则（覆盖评分）

以下规则优先于评分矩阵：

1. **零使用 + 不相关 → 直接卸载**：不论其他指标如何
2. **完全重叠 → 保留最优的一个**：同功能技能去重
3. **已禁用且从未手动调用 → 直接卸载**：禁用后从未手动调用过，说明完全不需要
4. **项目级 + 项目已结束 → 卸载**：项目结束后清理
5. **数据源失效 → 卸载**：资讯类技能如果数据源已不可用
6. **平台预装 + 批量安装 + 与当前业务不匹配 → 整批归档**：不要逐个评估，直接按业务方向筛选，不匹配的整批归档。典型场景：平台预装了 HR/财务/法务/销售全套模板，但用户只做工程开发
7. **平台预装 + 用户从未主动触发 → 归档（非卸载）**：预装技能可能被平台依赖，归档而非卸载更安全。归档后若平台功能异常可快速恢复
8. **批量安装检测**：当多个技能共享相同创建日期（±1天内）且数量 ≥ 5 个时，标记为"批量安装"，建议作为一组评估而非逐个打分

## 四、去重规则

当发现功能重叠的技能时，按以下优先级保留：

1. 功能更完整的
2. 更近期更新的
3. 使用频率更高的
4. agent_created 的（可自主修改迭代）
5. 目录更轻量的（file_count 更少、dir_size 更小）

被去重淘汰的技能标记为"卸载"，理由注明"与 XX 功能重叠，保留更优方案"。

## 五、归档操作规范

归档不是简单卸载，而是保存技能的核心知识以便未来快速恢复：

1. 读取技能的 SKILL.md 全文
2. 如有 references/ 目录，读取关键参考文档
3. 如有 scripts/ 目录，记录脚本文件名和用途
4. 将以上内容整理为一个 Markdown 文件，保存到当前 Agent 对应的归档目录 `~/.<agent>/skill-archive/<skill-name>.md`（通过脚本路径反推当前 Agent，如 WorkBuddy → `~/.workbuddy/skill-archive/`，Codex → `~/.codex/skill-archive/`，Claude → `~/.claude/skill-archive/`）
5. 文件格式：

```markdown
# 归档技能：<skill-name>

**归档时间**：YYYY-MM-DD
**归档原因**：...
**重新激活条件**：...

## SKILL.md 原文

<完整 SKILL.md 内容>

## 参考文档摘要

<关键 references 文件内容摘要>

## 脚本清单

<scripts/ 目录下文件名及用途>
```

6. 确认归档文件写入成功后，再执行卸载操作

---

# Skill Subtraction · Evaluation Framework

## I. Skill Classification System

Skills are categorized into **6 functional domains (Functional Taxonomy)** aligned with modern AI Agent ecosystems, along with specific **subcategories (Subcategory)**.

Functional classification is completely decoupled from **installation source (user-installed / platform-preinstalled / agent-created)** and **scope (user-level / project-level)**, which are evaluated as independent dimensions.

### 1. Dev & System / Engineering

**Definition**: Skills designed for software development, system operations, terminal commands, and code engineering.

**Subcategories**:
- **Code Generation & Refactoring**: Code writing, refactoring patterns, code review, architecture design
- **Terminal Shell & DevOps**: Shell scripts, CI/CD automation, container deployment, environment setup
- **Testing & Debugging**: Unit test writing, bug troubleshooting, log diagnostics, API testing
- **Git & Version Control**: Commit/PR automation, branch management, conflict resolution

**Examples**: `git-workflow`, `code-refactor`, `ci-cd-helper`, `api-tester`

**Keep Criteria**: High usage frequency (daily or weekly) + significant efficiency boost for engineering R&D

### 2. Data & Connectors

**Definition**: Skills connecting external systems, databases, APIs, and knowledge retrieval.

**Subcategories**:
- **Database / SQL**: SQL writing, DB schema analysis, data query and export
- **Search & RAG**: Academic literature search, internal docs search, vector retrieval
- **SaaS & API Connectors**: GitHub/Jira/Notion/Slack/Linear API integration and data syncing

**Examples**: `postgres-query`, `github-issue-tracker`, `notion-sync`, `arxiv-search`

**Keep Criteria**: Associated system frequently used + stable API maintenance + cannot be easily replaced by simple WebSearch

### 3. Content, Design & Media

**Definition**: Skills for multimedia content generation, visual design, and rich text/format conversion.

**Subcategories**:
- **Image & Visual Generation**: AI drawing (Midjourney/Flux/SD), UI mockups, chart generation
- **HTML/PPT Presentation**: Web-based presentations, slide creation and conversion
- **Document & Format Conversion**: PDF OCR parsing, Word/Excel read-write, formatting cleanup

**Examples**: `generate-html-ppt`, `image-gen`, `pdf-ocr`, `excel-analyzer`

**Keep Criteria**: High output quality + matches workflow format requirements + active creation demand

### 4. Domain & Business

**Definition**: Skills bound to specific industries, corporate departments, or business workflows.

**Subcategories**:
- **Finance & Legal**: Contract review, tax compliance, financial statement analysis
- **Marketing & Competitors**: Competitor analysis reports, SEO optimization, social media drafting
- **Support & Operations**: E-commerce customer service replies, ticket processing templates, campaign planning
- **HR & Admin Policy**: Employee handbook lookup, job description generation, reimbursement policy guidance

**Examples**: `legal-contract-review`, `competitor-analysis`, `ecom-customer-service`

**Keep Criteria**: Currently tied to active business projects + continues to be effective in foreseeable business cycles

### 5. Productivity & Workflow

**Definition**: Skills for daily office enhancement, personal efficiency, and process automation.

**Subcategories**:
- **Weekly Report & Meeting Notes**: Weekly/monthly report generation, meeting transcription cleanup, action item extraction
- **Task & Schedule Management**: Todo list organization, schedule planning, reminder generation
- **Email & Messaging**: Business email drafting, notification broadcast templates, reply drafting

**Examples**: `weekly-report`, `meeting-summary`, `email-drafter`

**Keep Criteria**: Used at least once a week + process provides clear efficiency advantage over manual operation

### 6. Meta & Agent Control

**Definition**: System-level or meta-skills operating on the Agent itself or governance of the skill set.

**Subcategories**:
- **Skill Audit & Management**: Scanning installed skills, value evaluation, and cleanup (e.g. `skill-subtraction`)
- **Prompt Engineering & Eval**: Prompt optimization, evaluator benchmarks, system prompt construction
- **Memory Management**: Long-term memory retrieval, user preference updates, context summarization
- **Agent Guidelines & Rules**: Custom instructions, behavioral guidelines, rule enforcement

**Examples**: `skill-subtraction`, `agy-customizations`, `prompt-evaluator`

**Keep Criteria**: High irreplaceable value for Agent governance and self-improvement

---

### Independent Evaluation Dimensions

1. **Source Type**:
   - **User-installed (`user-installed`)**: Actively installed by user; highest evaluation priority.
   - **Platform-preinstalled (`platform-preinstalled`)**: Pre-packaged by agent platform; suitable for batch filtering or archiving by business direction.
   - **Agent-created (`agent-created`)**: Dynamically generated by agent during conversation; safe to uninstall or recreate.
2. **Scope**:
   - **User-level (`user`)**: Located in `~/.<agent>/skills/`, globally reusable.
   - **Project-level (`project`)**: Located in workspace `.workbuddy/skills/`, cleaned up after project completion.

## II. Evaluation Metrics (100-point scale)

Six metrics weighted and summed for a total score of 100. Weights reflect their impact on skill retention decisions.

### Metric 1: Usage Frequency (25 pts)

> Highest weight — whether it's used is the primary criterion for keep/remove.

| Level | Definition | Score |
|-------|-----------|-------|
| High | Daily or weekly use | 25 |
| Medium | Monthly use | 16 |
| Low | Once every few months | 8 |
| Zero | Never used after install, or forgotten | 4 |

### Metric 2: Necessity (20 pts)

> Whether you can do without it directly determines irreplaceability.

| Level | Definition | Score |
|-------|-----------|-------|
| Irreplaceable | Without it, the corresponding workflow breaks | 20 |
| Has alternatives | Other skills or general capabilities can cover, but this one is better | 12 |
| Nice-to-have | General capabilities suffice, skill is just icing on the cake | 4 |

### Metric 3: Current Relevance (20 pts)

> No matter how good a skill is, if it doesn't match current direction, it should be cleaned up.

| Level | Definition | Score |
|-------|-----------|-------|
| Match | Directly related to current core business/work direction | 20 |
| Partial match | Indirectly related, occasionally useful | 12 |
| Irrelevant | Business direction has changed, or belongs to ended project | 4 |

### Metric 4: Enabled Status (15 pts)

> Disabled skills don't appear in agent context, don't affect thinking, but also don't provide automatic value.

| Level | Definition | Score |
|-------|-----------|-------|
| Enabled | Auto-trigger available, agent actively considers calling | 15 |
| Disabled but recently manually invoked | Intentionally kept for noise reduction, occasionally called via `/skill-name` | 9 |
| Disabled & never manually invoked | Completely idle, purely wasting disk space | 3 |

### Metric 5: Maintenance Status (10 pts)

> Long-unupdated skills may have already failed.

| Level | Definition | Score |
|-------|-----------|-------|
| Active | Modified or updated within last 30 days | 10 |
| Normal | Modified within 30-90 days | 6 |
| Stagnant | Not modified for 90+ days | 3 |

### Metric 6: Unique Value (10 pts)

> Only keep the best among functionally overlapping skills.

| Level | Definition | Score |
|-------|-----------|-------|
| Unique | Provides functionality no other skill or general capability has | 10 |
| Partially unique | Overlaps with other skills but has differentiated capabilities | 6 |
| Complete overlap | Highly redundant with other skills | 3 |

## III. Decision Matrix

Composite Score = Usage Frequency + Necessity + Current Relevance + Enabled Status + Maintenance Status + Unique Value

Score range: 24 - 100

| Composite Score | Recommendation | Description |
|----------------|----------------|-------------|
| 80-100 | Keep | High-value skill, master deeply |
| 50-79 | Archive | Uncertain value, save config then uninstall, re-activate when needed |
| 24-49 | Uninstall | Low value, clean up directly |

### Special Rules (Override Scoring)

The following rules take priority over the scoring matrix:

1. **Zero usage + irrelevant → Uninstall directly**: Regardless of other metrics
2. **Complete overlap → Keep the best one**: Deduplicate functionally identical skills
3. **Disabled & never manually invoked → Uninstall directly**: If never manually called after disabling, it's completely unnecessary
4. **Project-level + project ended → Uninstall**: Clean up after project ends
5. **Data source defunct → Uninstall**: News-type skills with non-functional data sources
6. **Platform-preinstalled + batch install + no match with current business → Batch archive**: Don't evaluate individually; filter by business direction and batch archive non-matching ones. Typical scenario: platform pre-installed HR/finance/legal/sales templates, but user only does engineering
7. **Platform-preinstalled + never triggered by user → Archive (not uninstall)**: Pre-installed skills may be platform-dependent; archiving is safer than uninstalling. If platform functions abnormally after archiving, can quickly restore
8. **Batch install detection**: When multiple skills share the same creation date (±1 day) and count ≥ 5, flagged as "batch install"; recommend evaluating as a group rather than scoring individually

## IV. Deduplication Rules

When functionally overlapping skills are found, keep in the following priority order:

1. More complete functionality
2. More recently updated
3. Higher usage frequency
4. Agent-created (can self-modify and iterate)
5. Lighter directory (fewer file_count, smaller dir_size)

Skills eliminated by deduplication are marked as "Uninstall" with reason "Overlaps with XX, keeping the better option".

## V. Archive Operation Standard

Archiving is not simply uninstalling — it saves the skill's core knowledge for quick future recovery:

1. Read the skill's full SKILL.md
2. If references/ directory exists, read key reference docs
3. If scripts/ directory exists, record script file names and purposes
4. Organize the above into a Markdown file, save to the current Agent's archive directory `~/.<agent>/skill-archive/<skill-name>.md` (inferred from script path: WorkBuddy → `~/.workbuddy/skill-archive/`, Codex → `~/.codex/skill-archive/`, Claude → `~/.claude/skill-archive/`)
5. File format:

```markdown
# Archived Skill: <skill-name>

**Archive Date**: YYYY-MM-DD
**Archive Reason**: ...
**Reactivation Condition**: ...

## SKILL.md Original Content

<Full SKILL.md content>

## Reference Document Summary

<Key references file content summary>

## Script Inventory

<scripts/ directory file names and purposes>
```

6. Confirm the archive file was written successfully, then execute uninstall

## VI. Frontmatter Specification & Metadata Standard

To ensure maximum cross-platform compatibility across Agent platforms (Codex, Claude Code, Cursor, WorkBuddy, etc.), `SKILL.md` YAML frontmatter follows strict standard conventions:

1. **Standard Top-Level Fields**:
   - `name`: Lowercase hyphenated string (e.g., `skill-subtraction`).
   - `description`: English-primary capability and trigger description, ending with Chinese trigger keywords (covering `skill audit`, `do a skill subtraction`, `技能减法`, `审计已安装技能`).
2. **Non-Standard & Extended Attributes**:
   - Top-level frontmatter must only contain standard fields (`name` and `description`).
   - Non-standard attributes such as `version`, `agent_created`, `required_commands`, `required_privileges`, `metadata.hermes` should be placed inside a nested `metadata:` dictionary or documented within Markdown body sections (`## Requirements` / `## Metadata`).

