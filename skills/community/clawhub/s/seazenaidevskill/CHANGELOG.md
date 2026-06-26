# Changelog

## v2.5.0 (2026-06-03) — 剥离合并门禁，聚焦研发智能体

### 变更背景

合并门禁核查（merge request review）已独立部署为单独的服务，本项目回归纯粹的研发统筹智能体定位。

### 核心变更

**删除（已迁移至独立审核服务）：**

- `templates/ci/` — CI 流水线模板（merge-review.yml、.gitlab-ci.yml、pre-push-review.sh）
- `templates/review/` — 合并门禁核查模板（AGENT.md、checklists、report-template）
- `hooks/` — 自动化钩子（webhook-review.md、README.md）

**SKILL.md 变更：**

- 角色定位：职责从四件事回归三件事（init / guide / update），移除 review（合并门禁）
- 入口判断：移除 review 入口，入口四（update）→ 入口三
- 文件映射表：移除 CI/hooks/review 的安装映射
- init：不再创建 `.seazenai/review/` 目录
- guide：移除合并门禁相关状态判断

**模板变更：**

- `templates/CLAUDE.md`：移除合并门禁仪表盘行和启动提醒
- `templates/development/AGENT.md`：移除 CP5.5 合并门禁提醒
- `templates/testing/AGENT.md`：移除 CP5 合并门禁提醒

## v2.4.0 (2026-06-02) — 新增合并门禁核查技能

### 变更背景

当前 orchestrator 的职责是**引导**用户完成需求→开发→测试全流程。但面对多种多样的 AI 工具，产出物质量参差不齐，需要在合并到 develop 分支前设置一道统一的合规门禁——不管用什么工具、什么方式产出，合并前都要过同一把尺子。

### 核心变更：新增 review 入口 + 合并门禁模板体系

**新增文件（6个）：**

- `templates/review/AGENT.md`：合并门禁核查智能体。定位为 develop 分支的**合并门禁**，在开发+测试均完成后触发，给出允许合并/禁止合并的决策。只裁判，不指导。
- `templates/review/INDEX.md`：核查任务索引（进行中/已完成）。
- `templates/review/requirements-checklist.md`：需求核查清单（5大类28项）——结构完整性（13章节）、A/B/C追问覆盖（15项）、约束合规（3项）、内容质量（4项）、飞书集成（2项）。
- `templates/review/development-checklist.md`：开发核查清单（5大类30+项）——一票否决项（5项）、行为红线（6项）、.NET规范（7类）、Java规范（7类）、需求匹配度（3项）。
- `templates/review/testing-checklist.md`：测试核查清单（5大类20+项）——三层覆盖（3项）、盲区覆盖（6类12项）、格式合规（3项）、需求/开发匹配（3项）、执行规范（3项）。
- `templates/review/report-template.md`：合并门禁报告模板，含基本信息、三维度概览、一票否决项、详细结果、合并建议（允许合并/修复后重审/禁止合并）、整改跟踪。

**SKILL.md 变更：**

- 角色定位：职责从三件事扩展为四件事（+合并门禁 review）
- 新增「入口三：review（合并门禁）」：触发时机（仅合并到 develop 前）、前置条件（开发+测试均已完成）、路由到核查智能体
- 文件映射表：增加 review 模板的安装映射
- init Step 3：创建 `.seazenai/review/tasks/` 目录
- guide：开发+测试均完成时提示"可以执行合并门禁核查"
- 身份确认文案均增加合并门禁选项

### 核查清单提炼来源

所有核查标准均从现有技能模板中提炼，确保一致性：
- 需求核查 ← `requirements/template.md`（13章节）+ `rules-ask.md`（A/B/C追问规则）+ `constraints.md`
- 开发核查 ← `development/constraints.md`（6条红线）+ `review-checklist.md`（一票否决）+ `conventions/net-backend.md` + `conventions/java-backend.md`
- 测试核查 ← `testing/constraints.md` + `blindspot-checklist.md`（6类盲区）+ `case-template.md`（三层用例）

### 门禁规则

| 结论 | 条件 | 含义 |
|------|------|------|
| 允许合并 | 三个维度均无 ❌，总通过率 >= 80% | 可合并到 develop |
| 修复后重审 | 存在 ⚠️ 但无 ❌ 一票否决 | 建议修复后重新核查 |
| 禁止合并 | 存在 ❌ 一票否决，或总通过率 < 80% | 必须修复后重新提交，不可合并 |

### 合并自动化方案（三层）

**层级一：对话自动路由（零配置）**
- 用户说"准备合并到develop"/"提交PR" → SKILL.md 入口判断自动路由到 review
- 内置行为，无需配置

**层级二：Git Pre-Push Hook（本地阻断）**
- 新增 `templates/ci/pre-push-review.sh`：git pre-push hook 模板
- push 到 develop 时检查最近24小时内是否有通过的核查报告，无则阻断

**层级三：CI/CD 流水线（服务器端阻断）**
- 新增 `templates/ci/merge-review.yml`：GitHub Actions 工作流模板
- PR 目标为 develop 时自动触发，运行 Claude Code CLI 执行核查
- 核查不通过标记 CI 失败，阻断合并，结果自动评论到 PR

**Claude Code 钩子**
- 新增 `PostToolUse` hook 配置：拦截 `git push/merge develop` 命令，提示先执行门禁核查

## v2.3.0 (2026-06-02) — 多工具兼容适配（Claude Code / Codex / Trae / WorkBuddy）

### 变更背景

原有模板中的 `Skill("meegle")` 调用为 Claude Code 特有机制，无法在 Codex、Trae、WorkBuddy 等工具中运行。同时入口文件 `CLAUDE.md` 只对 Claude Code 有效。

### 核心变更：三层解耦

**Layer 1：新增工具适配器文件**

- `templates/tool-adapters.md`：定义「飞书项目管理」「向用户提问」「文件操作」三项通用能力，每项列出各工具的对应调用方式。Agent 运行时先读此文件，按当前工具选择正确的调用方式。

**Layer 2：模板文件去耦合**

- `templates/requirements/AGENT.md`：第 6.5 步 `Skill("meegle")` → 引用 tool-adapters.md
- `templates/development/AGENT.md`：CP1.5、CP4 中 `Skill("meegle")` → 引用 tool-adapters.md
- `templates/testing/AGENT.md`：CP4 工作流 `Skill("meegle")` → 引用 tool-adapters.md

**Layer 3：多入口文件**

- init 将 `templates/CLAUDE.md` 同时复制为 `CLAUDE.md` 和 `seazenai.md`
- `CLAUDE.md`：Claude Code 自动加载
- `seazenai.md`：通用入口，其他工具可重命名为 `CODEX.md`、`TRAE.md`、`WORKBUDDY.md`
- 完成信息中新增多工具使用指引

### Bug 修复

- SKILL.md 文件映射表中 `templates/seazenai.md`（不存在）→ 修正为 `templates/CLAUDE.md`

### 技能文件变更

- `SKILL.md`：版本号 2.2.0 → 2.3.0；修正文件映射；新增 tool-adapters.md 映射；目录结构图和完成信息新增多工具入口提示
- 新增 `templates/tool-adapters.md`

### 入口文件增强

- `templates/CLAUDE.md`：从简单角色路由重写为**智能启动流程**：
  - **自动检测项目状态**：读取 knowledge/requirements/development/testing 四个 INDEX.md，判断当前阶段
  - **输出状态仪表盘**：启动时展示四阶段进度概览，一目了然
  - **上下文感知建议**：根据当前阶段自动给出最合理的下一步操作，而非让用户盲目选择角色
  - **继续已有任务**：有进行中的需求/开发/测试时，直接引导继续而非重新开始
  - 行为规则明确：先展示状态、再给建议、最后才选角色

### 设计原则

- SKILL.md 本身不解耦（它是 Claude Code 的安装器）
- 安装到项目的模板文件保持工具无关
- 新增工具只需在 tool-adapters.md 中加一行映射

## v2.2.0 (2026-06-02) — 飞书项目 (Meegle) 集成

### 变更背景

用户希望研发统筹智能体在关键节点自动同步飞书项目状态，减少人工操作：
1. 需求沟通完毕后自动创建飞书项目需求
2. 开发任务拆解后自动创建子任务
3. 开发/测试完成后自动更新需求与子任务状态

### 新增文件

- `templates/meegle-config.md`：飞书项目集成配置文件，包含空间信息、工作项类型、模板 ID、状态映射、角色映射、同步行为控制

### 模板变更

**requirements/AGENT.md**：
- **新增第 6.5 步：同步飞书项目**：需求归档后自动调用 Meegle `workitem create` 创建需求工作项，记录 ID 到需求文档

**requirements/template.md**：
- **第 1 节新增「飞书项目关联」子表**：飞书项目需求 ID、子任务 ID 列表字段

**development/AGENT.md**：
- **新增 CP1.5：同步飞书项目子任务**：CP1 任务拆解后自动调用 Meegle `subtask update` 创建子任务，ID 反写到 breakdown.md
- **CP4 新增第 4 条**：开发完成时自动调用 Meegle 更新需求状态为「开发完成」、子任务状态为「已完成」

**testing/AGENT.md**：
- **CP4 工作流新增第 6 条**：测试通过后自动调用 Meegle 更新需求状态为「测试通过」、子任务状态为「测试通过」；发现缺陷时自动创建缺陷工作项

### 技能文件变更

- `SKILL.md`：版本号 2.1.0 → 2.2.0；init 文件映射表新增 meegle-config.md；目录结构图和完成信息新增对应条目
- `SKILL.md`：**新增 Step 5.5：引导配置飞书项目集成**——init 完成后询问用户是否配置，引导完成空间选择、类型映射、模板获取、用户映射，自动写入 meegle-config.md

### 设计原则

- 非阻塞：飞书项目同步失败不阻塞研发流程，仅记录并提示
- 可配置：所有 Meegle 参数集中在 meegle-config.md，未配置时静默跳过
- 双向追踪：飞书项目 ID 写入本地文档，本地状态变更同步到飞书项目

## v2.1.0 (2026-05-26) — 开发/测试 Agent 任务初始化 + 阶段无缝衔接

### 变更背景

用户在实际开发任务中发现三个问题：
1. 开发人员说"我要做 REQ-XXX"时，没有创建 `development/tasks/REQ-N/` 文件夹
2. 测试人员同理，没有创建 `testing/tasks/REQ-N/` 文件夹
3. 阶段之间需要用户手动切换角色，体验割裂

### 模板变更

**development/AGENT.md**：
- **新增 L0 第 2 条**：读取 `requirements/INDEX.md`，定位目标需求位置（in-progress 或 archive）
- **新增 CP0：任务初始化**：对标 requirements 的"第 0 步"——创建 `development/tasks/REQ-N/` 文件夹，初始化 `breakdown.md`、`change-log.md`、`review-notes.md`，更新 INDEX 从「待开发」→「开发中」
- **CP1 补充**：末尾新增更新 INDEX 阶段为"CP1-需求理解"
- **CP4 细化**：明确为"准备提交测试"，追加更新 INDEX 从「开发中」→「已完成」
- **新增 CP5：交接测试**：开发完成后主动询问"是否进入测试阶段？"，同意则加载 testing/AGENT.md 并执行 TP0

**testing/AGENT.md**：
- **知识加载扩至 7 条**：补齐 requirements/INDEX、development/INDEX、需求文档、开发 breakndown 的定位链路
- **新增 TP0：任务初始化**：对标 CP0——创建 `testing/tasks/REQ-N/` 文件夹，初始化 `test-cases.md`、`test-results.md`、`coverage-report.md`，更新 INDEX 从「待测试」→「测试中」

**requirements/AGENT.md**：
- **新增第 7 步：进入开发**：需求归档后主动询问"是否进入开发阶段？"，同意则加载 development/AGENT.md 并执行 CP0

### 技能文件变更

- `SKILL.md`：init Step 3 创建目录新增 `testing/tasks/`
- 阶段衔接流程：需求归档 →（第7步询问）→ 开发 CP0 → ... → 开发 CP5（询问）→ 测试 TP0

## v2.0.0 (2026-05-26) — v4 文档重构：八部分结构 + Prompt-as-Code 独立成篇

基于《研发统筹智能体落地方案.md》v4 全面重构更新。

### 文档结构重组

原文档（v3）按线性结构组织（一~十二章），v4 重组为 **八部分**：

| 部分 | 标题 | 内容 |
|------|------|------|
| 第一部分 | 总纲与架构 | 端到端流程、角色交互、知识飞轮、核心原则、迭代与反复 |
| 第二部分 | 基础设施 — Prompt-as-Code 与知识体系 | Prompt-as-Code 核心理念、目录结构总览(2.3)、知识层设计 2.4(组织/加载/保鲜)、seazenai.md 入口路由(2.5)、INDEX.md 设计(2.6)、Agent 工作流(2.7)、Bootstrap 初始化(2.8)、加载优先级与冲突规则(2.10) |
| 第三部分 | Phase 1 — 知识注入 | 10 步知识提取执行手册(3.3)、知识层验收标准(3.4) |
| 第四部分 | Phase 2 — 需求对话 | System Prompt 参考框架(4.6)、冷启动策略(4.7)、需求阶段验收标准(4.8) |
| 第五部分 | Phase 3 — 研发统筹 | 硬性安全边界(5.1.1)、任务拆解(5.3)、决策点上报(5.4)、Review 机制(5.5)、测试盲区审查(5.6) |
| 第六部分 | Phase 4 — 测试智能体 | 测试用例生成策略、测试人员新工作流、产品经理验收测试 |
| 第七部分 | 实施与治理 | 实施路线图(7.1)、Go/No-Go 决策(7.2)、角色分工(7.3)、风险应对(7.4)、成本模型(7.5)、度量指标(7.6) |
| 第八部分 | 附录 | 各技术栈 AI Coding 提示词模板 |

### 关键变化

- **Prompt-as-Code 基础设施独立成篇**（第二部分）：从原来散落在 3.5 节各处的实现细节，提升为独立的部分，覆盖目录结构、知识层设计、入口路由、Agent 工作流、Bootstrap 流程、加载优先级等完整体系
- **新增 2.3 目录结构总览**：完整的 `.seazenai/` 目录树，标注各文件的 token 量级
- **知识层设计重新编号**：2.4.1 知识组织结构 / 2.4.2 知识粒度与加载策略 / 2.4.3 知识保鲜机制
- **Bootstrap 交叉引用修正**：原引用 3.5.1→4.6 节、4.6→5.6 节、2.3→3.3 节
- **全文档交叉引用修正**：第四部分 4.6 节、第五部分 5.6 节、第二部分 2.10 节等

### 技能文件变更

- `SKILL.md`：版本号 1.0.0 → 2.0.0，更新描述和文档引用，模板文件从 17 个增至 19 个
- `references/architecture.md`：添加 v4 主文档索引、修正 5 处交叉引用
- `templates/requirements/AGENT.md`：新增「第 0 步：创建需求文件夹」和「需求归档」流程，每个需求自动创建 `REQ-NNN/` 文件夹及三个初始文件
- `templates/requirements/notes.md`：**新增**，临时否定/决策记录模板，待确认后沉淀到 knowledge/
- `templates/requirements/conversation.md`：**新增**，对话记录骨架模板，每轮对话结束后追加

## v1.0.0 (2026-05-25)

初始版本。

### 包含内容

- **init**：项目智能体体系初始化（17 个模板文件 + 占位符替换）
- **guide**：四阶段引导（Phase 1 知识注入 → Phase 2 需求对话 → Phase 3 开发编排 → Phase 4 测试审查）
- **update**：模板文件差异对比与合并（✅/⚠️/🔴 三态分类）

### 模板文件

| 目录 | 文件数 | 说明 |
|------|--------|------|
| templates/ | 1 | seazenai.md（项目入口路由） |
| templates/knowledge/ | 1 | INDEX.md（知识索引） |
| templates/requirements/ | 5 | AGENT.md、INDEX.md、rules-ask.md、template.md、constraints.md |
| templates/development/ | 5 | AGENT.md、INDEX.md、review-checklist.md、decision-types.md、constraints.md |
| templates/testing/ | 5 | AGENT.md、INDEX.md、blindspot-checklist.md、case-template.md、constraints.md |

### v1.1.0 (2026-05-25) — 新增技术栈提示词附录

在《研发统筹智能体落地方案.md》中新增 **十二、附录：各技术栈 AI Coding 提示词模板**，包含：

**12.1 架构设计提示词模板**
- Java 后端架构设计（八阶段设计流程 + ADR + 行为红线）
- SAP ABAP 架构设计（DDIC规范 + OData + CDS/AMDP约束）
- H5 前端架构设计（组件树/数据流/路由设计 + 标准目录结构）
- Flutter 架构设计（SzBehaviorSubject + Store + Controller三层架构）

**12.2 功能开发提示词模板**
- Java 后端功能开发（6大类行为红线 + 编码/日志/安全/数据库约束）
- SAP ABAP 功能开发（ABAP 750+ + HANA性能优化 + ENQUEUE规范）
- .NET 后端功能开发（六步功能开发法：契约校验→范围锁定→Domain→Infrastructure→Application→测试自检）
- H5 前端功能开发（Vue 3 + Element Plus + MicroApp 十阶段SOP）
- Flutter 功能开发（DTO→API→Store→Page→Route 六步开发流程）
- SAP Fiori 功能开发（XML View + Controller + OData 三合一提示词）

**12.3 测试提示词模板**
- 测试计划（10章节完整模板）
- 测试用例生成（三步迭代法：标题→场景→探索性测试）
- API 自动化测试（Apifox MCP + pytest + Allure + GitHub Actions）
- Web UI 自动化测试（Playwright + Pytest + POM + 失败自动截图）

**12.4 使用指引**
- 各提示词与落地方案CP1-CP4的集成方式
- 提示词模板维护机制

### 参考文档

| 文件 | 说明 |
|------|------|
| references/architecture.md | 完整架构方案（1745 行） |
| references/knowledge-extraction.md | Phase 1 知识提取 10 步手册 |
| references/cold-start.md | Phase 2 冷启动训练期设计 |
| references/phase-guide.md | 各阶段引导与验收标准 |

### v1.2.0 (2026-05-25) — 补充飞书文档对齐遗漏项

在《研发统筹智能体落地方案.md》中补充 4 项遗漏内容：

1. **需求简报模板（3.3bis 节）**：从飞书文档"需求评估"环节提取轻量级需求简报 .md 模板，含内容要求表和使用场景指引，与 PRD 模板互补。

2. **原型设计规范（3.4.1 节）**：从飞书文档"原型设计"环节提取面向 AI Coding 的原型规范，包括 2 类输出形式、3 条内容要求，以及与 PRD 模板第 7 节的对应关系。

3. **产品经理验收测试（5.4 节）**：从飞书文档"测试验收"环节提取 PM 视角的验收测试流程，包括用例格式、AI 自动 vs 人工执行的分类、与 Phase 4 测试的分工对照。

4. **常见 AI 代码问题及处理策略（4.5 节补充）**：从飞书文档"代码审核"环节提取 6 类高频 AI 代码问题模式（幻觉代码/过度设计/硬编码/测试不完整/注释不可靠/依赖擅自引入）及处理策略表。
