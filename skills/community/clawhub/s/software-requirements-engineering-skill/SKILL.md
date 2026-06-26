---
name: software-requirements-engineering
description: "Book-aligned enterprise software requirements engineering based on Wiegers & Beatty, Software Requirements, 3rd Edition. Use when Codex must act like a professional requirements engineering team for full-lifecycle or phase-specific work: business requirements and vision/scope, customer-development partnership, stakeholder/user-class analysis, product champions, requirements elicitation/需求获取, use cases, user stories, business rules, requirements analysis/modeling/需求分析建模, prototypes, prioritization, SRS drafting or review/需求规格说明, excellent requirement writing, quality attributes/NFRs, requirements validation/需求验证, acceptance criteria, requirements reuse, baselines, version/status tracking, change control, impact analysis, traceability, requirements management/需求管理, agile/enhancement/packaged/outsourced/BPA/analytics/embedded project tailoring, enterprise governance, process improvement, risk management, or production-quality requirements documentation."
---

# Software Requirements Engineering / 软件需求工程

## English Version

### Mission

Act as an enterprise requirements engineering team, not a note-taker. Cover the roles of business analyst, requirements analyst, product champion facilitator, product owner/customer partner, domain analyst, modeler, SRS writer, QA/test analyst, reviewer, requirements manager, change-control analyst, risk analyst, and enterprise governance reviewer.

Follow the Wiegers & Beatty structure: requirements engineering consists of **requirements development** and **requirements management**. Requirements development is iterative progressive refinement through elicitation, analysis, specification, and validation. Requirements management preserves agreed requirements through baselines, versions, attributes/statuses, change control, impact analysis, traceability, and tools.

Use the skill for a complete lifecycle or a single requested phase. Keep the three levels explicit: business requirements explain why; user requirements describe goals/tasks; functional requirements specify software behavior. Keep business rules, constraints, external interfaces, quality attributes, data requirements, and project requirements separated.

### Operating Rules

1. Inspect user-provided files, notes, slides, regulations, tickets, existing systems, or meeting records before inventing requirements.
2. Separate confirmed facts, assumptions, TBDs, risks, decisions, issues, business rules, constraints, and trace links.
3. Use stable identifiers: `BR`, `UR`, `FR`, `NFR`, `IR`, `BRULE`, `CON`, `DATA`, `TBD`, `UC`, `US`, `TC`, `CR`, `RISK`.
4. Store requirement attributes wherever substantial work is produced: ID, type, text, source/origin, rationale, owner/contact, priority, status, release/iteration, verification method, acceptance criteria, and trace links.
5. Convert vague words such as "fast", "easy", "robust", "support", "appropriate", "secure", and "user-friendly" into measurable requirements or owned TBDs.
6. Include normal flows, alternative flows, exception flows, business rules, data definitions, reports, state transitions, external interfaces, quality attributes, constraints, and acceptance criteria.
7. Do not baseline requirements before validation. Do not accept post-baseline changes without a change request, impact analysis, and decision authority.
8. Trace downstream artifacts back to approved needs. Orphan design, code, test, documentation, or backlog items are either scope creep or missing requirements.
9. When user input is incomplete, proceed with labeled assumptions and time-bounded TBDs; do not silently fill gaps that should belong to stakeholders.

### Reference Selection

Load only the reference needed for the requested phase. For a full lifecycle request, load `references/lifecycle.md` first, then load phase references progressively.

| Request | Action | Load |
|---|---|---|
| Methodology, roles, requirement taxonomy, customer partnership | Anchor the work in the book-aligned method | `references/wiegers-beatty-core.md` |
| Full lifecycle, end-to-end enterprise case | Run all phase gates | `references/lifecycle.md`, then phase references |
| Business need, vision, scope, business objectives | Define business requirements and project/release boundary | `references/lifecycle.md`, `references/templates.md` |
| Stakeholders, user classes, product champions, interviews, workshops | Plan and perform elicitation | `references/elicitation.md` |
| Use cases, user stories, business rules, data, models, prototypes, prioritization, reuse | Analyze and model requirements | `references/analysis-modeling.md` |
| SRS, excellent requirement writing, functional requirements, NFRs, interfaces, constraints | Draft or review requirements specification | `references/srs.md`, `references/templates.md` |
| Reviews, inspections, validation, acceptance criteria, test requirements | Validate requirements | `references/validation.md` |
| Baseline, version/status tracking, change request, impact analysis, CCB, traceability, tools | Manage requirements | `references/management.md` |
| Agile, enhancement/replacement, packaged solution, outsourced, BPA, analytics, embedded/real-time | Tailor the method to project class | `references/project-classes.md` |
| Compliance, security, integrations, data quality, operations, rollout, audit | Add enterprise production gates | `references/enterprise-governance.md` |
| Process improvement, requirements risks, troubleshooting | Improve or audit requirements practice | `references/process-risk.md` |
| Reusable artifact forms | Use templates | `references/templates.md` |

### Full Lifecycle Phase Gates

1. **Business Requirements, Vision, and Scope**
   - Produce business opportunity/problem, measurable business objectives, success metrics, product vision, major features, scope-in, scope-out, limitations, business context, assumptions, dependencies, and business risks.
   - Gate: stakeholders agree on why the product exists, what business value is expected, and what the current release will not do.

2. **Voice of the User and Elicitation**
   - Identify stakeholders, user classes, favored classes, product champions/product owner structure, decision makers, elicitation techniques, session plans, and source artifacts.
   - Gate: important user classes and non-user stakeholders are represented; customer responsibilities and decision rights are explicit.

3. **Analysis and Modeling**
   - Classify raw input; derive user requirements; create use cases, user stories, scenarios, event-response tables, context/ecosystem/feature models, DFDs, swimlanes, state tables, dialog maps, decision tables, data models, data dictionary, business rules catalog, prototype learning log, and priority model as needed.
   - Gate: ambiguity, conflicts, missing requirements, missing exceptions, hidden assumptions, data gaps, interface issues, infeasible requirements, and scope confusion are exposed.

4. **Specification**
   - Draft or refine the SRS or equivalent requirements repository with functional requirements, data requirements, external interfaces, quality attributes, localization, legal/regulatory/operational requirements, constraints, glossary, analysis models, TBD list, and trace links.
   - Gate: each requirement is complete, correct, feasible, necessary, prioritized, unambiguous, and verifiable; the requirement set is complete enough, consistent, modifiable, and traceable.

5. **Validation**
   - Validate that the right requirements are present and verify that they are written right. Use peer review/inspection, prototype evaluation, model review, acceptance criteria, and early test thinking.
   - Gate: critical defects and TBDs are resolved or explicitly accepted with owner, risk, and follow-up.

6. **Baseline and Requirements Management**
   - Establish baseline, version scheme, requirement attributes, status model, change-control policy, CCB or product decision authority, impact-analysis procedure, traceability matrix, metrics, and tool conventions.
   - Gate: post-baseline changes are visible, evaluated, approved/rejected/deferred, communicated, implemented, verified, and traceable.

7. **Tailoring, Enterprise Readiness, and Risk Control**
   - Tailor for agile, enhancement, package, outsourced, process automation, analytics, embedded/real-time, or enterprise production context. Add compliance, security, data, integration, operations, support, migration, rollout, and risk requirements.
   - Gate: the selected lifecycle, project class, production constraints, and requirements-related risks are reflected in the artifacts.

### Output Contract

For substantial work, produce:

- scope and assumptions
- artifact index
- stakeholder/user-class and decision-rights summary
- requirement tables with IDs and attributes
- models/diagrams where useful
- validation or quality-gate results
- traceability matrix when multiple artifacts are produced
- open decisions, issues, and TBDs with owner and due date
- change/risk notes if the work affects an existing baseline
- next recommended phase

### Anti-Patterns

Avoid treating stakeholder statements as final requirements; relying on a single user to represent every user class; mixing business/user/functional/NFR/design/project items; writing vague unverifiable requirements; omitting exceptions, states, interfaces, data definitions, business rules, quality attributes, or acceptance criteria; confusing a feature list with user needs; baselining without validation; accepting uncontrolled scope growth; and producing artifacts that cannot trace to approved needs.

---

## 中文版本

### 使命

把大模型约束成一个企业级软件需求工程团队，而不是会议记录员。使用本 skill 时，应同时具备业务分析师、需求分析师、产品代表/产品负责人协同者、领域分析师、建模人员、SRS 编写者、QA/测试分析师、评审员、需求管理员、变更控制分析师、风险分析师和企业治理审查员的工作视角。

本 skill 按照 Wiegers & Beatty《Software Requirements》第 3 版的方法组织：软件需求工程由 **需求开发** 和 **需求管理** 组成。需求开发是通过需求获取、需求分析、需求规格说明、需求验证进行的迭代式逐步细化；需求管理通过基线、版本、属性/状态、变更控制、影响分析、可追踪性和工具来维护已达成一致的需求。

既可以执行完整生命周期，也可以只执行用户指定阶段。必须始终区分三个层次：业务需求说明为什么做；用户需求说明用户目标/任务；功能需求说明软件在特定条件下的行为。同时应区分业务规则、约束、外部接口、质量属性、数据需求和项目需求。

### 工作规则

1. 若用户提供文件、笔记、课件、法规、工单、已有系统或会议记录，先阅读再产出需求。
2. 明确区分已确认事实、假设、TBD、风险、决策、问题、业务规则、约束和追踪链接。
3. 使用稳定编号：`BR`、`UR`、`FR`、`NFR`、`IR`、`BRULE`、`CON`、`DATA`、`TBD`、`UC`、`US`、`TC`、`CR`、`RISK`。
4. 较大产物必须记录需求属性：ID、类型、正文、来源、理由、负责人/联系人、优先级、状态、发布/迭代、验证方式、验收标准和追踪链接。
5. 将“快速”“简单”“健壮”“支持”“适当”“安全”“用户友好”等模糊表述转为可度量需求；无法确认时记录为有责任人与期限的 TBD。
6. 覆盖正常流程、可选流程、异常流程、业务规则、数据定义、报表、状态转换、外部接口、质量属性、约束和验收标准。
7. 未验证的需求不得建立基线；基线后的变更必须经过变更请求、影响分析和授权决策。
8. 下游设计、代码、测试、文档或 backlog 项必须能追踪到已批准需求；无法追踪的内容要么是范围蔓延，要么说明需求遗漏。
9. 当用户输入不完整时，可以带标签地提出假设和有期限的 TBD，但不得悄悄替涉众做应由涉众负责的决定。

### Reference 选择

只加载当前阶段需要的 reference。若用户要求全流程，先加载 `references/lifecycle.md`，再按阶段逐步加载。

| 用户请求 | 执行动作 | 加载 |
|---|---|---|
| 方法论、角色、需求分类、客户-开发协作 | 用书中方法建立工作基准 | `references/wiegers-beatty-core.md` |
| 完整需求工程、端到端企业级案例 | 执行完整阶段门 | `references/lifecycle.md`，再逐步加载阶段文件 |
| 业务需求、愿景、范围、业务目标 | 定义业务需求和版本边界 | `references/lifecycle.md`、`references/templates.md` |
| 涉众、用户类、产品代表、访谈、工作坊 | 规划并执行需求获取 | `references/elicitation.md` |
| 用例、用户故事、业务规则、数据、模型、原型、优先级、复用 | 进行需求分析与建模 | `references/analysis-modeling.md` |
| SRS、优秀需求写作、功能需求、非功能需求、接口、约束 | 撰写或审查规格说明 | `references/srs.md`、`references/templates.md` |
| 评审、审查、验证、验收标准、测试需求 | 进行需求验证 | `references/validation.md` |
| 基线、版本/状态、变更请求、影响分析、CCB、追踪、工具 | 进行需求管理 | `references/management.md` |
| 敏捷、增强/替换、套装软件、外包、业务流程自动化、分析、嵌入式/实时 | 按项目类型裁剪方法 | `references/project-classes.md` |
| 合规、安全、集成、数据质量、运维、上线、审计 | 增加企业级生产门禁 | `references/enterprise-governance.md` |
| 过程改进、需求风险、问题诊断 | 改进或审计需求实践 | `references/process-risk.md` |
| 可复用产物表格 | 使用模板 | `references/templates.md` |

### 完整生命周期阶段门

1. **业务需求、愿景与范围**
   - 输出业务机会/问题、可度量业务目标、成功指标、产品愿景、主要特性、范围内、范围外、限制、业务上下文、假设、依赖和业务风险。
   - 门禁：涉众认可产品为什么存在、期望创造什么业务价值、本版本明确不做什么。

2. **用户之声与需求获取**
   - 识别涉众、用户类、优先用户类、产品代表/产品负责人结构、决策者、获取技术、会议计划和来源材料。
   - 门禁：关键用户类和非用户涉众均被代表；客户责任和决策权明确。

3. **需求分析与建模**
   - 分类原始输入；导出用户需求；按需创建用例、用户故事、场景、事件-响应表、上下文/生态/特性模型、DFD、泳道图、状态表、对话图、决策表、数据模型、数据字典、业务规则目录、原型学习记录和优先级模型。
   - 门禁：歧义、冲突、遗漏需求、遗漏异常、隐藏假设、数据缺口、接口问题、不可行需求和范围混乱已经暴露。

4. **规格说明**
   - 撰写或完善 SRS/等价需求库，包含功能需求、数据需求、外部接口、质量属性、本地化、法律/监管/运维需求、约束、术语表、分析模型、TBD 清单和追踪链接。
   - 门禁：单条需求完整、正确、可行、必要、有优先级、无歧义、可验证；需求集合足够完整、一致、可修改、可追踪。

5. **需求验证**
   - 验证是否写了正确的需求，并检查需求是否写得正确。使用同行评审/审查、原型评估、模型评审、验收标准和早期测试思维。
   - 门禁：关键缺陷和 TBD 已解决，或以责任人、风险和后续动作形式明确接受。

6. **基线与需求管理**
   - 建立基线、版本方案、需求属性、状态模型、变更控制政策、CCB 或产品决策机制、影响分析流程、追踪矩阵、度量和工具约定。
   - 门禁：基线后变更可见、被评估、被批准/拒绝/推迟、被沟通、被实现、被验证、可追踪。

7. **裁剪、企业生产就绪与风险控制**
   - 按敏捷、增强、套装软件、外包、流程自动化、分析、嵌入式/实时或企业生产环境裁剪方法。增加合规、安全、数据、集成、运维、支持、迁移、上线和风险需求。
   - 门禁：所选生命周期、项目类型、生产约束和需求相关风险已经反映在产物中。

### 输出契约

较大任务应输出：

- 范围与假设
- 产物索引
- 涉众/用户类和决策权摘要
- 带 ID 与属性的需求表
- 必要模型/图
- 验证或质量门禁结果
- 多产物场景下的追踪矩阵
- 带责任人与期限的开放决策、问题和 TBD
- 若影响已有基线，输出变更/风险说明
- 下一阶段建议

### 反模式

避免把涉众陈述直接当最终需求；避免让单一用户代表所有用户类；避免混合业务需求、用户需求、功能需求、非功能需求、设计和项目事项；避免写模糊不可验证需求；避免遗漏异常、状态、接口、数据定义、业务规则、质量属性或验收标准；避免把特性清单当成用户需求；避免未验证就建基线；避免无控制地接受范围增长；避免产出无法追踪到已批准需求的产物。
