# SEVO - 产品需求规格说明书

Codex（OpenClaw ACP Agent）| 2026-04-19

---

## 目录

1. 产品愿景与定位
2. 目标用户画像
3. 编排入口与流程编排
4. 功能需求（8 阶段 + 3 个验收阶段 + 2 个门禁 + 5 个跨阶段机制 + 3 个生命周期操作 + 4 个平台能力）
5. 非功能需求
6. 概念架构
7. 与 Self-Evolving Harness 其他模块的边界
8. Wave 规划
9. 约束与假设

## 1. 产品愿景与定位

SEVO（Spec-Execute-Verify-Operate）是面向 vibe coding 用户的 Agent 研发流水线。它把需求定义、方案约束、实现执行、独立审计、回归验证、部署发布、清洁环境验收和交付留痕收拢到同一条可追溯流水线上，让 Agent 软件研发从“能生成代码”升级为“能稳定交付结果”。SEVO 服务的核心人群是把 AI 当研发主力的人：他们要的不是一次性生成，而是每次改动都能看清目标、边界、证据和责任。

SEVO 以 npm 包（`sevo`）形式分发，`npx sevo init` 一条命令完成环境初始化，零配置即可启动第一条研发流水线。SEVO 把 PM、UX、架构师、审计等角色的专业标准内置到流水线阶段中——单 Agent 用户也能产出 PM 质量的 spec，多 Agent 环境有专职角色则效果更好，但不是必须。

SEVO 运行在 OpenClaw 环境中。架构层面通过 Adapter 抽象层隔离对 OpenClaw 内部 API 的直接依赖，保持代码职责清晰和可测试性——这是代码质量约束，不是支持其他平台的产品承诺。

**终局思维：以终局用户体验为目标的全自动化开发。** SEVO 流水线的终点不是「代码能跑」「测试通过」「npm 发布成功」，而是「陌生用户装上就能用、5 分钟内感受到产品的核心价值」。这是 SEVO 区别于传统 CI/CD 和 AI Coding 工具的核心差异——传统工具优化开发者体验，SEVO 优化终局用户体验。

**目标驱动 PDCA 闭环：OKR→SMART→PDCA 融入现有流程。** SEVO 的运转不是线性流水线跑一遍就结束，而是围绕终局目标的持续收敛循环。OKR→SMART→PDCA 是目标管理的核心理念，它指导 SEVO 的每一次闭环，融入到现有阶段中：

- **Pipeline 创建时（OKR 介入）**：SEVO 主动引导用户澄清需求的终局目标——「做完后，一个从没见过这个产品的人，装上 5 分钟内应该能做到什么？」锁定为 endStateGoal，拆解为 Objective + Key Results。这是 pipeline 的北极星。
- **Spec 阶段（SMART 介入）**：每个 KR 转化为具体（Specific）、可度量（Measurable）、可达成（Achievable）、相关（Relevant）、有时限（Time-bound）的 FR。FR 天然带着「服务于哪个 KR → 哪个 O → 终局目标」的溯源链。
- **Implement → Review → Verify → Deploy（PDCA 的 Do + Check）**：现有阶段不变，但每个 gate 的评估锚点升级——从「这个阶段的产出合格吗」到「这个阶段的产出在向终局目标收敛吗」。
- **Post-Release Validation（PDCA 的 Check，目标级）**：不是查 FR 清单，是查 KR 达成了没有。差距分析的对象是终局目标，不是功能列表。
- **差距 > 0（PDCA 的 Act）**：分析哪个 KR 未达成，重新 SMART 拆解，进入下一轮 pipeline 循环。
- **差距 = 0**：所有 KR 达成，Objective 达成，终局目标达成，pipeline 关闭。

现有 18 个阶段一个不改。加的是 pipeline 级别的目标元数据（endStateGoal、OKR 树、KR 达成度）和循环判定逻辑（差距分析 → 决定是否再来一轮）。Post-Release Validation Gate 是这条闭环的强制执行点。

## 2. 目标用户画像

### 2.1 Solo Founder / 独立产品操盘者

- 用 Agent 推进产品、技能、自动化系统的研发。
- 关心交付速度，也关心返工成本和线上事故。
- 需要看到每一轮改动的目标、边界、验收标准和交付证据。
- 上手路径：`npm install -g sevo && npx sevo init && sevo project create my-app`，5 分钟内看到第一条 pipeline 的 Spec 阶段产出。

### 2.2 Agent 原生开发者

- 把 AI 作为主要编码和调试执行者。
- 需要一条能约束 Agent 的研发流程，减少“写完就算完”的假完成。
- 需要把 Spec、Contract、Implement、Review 串起来，避免需求和代码脱节。
- 上手路径：`npx sevo init` 自动发现已有 Agent 并分配角色，`sevo fr add <project> "需求描述"` 后 pipeline 自动推进，开发者只需响应阶段任务。

### 2.3 质量与架构把关者

- 负责审计需求、架构、代码质量和交付完整性。
- 需要独立视角和统一工件链路，快速判断是否通过、卡在哪里、缺什么。
- 需要把经验沉淀回系统，而不是散落在聊天记录里。
- 上手路径：`sevo status` 查看所有 pipeline 状态，门禁阶段自动派发审查任务，审查结论写入结构化工件。

### 2.4 OpenClaw 环境管理者

- 负责配置和管理 OpenClaw 环境中的 Agent 池、模型、通知渠道等基础设施。
- 需要 SEVO 的流程能力与具体 Agent/模型/通知实现解耦，便于按需替换执行器、审计器、发布渠道。
- 需要通过配置而非改代码来适配不同的 Agent 池规模和模型组合。
- 上手路径：`npm install sevo`，`npx sevo init` 自动发现 OpenClaw 环境配置，核心阶段语义开箱可用。

### 2.5 陌生用户首次使用旅程

一个从未见过 SEVO 的用户，完整的首次体验路径：

1. `npm install -g sevo` — 安装 SEVO。
2. `npx sevo init` — 自动检测 OpenClaw 环境、注册插件、发现 Agent 并分配角色。单 Agent 环境自动降级，所有角色由同一个 Agent 承担。
3. 重启 OpenClaw（如 `openclaw gateway restart`）使插件生效。
4. `sevo project create my-first-project --description "项目描述"` — 创建第一个 Project。
5. `sevo fr add my-first-project "实现用户登录功能"` — 添加第一条 FR，pipeline 自动创建并开始推进。
6. `sevo status` — 查看 pipeline 当前走到哪个阶段、卡在哪里、下一步是什么。

从步骤 1 到步骤 5 产出第一份 Spec，预计耗时不超过 5 分钟。

## 3. 编排入口与流程编排

SEVO 是所有涉及代码变更的任务的默认研发流程。任务进入 SEVO 后，系统根据任务复杂度自动选择最合适的流程路径——简单任务走最小闭环，复杂任务走完整流水线。区别在于流程路径的深度，不在于是否进入 SEVO。

### 3.1 编排范围

所有涉及代码变更的任务默认进入 SEVO 编排范围。以下条件决定流程路径的深度（Level 0/1/2+）：

- 从零新建模块或系统 → Level 2+。
- 涉及两个及以上域的边界变化 → Level 2+。
- 预估改动超过 500 行或 10 个文件 → Level 2+。
- 涉及数据模型变化 → Level 2+。
- 涉及治理规则、调度逻辑、质量门禁的变化 → Level 2+。
- 涉及发布目标或交付方式变化 → Level 1+。
- 单域中等改动 → Level 1。
- 微小改动（bug 修复、配置调整、小功能）→ Level 0。
- 用户明确要求走完整流程 → Level 2+。
- 已有项目的需求规格说明书需要改动（新增/修改/删除 FR 或 AC）→ Level 1+。

查询、聊天、配置调整等不涉及代码变更的任务不进入 SEVO。

**触发判断实现（双层策略）**：
- 主路径：LLM 语义判断。系统将任务描述提交给 LLM，由 LLM 判断任务是否命中上述条件、应归入哪个 Level，返回结构化判定结果（是否触发、Level、命中条件、判定理由）。


### 3.2 流程路径

SEVO 根据任务复杂度自动选择最短有效路径：

- **Level 0**：微小改动。直接进入 Implement，经过 Review、Smoke Test、Verify、Ledger 的最小闭环。
- **Level 1**：单域中等改动。从 Spec 开始，Contract 可简化，门禁不能省。涉及 Web/UI 的任务走 UX Interaction Design；涉及前后端复杂功能/数据模型变化/多模块协作的任务走 Architecture Design。
- **Level 2+**：新系统、跨域重构、大范围变更、治理层变更。走完整 8 阶段，执行两道门禁。涉及 Web/UI 的任务默认走 UX Interaction Design；涉及前后端复杂功能的任务默认走 Architecture Design。

### 3.3 路由输出与编排启动

任务进入 SEVO 后，系统产出路由结果，至少包含：

- 目标 Project（project-slug）。
- 任务级别（Level 0/1/2+）。
- 是否需要 UX Interaction Design（布尔值 + 判定理由）。
- 是否需要 Architecture Design（布尔值 + 判定理由）。
- 必经阶段清单。
- 可跳过阶段及跳过理由。
- 当前轮次的验收重点。
- 需要追踪的核心工件。

路由结果直接驱动 PipelineEngine（FR-13）创建阶段执行队列并开始自动推进。PipelineEngine 通过状态机驱动 + OpenClaw Adapter 触发阶段执行，不需要人工干预。

### 3.4 验收标准

- AC-3.1：相同输入任务在同一套规则下得到稳定一致的路由结果。
- AC-3.2：每个进入 SEVO 的任务都有清晰的阶段清单和跳过理由。
- AC-3.3：任何被跳过的阶段都不影响最终交付可追溯性。
- AC-3.4：路由结果直接驱动 PipelineEngine 创建阶段执行队列，不需要人工重新解释。
- AC-3.5：每个 FR 流程实例有唯一 ID，所有阶段工件可通过实例 ID 关联。
- AC-3.6：多个 Project 的 FR 流程实例并行运行时，工件目录互不干扰。
- AC-3.7：FR 流程实例状态变化可追溯，任一时刻能回答“这条 FR 的 SDD 流程走到哪了”。
- AC-3.8：pipeline 创建后，PipelineEngine 在无人工干预的情况下自动推进到第一个阶段并开始执行。

### 3.5 FR 流程实例

FR 流程实例是一次完整的 SDD 流程执行。每当用户把一条 FR 添加到某个 Project，且该 FR 命中触发条件（§3.1）并完成路由判定后，系统创建一个 FR 流程实例，绑定到目标 Project，分配唯一 ID。这里的生命周期起点需要钉死：Project 由用户创建，最小输入是名称和描述；FR 由用户添加到 Project 中，最小输入是需求描述；FR 一旦创建成功，就自动进入 Specify 阶段对应的流程准备态，并据此生成或挂接到一个 FR 流程实例。

核心属性：

- **实例 ID**：全局唯一标识，格式 `fr-<project-slug>-<yyyyMMdd>-<seq>`，如 `fr-sevo-20260420-001`。
- **Project 绑定**：每个实例归属一个 Project，实例的全部工件存放在该 Project 的目录空间内。
- **路由结果**：实例创建时确定的任务级别、必经阶段、跳过阶段。
- **当前阶段**：实例正在执行的 SDD 流程阶段。
- **工件索引**：各阶段产出工件的引用列表。

状态模型：

- **created**：实例已创建，Project 目录已初始化，尚未进入第一个阶段。
- **active**：至少一个阶段处于 active 或 blocked 状态。
- **paused**：用户或系统主动挂起，所有阶段暂停推进。
- **completed**：最终阶段（Ledger）通过，交付闭环。
- **failed**：流程因不可恢复的原因终止。

状态流转：

- created → active：第一个阶段开始执行。
- active → paused：用户主动挂起或系统检测到阻断条件。
- paused → active：恢复执行。
- active → completed：Ledger 阶段通过。
- active → failed：不可恢复的失败（如用户取消、关键依赖永久不可用）。

生命周期：

1. 任务命中触发条件，路由判定完成。
2. 创建 FR 流程实例，绑定 Project，初始化目录结构。
3. 按路由结果依次推进各阶段，每个阶段的工件归档到实例目录。
4. Ledger 阶段完成后，实例状态变为 completed，交付账本条目记录实例 ID。

并行规则：

- 同一 Project 同一时刻只允许一个 active 的 FR 流程实例。前一个实例必须 completed 或 failed 后，才能创建新实例。
- 不同 Project 的 FR 流程实例完全独立，可并行运行。

### 3.6 Project 与标准目录结构

Project 是 SEVO 管理的独立交付单元。每个 Project 拥有自己的目录空间，所有 FR 流程实例的工件在该空间内按阶段归档。

标准目录结构：

```
<workspace>/projects/<project-slug>/
├── docs/                              # 过程文档
│   ├── product-requirements.md        # 需求规格
│   ├── architecture/                  # 架构文档
│   │   ├── arc42-architecture.md      # 主架构文档
│   │   └── decisions/                 # ADR（架构决策记录）
│   ├── ux/                            # UX 交互设计文档
│   └── test-cases/                    # 测试用例文档
├── src/                               # 源代码
├── tests/                             # 测试代码
├── skill/                             # Skill 定义（如有）
├── reports/                           # 评审报告、审计报告
├── artifacts/                         # 阶段产出工件（构建产物、发布包）
├── README.md
├── LICENSE
├── package.json
└── tsconfig.json
```

目录职责：

- `docs/`：过程文档。需求规格、架构设计、ADR、测试用例——描述“要做什么”和“怎么设计”。
- `src/`：源代码。实现产物——“做出来的东西”。
- `tests/`：测试代码。自动化测试——“怎么证明做对了”。
- `skill/`：Skill 定义文件。如果 Project 产出的是 Skill，定义文件放这里。
- `reports/`：质量证据。评审报告、审计报告、回归报告——“谁检查过、结论是什么”。
- `artifacts/`：阶段产出工件。构建产物、发布包、部署制品——“最终交付物”。

分类：

- 过程文档：`docs/`（描述意图和设计）。
- 结果代码：`src/`（实现产物）。
- 质量证据：`tests/` + `reports/`（验证和审计记录）。
- 交付物：`artifacts/`（可发布的最终产物）。

初始化规则：

- FR 流程实例创建时（FR-12），系统自动检查 Project 目录结构是否存在。
- 目录不存在时，按标准结构创建全部目录和占位文件。
- 目录已存在时，只补全缺失的子目录，不覆盖已有内容。

## 4. 功能需求（8 阶段 + 3 个验收阶段 + 3 个门禁 + 5 个跨阶段机制 + 3 个生命周期操作 + 4 个平台能力）

### FR-01 Spec

- **输入**：用户目标、业务背景、已有约束、历史参考材料。
- **处理**：明确问题、目标用户、范围、FR、NFR、概念架构和验收标准。Spec 产出阶段必须先完成四个用户层独立章节（用户人群、痛点、原始需求、用户体验流），再展开功能需求；缺任一章不得进入 Spec Review Gate。
- **输出**：需求规格包（Spec Package）。
- **执行阶段**：Spec。
- **审查阶段**：Spec Review Gate（独立评审）。
- **验收标准**：
  - AC-4.1：规格书能说清做什么、给谁做、做到什么程度算完成。
  - AC-4.2：每个核心功能都有验收标准。
  - AC-4.3：概念架构覆盖对象类型、状态流转和阶段间数据流。
  - AC-4.4：规格书不写具体技术选型和实现细节。
  - AC-4.4a：Spec 产出时必须先写四个用户层独立章节（用户人群、痛点、原始需求、用户体验流），且必须位于「功能需求」章节之前。任一章节缺失或仅有空标题，本 FR 视为未完成，禁止流转到 Spec Review Gate。
  - AC-4.4b：四个用户层章节必须有实质内容——用户人群描述具体到使用人群、典型场景、设备形态；痛点描述用户当前如何解决该问题、卡点在哪；原始需求用用户口语描述要什么；用户体验流给出从入口到产出的完整操作步骤。占位符、TODO、单句概述均判定为未完成。
  - AC-4.4c：FR 章节中的每个 FR 必须能追溯到上述四章中至少一条用户人群、痛点或体验流条目；找不到追溯关系的 FR 视为伪需求，由 PM 删除或回到四章补齐再产 FR。

### FR-02-pre Mandatory Spec Sections Pre-Gate

- **输入**：需求规格包（Spec Package）的 markdown 源文件。
- **处理**：Spec Review Gate（FR-02）启动前的硬前置子门禁。先于其他评审维度执行，以两步检查校验四个用户层独立章节：
  1. 存在性扫描：依据 markdown H2 结构定位四章——用户人群、痛点、原始需求、用户体验流。任一章缺失或仅为空标题（章节正文为空、TODO、占位符），直接判定不通过。
  2. 内容质量语义判定：对存在的章节调用 LLM 进行语义判定，检查内容是否回答了该章节应回答的问题（例如「用户人群」是否描述了具体使用人群和场景；「痛点」是否描述了用户当前的解决方式与卡点）。禁止用关键词匹配或正则伪装语义理解，正则仅作为章节定位辅助。
- **输出**：Spec Sections Pre-Gate 检查报告，包含每章存在性、章节起止行号、语义判定结论（pass/fail）、不通过项的具体缺口描述。
- **执行阶段**：Spec Review Gate 之前的硬前置子门禁。本子门禁不通过则 spec-review-gate 立即返工到 Spec 阶段（FR-01），不允许并行执行产品/技术/质量/体验四维评审，避免并行 Agent 浪费资源。
- **门禁判定**：四章存在 + 顺序正确 + 内容语义合格三项全通过才放行；任一项不通过即阻断 Spec Review Gate 主体维度评审。
- **验收标准**：
  - AC-4.4d：spec-review-gate 收到 spec 时，第一步必须执行 Mandatory Spec Sections Pre-Gate；该子门禁未通过前，禁止启动产品/技术/质量/体验四维度评审。
  - AC-4.4e：四章存在性扫描以 markdown H2 章节为粒度。章节标题语义可接受同义表达（如「目标用户」「用户画像」可对应「用户人群」），同义判定必须由 LLM 给出，不得仅靠静态关键词列表。
  - AC-4.4f：四章内容质量必须由 LLM 语义判定。每章产出 pass/fail + 一句话理由，理由必须指向章节具体行号或文本片段。仅靠章节字数阈值或关键词命中判定为不合规检查。
  - AC-4.4g：任一章存在性、顺序或语义判定不通过，Pre-Gate 直接返工到 FR-01 Spec 阶段，并产出明确缺口清单（缺哪章 / 哪章顺序错 / 哪章语义不达标 + 缺口描述）。返工后必须重新跑完整 Pre-Gate，不允许只复查不通过项。
  - AC-4.4h：Pre-Gate 报告作为 Spec Review Bundle 的强制前置工件留档，供后续阶段追溯；FR-02 Spec Review Gate 必须在评审包顶部引用 Pre-Gate 结论。
  - AC-4.4i：Pre-Gate 不允许由 spec 作者自审，至少由独立 Agent 调用 LLM 完成判定，与 FR-02 主体评审遵守同一禁止自审原则。
  - AC-4.4j：Mandatory Spec Sections Pre-Gate 适用对象覆盖所有 SEVO 受管项目（按 FR-14 受管项目发现规则确定，包括 aco、claw-design、exam-sprint、kivo、sevo 及未来通过 `projects/*/sevo.json` 自动纳管的新项目）的产品需求规格主文件 `docs/product-requirements.md`，不仅作用于流水线运行期产出的增量 Spec Package。检查规则：
    1. **章节齐全**：H2 级别必须独立存在四章——用户人群（谁用、什么场景、什么设备）、痛点（用户现在怎么解决、哪里痛）、原始需求（用户要什么，用人话说）、用户体验流（完整的用户操作步骤，从打开到完成）。同义表达（如「目标用户」「用户画像」对应「用户人群」）由 LLM 语义判定接受，禁止用静态关键词列表枚举允许的标题。
    2. **顺序正确**：四章必须出现在「功能需求」H2 章节之前。任一章节出现在功能需求之后，或散落于 FR 内部，判定不通过。
    3. **内容有实质**：每章正文必须由 LLM 做语义判定，回答该章应回答的问题；空标题、单句概述、TODO、占位符判定不通过。
    检查规则强制使用 LLM 语义判定，禁止用关键词匹配、字数阈值或正则伪装语义理解；正则仅作为 H2 章节定位辅助。任一项不通过则受管项目 spec-review-gate 立即打回，禁止进入产品/技术/质量/体验任一维度评审，禁止进入下一阶段（Contract、Implement 等）；返工修复后必须重新跑完整 Pre-Gate。本 AC 同样适用于 SEVO 自身的 `projects/sevo/docs/product-requirements.md`，SEVO 不豁免自身。
  - AC-4.4k：spec-review-gate 启动时，必须先按 AC-4.4j 检查项目当前的 `docs/product-requirements.md` 主文件四章合规性。主文件不合规时，无论本轮提交的是新增 FR、迭代修订还是局部优化，一律先打回补齐主文件四章，不允许「先评审本轮增量、之后再补齐主文件」。
  - AC-4.4l（用户视角端到端可验证准则）：spec 中每条 FR 必须包含一个「用户视角验证准则」子节（在 FR 定义中以明确小节出现，如「验证准则」或「用户视角验证」），内容必须明确以下三要素：
    1. **操作者**：谁来验证（默认「陌生用户」，可根据 FR 场景明确为「首次使用者」「运维者」等）。
    2. **操作路径与时间约束**：在什么入口（web 页面路由、CLI 命令）做什么操作，多长时间内完成。
    3. **可观测产出**：看到什么具体、可验证、可数的内容作为「FR 通过」的依据，产出必须可量化（数量、字数、字段、状态之一）。“页面能打开”、“列表能显示”、“接口能访问”不构成可观测产出。
    反例（页面级描述，不过关）：「FR-X 支持显示知识列表」、「FR-X 提供项目详情页」。
    正例（用户视角终态，过关）：「陌生用户上传 PDF 后，5 分钟内在 web 端能看到至少 3 个结构化知识点，每个知识点有标题（≤ 20 字）+ 描述（≥ 50 字）+ 来源 PDF 文件名」。
  - AC-4.4m（验证准则语义判定）：FR-02-pre Pre-Gate 除检查四章外，必须额外对每条 FR 的「用户视角验证准则」做 LLM 语义判定，区分「页面级描述」与「用户视角端到端」。判定依据：是否包含明确操作者、是否包含可补充的操作路径与时间约束、是否包含可量化产出。任一要素缺失 = 页面级描述 = 未通过。禁止用关键词匹配、字数阈值、正则伪装语义理解；正则仅作为定位辅助。
  - AC-4.4n（FR 验证准则不合规的处理）：任一 FR 缺失「用户视角验证准则」子节或 LLM 判定为页面级描述时，Pre-Gate 不通过，打回 FR-01 Spec 阶段。返工产出不合规 FR 缺口清单（FR 编号 + 缺失要素 + 需补充的验证准则示例）。由 PM 角色补全验证准则后重新进入 Pre-Gate。本 AC 适用于所有受管项目主文件与 SEVO 自身主文件。
  - AC-4.4o（过渡期处理）：AC-4.4l/m/n 生效后，现有 spec 中未补全「用户视角验证准则」的 FR 登记到§9.8「待补 spec 章节（已知违反清单）」类似表格中，由后续 wave 补齐；代码实现阶段允许补齐与实现并行，但在 FR-36 Verify-With-Real-Data Gate 中涉及的受检核心 FR 必须已补齐验证准则，否则 FR-36 门禁不通过。

### FR-02 Spec Review Gate

- **输入**：需求规格包（Spec Package）、FR-02-pre 通过的 Pre-Gate 报告、路由结果、适用规则。
- **处理**：先消费 FR-02-pre 输出的 Mandatory Spec Sections Pre-Gate 报告作为前置门禁结果；Pre-Gate 通过后再由多维度独立评审检查规格质量，并给出通过、有条件通过、不通过三档结论。评审维度：
  - 产品维度：spec 是否解决了用户真正的问题、需求是否完整、用户人群和痛点是否清晰。
  - 技术维度：spec 描述的功能是否技术可行、是否存在技术风险或不可实现的描述。
  - 体验维度（有 Web/UI 时）：spec 描述的交互是否合理、用户体验流是否完整、是否符合小白用户预期。纯后端/CLI 项目可省略。
  - 质量维度：规格完整性、阶段隔离、概念架构完整度、边界清晰度、验收标准质量。
- **输出**：规格评审包（Spec Review Bundle），顶部引用 Pre-Gate 结论，包含各维度结论、问题清单、修复要求、通过条件和是否允许进入 Contract 的门禁结果。
- **执行阶段**：Spec Review Gate。先执行 FR-02-pre Mandatory Spec Sections Pre-Gate；Pre-Gate 通过后，再并行执行产品维度、技术维度、体验维度（可选）、质量维度评审。禁止规格作者自审。
- **门禁判定**：Pre-Gate 通过 + 各维度共同放行。Pre-Gate 任一项不通过直接返工 FR-01；Pre-Gate 通过后任一维度结论为有条件通过或不通过时阻断，直到修复并复审通过。纯后端/CLI 项目可按项目配置省略体验维度。
- **验收标准**：
  - AC-4.5：Spec 进入 Contract 前必须先经过独立评审，默认禁止规格作者自审。
  - AC-4.5a：Spec Review Gate 至少覆盖产品、技术、质量三个维度；涉及 Web/UI 的任务必须增加体验维度。
  - AC-4.5b：任一维度结论为有条件通过或不通过时，门禁阻断，直到对应维度问题修复并复审通过。
  - AC-4.6：评审结果至少区分通过、有条件通过、不通过三档，并显式记录阻断问题。
  - AC-4.7：有条件通过和不通过都会阻断进入 Contract，直到阻断问题完成修复并复审通过。
  - AC-4.8：评审结论必须指向具体规格内容、缺口或越界点，不能只给抽象评价。
  - AC-4.9：Spec 必须包含四个独立章节，缺任一个即判定为“不通过”：
    1. 用户人群（谁用、什么场景、什么设备）
    2. 痛点（用户现在怎么解决这个问题、哪里痛）
    3. 原始需求（用户要什么，用人话说）
    4. 用户体验流（完整的用户操作步骤，从打开到完成）
  - AC-4.9a：四章节必须位于「功能需求」之前，不得散落在 FR 内部或附录中。
  - AC-4.9b：四章存在性、顺序、内容语义判定三项检查由 FR-02-pre Mandatory Spec Sections Pre-Gate 执行；本门禁必须在评审包顶部引用 Pre-Gate 报告，并以 Pre-Gate 通过作为本门禁启动主体评审的强制前提。
  - AC-4.9c：四章内容必须由 LLM 做语义质量判定，禁止用关键词匹配或字数阈值伪装语义理解。语义判定的最低标准：用户人群说清「谁、什么场景、什么设备」；痛点说清「现在怎么解决、哪里痛」；原始需求用用户口语写明「要什么」；用户体验流写明「从入口到产出的完整步骤」。任一章语义不达标判定为「不通过」。
  - AC-4.9d：Pre-Gate 任一项不通过时，spec-review-gate 直接返工 FR-01，不得进入产品/技术/质量/体验任一维度评审，避免无效消耗 Agent 资源。返工修复后必须重新跑完整 Pre-Gate + 主体评审。
  - AC-4.9e：FR 章节中的每个 FR 必须能在四章中找到至少一条来源（用户人群、痛点或体验流条目）。找不到来源的 FR，spec-review-gate 产品维度直接判定为「不通过」并标注「孤立 FR」。

### FR-02a Test Case Authoring

- **触发时机**：Spec Review Gate（FR-02）通过后，与 Contract（FR-03）并行启动。
- **输入**：已通过 Spec Review Gate 的需求规格包。
- **处理**：基于需求规格中的验收标准（AC）编写测试用例，产出独立的测试用例文档。
- **输出**：测试用例文档（独立交付物）。
- **执行阶段**：Test Case Authoring。
- **并行关系**：与 FR-03 Contract 并行执行，不互相阻塞。
- **验收标准**：
  - AC-4.8a：每个高优先级 FR 的验收标准至少有一条对应测试用例。
  - AC-4.8b：测试用例作为独立文档交付，不写入需求规格或契约包。
  - AC-4.8c：初期允许极简形态，后期可专项优化扩展。

### FR-02b UX Acceptance Authoring

- **触发时机**：Spec Review Gate（FR-02）通过后，与 Contract（FR-03）、Test Case Authoring（FR-02a）并行启动。
- **输入**：已通过 Spec Review Gate 的需求规格包。
- **处理**：由 UX 角色（ux-01）编写「用户开箱即用视角」评测用例——模拟陌生用户首次使用的完整旅程，产出 markdown 检查清单（非代码测试）。
- **输出**：UX 开箱即用评测检查清单（独立交付物，存放于项目 docs/ 下）。
- **执行阶段**：UX Acceptance Authoring。
- **角色约束**：仅 UX 角色可执行，禁止开发者或产品角色代写。
- **并行关系**：与 FR-02a Test Case Authoring、FR-03 Contract 并行执行，不互相阻塞。
- **验收标准**：
  - AC-4.8d：检查清单覆盖零配置安装、首次运行、核心功能体验、错误提示友好度、文档可读性五个维度。
  - AC-4.8e：检查清单作为独立 markdown 文档交付，不写入需求规格或契约包。
  - AC-4.8f：检查清单中每个检查项有明确的通过/失败判定标准。
  - AC-4.8g：产出工件记录 authorRole 为 ux，可追溯到执行角色。

### FR-02c Commercial Acceptance Authoring

- **触发时机**：Spec Review Gate（FR-02）通过后，与 Contract（FR-03）、Test Case Authoring（FR-02a）、UX Acceptance Authoring（FR-02b）并行启动。
- **输入**：已通过 Spec Review Gate 的需求规格包。
- **处理**：由 PM 角色（pm-01）编写「商用视角」评测用例——验证商用就绪标准，产出 markdown 检查清单（非代码测试）。
- **输出**：商用评测检查清单（独立交付物，存放于项目 docs/ 下）。
- **执行阶段**：Commercial Acceptance Authoring。
- **角色约束**：仅 Product 角色可执行，禁止开发者或 UX 角色代写。
- **并行关系**：与 FR-02a、FR-02b、FR-03 并行执行，不互相阻塞。
- **验收标准**：
  - AC-4.8h：检查清单覆盖 npm 包完整性、README 营销质量、依赖安全、许可证合规、发布三平台覆盖、版本号一致性六个维度。
  - AC-4.8i：检查清单作为独立 markdown 文档交付，不写入需求规格或契约包。
  - AC-4.8j：检查清单中每个检查项有明确的通过/失败判定标准。
  - AC-4.8k：产出工件记录 authorRole 为 product，可追溯到执行角色。

### FR-02d UX Interaction Design

- **触发条件**：任务涉及 Web 页面、用户交互界面、导航结构变更时触发；纯后端/CLI/SDK 不触发。由路由阶段自动判定。
- **触发时机**：Spec Review Gate（FR-02）通过后，与 Contract（FR-03）、Test Case Authoring（FR-02a）、UX Acceptance Authoring（FR-02b）、Commercial Acceptance Authoring（FR-02c）并行启动。
- **输入**：已通过 Spec Review Gate 的需求规格包。
- **处理**：由 UX 角色站在小白用户视角设计页面交互方案——页面布局、导航结构、操作流程、状态流转、信息层级。
- **输出**：UX 交互设计文档（存放于项目 docs/ux/ 下）。
- **执行阶段**：UX Interaction Design。
- **角色约束**：仅 UX 角色可执行，禁止开发者或产品角色代执行。
- **并行关系**：与 FR-02a、FR-02b、FR-02c、FR-03、FR-02e 并行执行，不互相阻塞。
- **完成后流向**：UX 交互设计完成后，由 PM 角色评审设计方案（评审维度：设计是否解决了 spec 定义的用户问题、操作流程是否完整、是否遗漏关键场景）。PM 评审通过后，UX 设计文档作为 Contract Review Gate（FR-04）和 Implement（FR-05）的输入。
- **验收标准**：
  - AC-4.8l：路由阶段自动判断任务是否涉及 Web/UI，产出“是否需要 UX Interaction Design”布尔值。
  - AC-4.8m：设计必须从小白用户视角出发，覆盖完整操作流程（从打开页面到完成核心任务）。
  - AC-4.8n：UX 设计文档是 Implement（FR-05）的强制输入，编码 prompt 必须引用该文档路径。
  - AC-4.8o：与其他并行阶段不阻塞，完成后经 PM 评审通过后进入 Contract Review Gate。
  - AC-4.8p：产出工件记录 authorRole 为 ux，可追溯到执行角色。
  - AC-4.8p2：UX 交互设计完成后必须经过 PM 角色评审，PM 评审不通过则打回 UX 角色修改，修改后重新提交 PM 评审。

### FR-02e Architecture Design

- **触发条件**：任务涉及前后端复杂功能、数据模型变化、多模块协作、新增 API 接口时触发；单文件小改动不触发。由路由阶段自动判定。
- **触发时机**：Spec Review Gate（FR-02）通过后，与 Contract（FR-03）、Test Case Authoring（FR-02a）、UX Interaction Design（FR-02d）并行启动。
- **输入**：已通过 Spec Review Gate 的需求规格包 + UX 交互设计文档（如有，作为参考）。
- **处理**：由 SA 角色产出技术架构设计——API 接口定义、数据模型、模块交互、前后端职责划分。
- **输出**：架构详设文档（存放于项目 docs/architecture/ 下）。
- **执行阶段**：Architecture Design。
- **角色约束**：仅 SA 角色可执行，禁止开发者或产品角色代执行。
- **并行关系**：与 FR-02a、FR-02b、FR-02c、FR-03、FR-02d 并行执行，不互相阻塞。如果同时有 UX Interaction Design，应参考 UX 设计文档。
- **完成后流向**：产出的架构详设文档作为 Contract Review Gate（FR-04）的输入之一。
- **验收标准**：
  - AC-4.8q：路由阶段自动判断任务是否涉及复杂功能/数据模型变化/多模块协作，产出“是否需要 Architecture Design”布尔值。
  - AC-4.8r：必须定义清晰的 API 接口（路径、方法、请求/响应结构、错误码）。
  - AC-4.8s：架构设计文档是 Implement（FR-05）的强制输入，编码 prompt 必须引用该文档路径。
  - AC-4.8t：如果同时有 UX Interaction Design，架构设计应参考 UX 设计文档中的页面结构和交互流程。
  - AC-4.8u：产出工件记录 authorRole 为 sa，可追溯到执行角色。

### FR-03 Contract

- **输入**：已通过 Spec Review Gate 的需求规格包。
- **处理**：把需求翻译为可执行的架构方案、实现边界、阶段门禁、工作包拆分和交付顺序。
- **输出**：契约包（Contract Package），包含架构方案、实现边界、工作包拆分（含 Task 级细粒度分解）和交付顺序。
- **执行阶段**：Contract。
- **审查阶段**：Contract Review Gate（四方会审）。
- **验收标准**：
  - AC-4.9：每个高优先级 FR 都能在契约中找到对应实现承接点。
  - AC-4.10：工作包拆分后可分派、可验收、可追责。
  - AC-4.11：关键边界、风险和依赖被显式记录。
  - AC-4.12：契约包能直接驱动 Implement，不需要口头补规则。
  - AC-4.12a：每个工作包内部拆分为 Task 列表，每个 Task 粒度控制在 2-5 分钟，包含精确文件路径和预期变更描述。

### FR-04 Contract Review Gate

- **输入**：契约包（Contract Package）、关键架构决策、评审规则、UX 交互设计文档（如有 FR-02d 产出）、架构详设文档（如有 FR-02e 产出）。
- **处理**：由产品视角、开发视角、质量视角、体验视角四方并行会审，检查需求承接完整度、实现可行性、决策严谨性、交互合理性、扩展边界和交付波次，并形成是否允许进入 Implement 的门禁结论。体验视角需核对契约与 UX 交互设计文档的一致性；开发视角需核对契约与架构详设文档的一致性。纯后端/CLI 项目可按项目配置省略 UX 视角，此时退化为三方会审。
- **输出**：会审包（Contract Review Bundle），包含四方评审结论、阻断问题、修复要求、复审范围和是否允许进入 Implement 的门禁结果。
- **执行阶段**：Contract Review Gate，四方并行评审——产品维度（需求承接完整度）、开发维度（实现可行性）、质量维度（决策严谨性与质量规范）、体验维度（交互合理性、用户流程完整性、可用性）。
- **门禁判定**：四方共同放行。任一方结论为有条件通过或不通过时阻断，谁的问题未过审由谁继续复审，四方全部通过后方可进入 Implement。
- **验收标准**：
  - AC-4.13：进入 Implement 前必须完成四方并行会审，缺任一评审视角都不能放行。纯后端/CLI 项目可配置省略体验视角，此时退化为三方会审。
  - AC-4.14：四方评审至少覆盖产品完整度、开发可行性、质量严谨性和交互体验四个视角。
  - AC-4.15：任一评审结论为有条件通过或不通过时，Implement 必须被阻断，直到对应问题修复并复审通过。
  - AC-4.16：会审产出必须明确记录每个问题对应的责任工件、修复项和复审责任方。
  - AC-4.17：项目配置中 hasUI=false 时，体验视角可省略，退化为三方会审。

### FR-05 Implement

- **输入**：契约包、工作包、阶段规则、验收标准、UX 交互设计文档（如有 FR-02d 产出，强制引用）、架构详设文档（如有 FR-02e 产出，强制引用）。
- **处理**：按工作包逐 Task 执行实现，遵循 TDD 循环（先写覆盖目标行为的失败测试 → 实现至测试通过 → 重构），限制改动边界，记录证据，形成可审计的变更集。编码 prompt 必须引用 UX 交互设计文档和架构详设文档的路径（如有），确保实现与设计一致。
- **输出**：实现包（Implementation Bundle），包含代码变更、执行记录、测试结果和偏差说明。
- **执行阶段**：Implement。
- **审查阶段**：Review（独立审查）。
- **验收标准**：
  - AC-4.17：每个工作包都有明确输入、输出、允许改动范围和验收项。
  - AC-4.18：实现过程产出证据，不允许只交代码不交说明。
  - AC-4.19：完成判定以验收结果为准，不以 Agent 自报完成为准。
  - AC-4.20：实现结果能追溯到对应 FR 和 Contract 决策。
  - AC-4.20a：每个工作包的实现遵循 TDD 循环：先写覆盖目标行为的失败测试，再写实现使测试通过，最后重构。
  - AC-4.20b：未经测试覆盖的代码变更不允许通过 Review 阶段。
  - AC-4.20f：编码 Agent 只能实现 spec 中明确定义的 FR 和 AC。觉得某功能有价值，必须先提需求变更请求，经 Specify 阶段评审写入 spec 后才能实现。
  - AC-4.20g：当存在 FR-02d 产出的 UX 交互设计文档时，编码 prompt 必须引用该文档路径，实现必须符合 UX 设计方案中定义的页面布局、导航结构和操作流程。
  - AC-4.20h：当存在 FR-02e 产出的架构详设文档时，编码 prompt 必须引用该文档路径，实现必须符合架构设计中定义的 API 接口、数据模型和模块职责划分。

### FR-05a Systematic Debugging

- **触发时机**：Implement（FR-05）执行过程中或完成后发现非预期行为时触发，作为 Implement 和 Review 之间的可选活动。
- **输入**：实现包（或部分实现结果）、失败测试、异常日志、非预期行为描述。
- **处理**：按四阶段框架执行系统化调试——复现（在可控条件下稳定重现问题）→ 定位（缩小问题范围至具体模块或代码路径）→ 分析（确定根因，排除表面症状）→ 验证（修复后确认问题消除且未引入新问题）。
- **输出**：调试记录（Debugging Record），包含问题描述、根因分析、修复方案和验证结果。
- **执行阶段**：Systematic Debugging（Implement 内部可选活动）。
- **验收标准**：
  - AC-4.20c：调试过程遵循复现→定位→分析→验证四阶段，禁止跳过复现直接猜测修复。
  - AC-4.20d：调试结论基于证据（日志、测试结果、代码路径分析），不基于主观推测。
  - AC-4.20e：修复后的验证必须覆盖原始失败场景和相关回归路径。

### FR-06 Review

- **输入**：实现包。审计时参考 FR-02a 产出的测试用例文档（仅做参考，不代表全部审计项）、UX 交互设计文档（如有 FR-02d 产出）、架构详设文档（如有 FR-02e 产出）。
- **处理**：由独立审查阶段三方并行评审，审查代码质量、需求一致性、架构符合度、边界遵守情况和高风险点。
- **输出**：评审包（Review Bundle），包含各维度结论、问题清单、修复要求和通过条件。
- **执行阶段**：Review，三方独立评审：
  - PM/产品维度：功能完整性、需求一致性确认。
  - 质量维度：代码质量、安全性、规范遵守。
  - SA/架构维度：实现是否符合架构详设文档（如有 FR-02e 产出），API 接口是否按设计实现，数据模型是否一致。无架构详设文档的任务，架构维度自动跳过。
- **门禁判定**：三方共同放行。任一方结论为有条件通过或不通过时阻断，直到对应问题修复并复审通过。
- **体验验收说明**：用户体验的验收由独立的 UX Acceptance 阶段（FR-06c）负责，不在 Code Review 中重复覆盖。
- **验收标准**：
  - AC-4.21：评审者与实现者职责分离。
  - AC-4.22：评审结果至少区分通过、有条件通过、不通过。
  - AC-4.23：每个阻断问题都能指向具体工件和修复项。
  - AC-4.24：通过结论建立在证据上，不建立在主观判断上。
  - AC-4.24k：Review 阶段必须包含 spec-code 覆盖检查——从需求规格书提取全量 AC，逐条比对实现包中的代码覆盖情况，产出 AC 覆盖矩阵（AC 编号 / 覆盖状态 / 对应代码位置）。
  - AC-4.24l：AC 覆盖矩阵中任何 AC 状态为未实现或部分实现时，Review 结论必须为不通过（blocker）。代码实现只能比需求定义多，不能比需求定义少。
  - AC-4.24m：类型定义存在不等于已实现。AC 覆盖判定必须同时检查类型定义、逻辑代码和测试三层，缺任何一层视为部分实现。
  - AC-4.24n：ImplementationReviewGate 作为 Review 阶段的程序化门禁，自动从 Spec Package 提取 AC、从 Implementation Bundle 提取覆盖证据，覆盖率低于 100% 时门禁结论为 rejected。
  - AC-4.24n2：Review 阶段必须检查：代码中每个功能模块是否都能追溯到 spec 中的 FR/AC 编号。无法追溯的代码视为伪需求，必须删除或补充 spec 定义后才能通过 Review。
  - AC-4.24n3：AC 覆盖扫描范围必须包含项目全部源码目录（src/、web/、plugin/、scripts/ 等），不能只扫部分目录。扫描范围由项目配置中的 sourceRoots 字段定义，默认值为项目根目录下所有包含源码的子目录。Review 报告中必须列出实际扫描的目录清单，遗漏目录视为 Review 不通过。
  - AC-4.24n4：当存在 FR-02e 产出的架构详设文档时，SA/架构维度必须逐项核对 API 接口实现与设计文档的一致性（路径、方法、请求/响应结构），不一致则判定为不通过。
  - AC-4.24n5：无架构详设文档的任务，SA/架构维度自动跳过，不阻断 Review 流程。
  - AC-4.24n6：Implementation Bundle 中每个 execution 的 allowedScope 必须精确到 AC 级别（如 AC-4.1、AC-4.2），不允许只声明 FR ID（如 FR-01）。仅声明 FR ID 的覆盖判定为 partial，产出 blocker finding。
  - AC-4.24n7：ImplementationReviewGate 在执行覆盖检查时，必须自动触发 L2 语义扫描（l2-ac-semantic-scanner），逐条验证 spec AC 是否有对应实现代码且逻辑正确。禁止仅依赖 allowedScope 自我声明作为覆盖证据。
  - AC-4.24n8：Review 结果必须包含 AC 覆盖矩阵，每条 AC 的覆盖判定包含三层检查：类型定义（接口/类型声明存在）、逻辑代码（业务逻辑实现存在且语义匹配 AC 描述）、测试（对应测试用例存在且覆盖核心路径）。三层全部通过才判定为 covered，缺任何一层判定为 partial。
  - AC-4.24n9：Pipeline 在 Review 阶段通过后、进入 Verify 阶段前，自动触发 Tiered Scan（L1→L2→L3 级联扫描）。扫描由 PipelineEngine 自动编排，无需编排者手动触发。
  - AC-4.24n10：Tiered Scan 任一必需层未产出明确 pass 结论时，pipeline 阻断，不允许进入 Verify 阶段。阻断条件至少包括：L2 扫描结果中 spec-code 覆盖率低于 100%、L1/L2/L3 任一层执行失败、扫描报告缺失或扫描流程异常中断。阻断时产出未覆盖 AC 清单或失败原因和修复建议，触发 Review Fix Loop（FR-06a）。
  - AC-4.24n11：当 L2 语义扫描因 LLM 不可用、超时或重试耗尽，导致全部 AC 最终状态为 `needs-review` 且 `coveredCount = 0` 时，Tiered Scan 结论必须为 `needs-review`/`failed`，不得判定为 pass，更不得放行进入 Verify。

### FR-06a Review Fix Loop

- **触发时机**：Review（FR-06）或 Contract Review Gate（FR-04）产出评审包且结论为有条件通过或不通过时自动触发。
- **输入**：评审包（Review Bundle 或 Contract Review Bundle），包含问题清单。
- **处理**：
  1. 自动解析评审报告，提取结构化问题清单，每个问题标注严重级别（P0/P1/P2/P3）、关联的原始 FR、问题所在工件和修复建议。
  2. P0 和 P1 问题自动生成修复任务卡片（Fix Task），关联原 FR 流程实例、评审报告和问题条目。P2/P3 问题记录待办，不阻断当前批次。
  3. 修复任务按优先级排入待办队列（P0 优先于 P1），可被空闲 Agent 认领执行。
  4. 修复任务完成后，自动触发原评审维度对修复范围做定向复验（Targeted Revalidation），复验范围限定为修复涉及的工件和关联影响面，不重跑全量评审。
  5. 复验通过 → 对应问题关闭 → 系统重新评估门禁放行条件（所有 P0 关闭且 P1 关闭或豁免时放行）。复验不通过 → 问题状态回退，继续修复→复验循环。
  6. 全链路状态（评审报告 → 问题清单 → 修复任务状态 → 复验结果）在驾驶舱实时可见。
- **输出**：问题清单（Review Issue List）、修复任务卡片（Fix Task）、复验结论（Revalidation Result）。
- **执行阶段**：Review Fix Loop（Review 和 Contract Review Gate 的内置子流程）。
- **验收标准**：
  - AC-4.24a：评审结论为有条件通过或不通过时，系统在评审完成后自动解析报告并生成结构化问题清单，无需人工介入。
  - AC-4.24b：问题清单中每个条目包含严重级别（P0/P1/P2/P3）、关联 FR、问题工件定位和修复建议。
  - AC-4.24c：P0 和 P1 问题自动生成修复任务卡片，卡片关联原 FR 流程实例 ID 和评审报告引用。
  - AC-4.24d：修复任务按 P0 > P1 优先级排序进入待办队列，可被 Agent 认领执行。
  - AC-4.24e：修复任务完成后，系统自动触发原评审维度对修复范围做定向复验，复验范围不超出修复涉及的工件及其关联影响面。
  - AC-4.24f：复验通过时对应问题自动关闭；复验不通过时问题状态回退，修复→复验循环继续，直到通过或人工干预终止。
  - AC-4.24g：所有 P0 问题关闭且所有 P1 问题关闭或经人工豁免后，门禁自动重新评估并放行。
  - AC-4.24h：评审报告、问题清单、修复任务状态、复验结果的全链路状态在驾驶舱实时可见。
  - AC-4.24i：修复→复验循环有最大轮次上限（默认 3 轮），超限后升级为人工介入，防止无限循环。
  - AC-4.24j：P2/P3 问题记录为待办项，不阻断当前门禁放行，但纳入后续迭代的输入。

### FR-06b Smoke Test

- **触发时机**：Review（FR-06）通过后自动触发，在进入 Regression 之前执行。
- **输入**：通过 Review 的实现包、FR-02a 产出的测试用例文档。
- **处理**：编码 Agent 在实现环境中执行 smoke test，验证核心功能路径可用、构建产物完整、关键入口无崩溃。
- **输出**：Smoke Test 结果（Smoke Test Result），包含测试执行记录、通过/失败状态和失败原因。
- **执行阶段**：Smoke Test。
- **角色约束**：由 review 角色执行。
- **验收标准**：
  - AC-4.24o：Review 通过后，PipelineEngine 自动推进到 Smoke Test 阶段，无需主会话人肉触发。
  - AC-4.24p：Smoke Test 覆盖核心功能路径、构建产物完整性和关键入口无崩溃三个维度。
  - AC-4.24q：Smoke Test 失败时阻断后续阶段，结果中明确列出失败项和复现步骤。

### FR-06c UX Acceptance

- **触发时机**：Smoke Test（FR-06b）通过后自动触发，与 PM Commercial Review（FR-06d）并行执行。
- **输入**：通过 Smoke Test 的实现包、FR-02b 产出的 UX 开箱即用评测检查清单。
- **处理**：由 UX 角色（ux-01）按 FR-02b 产出的检查清单执行视觉验收——模拟陌生用户首次使用，逐项检查零配置安装、首次运行、核心功能体验、错误提示友好度、文档可读性。
- **输出**：UX 验收结果（UX Acceptance Result），包含逐项通过/失败状态、截图证据和改进建议。
- **执行阶段**：UX Acceptance。
- **角色约束**：仅 UX 角色可执行，禁止开发者或产品角色代执行。
- **并行关系**：与 FR-06d PM Commercial Review 并行执行，两者均通过后方可进入 Regression。
- **验收标准**：
  - AC-4.24r：Smoke Test 通过后，PipelineEngine 自动推进到 UX Acceptance 阶段，无需主会话人肉触发。
  - AC-4.24s：UX 验收按 FR-02b 产出的检查清单逐项执行，每项有明确通过/失败判定。
  - AC-4.24t：UX 验收失败时阻断进入 Regression，结果中列出失败项和改进建议。
  - AC-4.24u：产出工件记录 authorRole 为 ux，可追溯到执行角色。
  - AC-4.24u2：UX 验收阶段的浏览器操作步骤必须产出可复用的标准操作手册（SOP），包含页面导航路径、交互步骤、预期结果和截图位置。SOP 纳入项目 docs/ 目录，后续迭代的 UX 验收可直接复用或增量更新，不需要从零编写。
  - AC-4.24u3（UX 验收自检清单）：UX 验收报告必须包含「UX 验收自检清单」专节，列出以下全部检查项及其通过与否；任一项不通过 = UX 验收不通过，阻断进入 PM Commercial Review 与 Regression：
    1. **截图哈希独立**：UX 验收产出的所有截图文件哈希（SHA-256）必须两两不同；出现重复哈希 = 浏览器工具异常或页面未加载完成，判定为自检失败。
    2. **浏览器 console 错误**：验收全程不得出现 ERROR 级别日志（排除项目 spec 明确允许的例外）。warning 级别不造成自检失败但需在报告中折叠列出。
    3. **关键页面主操作可完成**：项目主要 web 页面必须能完成「陌生用户最关键的一个操作」（如 KIVO：导入 PDF → 看到知识点；SEVO Web：触发流水线 → 看到状态推进），主操作的识别以 spec 中指定的核心 FR 为准。主操作中途失败、路径中断、需要人手干预才能跳过某步，都判定为自检失败。
    4. **页面不是空状态与默认模板**：主操作路径上的关键页面（列表页、详情页、产出页）不得以「暂无数据」「请先初始化」「demo 占位」「示例数据」作为验收通过依据；需以真实导入材料产生的内容作为验证依据（与 FR-36 Verify-With-Real-Data Gate 联动）。LLM 对截图内容做语义判定。
    5. **交互响应可感知**：点击、提交、跳转等主要交互后 2 秒内页面状态可感知（结果加载、loading 提示、跳转发生）；点击后无任何可感知反馈超过 2 秒 = 自检失败。
    6. **不出现 404 / 500 / 白屏**：验收路径上不得跳转到 404、500、白屏、未授权页面。
    报告要求：UX 验收报告中明确列出「自检通过项」与「自检失败项」两部分，失败项需含具体证据（截图路径、console 日志片段、失败位置描述）。缺少「自检清单」章节或任一项检查未覆盖 = UX 验收未完成，不予通过。

### FR-06d PM Commercial Review

- **触发时机**：Smoke Test（FR-06b）通过后自动触发，与 UX Acceptance（FR-06c）并行执行。
- **输入**：通过 Smoke Test 的实现包、FR-02c 产出的商用评测检查清单、README.md、package.json。
- **处理**：由 PM 角色（pm-01）执行商用就绪评审——陌生用户开箱即用验证、spec-code 一致性检查、README 营销质量评估。
- **输出**：PM 商用评审结果（PM Commercial Review Result），包含逐项通过/失败状态、spec-code 覆盖矩阵和改进建议。
- **执行阶段**：PM Commercial Review。
- **角色约束**：仅 Product 角色可执行，禁止开发者或 UX 角色代执行。
- **并行关系**：与 FR-06c UX Acceptance 并行执行，两者均通过后方可进入 Regression。
- **验收标准**：
  - AC-4.24v：Smoke Test 通过后，PipelineEngine 自动推进到 PM Commercial Review 阶段，无需主会话人肉触发。
  - AC-4.24w：PM 评审覆盖陌生用户开箱即用验证、spec-code 一致性、README 营销质量三个维度。
  - AC-4.24x：PM 评审失败时阻断进入 Regression，结果中列出失败项和修复建议。
  - AC-4.24y：产出工件记录 authorRole 为 product，可追溯到执行角色。

### FR-06e Deployment View Review Gate（部署视图审查门禁）

- **触发条件**：Review（FR-06）阶段检测到 diff 涉及以下内容时自动触发：
  - 包的 `exports` 字段变更
  - 公开 API 签名变更（函数名、参数、返回类型）
  - 包的 major/minor version bump
- **输入**：当前 diff、项目根目录的 `consumers.json` 注册表。
- **处理**：
  1. 检查项目根目录是否存在 `consumers.json`。不存在则跳过本门禁（不阻断）。
  2. 读取 `consumers.json` 中注册的所有消费者条目。
  3. 对每个消费者执行其声明的 `loadTest` 命令，验证消费者在当前代码变更后仍能正常加载/运行。
  4. 任何一个 loadTest 失败 = P0 阻断，Review 不通过。
  5. 支持 `--skip-deployment-check` 参数用于紧急 hotfix 场景，跳过时必须在 review 报告中标注跳过原因。
- **consumers.json 格式**：
  ```json
  {
    "consumers": [
      { "path": "hooks/kivo-intent-injection/handler.js", "type": "hook", "loadTest": "node -e \"require('<path>')\"" },
      { "path": "scripts/memory-promote.sh", "type": "cron", "loadTest": "bash -n <path>" }
    ]
  }
  ```
  其中 `<path>` 在执行时替换为消费者的实际路径。`type` 为语义标签（hook / cron / script / service 等），用于报告分类，不影响执行逻辑。
- **输出**：部署视图审查结果，写入 review 报告的独立章节「部署视图」。
- **执行阶段**：Review（FR-06 的内置子检查）。
- **设计约束**：轻量实现——不做 AST 分析、不做依赖图谱、不做自动发现。注册表 + load test，仅此而已。
- **验收标准**：
  - AC-4.24z1：`consumers.json` 不存在时，部署视图门禁自动跳过，不阻断 Review 流程。
  - AC-4.24z2：loadTest 失败时，输出具体错误信息——包含失败的消费者路径、消费者类型和命令执行的错误输出。
  - AC-4.24z3：新增消费者（hook / cron / script / service 等任何类型）时，必须同步注册到项目的 `consumers.json`。
  - AC-4.24z4：门禁结果写入 review 报告的独立章节「部署视图」，包含每个消费者的检查状态（通过/失败/跳过）。
  - AC-4.24z5：支持 `--skip-deployment-check` 参数跳过本门禁，跳过时 review 报告「部署视图」章节标注跳过原因，供审计追溯。

### FR-07 Regression

- **输入**：通过 Review 的实现包、FR-02a 产出的测试用例文档。
- **处理**：执行回归检查，确认新增改动没有破坏既有功能、关键路径和基础约束。
- **输出**：回归包（Regression Bundle）。
- **执行阶段**：Regression。
- **审查阶段**：Regression Review（审查回归结果完整性和覆盖度）。
- **验收标准**：
  - AC-4.25：关键路径有明确回归检查结果。
  - AC-4.26：已修问题附带防复发验证。
  - AC-4.27：回归失败时能定位到受影响范围。
  - AC-4.28：回归结果进入后续 Deploy 与 Verify 的判断依据。

### FR-08 Deploy

- **输入**：通过 Regression 的交付候选版本。
- **处理**：生成发布制品，绑定版本信息、发布说明和交付目标。
- **输出**：发布包（Release Artifact）。
- **执行阶段**：Deploy。
- **审查阶段**：Deploy Review（确认发布制品与架构方案一致、版本元数据完整）。
- **验收标准**：
  - AC-4.29：发布产物可识别版本、来源和适用范围。
  - AC-4.30：发布动作与对应 Spec、Contract、Review、Regression 结果可关联。
  - AC-4.31：发布失败不会污染已通过的候选版本。
  - AC-4.32：发布结果可被 Verify 阶段直接消费。

### FR-08a Commercialization Gate（商用化门禁）

- **定位**：Deploy 之前的强制阶段。当项目配置了发布目标（npm、GitHub、ClawHub）时自动触发，确保交付物达到商用级开源标准。
- **触发条件**：项目存在 `publishTarget` 配置，且目标为 npm、ClawHub、GitHub 之一时，在进入 Deploy 前自动触发。
- **核心原则**：GitHub 独立仓库推源码（开源可读、可构建），npm 推编译产物（开箱即用）。两条渠道并存，用户既能 `npm install` 直接用，也能 clone 源码自己 build。
- **输入**：交付候选版本、发布目标配置、项目源码目录、README.md、package.json、tsconfig.json。
- **处理**：按五层标准逐层检查，任一层不通过则阻断发布。

**第一层：代码清洁度**
  1. 无硬编码路径（`/root/`、`/home/`、`~/.openclaw/` 等内部路径）。
  2. 无内部引用（内部 agent 名称、内部 API 地址、内部配置键名）。
  3. 无调试残留（`console.log` 调试输出、TODO/FIXME/HACK 注释）。
  4. 无敏感信息（API key、token、密钥文件、.env 文件）。
  5. 依赖声明完整——package.json 的 dependencies 和 peerDependencies 覆盖所有 import，无遗漏无冗余。

**第二层：包完整性**
  6. package.json 必填字段完整：name、version、description、author、license、main/exports、bin（如有 CLI）。
  7. 入口文件指向存在的文件（main/exports/bin 指向的路径必须存在）。
  8. TypeScript 项目必须有 tsconfig.json，且 `npm run build` 能成功编译。
  9. .gitignore 排除编译产物（根目录 .js、dist/、node_modules/）。
  10. .npmignore 或 package.json files 字段正确配置，npm 包只包含编译产物 + 类型声明 + 文档。

**第三层：文档质量**
  11. README.md 存在且符合营销质量标准（tagline → 痛点 → 优势 → 快速体验 → 场景 → 文档链接）。
  12. README 同时引导两类用户：npm 用户（`npm install` 快速上手）和源码用户（clone → install → build）。
  13. 配置项有文档说明（环境变量、配置文件模板、CLI 参数）。
  14. CHANGELOG.md 或 GitHub Releases 记录版本变更。
  15. LICENSE 文件存在。

**第四层：可构建性**
  16. 在干净目录中 `git clone → npm install → npm run build` 能成功完成。
  17. `npm test` 能通过（如项目有测试）。
  18. CLI 项目：`npx <包名> --help` 能正常输出。

**第五层：开箱即用**
  19. `npm install <包名>` 能成功安装。
  20. 每个核心功能有可验证的首次使用路径，且产出有意义的结果（不是空壳）。
  21. 需要外部依赖（专用 API key、第三方服务）的功能，有明确的配置引导和错误提示。

- **输出**：商用化门禁结果（Commercialization Gate Result），包含五层检查的逐项通过/失败状态、具体失败原因、修复建议。
- **执行阶段**：Commercialization Gate（Deploy 前阶段）。
- **验收标准**：
  - AC-4.32a：存在 `publishTarget` 配置时，系统在 Deploy 前自动触发商用化门禁，无需用户确认。
  - AC-4.32b：系统执行全部五层检查，不允许只做部分检查。
  - AC-4.32c：任一检查项不通过时，发布被阻断，结果中明确列出具体失败原因和修复建议。
  - AC-4.32d：用户可选择跳过该阶段，跳过决定写入 ledger，标注"用户主动跳过商用化门禁"。
  - AC-4.32e：不存在 `publishTarget` 配置时，该阶段完全不出现，不影响 Deploy 流程。
  - AC-4.32f：发布目标包含 GitHub 独立仓库时，门禁自动执行独立仓库同步——推送源码（排除编译产物），推送前排除 .gitignore 中定义的文件。
  - AC-4.32g：推送独立仓库前，扫描待推送文件中是否包含敏感内容（.env、API key、密钥文件、内部配置），发现则阻断推送并报告。
  - AC-4.32h：npm publish 和独立仓库同步作为原子操作执行——任一步骤失败则整体回滚。
  - AC-4.32i：GitHub 独立仓库只推源码（TypeScript），编译产物由 .gitignore 排除；npm 包只推编译产物 + 类型声明 + 文档。
  - AC-4.32j：第四层可构建性检查在干净临时目录中执行（模拟陌生用户环境），不依赖开发现场。
  - AC-4.32k：门禁结果包含五层检查的逐项状态，支持增量修复（修复后只重跑失败项，不重跑已通过项）。


### FR-09 Verify

- **输入**：发布包。
- **处理**：在独立、清洁或最小依赖环境中验证功能、关键 NFR 和交付可用性。
- **输出**：验证包（Verification Bundle）。
- **执行阶段**：Verify（独立环境验证，与 Implement 阶段执行者分离）。
- **审查阶段**：Verify Review（确认核心用户路径和交付可用性达标）。
- **验收标准**：
  - AC-4.33：验证环境不依赖开发现场残留。
  - AC-4.34：验证覆盖核心用户路径和关键非功能指标。
  - AC-4.35：验证结论可明确区分可交付与不可交付。
  - AC-4.36：验证失败会阻断 Ledger 的通过结论。
  - AC-4.36a：Verify 阶段采用默认拒绝策略（deny by default）——没有显式验证证据的 AC 默认判定为未通过。子 Agent 正常返回但未提供验证证据时，该 AC 的验证状态为 failed，不允许因缺少失败信号而默认通过。
  - AC-4.36b：Verify 阶段的验证目标（VerifyTarget）自动从 spec AC 列表派生，每条 AC 生成对应的验证目标。编排者无需手动定义 targets，系统根据 AC 描述自动生成验证步骤和预期结果。
  - AC-4.36c：每条 AC 的验证必须包含实际运行证据——API 调用结果、浏览器截图、数据库查询结果、CLI 输出等可观测产出。tsc 编译通过、npm test 通过不算单条 AC 的验证证据，只能作为 L1 基础检查的一部分。
  - AC-4.36d：验证步骤必须使用真实数据或真实环境产生的数据。禁止使用 mock 数据、seed 数据或硬编码的预期值通过验证。验证环境可以是隔离的，但数据必须通过实际功能流程产生。
  - AC-4.36e：Tiered Scan、编译、测试或其他预检查报告只能作为 Verify 的前置筛查和补充证据，不能替代单条 AC 的运行时验证。若所有 VerifyTarget 都未产出 pass 级运行时证据，则 Verify 总结论必须为 failed。

### FR-10 Ledger

- **输入**：FR 流程实例 ID、Spec Package、Spec Review Bundle、Contract Package、Contract Review Bundle、Implementation Bundle、Review Bundle、Regression Bundle、Release Artifact、Verification Bundle。
- **处理**：生成交付记录，串起版本、日期、范围、证据、问题、结论和经验沉淀。每条 Ledger Entry 必须关联到对应的 FR 流程实例 ID。
- **输出**：交付账本条目（Ledger Entry）。
- **执行阶段**：Ledger（系统自动汇总）。
- **审查阶段**：Ledger Review，产品维度（确认交付范围和结论准确）和架构维度（确认证据链完整和经验沉淀质量）。
- **验收标准**：
  - AC-4.37：账本条目能追溯到本轮所有关键工件。
  - AC-4.38：账本记录交付结论、责任边界和后续动作。
  - AC-4.39：经验沉淀可被后续任务复用。
  - AC-4.40：没有 Ledger Entry 的交付不算流程闭环。
  - AC-4.40a：Ledger Entry 中的经验沉淀（lessons learned）必须在后续 pipeline 的 Specify 阶段被自动检索和注入。PipelineEngine 在启动 Specify 阶段时，自动查询同项目历史 Ledger Entry 的经验字段，将相关经验作为上下文注入给 Specify 执行者，避免重复踩坑。注入内容按相关性排序，最多注入最近 10 条。

### FR-11 Proactive Clarification

- **定位**：跨阶段机制。在 Spec、Contract、Implement 三个阶段内建模糊检测与主动澄清能力，确保歧义在产生阶段就地消解，而非流入下游造成返工。
- **触发条件**：任一阶段执行过程中，检测到以下模糊信号之一即触发澄清流程：
  - 验收标准缺失或不可验证。
  - 边界条件未定义（输入范围、异常路径、并发场景）。
  - 术语首次出现但未给出定义。
  - 依赖未声明（上游工件、外部服务、运行时假设）。
  - 接口契约不完整（参数、返回值、错误码缺失）。
  - 数据流向不明（谁产出、谁消费、格式是什么）。
  - 性能或资源约束缺失（超时、并发上限、存储配额）。
  - Spec 与 Contract 之间存在矛盾或不一致。
- **澄清类型分类**：每个澄清问题必须标注类型，便于收敛后按知识类型沉淀：
  - 纠偏（correction）：已有描述与事实或意图不符。
  - 方法（methodology）：如何做、用什么方法。
  - 决策（decision）：多个可选方案需要取舍。
  - 边界（boundary）：范围、限制、不做什么。
  - 经验（experience）：历史教训、已知陷阱。
  - 元认知（meta）：关于流程本身的反思。

#### FR-11.1 Spec 阶段澄清

- **输入**：正在编写或已产出的 Spec Package。
- **处理**：
  1. 扫描 Spec 内容，检测模糊信号（验收标准缺失、边界未定义、术语未解释、依赖未声明）。
  2. 对每个模糊点生成结构化澄清问题，包含：问题描述、模糊类型、影响范围、建议选项（如有）。
  3. 将澄清问题提交给需求来源方（用户或上游 Agent）。
  4. 收到澄清回复后，将收敛结论写回 Spec Package 对应位置。
- **输出**：澄清记录（Clarification Record）+ 更新后的 Spec Package。
- **验收标准**：
  - AC-4.41：Spec 产出前，所有被检测到的模糊点都已生成澄清问题或标注为已知风险。
  - AC-4.42：澄清问题包含类型标签、影响范围和上下文引用，不是孤立提问。
  - AC-4.43：澄清收敛后的结论直接写入 Spec Package，不留在对话或临时文件中。
  - AC-4.44：澄清收敛结论按知识类型沉淀（纠偏→事实、决策→ADR 候选、边界→约束条件、方法→方法论记录、经验→experience 知识（沉淀到经验库 / lessons learned）、元认知→meta 知识（沉淀到方法论 / 流程改进建议））。

#### FR-11.2 Contract 阶段澄清

- **输入**：正在编写或已产出的 Contract Package、关联的 Spec Package。
- **处理**：
  1. 扫描技术方案，检测模糊信号（接口未定义、数据流不明、性能约束缺失、模块职责重叠）。
  2. 对每个模糊点生成结构化澄清问题。
  3. 区分澄清对象：技术层面的模糊由架构阶段内部消解；需求层面的模糊上报给 Spec 来源方。
  4. 收到澄清回复后，将技术决策写入 ADR，将需求澄清回写 Spec Package。
- **输出**：澄清记录 + 更新后的 Contract Package + 相关 ADR。
- **验收标准**：
  - AC-4.45：Contract 产出前，所有被检测到的技术模糊点都已澄清或记录为待定风险。
  - AC-4.46：需求层面的模糊上报给 Spec 来源方，不由架构阶段单方面假设。
  - AC-4.47：技术决策类澄清收敛后写入 ADR，包含替代方案和取舍理由。
  - AC-4.48：Spec 与 Contract 之间的矛盾在此阶段被检测并消解，不流入 Implement。

#### FR-11.3 Implement 阶段澄清

- **输入**：Contract Package、Work Package、Task 描述。
- **处理**：
  1. 执行前检查 Task 描述完整性（目标文件、预期变更、验证步骤是否齐全）。
  2. 执行过程中发现 Spec/Contract 矛盾或未覆盖场景时，暂停实现并上报。
  3. 生成结构化澄清问题，标注阻断级别（blocking：必须等回复才能继续；non-blocking：可先按默认假设推进，但需确认）。
  4. 收到澄清回复后，更新 Task 描述或回写上游工件。
- **输出**：澄清记录 + 更新后的 Task 描述（或上游工件修正请求）。
- **验收标准**：
  - AC-4.49：Task 描述不完整时，执行者主动提问而非基于猜测开发。
  - AC-4.50：Spec/Contract 矛盾被发现时，实现暂停并上报，不自行决定以哪个为准。
  - AC-4.51：澄清问题标注阻断级别，blocking 类必须等回复，non-blocking 类可附默认假设先行。
  - AC-4.52：澄清结论回写到对应工件（Task 描述、Spec Package 或 Contract Package），不只留在执行日志中。

#### FR-11.4 实现路径

- 每个阶段的 Skill（specify/plan/implement）内置模糊检测逻辑，作为阶段执行的前置步骤或并行检查。
- 模糊检测规则可配置、可扩展，新增检测维度不需要改代码。
- 澄清流程通过阶段执行原则注入（参考 §6.6），绑定阶段而非 Agent 身份。
- 澄清记录作为阶段工件的一部分，纳入 Ledger 证据链。
- 验收标准：
  - AC-4.53：模糊检测规则可通过配置文件扩展，不需要修改 Skill 源码。
  - AC-4.54：澄清记录纳入 Ledger Entry 的证据链，可追溯每个澄清的触发点、问题、回复和收敛结论。
  - AC-4.55：澄清机制不依赖特定 Agent 身份，任何执行者进入对应阶段都自动获得澄清能力。

### FR-12 Pipeline Create

- **定位**：生命周期操作。研发流程的入口点，负责在用户已创建 Project、已添加 FR 之后，为该 FR 创建 FR 流程实例、初始化 Project 目录结构、生成路由结果。
- **输入**：任务描述、Project 标识（project-slug）、FR 描述、触发条件命中结果。
- **处理**：
  1. 校验 Project 标识合法性（命名规范、是否已存在）。
  2. 校验目标 FR 已被创建并归属到该 Project。
  3. 检查同一 Project 是否已有 active 的 FR 流程实例，有则拒绝创建。
  4. 生成实例 ID（格式见 §3.5）。
  5. 执行路由判定（§3.2），确定任务级别和必经阶段。
  6. 检查 Project 目录结构，按 §3.6 规范初始化或补全。
  7. 创建 FR 流程实例记录，状态设为 created，并使该 FR 自动进入 Specify 阶段的流程准备态。
  8. 向 PipelineEngine（FR-13）发送 pipeline-created 事件，PipelineEngine 接管后续生命周期推进。
- **输出**：FR 流程实例（含 ID、Project 绑定、路由结果、目录结构确认）。
- **执行阶段**：Pipeline Create（研发流程入口，在第一个业务阶段之前执行）。
- **验收标准**：
  - AC-4.56：每个 FR 流程实例有全局唯一 ID，格式符合 `fr-<project-slug>-<yyyyMMdd>-<seq>` 规范。
  - AC-4.57：同一 Project 已有 active 实例时，创建请求被拒绝并返回明确错误信息。
  - AC-4.58：创建完成后，Project 目录结构符合 §3.6 规范，缺失目录已补全。
  - AC-4.59：路由结果包含任务级别、必经阶段、可跳过阶段及跳过理由。
  - AC-4.60：已有 Project 目录的内容不被覆盖，只补全缺失的子目录。
  - AC-4.61：pipeline 创建完成后，PipelineEngine 自动接管并通过 OpenClaw Adapter 触发第一个阶段的执行，用户不需要手动触发。

### FR-13 PipelineEngine（流程编排引擎）

- **交付状态**：已交付（v1.12.1）。
- **定位**：SEVO 的核心运行时引擎。负责 pipeline 实例创建后的全生命周期推进——通过状态机驱动阶段流转，借助 OpenClaw Adapter 触发阶段执行，监听阶段完成事件，评估门禁条件，决定推进或阻断。PipelineEngine 定义的是编排语义（何时推进、何时阻断、何时重试），具体的任务派发方式由 OpenClaw Adapter 实现。
- **编排模型**：PipelineEngine 不直接调度任务。在 OpenClaw 环境中，它通过 hook 注入 + prompt 引导的方式工作：`before_prompt_build` hook 向主会话注入「下一步该派发什么任务」的指令，主会话仍然是调度者，PipelineEngine 提供编排决策。`subagent_ended` hook 监听任务完成事件，更新 pipeline 状态，设置下一阶段的推进指令。
- **角色知识内置**：PipelineEngine 在派发阶段任务时，自动注入该阶段应遵循的专业标准（§6.6）。Specify 阶段注入 PM 标准的 prompt 模板和质量门禁，Review 阶段注入审计标准，Contract 阶段注入架构设计原则。单 Agent 用户也能产出专业质量的工件，多 Agent 环境有专职角色则效果更好。
- **输入**：FR-12 创建的 FR 流程实例（含路由结果、阶段队列）。
- **处理**：
  1. 接收 pipeline-created 事件，读取路由结果中的阶段队列，生成 Stage Queue。
  2. 按 Stage Queue 顺序，通过 OpenClaw Adapter 触发当前阶段的执行。
  3. 监听阶段完成事件。
  4. 阶段完成后，自动评估该阶段的出口条件（工件是否齐全、门禁是否通过）。
  5. 出口条件满足 → 自动推进到下一阶段 → 重复步骤 2。
  6. 出口条件不满足（门禁失败）→ 自动触发 Review Fix Loop（FR-06a）→ 修复完成后重新评估。
  7. 支持并行阶段（如 FR-02a/FR-02b/FR-02c 与 FR-03 并行；FR-06c 与 FR-06d 并行）。
  8. 所有阶段完成 → Ledger 自动生成 → pipeline 实例状态变为 completed。
  9. 启动时扫描持久化状态文件，检测中断的 pipeline（Gateway 重启、主会话中断、系统 OOM），自动恢复到最后已知状态并继续推进。
  10. 多个 pipeline 竞争同一角色的 Agent 时，按先到先服务排队，不阻塞其他不竞争的阶段。用户可通过配置指定优先级。
- **输出**：pipeline 实例的完整生命周期推进记录，包含每个阶段的触发时间、完成时间、门禁结果、推进决策。
- **验收标准**：
  - AC-13.1：pipeline 创建后，PipelineEngine 在无人工干预的情况下自动通过 OpenClaw Adapter 触发第一个阶段的执行。
  - AC-13.2：每个阶段完成后，PipelineEngine 在 30 秒内评估门禁并决定推进或阻断。
  - AC-13.3：门禁失败时，PipelineEngine 自动触发修复流程（FR-06a），修复通过后自动恢复推进。
  - AC-13.4：并行阶段（如 UX Acceptance + PM Commercial Review）同时触发，两者均通过后才推进到下一阶段。
  - AC-13.5：pipeline 推进的每一步决策（推进/阻断/重试）都有结构化记录，可在驾驶舱查看。
  - AC-13.6：PipelineEngine 的编排语义与任务派发实现分离——它定义「何时推进、何时阻断」，具体的任务触发通过 Adapter 抽象层实现，保持代码职责清晰。
  - AC-13.7：用户可以在任意时刻查询 pipeline 当前状态：走到哪个阶段、卡在哪里、下一步是什么。
  - AC-13.8：Gateway 重启后，中断的 pipeline 在 60 秒内自动恢复推进，不需要用户手动干预。
  - AC-13.9：多个 pipeline 竞争同一角色的 Agent 时，按优先级排队，不阻塞其他不竞争的阶段。
  - AC-13.10：显式执行 `sevo:create <project-slug>` 或被 dispatch-guard 自动路由到创建入口后，PipelineEngine 必须直接进入 Specify 阶段并自动派发第一条 Specify 任务，不允许停留在 created 状态等待人工二次触发。
  - AC-13.11：通过显式 CLI 创建和通过 dispatch-guard 拦截创建的 pipeline，复用同一套状态机和自动推进逻辑；两种入口的阶段队列、门禁评估和恢复行为保持一致。

### FR-14 Package Distribution & CLI（包分发、初始化与命令行界面）

- **定位**：SEVO 的安装入口和用户交互界面。负责 npm 包分发、CLI 入口、初始化命令、插件自动注册、环境健康检查，以及 Project 管理、FR 管理、Pipeline 状态查询和手动干预的全部命令行操作。
- **包名**：`sevo`（统一 npm 包名）。
- **包结构**：单包双入口——`dist/` 提供库 API（PipelineEngine、GateEngine、LedgerEngine、Adapter 等），`plugin/` 提供 OpenClaw 插件入口（register + hooks），`bin/` 提供 CLI 入口。
- **输入**：用户执行 `npm install -g sevo` 和 CLI 命令。
- **处理**：
  1. npm 包包含 SEVO 核心库 + CLI 入口 + 内置 OpenClaw 插件。
  2. `sevo init` 执行环境检测：检测 OpenClaw 环境配置 → 生成默认配置 → 自动注册插件到 `openclaw.json` → 扫描 `projects/*/sevo.json` 发现受管项目 → 动态发现 Agent 并按命名规则 + runtime type 自动分类角色 → 单 Agent 环境自动启用降级模式 → 执行 doctor 检查 → 输出角色分配表和下一步指引。
  3. `sevo doctor` 检查配置完整性和环境就绪状态，每个问题附带修复建议。
  4. `sevo project create <name> [--description <desc>]` 创建 Project。
  5. `sevo project list` 列出所有 Project。
  6. `sevo fr add <project> <description>` 向 Project 添加 FR，自动触发 pipeline 创建。
  7. `sevo fr list <project>` 列出 Project 下所有 FR 及其 pipeline 状态。
  8. `sevo fr advance <project> --fr <fr-id>` 为已有项目中新增的 FR 触发增量实现子流程（implement → review → regression → publish），跳过 spec/contract 阶段。
  9. `sevo status [<instance-id>]` 查看 pipeline 当前状态。
  10. `sevo pause <instance-id>` 暂停 pipeline。
  11. `sevo resume <instance-id>` 恢复 pipeline。
  12. `sevo cancel <instance-id>` 取消 pipeline，状态设为 failed，取消原因记录到 Ledger。
  13. `sevo ledger [<project>]` 查看交付账本。
- **输出**：可用的 SEVO 运行环境 + 配置文件 + 插件注册 + CLI 交互能力。
- **验收标准**：
  - AC-14.1：陌生用户执行 `npm install -g sevo` + `npx sevo init` 后，5 分钟内能创建第一个 Project 并启动第一条 pipeline。
  - AC-14.2：`sevo init` 自动检测 OpenClaw 环境配置，不需要用户手动指定。
  - AC-14.3：在 OpenClaw 环境中，`sevo init` 自动注册 SEVO 插件，用户不需要手动编辑 `openclaw.json`。
  - AC-14.4：`sevo init` 生成的默认配置足以跑通完整流水线（L0 级别），不需要额外配置。
  - AC-14.5：`sevo doctor` 能检测并报告所有配置问题，每个问题附带修复建议。
  - AC-14.6：`sevo --help` 输出所有可用命令，每个命令有一句话说明。
  - AC-14.7：`sevo project create` + `sevo fr add` 后，pipeline 自动创建并开始推进，用户不需要额外操作。
  - AC-14.8：`sevo status` 能在任意时刻回答「当前走到哪了、卡在哪里、下一步是什么」。
  - AC-14.9：所有命令的错误提示可理解、可操作（告诉用户怎么修，不只是报错码）。
  - AC-14.10：CLI 核心命令（status、ledger 等查询类）在纯 Node.js 环境中可运行，流水线执行依赖 OpenClaw 环境。
  - AC-14.11：`sevo init` 检测到 OpenClaw 未安装时，错误提示包含 OpenClaw 安装链接。
  - AC-14.12：当自动分类无法识别任何 Agent 的角色时，`sevo init` 进入交互式角色分配模式，引导用户手动指定至少一个编码角色和一个审查角色。
  - AC-14.13：`sevo init` 自动检测 OpenClaw 环境中的 ACP Agent 类型（Claude Code、Codex、OpenCode、Gemini CLI 等），为每种已检测到的 ACP 生成对应的持久化提示注入配置文件（如 `.claude/CLAUDE.md`、`codex.md`、`.opencode/agents.md`）。注入内容包含 SEVO 流程规则、角色约束和项目上下文。配置文件在后续 pipeline 执行时被 ACP Agent 自动加载，无需每次通过 task prompt 重复注入。
  - AC-14.14：SEVO 插件启动时通过文件系统扫描 `projects/*/sevo.json` 自动发现受管项目。项目根目录下存在 `sevo.json` 且内容包含 `{"managed": true}` 的项目自动纳入受管列表。`sevo.json` 最小有效内容为 `{"managed": true}`。
  - AC-14.15：`plugins.entries.sevo-pipeline.config.managedProjects` 配置项作为覆盖/补充机制保留。插件的 `loadConfig()` 函数先扫描项目目录发现 `sevo.json`，再合并 config 中的显式列表，最终生成完整的受管项目列表。显式列表中的项目即使没有 `sevo.json` 也纳入受管。
  - AC-14.16：新增项目只需在项目根目录创建 `sevo.json`（内容 `{"managed": true}`），无需修改全局配置即可被 SEVO 自动纳管。
  - AC-14.17：发布到 npm 的安装包必须正确注册 `sevo` CLI 入口。陌生用户通过全局安装或 `npx` 调用时，`sevo --help`、`sevo init`、`sevo project create`、`sevo fr add` 四条首用命令都可直接执行，不需要手工修复 bin 链接。
  - AC-14.18：发布包包含安装后自检路径：`postinstall` 钩子或等效机制必须验证 CLI 入口和必需资源可用；自检失败时输出可操作修复提示，禁止静默成功。
  - AC-14.19：发布包提供一键初始化脚本 `scripts/init.sh` 或等效受支持入口，用于串联安装后检查、CLI 可用性确认和 `sevo init` 首次引导；README 与 CLI 首次输出引用同一入口，避免陌生用户在多条初始化路径之间猜测。
  - AC-14.20：`sevo-pipeline` 主包仅承载 CLI、引擎、流水线编排能力，禁止打包 Web 静态资源（`web/`、`web/.next/`、`web/components/` 等子目录）。Web 驾驶舱体验由独立 npm 包 `sevo-web` 提供，发版节奏与主包解耦。`npm pack --dry-run` 输出中不得出现 Web 子目录。
  - AC-14.21：`sevo-web` 包通过 `package.json.peerDependencies` 显式声明 `sevo-pipeline` 的兼容版本范围；`sevo-web` 启动时校验已安装的 `sevo-pipeline` 引擎契约版本，不在兼容范围内时拒绝启动并输出含「升级/降级 sevo-pipeline 至 X.Y.Z」的可操作错误信息。`sevo-pipeline` 的 `sevo init` 在检测到项目声明 Web 入口时，必须主动提示安装 `sevo-web` 并附完整命令，禁止默认无声忽略。

### FR-15 Progressive Disclosure（渐进式披露配置）

- **定位**：SEVO 的配置与定制分层模型。定义四个披露级别，用户按需逐级解锁更多控制能力。
- **处理**：

**L0 安装即用**（由 FR-14 保证）：
- `sevo init` 后零配置可用。默认阶段定义、默认门禁规则、默认路由策略、角色专业标准全部内置。
- 用户只需要 `sevo project create <name>` + `sevo fr add <project> <description>` 就能启动 pipeline。
- 单 Agent 环境自动降级：所有角色池填入同一个 agentId，流水线所有阶段由同一个 Agent 执行，质量保证降级但功能完整。
- 对未经编排的开发任务的默认处理策略为 `guide`（注入流程引导），不阻断执行。

**L1 按需配置**：
- 用户可以在配置中调整：
  - 默认路由级别阈值（多少行算 Level 1、多少行算 Level 2+）。
  - 门禁严格度（严格/标准/宽松）。
  - 通知渠道偏好。
  - 发布目标（npm / GitHub / ClawHub）。
  - 合规模式（`guide` 注入流程引导 / `auto-route` 自动为未编排的开发任务创建 pipeline 并路由进 SEVO 流程 / `off` 关闭）。

**L2 自定义阶段**：
- 用户可以添加自定义阶段（如 Security Audit、Performance Test）。
- 用户可以修改阶段顺序（在约束范围内）。
- 用户可以定义自定义门禁规则。

**L3 编程控制**：
- 用户可以通过 API 或 SDK 编程控制 pipeline 行为。
- 支持自定义 Adapter（替换默认的通知、发布、LLM 调用实现）。
- 支持自定义阶段执行器（替换默认的 Skill 执行）。

- **验收标准**：
  - AC-15.1：L0 级别下，用户不需要编辑任何配置文件就能跑通完整 pipeline。
  - AC-15.2：L1 级别的配置项有完整的文档说明和默认值，修改任一配置不会破坏 pipeline 运行。
  - AC-15.3：L2 级别的自定义阶段可以插入到标准阶段序列中，且不破坏工件链和门禁逻辑。
  - AC-15.4：L3 级别的 API 覆盖 pipeline 创建、阶段查询、门禁覆写、工件读取等核心操作。
  - AC-15.5：每个级别的能力是累加的——L1 包含 L0 的全部能力，L2 包含 L1 的全部能力，以此类推。
  - AC-15.6：用户从 L0 升级到 L1 不需要重新初始化，只需编辑配置文件。
  - AC-15.7：Agent 自主行动按操作风险分三级——L0 级操作（文件读写、构建、测试、代码生成）无需确认直接执行；L1 级操作（配置变更、依赖安装、分支创建）执行后通知用户；L2 级操作（发布、删除、外部通信、生产环境变更）必须获得用户确认后才能执行。分级规则在 `sevo.config.json` 的 `actionLevels` 字段中可自定义，默认值覆盖常见操作类型。

### FR-16 Onboarding Experience（开箱体验）

- **定位**：陌生用户的首次使用旅程设计。确保从 `npm install` 到「看到第一条 pipeline 跑完」的路径畅通、有意义。
- **处理**：
  1. 安装后首次运行 `sevo init`，输出欢迎信息 + 环境检测结果 + 下一步指引。
  2. 提供 `sevo demo` 命令，分两层验证：
     - `sevo demo --dry-run`：展示 pipeline 阶段流转和工件结构，用 mock 数据，不需要 LLM，验证安装正确性。
     - `sevo demo`：在有 LLM 的环境中用内置示例项目跑一条真实的 Level 0 pipeline，验证端到端可用性。
  3. demo 完成后，输出「你刚刚看到了什么」的解释 + 「如何用自己的项目」的指引。
- **验收标准**：
  - AC-16.1：陌生用户从 `npm install` 到看到第一条 pipeline 完整跑完，耗时不超过 5 分钟。
  - AC-16.2：`sevo demo --dry-run` 在无网络、无 LLM 的条件下能跑通，产出有意义的示例工件结构。
  - AC-16.3：`sevo demo` 在有 LLM 的环境中用内置示例项目跑通一条真实 Level 0 pipeline。
  - AC-16.4：demo 完成后的输出包含「你刚刚经历了什么」的解释和「下一步做什么」的指引。
  - AC-16.5：首次使用路径中的每一步都有明确的成功/失败反馈，失败时告诉用户怎么修。
  - AC-16.6：发布产物必须附带 stranger walkthrough（面向首次使用者的开箱路径说明），覆盖 `npm install` → `npx sevo init` → `sevo project create` → `sevo fr add` → `sevo status` 的完整路径；walkthrough 文案与实际 CLI 行为保持一致，并在干净环境中验过一次。

### FR-17 Post-Release Validation Gate（发布后验证门禁）

- **定位**：发布完成不等于产品可用。此阶段在 Deploy/Verify 之后、Ledger 之前自动执行终局差距扫描，逐条对照 spec FR 检查产品在真实环境中是否运行并产出价值。
- **处理**：
  1. npm publish / deploy 成功后，自动触发 Post-Release Validation 阶段。
  2. 差距扫描逐条对照 spec 中所有 FR，对每条 FR 检查三个维度：代码实现了？运行态跑起来了？陌生人能用？
  3. 每条 FR 产出三种状态之一：covered（全部通过）、code-only（有代码无运行态验证）、missing（完全缺失）。
  4. 发现差距时自动生成修复任务列表，包含 FR 编号和修复描述。
  5. 差距为零才允许流水线进入 Ledger 阶段标记为 completed。
- **验收标准**：
  - AC-17.1：npm publish 成功后，流水线自动进入 post-release-validation 阶段，无需人工触发。
  - AC-17.2：差距扫描逐条对照 spec FR，输出结构化 gap analysis report，包含 totalFrs、coveredCount、codeOnlyCount、missingCount、gaps 和逐条 entries。
  - AC-17.3：发现差距（gaps > 0）时，自动生成修复任务列表（fixTasks），每条包含 frId 和 description。
  - AC-17.4：差距为零（gaps === 0）时 canComplete 为 true，流水线可进入 Ledger 阶段；差距不为零时 canComplete 为 false，流水线阻塞。
  - AC-17.5：L1/L2+ 流水线包含 post-release-validation 阶段；L0 微小改动跳过此阶段。
  - AC-17.6（引擎与调度层职责边界）：SEVO 引擎是状态机 + 触发器，不是执行者。引擎的职责限于：感知「现在到了哪个节点」、在需要行动的节点向调度层（主 Agent）推送提醒、接收「差距已清零」的确认后放行进入下一阶段。引擎不做差距判定——差距分析由调度层派子 Agent 执行，结果回报给调度层，调度层确认后通知引擎。引擎不做任务拆解——修复任务的定义和派发由调度层负责。循环终止条件：调度层通知引擎「差距 = 0」，引擎放行。
  - AC-17.7：差距扫描维度扩展为两大类——技术可用性（项目结构完整性、安装验证、编译验证、测试验证、服务存活、运行态健康、依赖安全）和产品可感知性（README 质量、npm 元数据、GitHub 元数据、官网可达）。每个维度产出 PASS/FAIL/SKIP 状态和失败原因。
  - AC-17.8：产品可感知性扫描中的 README 质量评估必须调用 LLM API 进行语义级评估（tagline→痛点→优势→快速体验→场景→文档链接），产出 0-100 评分和改进建议。禁止降级为结构检查、关键词匹配或正则表达式。LLM 不可用时该检查项标记为 SKIP（原因：「LLM 不可用」），不标记为 PASS。
  - AC-17.9：`sevo scan --endgame [--project <slug>]` 命令可手动触发终局扫描。未指定 project 时扫描所有已注册项目；指定 project 时只扫描该项目。扫描结果为结构化 JSON 报告，写入项目的 `reports/endgame-scan-<date>.json`。
  - AC-17.10：Post-Release Validation 的差距扫描必须包含 L3 运行时行为验证——对每条 FR 触发实际功能执行并验证产出有意义。禁止仅依赖 artifact 元数据匹配（如 artifact.id 包含 frId）判定 FR 为 covered。元数据匹配只能作为预筛选，最终判定必须基于 L3 运行时验证结果。
  - AC-17.11：Post-Release Validation 中，任一 FR 的 L3 运行时验证未执行、执行失败、或只得到元数据/静态证据时，该 FR 不得标记为 covered，至少记为 code-only 或 missing，并阻断 canComplete。

### FR-18 目标驱动 PDCA 闭环

- **定位**：Pipeline 级别的目标管理机制。将 OKR→SMART→PDCA 融入现有流水线阶段，为每条 pipeline 提供终局目标锁定、目标拆解、目标对齐检查和差距驱动回环能力。所有新增能力向后兼容——未传入 endStateGoal 时，pipeline 行为与现有逻辑完全一致。
- **数据结构**：
  - `EndStateGoal { description: string; lockedAt: string }` — 终局目标描述 + 锁定时间戳。
  - `KeyResult { krId: string; description: string; measure: string; threshold?: string; status: 'not-started' | 'in-progress' | 'achieved' | 'blocked' }` — 单个关键结果。
  - `ObjectiveKeyResult { objectiveId: string; description: string; keyResults: KeyResult[] }` — 目标 + 关键结果树。
  - `PdcaCycleRecord { cycle: number; triggeredBy: string[]; newTasks: string[]; result: 'converged' | 'gap-remaining' | 'escalated' }` — 单轮 PDCA 记录。
  - `PipelineInstance` 新增可选字段：`endStateGoal?: EndStateGoal; okrTree?: ObjectiveKeyResult[]; pdcaCycles?: PdcaCycleRecord[]`。
  - `PipelineCreateRequest` 新增可选字段：`endStateGoal?: EndStateGoal`。
  - `FunctionalRequirement` 新增可选字段：`tracesTo?: string`（KR 标识符）。
- **输入**：Pipeline 创建时的 endStateGoal（可选）、Spec 阶段的 FR 列表、各 Gate 的评估结果、Post-Release Validation 的差距分析结果。
- **处理**：
  1. Pipeline 创建时（FR-12），接受可选的 endStateGoal 参数。未传入时，SEVO 生成引导提示帮助用户澄清终局目标。目标一旦锁定，写入 pipeline 实例元数据，后续修改需显式操作并记录变更理由。
  2. Spec 阶段（FR-01），若 pipeline 存在 endStateGoal，从目标拆解为 Objective + Key Results（OKR 树）。每个 KR 有明确的度量标准和达成阈值。FR 从 KR 反推，每个 FR 带 tracesTo 字段溯源到对应 KR。
  3. Spec 阶段，每个 FR/AC 按 SMART 原则（具体、可度量、可达成、相关、有时限）编写。Spec Review Gate（FR-02）增加 SMART 合规性检查维度。
  4. 各 Gate 评估时（FR-02、FR-04、FR-06），若 pipeline 存在 OKR 树，额外检查当前阶段产出是否在向终局目标收敛。目标对齐检查作为可选增强维度，不改变现有 Gate 的通过/阻断逻辑。
  5. Post-Release Validation（FR-17），若 pipeline 存在 OKR 树，差距分析升级为 KR 级——按 KR 逐条检查达成度，canComplete 判定基于 KR 达成情况。无 OKR 树时 fallback 到现有 FR 级扫描。
  6. Post-Release Validation 发现 KR 级差距（gaps > 0）时，pipeline 不进入 Ledger。Post-Release Validation 阶段内部生成新工作包（针对未达成 KR 的 SMART 任务），触发 Implement→Review→Deploy→Validate 子循环。子循环在 Post-Release Validation 内部管理，不回退 pipeline 主状态机。循环直到所有 KR 达成或达到最大轮次上限。
  7. `sevo demo` 展示完整闭环：目标锁定 → OKR 拆解 → SMART 任务化 → 阶段执行（Do）→ 差距扫描（Check）→ 回环修复（Act）→ 收敛完成。
- **输出**：OKR 树（OKR Tree，挂接到 pipeline 实例元数据）、KR 级差距分析报告（KR Gap Analysis Report）、PDCA 轮次记录（PDCA Cycle Record）。
- **执行阶段**：跨阶段机制，融入 Pipeline Create、Spec、Gate、Post-Release Validation 和 PipelineEngine 的现有流程中。
- **验收标准**：
  - AC-18.1：Pipeline 创建时（FR-12）支持可选的 endStateGoal 参数。传入时写入 pipeline 实例元数据；未传入时 SEVO 输出引导提示，pipeline 正常创建，后续阶段按现有逻辑执行。
  - AC-18.2：endStateGoal 锁定后，修改需通过显式操作（如 `sevo goal update <instance-id>`），变更理由写入 pipeline 元数据的变更日志。
  - AC-18.3：Spec 阶段存在 endStateGoal 时，系统从目标拆解为 Objective + Key Results，每个 KR 包含度量标准（metric）和达成阈值（threshold）。
  - AC-18.4：OKR 树中的每个 FR 带 tracesTo 字段，值为对应 KR 的标识符，溯源链完整可查。
  - AC-18.5：Spec 阶段产出的每个 FR/AC 满足 SMART 原则——具体（指向明确行为或产出）、可度量（有量化或可验证的标准）、可达成（在当前资源和约束下可实现）、相关（溯源到 KR 或 endStateGoal）、有时限（有预期完成的阶段或轮次）。
  - AC-18.6：Spec Review Gate（FR-02）在存在 OKR 树时，评审维度增加 SMART 合规性检查。不合规的 FR/AC 作为评审问题记录，严重级别为 P1。
  - AC-18.7：各 Gate（FR-02、FR-04、FR-06）在存在 OKR 树时，评估结论中增加目标对齐度评价（aligned / drifting / misaligned），作为参考信息附加到评审包中，不改变现有通过/阻断判定逻辑。
  - AC-18.8：Post-Release Validation（FR-17）在存在 OKR 树时，差距分析按 KR 逐条执行，每条 KR 产出达成状态（achieved / partially / not-achieved）和达成度百分比。
  - AC-18.9：Post-Release Validation 的 canComplete 判定在存在 OKR 树时升级为 KR 级——所有 KR 达成时 canComplete 为 true；任一 KR 未达成时 canComplete 为 false。无 OKR 树时 fallback 到现有 FR 级扫描逻辑，行为不变。
  - AC-18.10：canComplete 为 false 且存在 OKR 树时，Post-Release Validation 阶段内生成新工作包（针对未达成的 KR 的 SMART 任务），触发一轮 Implement→Review→Deploy→Validate 子循环。子循环在 Post-Release Validation 阶段内部管理，不回退 pipeline 主状态机，避免侵入 PipelineEngine 的单向推进逻辑。
  - AC-18.11：PDCA 循环有最大轮次上限（默认 3 轮，可通过 pipeline 创建参数或项目配置覆盖），超限后升级为人工介入，防止无限循环。每轮循环记录为 PdcaCycleRecord，包含轮次编号、触发原因（未达成的 KR 列表）、新增任务和轮次结果。
  - AC-18.12：`sevo demo` 在有 LLM 的环境中展示完整 PDCA 闭环——目标锁定 → OKR 拆解 → SMART 任务化 → 阶段执行 → 差距扫描 → 回环修复 → 收敛完成，用户可观察到至少一次回环过程。
  - AC-18.13：未传入 endStateGoal 的 pipeline，所有阶段行为与 FR-18 引入前完全一致——无 OKR 拆解、无 SMART 检查、无 KR 级差距分析、无 PDCA 回环。向后兼容零破坏。
  - AC-18.14：OKR 树、KR 达成度和 PDCA 轮次记录纳入 Ledger Entry 的证据链，可在驾驶舱和交付账本中查看。

### FR-19 终局交付自动推进（Endgame Delivery Automation）

- **定位**：Pipeline 级别的交付自动化机制。Review/Audit 通过后，自动推进 README 同步、版本管理、发布、终局差距扫描和用户通知，不需要用户手动触发。解决「代码是库不是引擎」的核心断点——阶段间推进从 prompt 软约束升级为程序化硬约束。
- **触发条件**：Pipeline 的 Review 阶段（FR-06）通过且所有验收阶段（FR-06b/06c/06d）通过后，自动进入终局交付链。
- **处理**：
  1. **README 同步**：检测项目 README 是否反映本次变更的新能力。如果 README 缺少新增 FR 的描述，自动生成 README 更新任务并派发。README 更新完成后进入下一步。
  2. **版本管理**：根据变更类型自动判定版本 bump 级别（patch：bug fix；minor：新功能；major：破坏性变更）。执行版本号 bump 并更新 package.json。
  3. **发布执行**：调用 OpenClaw 环境的发布 Adapter（如 npm publish + GitHub 同步 + ClawHub 同步）。发布失败时自动重试一次，仍失败则通知用户并阻断。
  4. **终局差距扫描**：发布后自动触发 Post-Release Validation（FR-17）。以 spec 全部 FR 为基准逐条对照当前实现。发现差距时自动生成修复任务，进入 PDCA 子循环（FR-18）。
  5. **差距修复循环**：差距修复任务完成后，重新进入 Review→Audit→终局交付链，循环到差距为零。
  6. **用户通知**：每个关键节点（审计通过、发布成功、差距扫描结果、最终完成）自动通知用户。通知内容包含版本号、新功能摘要、发布链接、差距状态。
  7. **阶段间推进机制**：PluginAdapter 的 hook handler 在 subagent_ended 事件中程序化调用 OpenClaw API 派发下一阶段任务，不依赖 prompt 注入。并行阶段通过 hook handler 一次性触发所有并行任务。
- **输出**：发布结果报告（Release Report，含版本号、平台链接、差距扫描结论）、用户通知记录。
- **执行阶段**：Review 通过后自动触发，贯穿 Deploy（FR-08）→ Verify（FR-09）→ Post-Release Validation（FR-17）→ Ledger（FR-10）。
- **验收标准**：
  - AC-19.1：Review 阶段（FR-06）所有子阶段通过后，Pipeline 自动进入终局交付链，不需要用户手动触发或主会话 prompt 驱动。
  - AC-19.2：终局交付链中，README 同步阶段检测 README 是否包含本次新增 FR 的描述。缺失时自动生成 README 更新任务；README 已包含时跳过。
  - AC-19.3：版本 bump 级别根据变更类型自动判定（patch/minor/major），执行 bump 并更新 package.json。判定规则可通过项目配置覆盖。
  - AC-19.4：发布阶段调用 PublishAdapter 执行发布。PublishAdapter 是接口，当前实现调用 publish-release.sh。
  - AC-19.5：发布失败时自动重试一次（间隔 30 秒）。重试仍失败时，Pipeline 状态设为 blocked，通知用户并附带错误信息。
  - AC-19.6：发布成功后自动触发 Post-Release Validation（FR-17），以 spec 全部 FR 为基准执行差距扫描。
  - AC-19.7：差距扫描发现未覆盖的 FR 时，自动生成修复工作包并触发 Implement→Review→终局交付 子循环。子循环复用 FR-18 的 PDCA 机制，共享最大轮次上限。
  - AC-19.8：终局交付链的每个关键节点（审计通过、README 更新完成、版本 bump 完成、发布成功/失败、差距扫描结果、最终完成）通过 NotificationAdapter 自动通知用户。
  - AC-19.9：NotificationAdapter 是接口。当前实现调用飞书 API 推送，通知渠道通过项目配置指定。
  - AC-19.10：阶段间推进通过 PluginAdapter 的 subagent_ended hook handler 程序化触发，不依赖 prompt 注入。hook handler 检测当前完成的阶段，调用 PipelineEngine.advance() 并通过 OpenClaw API 派发下一阶段任务。
  - AC-19.11：并行阶段（如 Test Case + UX Acceptance + Commercial Acceptance）通过 hook handler 一次性触发所有并行任务。所有并行任务完成后，hook handler 自动触发汇合点的下一阶段。
  - AC-19.12：整条终局交付链可通过项目配置关闭或部分关闭（如关闭自动发布但保留差距扫描）。未配置时默认全部启用。
  - AC-19.13：单 Agent 用户（无专职 PM/UX/审计 Agent）也能走完整终局交付链。角色知识注入（FR-15 渐进式披露）确保单 Agent 在每个阶段获得对应角色的专业标准。
  - AC-19.14：终局交付链的所有操作记录纳入 Ledger Entry 的证据链，包含 README diff、版本变更、发布结果、差距扫描报告、通知记录。
  - AC-19.15：Publish 阶段完成后、终局差距扫描之前，必须执行 liveness verification。liveness verification 读取项目的 SMART 目标配置（`pdca-liveness-config.json`），逐条执行 probe。任何 P0 probe 失败时，Publish 阶段不通过，必须修复后重新验证；P1 probe 失败时记录为待办，不阻断发布。liveness verification 的结果写入终局差距扫描报告。
  - AC-19.16（引擎与调度层职责边界）：终局交付自动推进中，SEVO 引擎的职责是状态机 + 触发器——感知当前节点、在需要行动时向调度层（主 Agent）推送提醒、接收确认后放行。引擎不做差距判定：差距分析由调度层派子 Agent 执行，结果回报给调度层，调度层确认后通知引擎。引擎不做任务拆解：修复任务的定义和派发由调度层负责。差距修复循环的终止条件：调度层通知引擎「差距 = 0」，引擎放行进入 Ledger。
  - AC-19.17：`sevo init` 执行时自动注册每日终局扫描 cron job（默认 04:30 本地时间，可通过 `sevo.config.json` 的 `endgameScan.schedule` 字段配置执行时间或关闭，设为 `"off"` 即禁用）。cron 调用 `sevo scan --endgame` 命令。注册失败时输出警告但不阻断 init 流程。定时触发与流水线内自动触发、手动触发并列，是终局扫描的三种触发方式之一。
  - AC-19.18：终局差距扫描发现 FAIL 项后，系统自动执行可修复性分析（通过 LLMAdapter 调用 LLM 判定），将 FAIL 项分为「可自动修复」和「需人工介入」两类。分类结果写入扫描报告。
  - AC-19.19：可自动修复的项通过 RepairAdapter 派发修复任务给 agent。修复任务包含结构化信息：失败检查项标识、失败原因、修复建议、目标文件路径。RepairAdapter 是接口，当前实现调用 `sessions_spawn` 派发 ACP agent。
  - AC-19.20：修复完成后自动重跑失败项的扫描验证（增量重跑，不重跑已 PASS 项）。验证通过 → 标记为 repaired；验证仍失败 → 进入下一轮修复或标记为 escalated。
  - AC-19.21：修复→验证循环最大轮次默认 3 轮（可通过 `endgameScan.repair.maxRounds` 配置）。超限后标记为 escalated，不再自动修复，等待人工介入。
  - AC-19.22：终局扫描结果的通知策略通过 NotificationAdapter（AC-19.9）配置。有 FAIL 项时立即通知（含失败项数量、摘要和修复状态）；全 PASS 时默认静默（可配置为每周汇总通知）。修复完成后发送修复结果通知（含修复项、验证结果、仍需人工介入的项）。通知渠道不绑定特定平台。
  - AC-19.23：终局扫描引擎通过三个 Adapter 接口实现通用化——RepairAdapter（修复任务派发）、LLMAdapter（语义评估）、NotificationAdapter（通知发送）。不绑定特定 agent 池、LLM provider 或通知渠道。缺少任何 Adapter 时对应能力降级但不中断扫描执行。


### FR-20 PDCA 自动 Check

- **定位**：跨阶段机制。为每个 SEVO 管理的项目提供基于 SMART 目标配置的自动化 liveness 检查能力。通过可扩展的 probe 函数库，定期或按需验证项目功能在运行时是否真正生效，弥补代码审计只检查逻辑正确性而不检查运行时行为的盲区。
- **输入**：项目的 SMART 目标配置文件（`pdca-liveness-config.json`）。
- **处理**：
  1. 读取项目根目录下的 `pdca-liveness-config.json`，解析 SMART 目标条目列表。
  2. 逐条执行 probe 命令，收集 PASS/FAIL 结果和失败原因。
  3. 输出标准化报告（JSON + 可读 markdown），包含每条目标的 goalId、描述、probe 命令、执行结果、失败原因。
  4. P0 失败时自动创建修复任务到看板。
  5. 支持 cron 定时执行和 CLI 手动触发。
- **输出**：PDCA Check 报告（PDCA Check Report），包含逐条 PASS/FAIL 结果、失败原因和自动创建的任务列表。
- **执行阶段**：跨阶段机制，可在 Post-Release Validation（FR-17）中被 Liveness Verification Gate（AC-19.15）调用，也可独立定时执行。
- **验收标准**：
  - AC-20.1：每个项目可在项目根目录定义 `pdca-liveness-config.json`，格式为 JSON 数组，每个条目包含 goalId（唯一标识）、description（目标描述）、metric（可度量指标）、probe（可执行的 shell 命令或内置函数名）、severity（P0/P1/P2）。
  - AC-20.2：PDCA Check 脚本读取配置后逐条执行 probe，每条 probe 输出标准化结果：goalId、status（PASS/FAIL）、reason（失败原因，PASS 时为空）、executedAt（执行时间戳）。汇总报告包含 totalGoals、passCount、failCount 和逐条 entries。
  - AC-20.3：PDCA Check 支持通过 cron 定时执行（建议每日 06:00），cron 配置在 `sevo init` 时自动注册，用户可通过 `sevo config` 修改执行频率或关闭。
  - AC-20.4：任何 severity 为 P0 的 probe 失败时，PDCA Check 自动通过看板 API（`local-subagent-board.js enqueue`）创建修复任务，任务描述包含 goalId、失败原因和关联的 FR 编号。
  - AC-20.5：probe 函数库内置以下检查函数，每个函数接受参数并返回 PASS/FAIL + reason：check_log_recent（检查日志文件最近 N 分钟内有新条目）、check_sqlite（执行 SQL 查询并验证结果非空或满足条件）、check_npm_version（验证 npm 包已发布且版本号匹配）、check_file_exists（验证文件存在且非空）、check_hook_registered（验证指定 hook 在 OpenClaw 配置中已注册且 import 路径可解析）。函数库可通过在配置中指定自定义 shell 命令扩展，不需要修改 PDCA Check 源码。
  - AC-20.6：新项目接入 PDCA Check 只需在项目根目录创建 `pdca-liveness-config.json` 并添加条目，不需要修改 PDCA Check 脚本或注册额外配置。
  - AC-20.7：probe 函数库支持 LLM 调用类型的 probe。配置条目的 probe 字段支持 `llm:` 前缀（如 `llm:check_semantic_quality`），执行时调用 OpenClaw 环境的 LLM 能力进行语义级质量检查（如文档可读性评估、代码注释质量评分、错误提示友好度判定）。LLM probe 的判定结果必须包含置信度分数和判定依据文本，置信度低于阈值（默认 0.7）时标记为 INCONCLUSIVE 而非 FAIL，避免误判。

### FR-21 SMART 目标声明

- **定位**：Specify 阶段的强制质量门禁增强。要求每个 SEVO 管理的项目在 Specify 阶段声明 SMART 目标，并将目标与 FR 和 liveness probe 关联，确保每个功能需求都有可度量、可自动验证的终局验收标准。
- **输入**：项目的需求规格包（Spec Package）。
- **处理**：
  1. Specify 阶段产出 Spec Package 时，同步产出或更新项目的 SMART 目标声明。
  2. 每个 SMART 目标关联到一个或多个 FR，每个 FR 至少关联一个可度量的 liveness probe。
  3. SMART 目标在 Publish 阶段被 Liveness Verification Gate（AC-19.15）消费，驱动 PDCA Check（FR-20）执行。
  4. Spec Review Gate（FR-02）增加 SMART 目标完整性检查维度。
- **输出**：SMART 目标声明文档（作为 Spec Package 的组成部分）+ 项目的 `pdca-liveness-config.json` 初始版本。
- **执行阶段**：Specify 阶段内嵌，与 FR-01 Spec 同步执行。
- **验收标准**：
  - AC-21.1：每个 SEVO 管理的项目在 Specify 阶段必须声明 SMART 目标。每个目标包含五个维度：Specific（指向明确的功能行为或产出）、Measurable（有量化或可自动验证的指标）、Achievable（在当前资源和约束下可实现）、Relevant（溯源到项目的 endStateGoal 或 OKR 树中的 KR）、Time-bound（有预期完成的阶段或时间点）。
  - AC-21.2：每个 FR 至少关联一个可度量的 liveness probe。probe 定义写入 `pdca-liveness-config.json`，包含 goalId、关联的 FR 编号、probe 命令和预期结果。FR 与 probe 的关联关系在 Spec Package 中可追溯。
  - AC-21.3：SMART 目标在 Publish 阶段被 Liveness Verification Gate（AC-19.15）消费。Liveness Verification Gate 读取 `pdca-liveness-config.json`，调用 PDCA Check（FR-20）逐条执行 probe，根据结果决定 Publish 是否通过。
  - AC-21.4：缺少 SMART 目标的项目，Spec Review Gate（FR-02）增加一条检查维度——SMART 目标完整性。检查项包括：是否存在 SMART 目标声明、每个 FR 是否关联了 probe、probe 定义是否完整。任一检查不通过时，作为 P1 问题记录到 Spec Review Bundle，阻断进入 Contract 阶段。
  - AC-21.5：项目配置文件（`sevo.config.json`）支持 `probeExempt` 字段，值为数组，每个元素包含 `frId`（豁免的 FR 编号）和 `reason`（豁免原因）。被豁免的 FR 在 liveness report 中标记为 "exempt"，不计入 PASS 也不计入 FAIL，不影响整体通过率计算。豁免原因在报告的 entries 中展示，供人工审查。默认值为空数组（无豁免）。

### FR-22 角色-任务匹配调度约束（Role-Task Dispatch Constraint）

- **定位**：跨阶段机制。流水线每个阶段有明确的角色要求，调度器在派发阶段任务前必须校验目标 Agent 的角色标签是否匹配阶段要求，防止角色越权导致产出质量不达标。
- **角色-阶段映射（默认）**：
  - Specify（FR-01）、Spec Review Gate（FR-02）、Commercial Acceptance Authoring（FR-02c）、PM Commercial Review（FR-06d）→ Product 角色
  - UX Acceptance Authoring（FR-02b）、UX Acceptance（FR-06c）→ UX 角色
  - Contract（FR-03）、Contract Review Gate（FR-04，开发维度）→ Architect 角色
  - Implement（FR-05）、Smoke Test（FR-06b）→ Coder 角色
  - Review（FR-06）、Regression（FR-07）→ Auditor 角色
  - Deploy（FR-08）、Verify（FR-09）、Ledger（FR-10）→ 任意角色（系统自动执行或可配置）
- **输入**：阶段任务的派发请求（含目标阶段、候选 agentId）、Agent 角色注册表。
- **处理**：
  1. PipelineEngine 在通过 OpenClaw Adapter 触发阶段执行前，查询 Agent 角色注册表，获取候选 Agent 的角色标签。
  2. 比对候选 Agent 的角色标签与当前阶段的角色要求。
  3. 角色匹配 → 正常派发。
  4. 角色不匹配 → 生成审计事件（包含阶段名、要求角色、实际角色、agentId），记录到调度审计日志。多 Agent 环境下阻断派发并提示选择正确角色的 Agent；单 Agent 环境下降级为警告，允许派发但在审计日志中标注"角色降级"。
  5. Agent 角色注册表在 `sevo init` 时自动生成（基于 Agent 命名规则和 runtime type 推断），用户可通过配置文件手动覆盖。
- **输出**：角色校验结果（通过/警告/阻断）、审计事件记录。
- **执行阶段**：跨阶段机制，嵌入 PipelineEngine（FR-13）的阶段派发逻辑中。
- **验收标准**：
  - AC-22.1：每个流水线阶段在 Stage 定义中声明所需的角色类型（requiredRole），角色类型为枚举值：product、ux、architect、coder、auditor、any。
  - AC-22.2：PipelineEngine 在派发阶段任务前，自动校验候选 Agent 的角色标签是否匹配阶段的 requiredRole。校验逻辑在 OpenClaw Adapter 触发执行之前执行。
  - AC-22.3：角色不匹配时，系统生成结构化审计事件，包含字段：timestamp、pipelineInstanceId、stageName、requiredRole、actualRole、agentId、action（blocked/warned）。审计事件写入调度审计日志。
  - AC-22.4：多 Agent 环境下，角色匹配的默认严重级别由配置项 `strictRoleMatching: boolean` 决定。`strictRoleMatching=false`（默认）时，blocked dispatch 在 `sevo doctor` 输出为 warn、不计入 Errors，PipelineEngine 派发时使用兜底 agent（按 ux→product→architect→coder→auditor 优先顺序选择最近的可用角色）并写入 `role-degraded` 审计事件。`strictRoleMatching=true` 时，blocked dispatch 在 doctor 输出为 error 并阻断派发，要求用户显式补齐角色映射。两种模式都禁止静默忽略。
  - AC-22.5：单 Agent 环境下（Agent 池中只有一个 Agent 或无匹配角色的 Agent），角色不匹配时降级为警告，允许派发，审计事件的 action 字段标注为 warned，日志中标注"角色降级：单 Agent 环境"。
  - AC-22.6：Agent 角色注册表支持两种来源：自动推断（`sevo init` 基于 Agent 命名规则和 runtime type 生成）和手动配置（用户在 SEVO 配置文件中显式指定 agentId → role 映射）。手动配置优先级高于自动推断。
  - AC-22.7：角色-阶段映射可通过 SEVO 配置文件自定义。用户可修改任意阶段的 requiredRole，新增自定义阶段时可指定角色要求。
  - AC-22.8：`sevo init` 产出的角色分配表（已有 AC-14.12）包含每个 Agent 的推断角色和每个阶段的角色要求，用户可在此确认或修改。
  - AC-22.9：陌生宿主自适应。`sevo init` 禁止硬编码 `dev-01` / `dev-02` / `cc` 等 SEVO 维护者私有 agent ID 作为默认 roleAssignment.agentRoles。生成逻辑必须：(a) 读取宿主 `openclaw.json`（路径解析顺序：`process.env.OPENCLAW_CONFIG_PATH` → cwd 向上探测 → 抛错），枚举已注册 agent；(b) 按命名模式 + runtime type 自动分类到 product / ux / architect / coder / auditor 五种角色；(c) 任一角色无 agent 时，自动用宿主主 agent 或第一个可用 agent 兜底，并在 roleAssignment 中标注 `autoFallback: true`；(d) 零 agent 注册环境下生成占位 `{ "self": ["product","ux","architect","coder","auditor"] }` 并提示用户后续手动替换。生成结果写入 sevo.config 后，`sevo doctor` 在该配置下必须报 `Errors: 0`。
  - AC-22.10：配置 schema 新增 `strictRoleMatching: boolean` 字段，默认 `false`。`sevo init` 生成的初始配置必须显式写入该字段（默认 false）并附注释说明取值含义；用户可通过编辑配置文件或 CLI flag `--strict-role-matching` 切换严格模式。配置变更后立即生效，不要求重新 init。

### FR-23 Executable Gate Evaluators（可执行门禁评估器）

- **定位**：跨阶段机制。为流水线门禁引入可执行评估脚本，产出确定性 pass/fail 判定和量化分数，与现有 GateVerdict / ImplementationReviewGate 的 LLM 评估互补。评估器是可选增强——没有挂载评估器的门禁退化为纯 LLM 评估，向后兼容。
- **核心原则**：谁写代码，谁就不能碰评分标准。评估器由独立于编码 Agent 的角色编写和维护，编码 Agent 对评估器目录只有只读权限（隔离机制见 FR-24）。
- **输入**：阶段产出工件（Implementation Bundle、Review Bundle 等）、项目配置中的评估器注册表、评估器脚本。
- **处理**：
  1. PipelineEngine 在门禁评估阶段，读取项目配置中当前阶段挂载的评估器列表。
  2. 按注册顺序依次执行每个评估器脚本，传入标准化输入（JSON 格式，包含阶段名、工件路径、项目元数据）。
  3. 每个评估器脚本输出标准化结果（JSON 格式，包含 verdict: pass/fail、score: 0-100、details: 问题明细数组）。
  4. 汇总所有评估器结果，任一评估器 verdict 为 fail 则门禁整体不通过。
  5. 评估器执行超时（默认 60s，可配置）时标记为 error，不等同于 pass。
  6. 评估器列表为空时，门禁退化为纯 LLM 评估（现有行为不变）。
- **输出**：评估器执行结果集（Evaluator Result Set），包含每个评估器的 verdict、score、details 和执行耗时。
- **执行阶段**：嵌入所有门禁阶段（Spec Review Gate、Contract Review Gate、Review、Regression 等）的评估流程中。
- **评估器标准协议**：
  - 输入：通过 stdin 接收 JSON，schema 为 `{ stage: string, artifactPaths: string[], projectMeta: object }`。
  - 输出：通过 stdout 输出 JSON，schema 为 `{ verdict: "pass" | "fail", score: number (0-100), details: Array<{ rule: string, passed: boolean, message: string }> }`。
  - 退出码：0 = 正常执行（verdict 由输出决定），非 0 = 评估器自身错误（视为 error，不等于 fail）。
  - 运行时：评估器脚本可以是任意可执行文件（shell、Node.js、Python 等），只要遵循 stdin/stdout JSON 协议。
- **评估器注册机制**：
  - 项目配置文件（`sevo.config.json` 或 `package.json` 的 sevo 字段）中声明评估器挂载关系。
  - 注册格式：`{ evaluators: { "<stageName>": [{ name: string, script: string, timeout?: number }] } }`。
  - `script` 路径相对于项目根目录的 `evaluators/` 目录。
  - 同一阶段可挂载多个评估器，按数组顺序执行。
- **内置评估器（开箱即用）**：
  - `test-pass-rate`：解析测试执行结果，计算通过率，低于阈值（默认 100%）则 fail。
  - `lint-score`：执行 lint 检查，输出违规数量和严重级别分布。
  - `spec-ac-coverage`：从 Spec Package 提取 AC 列表，扫描实现代码和测试，输出 AC 覆盖矩阵。
  - `dependency-audit`：检查依赖安全漏洞（调用 `npm audit` 或等效工具）。
  - 内置评估器随 `sevo` npm 包分发，`sevo init` 时自动复制到项目 `evaluators/` 目录。
- **验收标准**：
  - AC-23.1：项目配置中可声明每个门禁阶段挂载的评估器列表，PipelineEngine 在门禁评估时按列表顺序执行。
  - AC-23.2：评估器通过 stdin 接收标准化 JSON 输入，通过 stdout 输出标准化 JSON 结果，退出码区分正常执行和评估器自身错误。
  - AC-23.3：任一评估器 verdict 为 fail 时，门禁整体结论为不通过，结果中列出所有失败评估器的 details。
  - AC-23.4：评估器列表为空时，门禁退化为纯 LLM 评估，现有 GateVerdict / ImplementationReviewGate 行为不变。
  - AC-23.5：评估器执行超时时标记为 error 并记录到结果集，不等同于 pass，不静默跳过。
  - AC-23.6：`sevo init` 自动将内置评估器复制到项目 `evaluators/` 目录，用户可直接使用或修改。
  - AC-23.7：评估器脚本支持任意可执行文件格式（shell、Node.js、Python 等），只要遵循标准协议。
  - AC-23.8：评估器执行结果集作为门禁工件的一部分，纳入 Ledger 证据链，可追溯每个评估器的 verdict、score 和 details。

### FR-24 Evaluation-Implementation Workspace Isolation（评估-实现工作区隔离）

- **定位**：跨阶段机制。物理隔离编码 Agent 的可编辑范围与评估器代码，确保「谁写代码，谁就不能碰评分标准」的原则在 OS 层面强制执行，而非仅依赖 prompt 约束。
- **核心原则**：编码 Agent 的可写范围限制在 `src/` 和 `tests/`，`evaluators/` 目录对编码 Agent 只读。隔离优先用 L0 层（OS 文件权限）实现，L4 层（ACP harness 约束）做冗余兜底。
- **输入**：项目目录结构、Agent 角色注册表（FR-22）、OpenClaw 环境能力。
- **处理**：
  1. Pipeline Create（FR-12）初始化项目目录时，自动创建 `evaluators/` 目录并设置文件权限。
  2. L0 层隔离（OS 文件权限）：`evaluators/` 目录的 owner 设为非编码 Agent 的执行用户（如 root 或专用 evaluator 用户），编码 Agent 的执行用户只有 read + execute 权限，无 write 权限。具体实现取决于 OpenClaw 环境是否支持多用户隔离。
  3. L4 层隔离（ACP harness 约束）：在编码 Agent 的 session 配置中注入文件写入白名单（`allowedWritePaths: ["src/**", "tests/**"]`），禁止写入 `evaluators/`、`docs/` 等目录。ACP harness 在工具调用层拦截越界写入。
  4. L6 层冗余（prompt 注入）：Implement 阶段的执行原则注入（§6.6）中增加「禁止修改 evaluators/ 目录」的显式约束。
  5. 隔离状态在 pipeline 创建时校验，校验失败时记录警告但不阻断（OpenClaw 环境可能不支持 L0 层隔离）。
- **输出**：隔离状态报告（Isolation Status），包含 L0/L4/L6 各层的生效状态。
- **执行阶段**：Pipeline Create（FR-12）的目录初始化步骤 + Implement（FR-05）的执行环境准备。
- **标准目录结构扩展**：
  ```
  <workspace>/projects/<project-slug>/
  ├── src/                  # 编码 Agent 可写
  ├── tests/                # 编码 Agent 可写
  ├── evaluators/           # 编码 Agent 只读，评估器脚本存放
  │   ├── test-pass-rate.sh
  │   ├── lint-score.js
  │   ├── spec-ac-coverage.py
  │   └── ...
  ├── docs/                 # 编码 Agent 只读
  └── ...
  ```
- **验收标准**：
  - AC-24.1：Pipeline Create 初始化项目目录时，自动创建 `evaluators/` 目录。
  - AC-24.2：OpenClaw 环境支持多用户隔离时，`evaluators/` 目录的文件权限设置为编码 Agent 执行用户只读（L0 层）。
  - AC-24.3：编码 Agent 的 session 配置中注入文件写入白名单，禁止写入 `evaluators/` 目录（L4 层）。
  - AC-24.4：Implement 阶段的执行原则注入中包含「禁止修改 evaluators/ 目录」的显式约束（L6 层）。
  - AC-24.5：编码 Agent 尝试写入 `evaluators/` 目录时，至少有一层隔离机制拦截并记录审计事件。
  - AC-24.6：OpenClaw 环境不支持 L0 层隔离时，系统记录警告并依赖 L4 + L6 层兜底，不阻断 pipeline 执行。
  - AC-24.7：隔离状态报告纳入 Pipeline Create 的产出工件，记录各层生效状态，可追溯。
  - AC-24.8：评估器的编写和修改只能由非 Coder 角色（Auditor、Architect、Product）执行，角色校验复用 FR-22 的角色-任务匹配机制。

### FR-25 Hybrid Evaluation Mode（混合评估模式）

- **定位**：跨阶段机制。定义可执行评估器与 LLM 评估的协作模式——可执行评估器处理确定性检查（测试通过率、覆盖率、lint 分数、spec AC 覆盖），LLM 评估处理模糊判断（代码质量、架构合理性、命名可读性）。两者结果汇总为统一的门禁判定。
- **输入**：可执行评估器结果集（FR-23 产出）、LLM 评估结论（现有 GateVerdict 产出）。
- **处理**：
  1. 可执行评估器先于 LLM 评估执行（fast-fail：确定性检查不通过时，跳过 LLM 评估，节省 token 和时间）。
  2. 可执行评估器全部 pass 后，触发 LLM 评估。
  3. LLM 评估接收可执行评估器的量化结果作为上下文（如覆盖率 95%、lint 违规 3 项），辅助做出更精准的模糊判断。
  4. 最终门禁判定：可执行评估器任一 fail → 整体 fail；可执行评估器全 pass + LLM 评估 fail → 整体 fail；两者都 pass → 整体 pass。
  5. 门禁结果中明确标注每个判定的来源（evaluator / llm），便于定位问题。
- **输出**：混合评估结果（Hybrid Evaluation Result），包含可执行评估器结果集、LLM 评估结论和最终汇总判定。
- **执行阶段**：嵌入所有门禁阶段的评估流程中，作为 FR-23 和现有 GateVerdict 的编排层。
- **验收标准**：
  - AC-25.1：可执行评估器在 LLM 评估之前执行，任一评估器 fail 时跳过 LLM 评估，门禁直接判定为不通过。
  - AC-25.2：可执行评估器全部 pass 后，LLM 评估自动触发，且接收评估器的量化结果作为评估上下文。
  - AC-25.3：最终门禁判定遵循「任一层 fail 则整体 fail」的逻辑，不存在可执行评估器 fail 但门禁 pass 的情况。
  - AC-25.4：门禁结果中每个判定条目标注来源（evaluator / llm），可区分确定性检查失败和模糊判断失败。
  - AC-25.5：没有挂载可执行评估器时，门禁完全退化为纯 LLM 评估，行为与 FR-23 引入前一致。
  - AC-25.6：混合评估结果作为门禁工件的一部分，纳入 Ledger 证据链。
  - AC-25.7：LLM 评估的 prompt 中自动注入可执行评估器的量化摘要（如「测试通过率 100%，lint 违规 0 项，AC 覆盖率 95%」），LLM 不需要重复检查已有确定性结论的维度。

### FR-26 Ratchet Mechanism（棘轮机制）

- **定位**：跨阶段机制（可选）。针对性能优化、重构等改进类任务，支持固定时间预算内的自动试错——改进则保留，退步则自动回退（git reset）。棘轮机制是 Implement 阶段的可选增强，不影响常规开发流程。
- **触发条件**：项目配置中为特定 FR 或工作包启用棘轮模式（`ratchet: { enabled: true, timeBudgetSeconds: number, baselineMetric: string, baselineValue: number }`）。
- **输入**：工作包、基线指标（如测试执行时间、包体积、响应延迟）、时间预算、关联的可执行评估器（FR-23）。
- **处理**：
  1. Implement 阶段开始前，记录基线快照（git commit SHA + 基线指标值）。
  2. 编码 Agent 在时间预算内执行优化实现。
  3. 实现完成后（或时间预算耗尽时），运行关联的可执行评估器，获取优化后的指标值。
  4. 比较优化后指标与基线：改进（指标优于基线）→ 保留变更，提交 commit；退步（指标劣于基线）→ 自动 `git reset --hard` 到基线 SHA，记录回退原因。
  5. 时间预算耗尽且未产出改进 → 回退到基线，标记为「预算内未达成改进」，不视为 pipeline 失败。
  6. 棘轮结果写入 Stage Record，包含基线值、优化后值、是否保留、回退原因（如有）。
- **输出**：棘轮执行结果（Ratchet Result），包含基线快照、优化后指标、保留/回退决定和执行耗时。
- **执行阶段**：Implement（FR-05）的可选增强模式。
- **验收标准**：
  - AC-26.1：项目配置中可为特定工作包启用棘轮模式，配置包含时间预算、基线指标名称和基线值。
  - AC-26.2：棘轮模式启用时，Implement 阶段开始前自动记录基线快照（git commit SHA + 指标值）。
  - AC-26.3：优化后指标优于基线时，变更被保留并提交；劣于基线时，自动 `git reset --hard` 到基线 SHA。
  - AC-26.4：时间预算耗尽且未产出改进时，自动回退到基线，不视为 pipeline 失败，Stage Record 中标记「预算内未达成改进」。
  - AC-26.5：棘轮执行结果纳入 Stage Record 和 Ledger 证据链，包含基线值、优化后值和保留/回退决定。
  - AC-26.6：棘轮模式未启用时，Implement 阶段行为与 FR-05 定义完全一致，无任何副作用。
  - AC-26.7：棘轮的指标比较依赖可执行评估器（FR-23）产出的 score，不依赖 LLM 主观判断。
  - AC-26.8：回退操作（git reset）执行前记录审计事件，包含回退原因、基线 SHA 和被丢弃的变更摘要。

### FR-27 Flexible Stage Entry（任意阶段切入）

- **定位**：生命周期操作。允许用户从流水线的任意阶段开始执行，而非强制从 spec 开始。这是 SEVO 开箱即用的核心能力——已有代码的项目可以直接从 implement、review、deploy 等阶段切入。
- **与 FR-12 的关系**：FR-27 复用 FR-12 的实例创建逻辑（Pipeline Create），在创建实例时额外将起始阶段之前的阶段标记为 skipped。FR-27 不是平行实现，而是 FR-12 创建流程的扩展入口。
- **触发条件**：用户通过 `sevo:from <project-slug> <stage>` 命令指定起始阶段，或主会话调度时在 label 中包含 `from:<stage>` 标记。
- **输入**：Project 标识、目标起始阶段、任务描述。
- **合法阶段标识**：`spec`、`contract`、`implement`、`review`、`deploy`、`verify`。Gate 阶段（`spec-review-gate`、`contract-review-gate`、`publish-generalization-gate`）及辅助阶段（`test-case-authoring`、`smoke-test`、`ux-acceptance`、`e2e-verification`、`regression`、`ledger`）不允许作为切入点。
- **处理**：
  1. 解析命令或 label：识别 `sevo:from <project> <stage>` 格式，或从任务 label 中提取 `from:<stage>` 标记。
  2. 校验目标阶段是否在合法阶段标识列表中；若为 gate 阶段或非法标识，返回错误。
  3. 校验 Project 是否已存在（已有代码/spec 的项目才能跳过前置阶段）。
  4. 若 `sevo:from <project> spec`，等价于 `sevo:create <project>`，直接转发至 FR-12 创建流程。
  5. 若该 Project 已有 active pipeline（FR-12 AC-4.57），拒绝创建并返回错误提示。
  6. 调用 FR-12 的实例创建逻辑，将起始阶段之前的所有阶段标记为 skipped（附跳过理由："用户指定从 <stage> 开始"）。
  7. 校验 Tier 路由兼容性：若用户指定的阶段不在该任务 Tier 的阶段集合中，返回错误。
  8. 直接进入目标阶段，注入该阶段对应的 prompt 模板和质量门禁。
  9. 从目标阶段开始，后续阶段按正常流水线顺序推进。
- **输出**：FR 流程实例（含跳过阶段记录、起始阶段标识）。
- **执行阶段**：Pipeline Create 的扩展入口（复用 FR-12 实例创建逻辑）。
- **验收标准**：
  - AC-27.1：`sevo:from <project> <stage>` 命令被正确解析，合法阶段标识为 `spec`、`contract`、`implement`、`review`、`deploy`、`verify`。Gate 阶段（`spec-review-gate`、`contract-review-gate`、`publish-generalization-gate`）作为切入点时返回明确错误。
  - AC-27.2：起始阶段之前的阶段在 Stage Record 中标记为 skipped，包含跳过理由。
  - AC-27.3：从目标阶段开始，后续阶段推进逻辑与从头创建的流水线完全一致（复用 FR-12 推进机制）。
  - AC-27.4a：Project 目录不存在时，只允许从 `spec` 切入（等价于 `sevo:create`）。
  - AC-27.4b：跳过 `spec` 阶段时，必须存在 spec 文件（`product-requirements.md`），否则拒绝。
  - AC-27.4c：跳过 `contract` 阶段时，建议存在架构文件（非强制，仅警告）。
  - AC-27.5：陌生用户通过 `sevo:from myproject implement` 可以直接对已有代码启动 implement→review→deploy→verify 流程，无需先走 spec。
  - AC-27.6：主会话调度修复类任务时，可通过 label 中包含 `from:<stage>` 标记告知 SEVO 插件从哪个阶段切入。SEVO 插件解析 label 中的 `from:` 前缀，提取阶段标识后自动创建对应的流程实例。
  - AC-27.7：`sevo:from <project> spec` 等价于 `sevo:create <project>`，直接转发至 FR-12 创建流程。
  - AC-27.8：已有 active pipeline 的 Project 拒绝重复创建（引用 FR-12 AC-4.57）。
  - AC-27.9：用户指定的阶段不在该任务 Tier 的阶段集合中时，返回明确错误提示。

### FR-28 Clean-Install Verification Gate（发版前干净环境端到端验证）

- **定位**：发布阶段门禁。FR-17（Post-Release Validation Gate）验证的是「当前环境中 FR 是否覆盖」，但当前环境可能存在手动放置的文件、已有数据、历史配置等隐性依赖。本 FR 补全最后一公里：在隔离的干净环境中模拟陌生用户从零安装，验证产品端到端可用。
- **与 FR-17 的关系**：FR-17 是 FR 级差距扫描（代码覆盖 + 运行态存在性），FR-28 是环境级端到端验证（干净环境从安装到产出价值的完整链路）。FR-28 在 FR-17 通过之后、Ledger 之前执行。两者互补，不替代。
- **与 FR-19 AC-19.15 的关系**：AC-19.15 的 liveness verification 在当前环境执行 probe，FR-28 在隔离环境执行完整安装+初始化+功能验证。FR-28 覆盖范围更广（包含安装和初始化过程），liveness verification 覆盖深度更细（针对已部署服务的健康探针）。
- **触发条件**：FR-17 Post-Release Validation 通过（gaps === 0）后，流水线自动进入 clean-install-verification 阶段。
- **输入**：已发布的 npm 包名+版本、spec 中的 FR 列表、项目声明的运行态组件清单。
- **处理**：
  1. 创建隔离验证目录（`/tmp/stranger-verify-<instance-id>/`），确保不继承当前 workspace 的任何文件、环境变量或配置。
  2. L1 机械层验证：
     - `npm install -g <包名>@<版本>` 安装成功。
     - CLI 入口存在且 `--help` 正常输出。
     - `init` 命令执行成功，生成的配置文件完整且合法。
     - 错误提示可理解、可操作（非 stack trace）。
  3. L2 运行层验证：
     - init 后所有声称的运行态组件（hook、cron job、数据库文件、服务进程）都存在。
     - 每个运行态组件可被触发（hook 能响应事件、cron 脚本能手动执行、DB 能查询、服务能响应请求）。
     - 配置文件中引用的路径和依赖在隔离环境中都可解析。
  4. L3 价值层验证：
     - 每个 spec 中声明的核心功能，执行一次完整的端到端数据流：从用户输入到系统产出。
     - 产出必须是有意义的结果（非空数据库、非空报告、非默认模板、非报错）。
     - 首次使用路径在 5 分钟内可完成，且产出让用户感受到产品核心价值。
  5. 生成结构化验证报告（Clean-Install Verification Report），包含三层各检查项的 pass/fail 状态和失败详情。
  6. 清理隔离验证目录。
- **输出**：Clean-Install Verification Report（结构化 JSON + 人类可读摘要）。
- **阻断条件**：任何一层存在 fail 项时，canComplete 为 false，流水线阻塞，不进入 Ledger。
- **执行阶段**：clean-install-verification（位于 post-release-validation 之后、ledger 之前）。
- **验收标准**：
  - AC-28.1：FR-17 通过后，流水线自动进入 clean-install-verification 阶段，无需人工触发。L0 微小改动（Tier 路由判定为 L0）跳过此阶段。
  - AC-28.2：验证在隔离目录中执行，该目录不包含当前 workspace 的任何文件、不继承项目特有的环境变量。验证结束后目录被清理。
  - AC-28.3：L1 机械层——`npm install -g`、CLI `--help`、`init` 命令三项全部通过才算 L1 pass。任一失败即整体 fail，附带具体错误输出。
  - AC-28.4：L2 运行层——init 后项目声明的每个运行态组件（在 spec 或项目配置中注册）都存在且可触发。组件清单从项目的 `sevo.config.json` 或 spec 的 FR 描述中提取。
  - AC-28.5：L3 价值层——spec 中每个标记为核心功能的 FR，至少有一条端到端数据流验证通过（输入→处理→有意义产出）。「有意义」的判定标准：产出非空、非默认模板、非错误信息。
  - AC-28.6：验证报告包含 `{ l1: {pass, checks[]}, l2: {pass, checks[]}, l3: {pass, checks[]}, overall: pass|fail, failedChecks[] }` 结构。报告写入项目的 `docs/clean-install-report.json`。
  - AC-28.7：验证失败时，自动生成修复任务列表（fixTasks），每条包含失败层级、检查项标识和修复建议。调度层负责派发修复任务，修复完成后重新发版并再次触发 FR-28 验证。
  - AC-28.8：已有脚本 `scripts/npm-stranger-verify.sh` 作为 L1 层的默认实现。L2/L3 层验证逻辑由项目在 `sevo.config.json` 中声明验证步骤（`cleanInstallChecks.l2[]` 和 `cleanInstallChecks.l3[]`），SEVO 引擎按声明顺序执行。
  - AC-28.9：单 Agent 用户也能走完 clean-install-verification。验证逻辑内置于 SEVO CLI（`sevo verify --clean-install`），不依赖专职验证 Agent。多 Agent 环境下由调度层派非开发 Agent 执行验证（禁止开发者自验）。
  - AC-28.10（引擎与调度层职责边界）：SEVO 引擎在 post-release-validation 通过后自动触发 clean-install-verification 阶段，向调度层推送验证提醒。验证执行由调度层负责（派 Agent 或直接调用 `sevo verify --clean-install`）。验证结果回报给引擎，引擎根据 overall pass/fail 决定放行或阻塞。

### FR-29 Tiered Endgame Gap Scan（分层终局差距扫描）

- **定位**：终局差距扫描的分层升级。当前差距扫描仅做文件级覆盖检查（L1），无法发现「代码存在但 AC 未覆盖」和「功能存在但运行态无意义产出」两类深层缺口。本 FR 将终局差距扫描升级为三层体系（L1 文件级 → L2 AC 级 → L3 运行态），逐层加深验证粒度，确保发版产物从「代码存在」到「功能可用且有意义」全链路闭合。
- **与 FR-17 的关系**：FR-17 定义 Post-Release Validation Gate 的整体框架，FR-29 细化其中「差距扫描」环节的分层执行标准和触发时机。FR-17 是门禁容器，FR-29 是门禁内部的扫描引擎规格。
- **与 FR-28 的关系**：FR-28 在隔离干净环境中做端到端验证（陌生用户视角），FR-29 在当前开发环境中做 spec→代码→运行态的逐层对照（开发者视角）。FR-28 验证「装上能用」，FR-29 验证「每条需求都有实现且实现有效」。两者互补，不替代。

#### L1 文件级扫描（快速覆盖检查）

- **目标**：确认每个 FR 有对应代码文件、编译通过、测试全绿。
- **触发时机**：每次 implement 阶段完成后自动触发。
- **耗时预期**：10 分钟内。
- **检查内容**：
  - 每个 FR 至少有一个对应的源码文件（通过项目的 FR→文件映射表或目录约定判定）。
  - `tsc`（或项目对应的编译命令）零错误通过。
  - 项目测试套件全绿（`npm test` 或等效命令退出码为 0）。
- **产出**：L1 扫描报告（`docs/gap-scan-l1.json`），包含每个 FR 的 covered/uncovered 状态和编译/测试结果。

#### L2 AC 级深度扫描（三阶段语义流水线）

- **目标**：逐条 AC 对照代码逻辑，确认每条 AC 都有实现代码和对应测试。采用三阶段流水线架构，在保证语义准确性的同时将 token 消耗降低 95% 以上（相比逐条 AC 独立调用 LLM）。
- **触发时机**：endgame 阶段发版前强制执行；支持独立 cron 定期扫描（不依赖 pipeline endgame 触发）。
- **耗时预期**：5-15 分钟（三阶段流水线，LLM 调用次数 ≤ 批次数 + 可疑项数）。
- **扫描范围**：通过 `scanDirs` 配置项指定待扫描目录列表（相对于项目根目录），默认扫描整个项目（`['.']`），不限于 `src/`。支持配置 `extensions`（文件扩展名白名单）和 `ignoreDirs`（忽略目录黑名单）。
- **三阶段架构**：

  **Phase 1: Code Map Generation（纯静态分析，零 LLM 调用）**
  - 遍历所有配置的 scanDirs，对每个源码文件提取：相对路径、导出符号列表（函数/类/变量名）、文件头注释摘要。
  - 产出紧凑文本表示（每文件约 100-200 字符），作为 Phase 2 的输入上下文。
  - 不依赖 LLM，纯文件系统读取 + 正则提取，确保零成本、确定性、可重复。

  **Phase 2: Batch Triage（批量初筛，1-N 次 LLM 调用）**
  - 将全部 AC 列表与 Phase 1 产出的代码地图一起发送给 LLM（利用大 context window 模型一次性处理）。
  - 按 `batchSize`（默认 150 条 AC/批）分批，每批一次 LLM 调用。
  - LLM 对每条 AC 做三分类：`covered`（代码地图中有充分证据）、`suspect`（有部分证据但不确定）、`uncovered`（无证据）。
  - 对 covered/suspect 的 AC，标注最可能的实现文件路径。
  - 禁止关键词匹配、正则表达式或文件名推断作为分类依据，必须基于语义理解。

  **Phase 3: Precise Verification（精确验证，仅对可疑项）**
  - 仅对 Phase 2 判定为 `suspect` 或 `uncovered` 的 AC 执行精确验证。
  - 读取 Phase 2 标注的候选文件实际源码内容，连同 AC 描述发送给 LLM。
  - LLM 判定每条 AC 的最终状态（covered/uncovered/needs-review）、置信度评分、证据文件路径和行号范围。
  - 低置信度（<0.7）的映射标记为 needs-review。

- **Token 效率**：三阶段设计将 LLM 调用从 O(AC数量) 降低到 O(批次数 + 可疑项数量)。典型项目（~285 文件、~50 条 AC）总消耗约 30K tokens，相比逐条调用（~6.5M tokens）降低 99%+。
- **产出**：AC 覆盖率报告（`docs/gap-scan-l2.json`），每条 AC 标注 covered/uncovered/needs-review + 置信度 + 证据文件路径 + 代码行号范围。扫描日志（`docs/gap-scan-l2-log.json`）记录每次 LLM 调用的 prompt 和响应，确保可追溯。

#### L3 运行态验证（活性与有意义产出验证）

- **目标**：在真实环境中触发功能，验证产出非空且有意义。
- **触发时机**：npm publish 成功后 OR 任何涉及「用户可感知功能」的 implement 阶段完成后。「用户可感知功能」定义：改动涉及 hook、cron、CLI 行为、配置模板、init 流程、Web 页面等用户运行时能接触到的组件。
- **耗时预期**：视项目规模，15-60 分钟。
- **检查内容**（按项目类型分类）：
  - CLI 工具：执行核心命令，检查退出码为 0 且 stdout 包含有意义输出（非空、非纯 help 文本、非错误信息）。
  - Web 服务：启动服务，访问核心页面，验证 HTTP 200 且响应体包含业务内容（非空白页、非默认 404）。
  - Hook/Plugin：触发对应事件，验证 handler 执行且产生可观测副作用（日志、文件写入、状态变更）。
  - Library：import 核心模块，调用核心 API，验证返回值类型正确且内容有意义（非 null、非空对象、非默认值）。
- **「有意义」判定标准**：产出能让用户感知到功能在工作——非空、非默认模板、非错误信息、非占位符。具体判定由 LLM 对产出内容做语义评估。
- **产出**：运行态验证报告（`docs/gap-scan-l3.json`），每个功能域标注 alive/dead + 验证命令 + 实际输出摘要 + 判定理由。

#### 流水线集成

- L1 在 review 阶段自动触发（扩展现有 ImplementationReviewGate）。
- L2 在 endgame 阶段发版前触发（新增 ACCoverageGate）。
- L3 在 post-release 阶段触发（npm publish 后），或在涉及用户可感知功能的 implement 阶段完成后触发（与 FR-28 Clean-Install Gate 协同，FR-29 L3 先于 FR-28 执行）。
- 任何一层不通过 = 阻断当前阶段，必须修复后复验。
- 三层扫描结果汇总写入 `docs/gap-scan-summary.json`，供 Ledger 阶段归档。

#### 验收标准

- AC-29.1（L1 自动触发）：implement 阶段完成后，流水线自动触发 L1 扫描，无需人工干预。扫描在 10 分钟内完成。扫描结果写入 `docs/gap-scan-l1.json`。
- AC-29.2（L1 阻断逻辑）：L1 扫描发现任一 FR 无对应代码文件、编译失败或测试失败时，阶段状态为 blocked，流水线不进入下一阶段。阻断信息包含具体失败 FR 编号和失败原因。
- AC-29.3（L1 产出格式）：L1 报告为结构化 JSON，包含 `{ frId, status: "covered"|"uncovered", compilePassed: boolean, testsPassed: boolean, evidence: { files: string[] } }` 数组。
- AC-29.4（L2 Phase 1 代码地图生成）：L2 扫描的 Phase 1 遍历所有配置的 scanDirs，对每个匹配文件提取相对路径、导出符号列表和文件头注释。Phase 1 不调用 LLM（零 token 消耗）。验证方式：mock 文件系统执行 Phase 1，确认产出包含所有目标文件且无 LLM 调用记录。
- AC-29.5（L2 扫描范围可配置）：L2 扫描通过 `scanDirs` 参数接受目录列表（相对于项目根目录），默认值为 `['.']`（整个项目）。支持 `extensions`（文件扩展名白名单）和 `ignoreDirs`（忽略目录黑名单）配置。验证方式：配置 `scanDirs: ['src/', 'scripts/']` 后执行扫描，确认只有这两个目录下的文件出现在代码地图中。
- AC-29.6（L2 Phase 2 批量初筛）：Phase 2 将 AC 列表与代码地图合并为 prompt，按 batchSize 分批发送给 LLM。每批一次 LLM 调用，对每条 AC 返回三分类结果（covered/suspect/uncovered）及候选文件路径。禁止使用关键词匹配、正则表达式或文件名推断作为分类依据。验证方式：50 条 AC + batchSize=150 时，Phase 2 LLM 调用次数 = 1；batchSize=25 时调用次数 = 2。
- AC-29.7（L2 Phase 3 精确验证）：Phase 3 仅对 Phase 2 判定为 suspect 或 uncovered 的 AC 执行。读取候选文件实际源码，发送给 LLM 做精确语义验证。Phase 2 判定为 covered 的 AC 不进入 Phase 3（跳过验证）。验证方式：Phase 2 返回 40 covered + 10 suspect 时，Phase 3 仅处理 10 条。
- AC-29.8（L2 Token 效率）：三阶段流水线的总 LLM token 消耗相比逐条 AC 独立调用降低 95% 以上。验证方式：对同一项目分别执行三阶段流水线和逐条调用（或计算理论值），对比总 token 数，流水线 ≤ 逐条的 5%。
- AC-29.9（L2 触发时机与独立扫描）：endgame 阶段发版前，流水线自动触发 L2 扫描。L2 扫描在 L1 通过的前提下执行（L1 未通过则 L2 不触发）。支持独立触发：通过 CLI 命令（`sevo scan --level 2`）或 cron 定时任务直接执行 L2 扫描，不依赖 pipeline endgame 阶段。验证方式：(a) endgame 阶段 L1 通过后 L2 自动触发；(b) 手动执行 `sevo scan --level 2` 成功产出报告。
- AC-29.10（L2 阻断逻辑）：L2 扫描发现任一 AC 最终状态为 uncovered（Phase 3 确认无实现代码）时，阶段状态为 blocked，流水线不进入下一阶段。needs-review 状态不自动阻断，但写入报告供人工确认。验证方式：构造一条无实现的 AC，执行 L2 扫描后确认阶段状态为 blocked。
- AC-29.11（L2 产出格式）：L2 报告为结构化 JSON，包含 `{ frId, acId, status: "covered"|"uncovered"|"needs-review", confidence: number, evidence: { file: string, lineRange: [number, number], testFile?: string } }` 数组。扫描日志为独立 JSON 文件，记录每次 LLM 调用的 prompt 摘要和完整响应，确保映射过程可追溯。验证方式：执行 L2 扫描后，报告文件和日志文件均存在且 JSON schema 校验通过。
- AC-29.12（L2 语义约束）：L2 全流程（Phase 2 初筛 + Phase 3 验证）的 LLM prompt 明确禁止关键词匹配、正则表达式和文件名推断。System prompt 中包含该约束声明。验证方式：检查 L2 扫描器的 system prompt 常量，确认包含禁止关键词匹配/正则/文件名推断的明确指令。
- AC-29.13（L3 运行态验证）：L3 扫描在真实环境中执行功能，验证产出「有意义」而非仅「命令能跑」。判定标准：产出非空、非默认模板、非错误信息、非占位符，由 LLM 对实际输出做语义评估并给出判定理由。
- AC-29.14（L3 触发时机）：以下任一条件满足时，流水线自动触发 L3 扫描：(a) npm publish 成功后；(b) 任何涉及「用户可感知功能」的 implement 阶段完成后。L3 在 FR-28 Clean-Install Verification 之前执行（L3 验证当前环境，FR-28 验证干净环境）。
- AC-29.15（L3 阻断逻辑）：L3 扫描发现任一功能域状态为 dead（退出码非 0、响应异常、产出为空或无意义）时，阶段状态为 blocked，不进入 FR-28 验证。阻断信息包含功能域标识、验证命令、实际输出和失败判定理由。
- AC-29.16（L3 产出格式）：L3 报告为结构化 JSON，包含 `{ domain: string, status: "alive"|"dead", verifyCommand: string, actualOutput: string (truncated to 1KB), judgment: string, evidence: { exitCode?: number, httpStatus?: number, sideEffect?: string } }` 数组。
- AC-29.17（三层汇总）：三层扫描完成后，自动生成汇总报告 `docs/gap-scan-summary.json`，包含 `{ l1: { pass: boolean, total: number, covered: number }, l2: { pass: boolean, total: number, covered: number, needsReview: number }, l3: { pass: boolean, total: number, alive: number }, overall: "pass"|"fail", timestamp: string }`。汇总报告供 Ledger 阶段归档。
- AC-29.18（单 Agent 兼容）：单 Agent 环境下，三层扫描均可由同一 Agent 执行（通过 `sevo scan --level 1|2|3|all` 命令触发）。多 Agent 环境下，L2/L3 由非开发 Agent 执行（禁止开发者自验）。
- AC-29.19（用户可感知功能定义）：「用户可感知功能」指改动涉及以下任一组件：hook handler、cron 定时任务、CLI 命令/子命令行为、配置模板（init 生成的文件）、init/setup 流程、Web 页面/API 端点。判定依据：陌生用户在运行时能否接触到该组件。若能接触到，则该改动属于用户可感知功能变更，implement 完成后必须触发 L3 扫描。
- AC-29.20（可达性验证）：L3 扫描内容必须包含可达性检查——新实现的功能，陌生用户通过 `npm install` + `init` 后能否自动获得？如果不能自动获得，是否有 init/setup 命令自动配置？发现「代码存在但用户不可达」的功能（代码在仓库中但用户正常安装流程无法触达）= P0 阻断，必须修复后复验。
- AC-29.21（独立仓库同步门禁）：implement 完成后如果涉及用户可感知功能变更，L3 扫描必须验证改动已同步推送到项目的独立 GitHub 仓库。仅存在于主仓库（monorepo）但未同步到独立仓库的用户可感知功能变更 = P0 阻断。验证方式：对比独立仓库最新 commit 与主仓库对应目录的 diff，diff 非空则阻断。

### FR-30 OKR Goal Declaration Stage（OKR 目标声明阶段）

- **定位**：Spec 阶段内部的目标拆解子阶段。将 Pipeline 的终局目标（endStateGoal）拆解为结构化的 OKR 树（Objective + Key Results），为下游阶段（SMART Decomposition、PDCA Gap Analysis）提供对齐基线。是 FR-18 目标驱动 PDCA 闭环的具体执行入口。
- **与 FR-18 的关系**：FR-18 定义了 OKR→SMART→PDCA 的整体机制和数据结构，本 FR 定义该机制中「OKR 拆解」环节的具体阶段行为、输入输出和容错逻辑。
- **触发条件**：Pipeline 存在 endStateGoal 且 Spec 阶段启动时，由 PipelineEngine 在 Spec 阶段内部调度执行。
- **输入**：endStateGoal（终局目标描述）、existingOkrTree（可选，已有 OKR 树用于增量更新）、taskId、artifactBasePath（可选）。
- **处理**：
  1. 若已有 OKR 树（existingOkrTree 非空），直接复用，不重复拆解。
  2. 若无已有 OKR 树，调用 Adapter 的 `decomposeOkr` 方法，由 LLM 将终局目标拆解为 1-N 个 Objective，每个 Objective 下挂 3-5 个可度量的 Key Results。
  3. 无 Adapter 时 fallback：生成单 Objective + 单 KR 的骨架树，确保流水线不因缺少 LLM 而中断。
  4. 为每个 Objective 和 KR 分配稳定 ID（OBJ-NN、KR-NN.M）。
  5. 将 OKR 树持久化为 JSON 工件。
- **输出**：OKR 树（ObjectiveKeyResult[]）、元数据（objectiveCount、totalKeyResults、declaredAt）、工件引用（ArtifactRef）。
- **执行阶段**：Spec 阶段内部（stageId = 'spec'）。
- **验收标准**：
  - AC-30.1：存在 endStateGoal 时，阶段产出包含至少一个 Objective 和对应的 Key Results，每个 KR 包含 description、measure 字段。
  - AC-30.2：已有 OKR 树时直接复用，不调用 Adapter，产出与输入一致。
  - AC-30.3：无 Adapter 配置时，fallback 产出单 Objective + 单 KR 骨架，流水线不中断。OKR 树工件写入 `artifacts/okr/<taskId>-okr-tree.json`。

### FR-31 SMART Decomposition Stage（SMART 任务分解阶段）

- **定位**：Spec 阶段内部的任务分解子阶段。将 Spec 产出的 FR 列表分解为 SMART 限定的任务（Specific / Measurable / Achievable / Relevant / Time-bound），建立 FR→KR 的溯源映射。是 FR-18 SMART 原则的程序化执行点。
- **与 FR-18 的关系**：FR-18 AC-18.5 要求 FR/AC 满足 SMART 原则，本 FR 定义将该原则程序化为具体阶段的执行逻辑——从 FR 列表自动生成 SMART 任务清单。
- **与 FR-21 的关系**：FR-21 定义 SMART 目标声明（liveness probe 关联），本 FR 定义 FR→SMART 任务的分解过程。两者互补：FR-31 产出 SMART 任务，FR-21 为每个任务关联 liveness probe。
- **触发条件**：Spec 阶段产出 FR 列表后，由 PipelineEngine 在 Spec 阶段内部调度执行。
- **输入**：functionalRequirements（FR 列表）、okrTree（可选，OKR 树）、krMapping（可选，FR→KR 映射表）、taskId、artifactBasePath（可选）。
- **处理**：
  1. FR 列表为空时，graceful skip，返回空任务列表。
  2. 有 Adapter 时，调用 `decomposeSmart` 方法，由 LLM 为每个 FR 生成 SMART 五维度描述。
  3. 无 Adapter 时 fallback：从 FR 结构确定性提取 SMART 维度——Specific 取 FR description，Measurable 取 AC 摘要，Achievable 默认「当前架构可行」，Relevant 映射到对应 KR，Time-bound 默认「当前迭代」。
  4. 为每个 SMART 任务分配稳定 ID（SMART-NNN），关联 frId 和 krId。
  5. 计算 KR 覆盖率（有 krId 的任务数 / OKR 树中总 KR 数）。
  6. 将 SMART 任务列表持久化为 JSON 工件。
- **输出**：SMART 任务列表（SmartTask[]）、元数据（totalTasks、krCoverage、decomposedAt）、工件引用（ArtifactRef）。
- **执行阶段**：Spec 阶段内部（stageId = 'spec'）。
- **验收标准**：
  - AC-31.1：每个产出的 SMART 任务包含 id、frId、specific、measurable、achievable、relevant、timeBound 六个字段，均非空。
  - AC-31.2：存在 OKR 树和 krMapping 时，任务的 Relevant 维度映射到对应 KR，krCoverage 反映实际覆盖比例。
  - AC-31.3：无 Adapter 时 fallback 产出确定性 SMART 任务（从 FR 结构提取），流水线不中断。工件写入 `artifacts/smart/<taskId>-smart-tasks.json`。

### FR-32 PDCA Gap Analysis Stage（PDCA 差距分析阶段）

- **定位**：Verify 阶段内部的差距分析子阶段。以 OKR 树为基准，按 Plan/Do/Check/Act 四维度评估当前迭代的目标收敛状态，识别差距并生成下一轮修复任务。是 FR-18 PDCA 闭环的程序化 Check+Act 执行点。
- **与 FR-18 的关系**：FR-18 AC-18.8-18.11 定义了 KR 级差距分析和 PDCA 循环的行为规范，本 FR 定义该行为的具体阶段实现——输入结构、四维度评估逻辑、收敛判定算法和工件格式。
- **触发条件**：Pipeline 存在 OKR 树且进入 Verify 阶段时，由 PipelineEngine 调度执行。
- **输入**：okrTree、krMapping（FR→KR 映射）、functionalRequirements、implementationStatus（FR 实现状态）、acImplementationStatus（AC 实现状态）、auditFindings（审计发现）、cycleNumber（当前 PDCA 轮次）、taskId、artifactBasePath（可选）。
- **处理**：
  1. **Plan 评估**：检查 OKR 树中每个 KR 是否被至少一个 FR 覆盖（通过 krMapping 和 FR.tracesTo 双路径检查）。产出 KR 覆盖详情（covered/uncovered）。
  2. **Do 评估**：统计 FR 和 AC 的实现率（已实现数 / 总数）。
  3. **Check 评估**：分析审计发现的严重程度，判定是否存在 OKR 偏移（critical/blocker 级发现 = 偏移）。
  4. **Act 产出**：汇总所有差距（Plan 中未覆盖的 KR、Do 中未实现的 FR、Check 中的关键审计发现），为每个差距生成修复建议。
  5. **收敛判定**：gaps = 0 → converged；有 critical 差距 → escalated；其他 → gap-remaining。
  6. 记录 PDCA 轮次（PdcaCycleRecord），持久化为 JSON 工件。
- **输出**：PDCA 差距报告（PdcaGapReport，含 plan/do/check/act 四维度 + convergence + cycleRecord）、元数据（totalGaps、criticalGaps、convergence、analyzedAt）、工件引用（ArtifactRef）。
- **执行阶段**：Verify 阶段内部（stageId = 'verify'）。
- **验收标准**：
  - AC-32.1：Plan 维度正确识别未被 FR 覆盖的 KR，每个未覆盖 KR 生成 severity=critical 的差距条目。
  - AC-32.2：收敛判定逻辑——差距为零时 convergence='converged'，存在 critical 差距时 convergence='escalated'，其他情况 convergence='gap-remaining'。
  - AC-32.3：无 OKR 树时产出最小报告（仅含 Do 维度的实现率统计），不中断流水线。工件写入 `artifacts/pdca/<taskId>-pdca-gap-report.json`。

### FR-33 MECE Validation & Dependency Analysis（MECE 验证与依赖分析）

- **定位**：Contract 阶段的工作包质量校验机制。验证工作包拆分满足 MECE 原则（Mutually Exclusive, Collectively Exhaustive），并分析工作包间的依赖关系和执行顺序，检测循环依赖。
- **与 FR-03 的关系**：FR-03 AC-4.10 要求「工作包拆分后可分派、可验收、可追责」，本 FR 定义实现该要求的具体校验算法——MECE 验证确保拆分无重叠无遗漏，依赖分析确保执行顺序合理。
- **触发条件**：Contract 阶段产出工作包列表后，自动执行 MECE 验证和依赖分析。
- **输入**：tasks（WorkPackage 列表，每个包含 id、frIds、dependencies）、allFrIds（可选，全量 FR ID 列表用于 CE 检查）。
- **处理**：
  1. **互斥性检查（ME）**：两两比对工作包的 frIds，检测是否存在同一 FR 被多个工作包覆盖的情况。存在重叠时记录具体重叠的 WP 对和共享 FR。
  2. **穷尽性检查（CE）**：汇总所有工作包覆盖的 FR，与全量 FR 列表比对，识别未被任何工作包覆盖的 FR。
  3. **依赖图构建**：从工作包的 dependencies 字段构建有向依赖图，填充 dependsOn 字段，标记无依赖的工作包为可并行执行。
  4. **循环依赖检测**：使用拓扑排序（Kahn 算法）检测依赖图中的环。存在环时报告参与环的工作包 ID。
  5. **修复建议生成**：对每个 MECE 违规和循环依赖生成可操作的修复建议。
- **输出**：
  - MECE 验证结果（valid、mutuallyExclusive、collectivelyExhaustive、overlaps、uncoveredFrIds、suggestions）。
  - 依赖分析结果（tasks with dependsOn populated、hasCycle、cycleDetails、dependencyGraph）。
- **执行阶段**：Contract 阶段内部。
- **验收标准**：
  - AC-33.1：同一 FR 出现在两个及以上工作包的 frIds 中时，mutuallyExclusive = false，overlaps 列出具体重叠的 WP 对和共享 FR ID。
  - AC-33.2：提供 allFrIds 时，任一 FR 未被任何工作包覆盖则 collectivelyExhaustive = false，uncoveredFrIds 列出遗漏的 FR。valid = true 当且仅当 ME 和 CE 同时满足。
  - AC-33.3：依赖图存在环时 hasCycle = true，cycleDetails 列出参与环的工作包 ID。无环时所有工作包可按拓扑序执行，无依赖的工作包标记为 parallel = true。

### FR-34 Incremental FR Lifecycle（增量 FR 生命周期管理）

- **定位**：生命周期操作。为已有项目追加的增量 FR 提供从 implement 到 publish 的子流程触发能力。解决的核心问题：项目已有完整 pipeline 历史，PM 在 spec 中新增了 FR，但 `sevo:create` 报「已存在」，`sevo:from` 会重跑整个项目而非聚焦单个 FR。本 FR 提供精确到单个 FR 粒度的增量推进入口。
- **与 FR-12 的关系**：FR-12 为项目创建首次 FR 流程实例（全量 pipeline）。FR-34 为已有项目中新增的 FR 创建增量流程实例，复用 FR-12 的实例创建逻辑但跳过 spec/contract 阶段。
- **与 FR-27 的关系**：FR-27 允许从任意阶段切入但作用于整个项目。FR-34 作用于项目中的特定 FR，只推进该 FR 相关的实现子流程。
- **与 FR-13 的关系**：增量流程实例创建后，由 PipelineEngine（FR-13）接管后续生命周期推进，复用相同的状态机和阶段流转逻辑。
- **触发条件**：用户通过 CLI 命令 `sevo fr advance <project-slug> --fr <fr-id>` 触发，或主会话调度时在 label 中包含 `fr-advance:<project>:<fr-id>` 标记。
- **输入**：Project 标识（project-slug）、目标 FR 标识（fr-id）、可选的任务描述补充。
- **处理**：
  1. 校验 Project 存在且有历史 pipeline 记录（至少有一个 completed 或 failed 的流程实例）。
  2. 校验目标 FR 存在于项目的 spec 文件（`product-requirements.md`）中——通过解析 FR 编号格式匹配。
  3. 校验该 FR 没有正在进行的 active 流程实例（同一 FR 同时只能有一个 active 实例）。
  4. 生成增量流程实例 ID（格式：`fr-<project-slug>-<fr-id>-<yyyyMMdd>-<seq>`）。
  5. 将 spec 和 contract 阶段标记为 skipped（跳过理由：「增量 FR，spec 已就绪」）。若项目有 arc42 架构文档，将其作为 implement 阶段的输入上下文注入。
  6. 确定增量流程的阶段队列：implement → review → regression → publish。根据 Tier 路由（§3.2）裁剪——L0 微小改动可跳过 regression。
  7. 创建增量流程实例记录，状态设为 created。
  8. 向 PipelineEngine（FR-13）发送 pipeline-created 事件，PipelineEngine 接管后续推进。
  9. implement 阶段的 prompt 自动注入：目标 FR 的完整定义（从 spec 提取）、关联的 AC 列表、项目架构上下文（若存在）。
- **输出**：增量 FR 流程实例（含实例 ID、目标 FR 绑定、跳过阶段记录、阶段队列）。
- **执行阶段**：Pipeline Create 的增量入口（复用 FR-12 实例创建逻辑的子集）。
- **验收标准**：
  - AC-34.1：`sevo fr advance <project-slug> --fr <fr-id>` 命令被正确解析。project-slug 不存在时返回错误「项目不存在」；fr-id 在 spec 中不存在时返回错误「FR 未在 spec 中定义」。
  - AC-34.2：增量流程实例的 spec 和 contract 阶段在 Stage Record 中标记为 skipped，跳过理由为「增量 FR，spec 已就绪」。
  - AC-34.3：增量流程实例创建后，PipelineEngine 自动接管并触发 implement 阶段执行，implement 阶段的执行上下文包含目标 FR 的完整定义和 AC 列表。
  - AC-34.4：同一 FR 已有 active 流程实例时，创建请求被拒绝并返回错误「该 FR 已有进行中的流程实例」。不同 FR 的增量流程可以与项目的其他增量流程并行存在（受 Agent 资源池约束）。
  - AC-34.5：增量流程的 review 阶段复用 FR-06 的审计逻辑，审计范围限定为目标 FR 相关的代码变更。
  - AC-34.6：增量流程的 publish 阶段复用 FR-19 的终局交付链逻辑。若项目配置了版本管理，自动 bump patch 版本。
  - AC-34.7：增量流程完成后，Ledger 中生成独立的 Entry，记录该 FR 从 implement 到 publish 的完整证据链，可追溯到项目的 spec 版本。
  - AC-34.8：一个项目可以有多个已完成的增量流程实例（每个对应不同的 FR），Ledger 按时间线聚合展示。
  - AC-34.9：`sevo status` 和 Web 驾驶舱能区分显示全量 pipeline 和增量 FR 流程实例，增量实例标注关联的 FR 编号。
  - AC-34.10：主会话调度时，label 中包含 `fr-advance:<project>:<fr-id>` 标记可被 SEVO 插件识别并自动创建增量流程实例，无需用户手动执行 CLI。
  - AC-34.11：`inferProjectSlug` 从已注册 pipeline 列表动态推断 project-slug，不硬编码项目名。新注册的项目无需修改源码即可被正确识别和路由。静态项目名列表仅作为尚未注册 pipeline 的新项目的 fallback。

### FR-35 Full R&D Activity Pipeline Enforcement & Pre-Publish Stranger Verification（全研发活动强制流水线 + 发布前陌生人验证）

- **定位**：治理增强。将 SEVO 流水线的路由覆盖范围从「spawn 时检测到代码变更意图」扩展为「已注册项目的任何研发活动」，并在 publish 阶段新增陌生人开箱即用验证 gate。解决的核心问题：主会话可通过手动分步派发（先派 PM 写 spec，再派 SA implement）绕过流水线；publish 阶段缺少面向陌生用户的可用性验证。
- **与 FR-12 的关系**：FR-12 定义流程实例创建。FR-35 扩展触发路由的覆盖面，确保所有应走流水线的活动都被引导到 FR-12 的创建入口。
- **与 FR-19 的关系**：FR-19 定义终局交付链。FR-35 在 FR-19 的 publish 阶段插入 stranger-ready gate 作为前置门禁。
- **与 FR-27 的关系**：FR-27 允许从任意阶段切入。FR-35 确保即使从中间阶段切入，也必须有活跃 pipeline 上下文。
- **背景**：当前 SEVO 插件的 LLM_TRIGGER_SYSTEM_PROMPT 只在 spawn 时检测「代码变更意图」。以下场景可绕过：(1) 主会话分步派发——先派 PM 修改 spec 文件，再派 SA implement，每步 label 不含 sevo: 前缀；(2) 直接派发 review/publish 阶段任务而无活跃 pipeline。此外，publish 完成后没有强制验证产物对陌生用户是否可用。
- **目标**：
  1. 对已注册项目的任何研发活动（spec 修改、implement、review、audit、publish）都必须走 SEVO 流水线。
  2. 发布前必须通过陌生人开箱即用验证。
- **处理**：
  1. **路由覆盖范围扩展**：SEVO 插件的路由判定逻辑从「检测代码变更意图」扩展为「检测已注册项目的研发活动」。判定维度包括：目标文件路径是否属于已注册项目、task prompt 语义是否涉及已注册项目的 spec/代码/架构/测试/发布。
  2. **活跃 pipeline 校验**：对已注册项目的 implement/review/audit/publish 阶段任务，插件检查是否存在对应的活跃 pipeline 实例。不存在时阻断执行并提示 `sevo:create <project-slug>`。
  3. **分步派发检测**：当 spawn 的 label 不含 `sevo:` 前缀，但 task prompt 语义分析判定目标文件属于已注册项目的研发产物时，插件路由并提示走流水线。
  4. **Stranger-Ready Gate**：pipeline 的 publish 阶段执行前，插件检查 stranger-ready gate 是否通过。gate 执行 `scripts/npm-stranger-verify.sh` 或项目配置的等效验证脚本，在干净环境中验证产物对陌生用户的开箱即用性。
  5. **Gate 失败处理**：stranger-ready gate 失败时，pipeline 状态设为 `publish-blocked`，记录失败原因（脚本 stderr + exit code），输出修复建议，等待修复后重新触发 gate。
  6. **Gate 跳过机制**：项目 pipeline 配置中声明 `strangerVerify: false` 时，stranger-ready gate 自动标记为 skipped（跳过理由：「项目配置声明非 npm 包，跳过陌生人验证」）。CLI 支持 `--skip-stranger-verify` 参数作为运行时覆盖。
  7. **语义判定**：路由判定使用 LLM 语义理解（复用 LLM_TRIGGER_SYSTEM_PROMPT 的判定机制），分析 task prompt 内容判断是否涉及已注册项目的研发活动。禁止纯关键词匹配或 FTS5 或正则表达式冒充语义理解。
- **输入**：spawn 请求（label + task prompt + 目标 agent）、已注册 pipeline 列表、项目 pipeline 配置。
- **输出**：路由决策（pass/block + 理由）、stranger-ready gate 结果（pass/fail/skipped + 证据）。
- **执行阶段**：Pipeline Governance（贯穿所有阶段的治理层）。
- **验收标准**：
  - AC-35.1：对已注册 pipeline 的项目，spawn 涉及 spec 文件修改时（如派 PM 修改 `product-requirements.md`），SEVO 插件触发路由并提示走流水线。
  - AC-35.2：对已注册项目的 implement/review/publish 阶段任务，若没有对应的活跃 pipeline 实例，插件阻断执行并返回提示「该项目需要活跃的 SEVO pipeline，请先执行 sevo:create <project-slug>」。
  - AC-35.3：主会话手动分步派发（label 不含 `sevo:` 前缀，但 task prompt 目标文件属于已注册项目）时，插件检测到研发活动并路由，提示走流水线。路由判定基于 LLM 语义分析，不依赖关键词匹配。
  - AC-35.4：pipeline 的 publish 阶段新增 stranger-ready gate。gate 执行 `scripts/npm-stranger-verify.sh`（或项目配置的等效脚本），在干净环境中安装并运行产物，验证陌生用户开箱即用性。gate 通过后才能标记 publish 完成。
  - AC-35.5：stranger-ready gate 失败时，pipeline 状态停留在 `publish-blocked`，不推进到 completed。输出内容包含：失败原因（脚本 stderr）、exit code、修复建议。修复后可通过 `sevo gate retry <instance-id> stranger-ready` 重新触发验证。
  - AC-35.6：项目 pipeline 配置中声明 `strangerVerify: false` 时，stranger-ready gate 自动跳过。CLI 支持 `--skip-stranger-verify` 参数作为单次运行时覆盖。未声明且未传参时，gate 为强制执行。
  - AC-35.7：路由判定使用 LLM 语义理解，分析 task prompt 内容判断是否涉及已注册项目的研发活动。判定结果包含置信度和推理依据，记录到 dispatch-guard-events.jsonl 供审计追溯。禁止纯关键词匹配、FTS5 全文检索或正则表达式作为判定手段。
  - AC-35.8：dispatch-guard 在 L2 插件层提供确定性拦截兜底：当目标路径属于受管项目，且任务入口是构建、打包、发布、review、audit 或 spec 修改等研发动作时，即使 prompt 未显式包含 `sevo:` 前缀，也必须强制路由到 SEVO。
  - AC-35.9：对受管项目执行构建命令或等效研发入口时，必须存在活跃 pipeline 上下文；不存在时直接阻断，并提示用户执行 `sevo:create <project-slug>` 或 `sevo:from <project-slug> <stage>`，禁止“先构建再补流水线”。

### FR-36 Verify-With-Real-Data Gate（发版前真实数据通路门禁）

- **定位**：发版前置门禁。受管项目的 web 端反复出现「假数据冒充真数据」——种子写死、mock 数据未替换、API 返回硬编码列表，导致发版后陌生人看到的是假产品。本 FR 在 publish 链路前段插入硬门禁，强制要求受管项目 web 端关键页面的数据来自真实数据源（DB、真实 API、运行时产生的内容），并要求陌生环境 + 真数据的端到端可视证据。
- **与 FR-17 的关系**：FR-17 是发布后的差距扫描（已发布产物的 FR 覆盖度），FR-36 是发布前的数据通路审查。FR-36 通过后才允许进入 FR-08a 商用化门禁与 FR-08 Deploy。
- **与 FR-28 的关系**：FR-28 在隔离干净环境验证「能装能跑」，FR-36 在 implement 完成后审查「数据是否真实」。FR-36 在 FR-28 之前执行，避免把假数据通路打包发布。
- **与 FR-35 stranger-ready gate 的关系**：FR-35 stranger-ready gate 验证陌生用户能装能跑，FR-36 验证陌生用户看到的内容是真实数据。两者互补，stranger-ready 通过不代表数据真实。
- **与 AC-4.36d 的关系**：AC-4.36d 约束「SEVO 自身 Verify 阶段的验证证据不得使用 mock/seed」，FR-36 约束「受管项目产品代码本身的数据通路不得用 mock/seed 冒充真实数据」，两者层级不同。
- **触发时机**：受管项目 pipeline 的 implement → review（FR-06）→ smoke test（FR-06b）→ ux acceptance（FR-06c）→ pm commercial review（FR-06d）→ regression（FR-07）全部通过后，自动进入 verify-with-real-data 阶段；该阶段通过后才允许进入 FR-08a Commercialization Gate 与 FR-08 Deploy。失败则阻塞发版，回退到 implement。
- **适用范围**：spec 中标注存在 web 端的受管项目（含 KIVO、SEVO、exam-sprint 等当前已注册项目，以及未来通过 `projects/*/sevo.json` 自动纳管的具备 web 入口的项目）。纯 CLI / SDK / 后端项目通过项目配置 `verifyWithRealData: false` 显式跳过；未声明且 spec 中存在 web 路由时强制执行。
- **检查内容**：分三大维度，全部使用 LLM 语义判定，禁止纯关键词匹配 / FTS5 / 正则伪装语义理解。
  1. **数据源真实性**：spec 中列出的核心 FR 对应的 web 路由必须从真实数据源读取——具体定义为：从持久化存储（数据库、文件系统）、真实运行的内部服务接口、用户操作后由系统生成的运行时内容中读取。禁止以下三类「假数据」：
     - 硬编码常量数组直接渲染到页面（如 `const items = [{title: '示例 1'}, {title: '示例 2'}]`）。
     - 内存常量字典作为唯一数据源（无任何写入/更新通路）。
     - 服务端代码中的 mock 函数返回值未接入真实数据通路（如 API handler 直接 `return mockList`）。
  2. **mock 数据标记规范**：实现过程中若不可避免出现 seed/mock/fixture/占位数据，必须满足三项强制要求：
     - **代码标记**：mock/seed 数据所在位置必须有显式标记注释，标准前缀为 `// SEED`、`// MOCK`、`// FIXME-mock` 之一，标记必须紧贴 mock 数据声明上方一行。
     - **迁移路径文档**：项目 `docs/` 目录下必须存在 `mock-migration-plan.md` 文件，列出每处 mock 数据的位置（文件路径 + 行号）、替换为真实数据源的具体方案、计划替换时间。
     - **运行时区分**：默认 build / production 构建产物中不允许命中未替换的 mock 数据；若 mock 仅作为 demo/dry-run 模式存在，必须由显式开关（如 `--demo` 或 `DEMO_MODE=true`）启用，普通用户路径不能命中。
  3. **陌生环境 + 真数据端到端证据**：FR-06c UX Acceptance 阶段（受 FR-36 校验时）必须产出至少一组「陌生环境 + 真实材料」证据：在隔离的 stranger 验证目录或全新账号下，导入真实业务材料（如 KIVO 导入真实 PDF、SEVO 触发一次完整 spec→ledger 流程），关键页面截图必须呈现导入材料产生的真实内容，禁止使用空状态、默认模板、demo 占位作为通过依据。
- **检查实现要求**：
  - 检查 1（数据源真实性）使用 LLM 对受管项目核心 FR 对应的 web 路由源码 + API handler 源码做语义判定，结合数据流追溯。每条 web 路由产出 PASS / FAIL / NEEDS_REVIEW + 推理依据。
  - 检查 2（mock 标记规范）由静态扫描 + LLM 判定组合：静态扫描定位疑似 mock 数据的代码位置（基于变量命名、数组字面量、API handler return 语句），LLM 判定每处疑似位置是否属于 mock 数据；判定为 mock 的位置必须满足代码标记 + 迁移文档登记两项要求。
  - 检查 3（端到端证据）从 FR-06c UX Acceptance 阶段产出物中提取 stranger 模式截图证据，由 LLM 判定截图内容是否呈现真实导入材料产生的内容（如截图中是否包含真实 PDF 文件名、真实知识点、真实 spec 内容），不允许只看到 demo 占位或空状态截图。
- **失败处理**：任一检查不通过即整体阻断发版。pipeline 状态设为 `verify-with-real-data-blocked`，回退到 implement 阶段（FR-05），生成修复任务列表（fixTasks）派给开发 Agent。修复任务内容由 LLM 根据失败维度自动生成，包含：失败的 web 路由列表、需要替换的假数据位置（文件 + 行号）、迁移到真实数据源的具体方案。开发完成后重新跑 review→regression→FR-36 全链路。
- **跳过机制**：项目 pipeline 配置中声明 `verifyWithRealData: false` 时，本门禁标记为 skipped，跳过理由必须显式写入 ledger（如「项目为纯 CLI，无 web 端」）。CLI 支持 `--skip-verify-with-real-data` 单次运行覆盖；未声明且 spec 中存在 web 路由时强制执行，禁止默认跳过。
- **输入**：受管项目源码、spec 中标注的核心 FR 列表、对应 web 路由清单、FR-06c UX Acceptance 产出的截图证据、`docs/mock-migration-plan.md`（如存在）。
- **输出**：Verify-With-Real-Data Report（结构化 JSON + 人类可读摘要），包含：
  - 受检 web 路由列表与每条路由的数据源真实性判定（PASS / FAIL / NEEDS_REVIEW + 理由 + 关键代码片段引用）。
  - mock 数据登记表（位置、是否带标记、是否登记到 mock-migration-plan）。
  - 端到端证据评估（截图引用、LLM 对截图内容真实性的判定）。
  - overall 通过 / 阻断结论 + fixTasks 列表（如阻断）。
  - 报告写入项目 `docs/verify-with-real-data-report.json`。
- **执行阶段**：Verify-With-Real-Data Gate（位于 Regression 之后、Commercialization Gate 之前）。
- **角色约束**：禁止开发者自检；由独立非开发 Agent 执行（默认 audit-01 或 ux-01，根据可用性路由）。
- **验收标准**：
  - AC-36.1：spec 中存在 web 路由的受管项目，Regression（FR-07）通过后，PipelineEngine 自动进入 verify-with-real-data 阶段，无需主会话人肉触发。
  - AC-36.2：检查 1（数据源真实性）必须使用 LLM 对受检 web 路由源码 + 对应 API handler 源码做语义判定，禁止用关键词匹配、字数阈值、正则表达式、FTS5 全文检索冒充语义理解。每条路由产出三档判定（PASS / FAIL / NEEDS_REVIEW）+ 推理依据 + 关键代码片段。
  - AC-36.3：检查 2（mock 标记规范）必须同时满足两项硬性要求才算通过：(a) 代码中所有 mock/seed 数据位置有标记注释（标准前缀 `// SEED`、`// MOCK`、`// FIXME-mock` 之一，紧贴上方一行）；(b) 项目 `docs/mock-migration-plan.md` 存在且包含每处 mock 的位置（文件 + 行号）+ 替换方案 + 计划时间。任一项不满足判定为 fail。
  - AC-36.4：检查 3（端到端证据）必须从 FR-06c UX Acceptance 产出物中提取陌生环境下导入真实业务材料后的截图证据。LLM 判定截图内容是否呈现真实导入材料产生的内容；只看到 demo 占位、空状态、默认模板的截图判定为 fail。每个核心 FR 至少需要一组陌生环境 + 真数据的截图证据。
  - AC-36.5：默认 build / production 构建产物中不允许命中未替换的 mock 数据。验证方式：在干净环境中执行项目构建，扫描构建产物中是否存在 mock 数据特征（标准前缀注释、命名为 `mock*` / `fake*` / `seed*` 的数组常量未被标记或未被环境变量门控）。命中即 fail。mock 仅作为 demo/dry-run 模式存在时，必须有显式开关（如 `--demo` 或 `DEMO_MODE=true`），普通安装路径不能命中 mock。
  - AC-36.6：任一检查不通过时，pipeline 状态设为 `verify-with-real-data-blocked`，回退到 implement（FR-05）。系统生成 fixTasks 列表派给开发 Agent，修复任务内容包含失败的 web 路由列表、需要替换的假数据位置（文件 + 行号）、迁移到真实数据源的具体方案。修复完成后重新跑 review→regression→FR-36 全链路。
  - AC-36.7：项目 pipeline 配置声明 `verifyWithRealData: false` 时，本门禁标记为 skipped，跳过理由显式写入 ledger。CLI 支持 `--skip-verify-with-real-data` 单次覆盖。spec 中存在 web 路由且未声明跳过时，门禁强制执行，不允许默认跳过。
  - AC-36.8：禁止开发者自检。由独立非开发 Agent 执行（默认 audit-01；audit-01 不可用时降级到 ux-01）。审计 Agent 与本次实现 Agent 不得为同一身份。
  - AC-36.9：报告写入项目 `docs/verify-with-real-data-report.json`，结构包含 `{ webRoutes: [{ route, dataSourceJudgment, reasoning, codeSnippet }], mockRegister: [{ filePath, line, hasMarker, inMigrationPlan }], strangerEvidence: [{ frId, screenshotPath, llmJudgment, reasoning }], overall: "pass"|"fail"|"skipped", fixTasks: [], timestamp }`。
  - AC-36.10：单 Agent 环境下也能走完 verify-with-real-data 门禁。检查逻辑内置于 SEVO CLI（`sevo verify --real-data`），不依赖专职审计 Agent；多 Agent 环境下由调度层派非开发 Agent 执行。
  - AC-36.11：本门禁的判定结果作为 FR-08a Commercialization Gate、FR-08 Deploy、FR-17 Post-Release Validation 的强制前置工件留档；后续阶段必须能在评审包顶部引用本门禁的结论与报告路径。
  - AC-36.12（术语澄清）：「真实数据源」定义为：(a) 持久化存储（数据库、本地文件系统、云存储）；(b) 真实运行的内部服务 API 接口；(c) 用户操作后由系统生成的运行时内容（如用户上传 PDF 后系统提取的知识点）。「假数据」定义为：(a) 硬编码常量数组直接渲染到页面；(b) 内存常量字典作为唯一数据源且无写入通路；(c) API handler 直接 return mock 数据未接入真实数据通路。判定边界由 LLM 语义判定为准，配合标准定义。

## 5. 非功能需求

### 5.1 性能

- NFR-5.1：任务进入流水线后的路由判定应在秒级完成，不能把主会话卡成长任务。
- NFR-5.2：阶段门禁检查默认优先脚本化与结构化检查，减少纯人工逐项核对。
- NFR-5.3：单个工作包的状态、工件、结论查询应能快速返回，便于调度和审计。
- NFR-5.4：长流程支持增量推进，单个阶段失败不要求整条流水线从头重跑。

### 5.2 可靠性

- NFR-5.5：每个阶段都有明确输入、输出和阻断条件，避免“状态不明”。
- NFR-5.6：完成判定不能依赖聊天回复，必须依赖文件、工件或可验证结果。
- NFR-5.7：长流程状态必须持久化，主会话中断不应导致整条流水线失忆。
- NFR-5.8：阶段失败后支持修复、复审、续跑，不要求手工重建全链路上下文。

### 5.3 可扩展性

- NFR-5.9：SEVO 的阶段定义、工件定义、门禁定义与具体运行时解耦。
- NFR-5.10：支持不同类型 Agent 接入同一流程，包括 ACP agent、原生 subagent、未来独立验证器。
- NFR-5.11：支持按任务级别裁剪流程，但不破坏统一工件语言。
- NFR-5.12：新阶段规则和新门禁可以增量追加，不要求重写整套流程。

### 5.4 安全性

- NFR-5.13：审计角色与开发角色职责分离，默认禁止自审。
- NFR-5.14：高风险改动在 Implement、Review、Verify 阶段都要有加厚检查。
- NFR-5.15：账本和审计工件必须保留关键证据，便于追责和复盘。
- NFR-5.16：核心流程代码通过 Adapter 抽象层隔离对 OpenClaw 具体 API 的直接调用，保持代码职责清晰和可测试性。高价值的治理机制（执行前检查、执行后验证、上下文注入、会话边界控制）属于 SEVO 内建能力。
- NFR-5.17：受保护环境中的访问和关键操作必须可追溯到具体操作者，不能只有共享口令而无身份标识。
- NFR-5.18：路径默认值守则。SEVO 源码中任何 `DEFAULT_*` 常量、`?? 'fallback'` 兜底字面量、`process.env.X ?? '...'` 表达式，禁止字面量包含宿主特定绝对路径前缀（`/root/`、`/home/<user>/`、`/Users/<name>/` 等）。允许的默认值形式仅限：(a) `null` 兜底强制注入（找不到时抛可读错误）；(b) 相对工件根或项目根的相对路径（`path.resolve(workspaceRoot, ...)`）；(c) 通过 `__dirname` 解析的包内嵌资源路径（`path.resolve(__dirname, '../scripts/...')`）。
- NFR-5.19：环境变量统一命名约定。SEVO 暴露给用户的环境变量必须以 `SEVO_` 前缀开头（如 `SEVO_PROJECTS_DIR`、`SEVO_LLM_GATE_AUDIT_LOG`、`SEVO_PUBLISH_SCRIPT`），引用宿主能力的环境变量沿用宿主既有命名（如 `OPENCLAW_CONFIG_PATH`、`OPENCLAW_WORKSPACE`）。同一能力禁止存在两个并行环境变量，新增环境变量必须在 README + `sevo --help` + 配置参考中三处同步登记。

### 5.5 NFR 验收标准

- AC-5.1：任一阶段失败时，系统能明确回答失败位置、缺失工件和下一步动作。
- AC-5.2：任一完成结论都能找到对应文件或结构化证据。
- AC-5.3：更换执行 Agent 后，核心阶段语义不变。
- AC-5.4：审计、验证、账本三个阶段至少有一个独立于开发执行者。
- AC-5.5：受保护环境的登录与关键操作具备可追溯的操作者标识，支持审计追责。

### 5.6 Web 驾驶舱展示层验收标准

- AC-5.6（Web 层）：项目驾驶舱至少提供 Dashboard、Projects、FR 列表、待办队列、统计分析、交付物、通知中心、交付账本等稳定入口；导航引用的页面可直达，不允许出现 404、空白落地页或无效入口。
- AC-5.7（Web 层）：Projects 页面按项目展示 FR 完成进度、健康度和最近活动，并支持从项目视角钻取到对应 FR 列表或详情。
- AC-5.8（Web 层）：登录页把说明提示、错误反馈和输入控件做清晰区分；密码输入支持显示/隐藏；错误反馈有固定位置；页面提供获取访问权限的明确指引；移动端保留简短价值说明。
- AC-5.9（Web 层）：Dashboard 首屏优先展示失败项、阻塞项、待审批项或其他当前最危险对象，并支持一键钻取；风险提示使用红色或琥珀色语义；KPI 明确时间范围，并解释健康度、完成率等容易混淆指标的关系。
- AC-5.10（Web 层）：Dashboard 中的阶段分布、风险提示和关键指标卡片可钻取到对应对象列表；长内容区域提供明确的继续阅读或滚动提示。
- AC-5.11（Web 层）：FR 列表支持按项目、阶段、更新时间等维度搜索、筛选和排序，展示结果总数；时间信息使用中文习惯的绝对或相对格式；失败、阻塞状态的视觉优先级高于普通阶段标签。
- AC-5.12（Web 层）：FR 卡片默认只暴露状态、标题、阶段、更新时间和主动作；扩展说明按需展开；AI 判断文案依据当前阶段、风险和阻断原因生成，不能对不同 FR 大量重复模板化表述。
- AC-5.13（Web 层）：每条 FR 都有详情页，至少展示阶段历史、关联交付物、评审与复验记录、当前判断和下一步动作。
- AC-5.14（Web 层）：待办队列支持按类型、优先级和等待时长筛选排序，筛选项显示计数；门禁、澄清、失败三类待办有稳定且可快速识别的视觉区分；超时待办进入更强警示态。
- AC-5.15（Web 层）：待办、FR、通知等卡片型列表把主动作固定为明确按钮或整卡点击区域，避免动作入口与说明文案混淆。
- AC-5.16（Web 层）：统计分析页面在 0 异常或 0 失败时显示正向空状态，不以占位数据冒充真实结果；关键指标支持时间趋势、基准线或目标值对比；移动端优先展示风险结论和异常项目，并支持导出。
- AC-5.17（Web 层）：交付物页面优先帮助用户找到结果；移动端首屏先呈现命中结果或结果摘要，再呈现统计和高级筛选；预览区域展示真实文档摘要，不展示占位说明。
- AC-5.18（Web 层）：交付物、账本、FR、待办、通知等长列表在结果规模增长后仍可稳定浏览，必须提供分页或虚拟滚动，并展示总数与当前筛选命中数。
- AC-5.19（Web 层）：通知中心支持按级别筛选、未读计数、时间分组和全部已读；关键通知与普通信息在结构和颜色上有明显差异；下一步以简洁动作条呈现。
- AC-5.20（Web 层）：交付账本的筛选文案和状态标签对用户一眼可懂；证据链接可点击预览；次级说明默认折叠；界面不展示开发备注或内部说明；至少提供一种适合追踪时序演进的视图。
- AC-5.21（Web 层）：移动端 375px 宽度下，FR、待办、交付物、通知、账本等页面首屏优先露出首个可处理对象或主动作；筛选器、统计卡和长说明默认可折叠；不允许横向滚动。
- AC-5.22（Web 层）：状态、优先级、未读、阶段等标签在全站使用一致的颜色语义、视觉优先级和对比度；失败、阻塞、关键、未读的视觉权重高于普通信息。
- AC-5.23（Web 层）：图标按钮、顶部操作和筛选控件具备稳定的焦点态、清晰选中态、文本语义和键盘可达性；浅色标签与文字满足可读性要求。
- AC-5.24（Web 层）：驾驶舱提供全局搜索，可跨 Project、FR、交付物、通知和账本定位对象，并展示结果类型与跳转落点。
- AC-5.25（Web 层）：登录页、仪表盘、统计页和列表页的辅助文案以短句为主，不抢主操作；空状态、零结果和异常状态的提示语可直接指导下一步动作。
- AC-5.26（Web 层）：驾驶舱统一使用白色背景 + 黑色文字的亮色主题，列表密度切换和高频操作的快捷导航扩展；不因输入方式变化破坏信息层级。

## 6. 概念架构

### 6.1 核心对象类型

SEVO 管理的不是“聊天消息”，而是研发过程里的标准工件和状态对象。核心对象包括：

- **Project**：独立交付单元，拥有标准目录结构（§3.6），是 FR 流程实例的归属容器。
- **FR 流程实例**：一次完整的 SDD 流程执行实例，绑定到一个 Project，承载唯一 ID、当前状态、所属阶段和全部工件引用（§3.5）。
- **Pipeline Task**：FR 流程实例内部某个阶段的具体执行单元，用来承载该阶段里要完成的一次动作，如“写 spec”“做架构设计”“编码”“执行审计”。它不等于整条 FR 生命周期，而是从属于某个 FR 流程实例的阶段执行项；一条 FR 流程实例在完整 SDD 生命周期里会产生一个或多个 Pipeline Task，二者关系是一对多。
- **Stage Record**：某个阶段的执行记录，记录输入、输出、状态、阻断原因和通过结论。
- **Spec Package**：需求规格工件集合。
- **Spec Review Bundle**：需求规格门禁评审结果集合。
- **Contract Package**：架构、实现边界、工作包规划工件集合。
- **Contract Review Bundle**：四方会审结果集合。
- **Work Package**：可派发、可验收、可追责的最小实现单元，最小字段集至少包含 `id`、`title`、`status`、`spec_ref`、`artifacts[]`、`created_at`、`updated_at`。每个 Work Package 内部拆分为 Task 列表。
- **Task**：Work Package 内部的最小执行单元，粒度 2-5 分钟，最小字段集至少包含 `id`、`work_package_ref`、`title`、`target_files[]`、`expected_changes`、`status`、`verification_steps[]`。
- **Implementation Bundle**：某个工作包或某个阶段的实现结果集合。
- **Review Bundle**：实现后独立评审与审计结论集合。
- **Review Issue**：从评审包中提取的单个问题条目，包含严重级别（P0/P1/P2/P3）、关联 FR、问题工件定位、修复建议和当前状态（open/fixing/revalidating/closed/deferred）。
- **Fix Task**：由 Review Issue 自动生成的修复任务卡片，关联原 FR 流程实例 ID、评审报告引用和问题条目，承载修复执行和复验触发。
- **Regression Bundle**：回归验证结果集合。
- **Release Artifact**：发布制品及其版本元数据。
- **Verification Bundle**：清洁环境验证结果集合。
- **Ledger Entry**：交付账本记录，关联 FR 流程实例 ID，作为一次研发闭环的最终摘要对象。
- **Clarification Record**：澄清记录，记录模糊检测触发点、澄清问题、回复内容和收敛结论，挂接到对应阶段的 Stage Record。
- **PipelineEngine**：SEVO 的核心运行时引擎，负责 pipeline 实例的全生命周期推进。读取路由结果中的阶段队列，按顺序或并行通过 Adapter 触发阶段执行，监听完成事件，评估门禁，决定推进或阻断。PipelineEngine 定义编排语义，具体任务派发通过 Adapter 抽象层实现。
- **SEVO Config**：SEVO 的配置对象，承载渐进式披露的四级配置（L0 默认值 → L1 用户配置 → L2 自定义阶段 → L3 编程控制）。
- **Stage Queue**：pipeline 实例的阶段执行队列，由路由结果生成，PipelineEngine 按此队列推进。支持顺序阶段和并行阶段组。

### 6.2 阶段状态机

每个阶段至少支持以下状态：

- **pending**：等待开始。
- **active**：正在执行。
- **blocked**：被上游缺失、外部依赖或门禁失败阻断。
- **passed**：当前阶段通过。
- **failed**：当前阶段结论不通过，需要修复后重试。
- **skipped**：因任务级别裁剪而跳过。

状态流转规则：

- pending → active：前置阶段通过，且本阶段入口条件满足。
- active → passed：出口工件齐全，且本阶段验收通过。
- active → blocked：前置工件缺失、依赖未满足或门禁中断。
- active → failed：已执行但验收不通过。
- failed → active：问题修复后重新进入。
- pending → skipped：路由规则允许跳过，且跳过理由已记录。

### 6.3 阶段间数据流转

SEVO 的数据流是工件驱动，不是口头驱动：

0. PipelineEngine 接收 pipeline-created 事件，读取路由结果，生成 Stage Queue，开始自动推进。
0a. Pipeline Create 在用户已创建 Project、已新增 FR 的前提下，为该 FR 创建 FR 流程实例，绑定 Project，初始化目录结构，产出路由结果。
1. Spec 产出 Spec Package，作为 Spec Review Gate 的唯一需求输入。
2. Spec Review Gate 产出 Spec Review Bundle，决定是否允许进入 Contract。
3. Contract 产出 Contract Package 和 Work Package，作为 Contract Review Gate 与 Implement 的执行输入。
4. Contract Review Gate 产出 Contract Review Bundle，决定是否允许进入 Implement。
5. Implement 产出 Implementation Bundle，作为 Review 和 Regression 的验证基础。
6. Review 产出 Review Bundle，决定是否允许进入 Smoke Test。
   - 6a. Review 结论为有条件通过或不通过时，自动触发 Review Fix Loop：解析报告 → 生成 Review Issue → P0/P1 自动生成 Fix Task → Agent 认领修复 → 定向复验 → 问题关闭 → 门禁重新评估。循环直到放行条件满足。
   - 6b. Smoke Test 验证核心功能路径可用，通过后自动触发 UX Acceptance 和 PM Commercial Review 并行执行。
   - 6c. UX Acceptance 由 ux-01 按检查清单执行视觉验收。
   - 6d. PM Commercial Review 由 pm-01 执行商用就绪评审。UX Acceptance 和 PM Commercial Review 均通过后进入 Regression。
7. Regression 产出 Regression Bundle，决定是否允许生成 Release Artifact。
8. Deploy 产出 Release Artifact，作为 Verify 的唯一交付对象。
9. Verify 产出 Verification Bundle，决定 Ledger 是否可以写入通过结论。
10. Ledger 汇总全部关键工件，形成可查询、可复盘、可回流的交付账本。

### 6.4 核心原则

- 统一用工件交接，不靠聊天解释上下文。
- 统一用 PipelineEngine 驱动阶段推进，不靠主会话手工盯盘或人工触发下一阶段。
- 统一用阶段状态表达进展，不靠主观描述表达“差不多完成”。
- 统一用验收标准定义通过，不靠执行者自报完成。
- 统一保留证据链，方便复盘、审计和经验回流。

#### 6.4.1 核心逻辑与可配置实现的边界

SEVO 的设计必须明确区分“核心逻辑”和“可配置实现”，前者是 SEVO 引擎，后者通过 Adapter 适配。这是代码架构质量约束（职责分离、可测试性），不是支持其他平台的产品承诺。

判断标准（三问）：
1. 去掉这个能力，“研发流程闭环交付”还成立吗？不成立 = 核心逻辑。
2. 这个能力的实现方式是否可能随配置变化（如换通知渠道、换 LLM provider、换 Agent 池规模）？会变 = 放 Adapter。
3. 这个能力描述的是“做什么”还是“怎么做”？“做什么” = 核心逻辑，“怎么做” = 可配置实现。

核心逻辑（SEVO 引擎，不随配置变化）：
- 流程阶段语义（Spec→Contract→Implement→Review→Regression→Deploy→Verify→Ledger）
- 阶段状态机（每个阶段的输入工件、输出工件、状态变化规则）
- 门禁逻辑（Gate 的通过/阻断判定标准）
- 工件交接协议（阶段间通过工件传递上下文）
- 阶段执行原则注入（Stage-Bound Design，每个阶段该遵循什么原则）
- 账本留痕（每次交付都有证据链）
- 审计独立性（Review 必须独立于 Implement 执行者）
- 主动澄清（模糊检测 + 结构化提问 + 收敛回写）

可配置实现（因环境配置不同而不同，通过 Adapter 适配）：
- Agent 池配置（几个 Agent、叫什么名字、用什么模型）
- 执行治理实现方式（hook 注入 + prompt 引导）
- 工件存储位置（本地文件系统 / 数据库）
- 任务调度方式（sessions_spawn / CLI）
- 通知渠道（飞书 / Slack / Discord / 无通知）
- 并行策略（取决于 Agent 池大小和资源）

这个边界是 SEVO 代码架构设计的基础约束。所有 FR 和架构决策都必须经过三问检验，确保核心逻辑不混入可配置实现。

### 6.5 概念架构验收标准

- AC-6.1：任一阶段都能明确说清输入工件、输出工件和状态变化。
- AC-6.2：任一工作包都能挂接到上游 Spec 与下游 Ledger。
- AC-6.3：Spec Review Gate 和 Contract Review Gate 都有明确输入、输出和阻断语义。
- AC-6.4：跳过阶段不会造成账本断链。
- AC-6.5：状态机同时适用于 ACP agent 和原生 subagent。

### 6.6 流程阶段执行原则注入

SEVO 在派发任务时，根据任务所属的流程阶段自动注入该阶段应遵循的执行原则。原则绑定的是阶段，不是 Agent 身份——无论用户派谁来执行，只要在该阶段工作，就自动获得对应原则。

这些原则来源于经过验证的最佳实践（SDD 三阶段、wow-harness 执行治理、Karpathy Guidelines 等），由 SEVO 内建管理。

阶段与注入原则的映射：

- Spec 阶段：用户价值优先、需求完整度校验、概念-技术阶段隔离、主动澄清（模糊检测 + 结构化提问 + 收敛回写）。Spec 必须包含四个独立章节：用户人群（谁用、什么场景、什么设备）、痛点（用户现在怎么解决、哪里痛）、原始需求（用户要什么，用人话说）、用户体验流（完整操作步骤，从打开到完成）。缺任一个 spec-review-gate 打回。spec-review-gate 区分两种场景：首次定义时强制要求四章节完整存在；后续优化/迭代时只检查四章节仍然完整（存在性检查），不强制重写。
- UX Design 阶段：以陌生小白用户为设计基准，操作流必须简单易懂，不依赖命令行或内部知识，核心流程从打开页面到产出有意义结果全程可视化引导。
- Contract 阶段（架构设计）：通用化判断标准、问题定义先行、结构设计四问、约束先于方案、最简可行架构、合理复用宿主能力、主动澄清（技术模糊检测 + 需求矛盾上报）。架构必须满足陌生用户 init 后开箱即用（安装→初始化→核心功能自动运行，零手动配置）。
- Implement 阶段：最小改动（Surgical Changes）、最简实现（Simplicity First）、目标驱动执行（Goal-Driven）、主动澄清（不清楚就问，不猜测后开发）。
- Review / Regression 阶段：独立性（不做开发只做检查）、可验证结论（附证据）、不放过设计方向问题。
- Contract Review Gate（四方会审）：各方按自己的审查维度注入对应原则（产品视角、开发视角、质量视角、体验视角）。

核心设计约束：
- 原则绑定阶段，不绑定 Agent。用户可以派任何 Agent 执行任何阶段，SEVO 不限制。
- 原则是指导而非门禁：注入后 Agent 应遵循，但不会因为违反原则而被机械式阻断（与 Session Guards 的强制路由区分）。
- 原则集可编辑、可扩展，新增阶段或新增原则时不需要改代码。

验收标准：
- AC-6.6.1：派发 Contract 阶段任务时，执行上下文中包含架构设计执行原则，无论执行者是谁。
- AC-6.6.2：派发 Implement 阶段任务时，执行上下文中包含开发执行原则，无论执行者是谁。
- AC-6.6.3：原则集可编辑、可扩展，新增阶段或新增原则时不需要改代码。
- AC-6.6.4：原则注入失败时，任务仍可执行（降级而非阻断）。
- AC-6.6.5：用户派一个任意 Agent 执行 Contract 阶段，流程正常跑通，且该 Agent 收到架构设计原则。

## 7. 与 Self-Evolving Harness 其他模块的边界

### 7.1 与 KIVO 的边界

KIVO 负责知识、规则、意图和经验资产的编译、检索、治理与回流。SEVO 消费这些资产，但不替代 KIVO 做知识治理。

- KIVO 提供：历史规格、方法论、规则、经验、意图线索。
- SEVO 负责：把这些输入转成一次具体研发任务的流程推进与交付闭环。
- SEVO 内部的阶段规则属于流程约束，例如"Specify 阶段必须通过概念定义四问""Contract 阶段必须经过四方会审后才能进入 Implement"。这些规则定义的是流程怎么推进、何时阻断、何时放行。
- KIVO 的 Rule Entry 属于知识治理对象，用来存档、检索、分发和追踪某条规则资产，例如某个术语的标准定义、某条方法论约束、某个经验规则的版本化记录。
- 两者层面不同：SEVO 的阶段规则是真相源，决定流程行为；KIVO 的 Rule Entry 是知识管理与分发载体，可以引用 SEVO 规则，但不改写 SEVO 的流程语义。
- 边界结论：KIVO 管“知道什么”，SEVO 管“如何把一次研发任务做完”。

### 7.2 与 AEO 的边界

AEO 负责度量 Agent 效果、发现漂移、诊断根因、推动优化。SEVO 负责把一次研发任务执行完并沉淀账本。

- AEO 关注：阶段耗时、失败分布、Agent 表现、质量漂移。
- SEVO 关注：阶段工件、门禁结论、交付闭环。
- 边界结论：AEO 管“做得怎么样”，SEVO 管“按什么流程做完”。

### 7.3 与 Claw Design 的边界

Claw Design 是面向设计产物生成与交付的独立产品。SEVO 可以作为其研发流水线，但不吞并其业务能力。

- Claw Design 负责：图表、PPT、海报、架构图等设计产物能力。
- SEVO 负责：Claw Design 自身功能研发时的规格、实现、审计、验证和交付记录。
- 边界结论：Claw Design 是被研发的产品，SEVO 是研发该产品时使用的流水线。

### 7.4 与 OpenClaw 环境的边界

- OpenClaw 负责：Agent 运行、工具接入、消息调度、执行沙箱。
- SEVO 负责：阶段语义、工件语言、门禁逻辑、验收闭环。
- 边界结论：SEVO 定义流程语义，OpenClaw 提供执行基础设施。代码架构通过 Adapter 抽象层保持职责分离，不把流程写死到某个目录结构或 hook 协议里。
- 推荐适配模式：OpenClaw 环境支持 git worktree 时，Implement 阶段在独立 worktree 中执行，主分支不受影响。worktree 隔离支持多工作包并行开发，失败时可直接丢弃 worktree 回滚，不污染主工作区。

## 8. Wave 规划

### Wave 1：最小可用闭环

目标：先把“能闭环交付”跑通。

范围：

- 支持 8 阶段的最小语义定义和 2 个关键门禁。
- 支持 FR 流程实例创建、Project 目录自动初始化和路由判定。
- 支持 Level 0 / Level 1 / Level 2+ 路由。
- FR-13 PipelineEngine 最小实现：顺序推进 + 门禁评估 + 单项目。不含并行阶段、不含多项目调度。
- FR-14 Package Distribution & CLI：npm install + sevo init + 插件注册 + 核心命令集（init / project create / fr add / status）。
- 支持 Spec、Spec Review Gate、Contract、Contract Review Gate、Implement、Review、Regression、Verify、Ledger 的基础工件。
- 支持工作包级证据记录与独立评审。
- 支持账本落盘与可追溯引用。

验收：

- 陌生用户 `npm install` + `sevo init` 后，5 分钟内能创建 Project、添加 FR、看到 pipeline 自动推进到 Spec 阶段并产出 Spec Package。
- 一条中等复杂度研发任务可完整走完，从 Pipeline Create 到 Ledger。
- 任一阶段都能拿出对应工件。
- 最终交付有 Ledger Entry，关联到 FR 流程实例 ID。

### Wave 2：增强治理与自动化

目标：把“能跑”升级为“跑得稳、查得快”。

范围：

- FR-15 Progressive Disclosure（L1/L2 配置能力）。
- FR-16 Onboarding Experience（demo 命令）。
- FR-14 补充命令：pause / resume / cancel / ledger。
- 路由判定自动化。
- 门禁检查脚本化。
- 评审修复闭环自动化（Review Fix Loop）。
- 风险分级与验证厚度联动。
- 长流程持久化编排。
- 审计与验证模板标准化。

验收：

- 长流程不依赖主会话手工盯盘。
- 阻断原因和缺失工件可结构化输出。
- Review / Regression / Verify 的结论格式统一。

### Wave 3：完整产品化

目标：把 SEVO 做成成熟的 OpenClaw 研发流水线产品，完善编程控制和高级配置能力。

范围：

- FR-15 L3 编程控制、Adapter SDK。
- 支持自定义 Adapter 实现（替换通知、发布、LLM 调用等实现细节）。
- 支持统一账本查询、复盘与经验回流接口。
- 支持更多交付目标和发布形态。
- 支持将阶段效果数据回流到 AEO，将经验沉淀回流到 KIVO。

验收：

- Adapter SDK 文档完善，用户可自定义通知、发布、LLM 调用的实现。
- 账本、审计、验证三类工件可以被外部系统消费。
- 流水线能力完整覆盖从创建到交付的全生命周期。

## 9. 约束与假设

### 9.1 约束

- SEVO 为 OpenClaw 环境提供研发流水线，代码架构通过 Adapter 抽象层保持职责分离和可测试性。
- SEVO 输出的是规格语言、阶段语言和工件语言，不直接等同某种技术栈。
- 任何“完成”结论都要有可验证工件支撑。
- 审查与实现阶段默认分离，高风险改动不能只靠实现阶段执行者自证。
- 长流程需要状态持久化，不能依赖主会话长期占线。

### 9.2 假设

- OpenClaw 环境提供文件读写、任务派发（sessions_spawn）和结果回收（completion event）能力。
- 每个阶段至少能落一个可读工件，而不是只有口头说明。
- 团队或系统愿意为质量闭环付出额外成本，而不是只追求最快生成。
- 用户接受按任务级别裁剪流程，但不接受没有证据链的交付。

### 9.3 非目标

- SEVO 不负责替代 IDE、代码编辑器或具体模型提供商。
- SEVO 不负责定义业务产品本身的全部功能细节，那是具体产品 spec 的职责。
- SEVO 不负责知识库治理、效果运营或设计产物生成本身，这些分别属于 KIVO、AEO、Claw Design。

### 9.4 进度透明约束

- 项目进度必须对用户实时可见，禁止用户需要主动追问才能知道进展。
- 每个 FR 的完成状态（已完成/未完成）必须在项目驾驶舱实时展示。
- 任务完成、阶段推进、进度变化时，必须通过 IM 主动通知用户。
- 进度汇报以 spec 中全部 FR 为分母，已实现 FR 为分子；禁止用内部分期偷换完成度口径。
- 只有 spec 中所有 FR 全部实现并通过审计，才能汇报「项目完成」。
- 驾驶舱作为用户主入口时，首页首屏优先暴露当前最危险 FR、最紧急待办和关键异常，不把可处理对象藏在统计卡和长文案之后。

### 9.5 Web 驾驶舱边界

- Web 驾驶舱负责项目、FR、待办、通知、交付物、账本等对象的展示、筛选、钻取、告警和处理入口。
- 只影响页面信息架构、视觉表达、交互效率和访问体验的问题，归入 Web 展示层，不改变 SEVO 核心流程引擎语义。
- Web 层必须忠实呈现核心流程工件与状态，不允许用占位内容、无效页面或不可点击证据链接掩盖真实能力缺口。
- Web 层的搜索、分页、排序、响应式、可访问性和主题能力属于体验能力，不改变 FR 流程实例、门禁和工件的定义边界。

### 9.6 Specify 阶段质量门禁

#### 概念定义四问（Specify 阶段强制）

spec 中出现的每个名词实体（会成为系统中的对象、状态机、UI 元素的东西），必须能回答四个问题：

1. 它的存在解决了什么问题？（存在理由）
2. 用它的人是谁？（使用者）
3. 如何使用？（交互方式）
4. 使用的边界是什么？（scope，什么情况下不适用）

回答不了任何一个 = 概念模糊 = 不能作为功能实体写进 spec。

补充规则：

- 品牌词/营销词可以出现在产品名称中，但不能作为功能实体出现在 FR 定义里。
- 发现概念模糊时，先停下来定义清楚，再继续写 FR。
- 违反 = Specify 阶段门禁不通过，需返工。

定位：SEVO 是研发基础设施，所有工程流程约束都沉淀在 SEVO 中。角色（如 pm-01）可以引用 SEVO 的规则，但规则本体在 SEVO。

### 9.7 总体验收标准

- AC-9.1：文档完整覆盖产品定位、用户、8 阶段 FR、2 个关键门禁、NFR、概念架构、模块边界、Wave 规划和约束。
- AC-9.2：文档内容清晰区分核心流程逻辑与 Adapter 实现细节。
- AC-9.3：读者可以据此进入后续 Spec Review 和 Contract 设计，不需要额外口头补课。
- AC-9.4：文档正文不含修订痕迹、过程噪音和 AI 套话。

### 9.8 待补 spec 章节（已知违反清单）

FR-02-pre AC-4.4j 要求受管项目 `docs/product-requirements.md` 主文件在「功能需求」之前独立出现四章：用户人群、痛点、原始需求、用户体验流。以下项目主文件当前不合规，需在后续 wave 补齐后才能通过本 spec-review-gate。补齐任务不在本 wave 范围，仅在此登记，避免后续遗忘。

| 受管项目 | 主文件路径 | 已有章节 | 缺失章节 |
| --- | --- | --- | --- |
| sevo | `projects/sevo/docs/product-requirements.md` | 「目标用户画像」（可被 LLM 语义判定为「用户人群」） | 痛点、原始需求、用户体验流 |
| kivo | `projects/kivo/docs/product-requirements.md` | 「目标用户画像」（同上） | 痛点、原始需求、用户体验流 |
| aco | `projects/aco/docs/product-requirements.md` | 「目标用户画像」（同上） | 痛点、原始需求、用户体验流 |
| claw-design | `projects/claw-design/docs/product-requirements.md` | 无 | 用户人群、痛点、原始需求、用户体验流（四章全缺） |
| exam-sprint | `projects/exam-sprint/docs/product-requirements.md` | 用户人群、痛点、原始需求、用户体验流 | 无（合规，仅需复检顺序是否位于「功能需求」之前） |

补齐优先级（由后续 wave 插入 SEVO 流水线不在本 AC 范围）：

1. **sevo 自身**：本 spec 必须同步补齐三章，否则 AC-4.4j 适用于 SEVO 自身时会在下一轮 spec-review-gate 被自己打回。
2. **kivo / aco**：同为核心受管项目，必须在 AC-4.4k 生效后的首轮 spec-review-gate 之前补齐。
3. **claw-design**：四章全缺，补齐工量最大，需单独拆 wave。
4. **exam-sprint**：已有四章实体，仅需验证顺序与 LLM 语义判定是否达标，不达标时补内容。

本清单不是评审结论，仅作为状态登记。Pre-Gate 实际运行时，以调用时对应项目主文件的 LLM 语义判定为准，不以本表为准。
