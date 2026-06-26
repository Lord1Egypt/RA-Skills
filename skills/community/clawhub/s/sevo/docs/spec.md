# SEVO — 需求规格说明书

OpenClaw（sa-01 子Agent）| 2026-04-24

---

## 产品定位

SEVO 是一个 OpenClaw 插件，让 AI Agent 按照标准研发流程（需求→架构→编码→审计→验证→部署）自动完成软件开发，每一步都有质量门禁和可追溯记录。

### 目标用户

- 主要用户：使用 OpenClaw + AI Agent 做软件开发的技术负责人，需要流程自动化和质量保障
- 次要用户：任何 ACP 兼容环境的开发者，需要结构化的 Agent 研发流程

### 使用场景

- 从零开发一个新的 OpenClaw skill 或插件
- 对现有系统做跨模块重构
- 修复涉及数据模型变更的 bug
- 团队新成员接手项目，需要标准化研发流程

### 竞品差异化

- vs 手动管理 Agent：SEVO 自动化全流程，人只需定义需求和做方向性决策
- vs GitHub Actions/CI：SEVO 管理的是 Agent 研发流程（需求→架构→编码），不是代码构建流程（编译→测试→部署）
- vs Devin/Cursor Agent：SEVO 是流程编排层，不是 Agent 本身；它可以调度任何 ACP 兼容的 Agent

---

## 一、功能需求（FR）

### S. Specify 阶段（需求冻结）

#### FR-S01: SEVO 流水线触发 ｜ 已实现(插件)

命中以下任一条件的任务，必须走 SEVO 完整流水线（Specify → Execute → Verify → Operate），禁止直接编码：
- 从零新建模块或系统
- 跨域改动（涉及 2 个以上域的边界变更）
- 预估改动超过 500 行或 10 个文件
- 涉及数据模型变更

**AC:**
- AC1: 流水线接收到任务描述后，自动评估是否命中强制触发条件
- AC2: 命中时自动创建完整 SEVO 流水线（含 spec → spec-review-gate → contract → implement → review → verify 全阶段）
- AC3: 未命中时走轻量流程（implement → review → verify）
- AC4: 触发评估结果写入流水线事件日志

#### FR-S02: 需求规格产出 ｜ 已实现(插件)

流水线 spec 阶段自动派发需求规格编写任务。

**AC:**
- AC1: spec 阶段的 task prompt 包含项目名称、上下文引用、产出路径要求
- AC2: 产出文件路径为 `docs/design/product-requirements.md`
- AC3: 产出必须包含 FR 列表和每个 FR 的验收标准（AC）
- AC4: 未写入文件视为阶段失败

#### FR-S03: Spec Review 门禁 ｜ 已实现(插件)

Spec 写完后，必须经过架构师评审，评审通过才能进入 Plan 阶段。

**AC:**
- AC1: spec 阶段完成后，流水线自动创建 spec-review-gate 阶段任务
- AC2: 评审产出写入 `reports/<project>-spec-review.md`
- AC3: 评审结论三档：通过 / 有条件通过（列出必须解决的问题）/ 不通过（列出阻断问题）
- AC4: 「有条件通过」触发修复→复审循环；「不通过」回退到 spec 阶段重做
- AC5: 评审通过后流水线自动推进到下一阶段

#### FR-S04: 测试用例编写 ｜ 已实现(插件)

Spec Review 通过后，自动派发测试用例编写任务。

**AC:**
- AC1: 测试用例基于冻结的 spec 编写，覆盖每个 AC
- AC2: 产出为独立文档 `docs/design/test-cases-<project>.md`
- AC3: 每个 AC 至少对应一条测试用例，含测试方法、预期结果、优先级
- AC4: 测试用例在后续 Review 和 Regression 阶段被引用

#### FR-S05: 编码任务 AC 逐条覆盖 ｜ 已实现(插件)

编码任务的 task prompt 必须显式列出所有待实现的 AC 编号和摘要。

**AC:**
- AC1: 主会话派发编码任务时，从 spec 中提取 AC 列表写入 task prompt
- AC2: 编码 Agent 完成后逐条自检每个 AC 的实现状态
- AC3: 回复中包含 AC 覆盖清单（AC编号 + 覆盖/未覆盖/部分覆盖 + 对应代码位置）
- AC4: 未覆盖的 AC 必须说明原因

#### FR-S06: 阶段方法论注入 ｜ 已实现(插件)

每个流水线阶段的 task prompt 包含该阶段对应的方法论指导，确保 Agent 按最佳实践执行。

**AC:**
- AC1: spec 阶段注入需求规格方法论（批判性思维清单、第一性原理、概念架构隔离、Phase 隔离禁止技术选型）
- AC2: contract 阶段注入架构设计方法论（arc42 模板、Phase 隔离、Gate Check 7 项、ADR 纪律）
- AC3: spec-review-gate / contract-review-gate 注入发散验证方法论（7 维审查、交叉审计、三档结论）
- AC4: review 阶段注入安全审查方法论（OWASP Top 10:2025、git diff-aware 漏洞检测、置信度阈值）
- AC5: implement 阶段注入编码纪律（最小改动、最简实现、目标驱动执行）
- AC6: test-case-authoring / smoke-test 注入测试方法论（AC 覆盖规则、边界值、独立验证者）
- AC7: 方法论内容由 methodology.js 模块统一管理，task-mapper.js 通过 spread 注入各阶段 prompt

### E. Execute 阶段（架构设计 + 编码实现）

#### FR-E01: 架构设计（Contract）｜ 已实现(插件)

Spec Review 通过后，自动派发架构设计任务。

**AC:**
- AC1: 架构设计使用 arc42 模板，产出 `docs/architecture/arc42-architecture.md`
- AC2: 关键决策写 ADR（`docs/architecture/decisions/ADR-*.md`）
- AC3: arc42 必须定义对外暴露的 Skill 接口清单
- AC4: 架构设计引用 spec 和 spec-review 产出

#### FR-E02: 三方会审门禁（Contract Review Gate）｜ 已实现(插件)

架构设计完成后，必须经过三方评审。

**AC:**
- AC1: 三方并行评审：产品视角（pm-01）、开发视角（编码 Agent）、质量视角（audit-01）
- AC2: 各自产出评审报告写入 `reports/<project>-arch-review-<agentId>.md`
- AC3: 评审结论三档：通过 / 有条件通过 / 不通过
- AC4: 修复后只需未通过方复审，不需要三方重新全审
- AC5: 三方全部通过后自动进入编码阶段

#### FR-E03: 编码实现（Implement）｜ 已实现(插件)

架构设计通过后，自动派发编码任务。

**AC:**
- AC1: 编码任务的 task prompt 引用 spec、arc42、测试用例文档路径
- AC2: 编码 Agent 按 AC 逐条实现
- AC3: 编码完成后产出包含 AC 覆盖清单

#### FR-E04: Agent 梯队路由 ｜ 已实现(插件)

流水线根据阶段类型自动选择最优 Agent。

**AC:**
- AC1: 每个阶段有默认的 Agent 映射（tier + agentId + timeout）
- AC2: 映射可通过配置覆盖（stageAgentMap）
- AC3: 编码任务优先派 T1/T2 ACP agent（cc/free-code），审计任务派 audit-01，架构任务派 sa-01
- AC4: agentId 为 null 时由主会话根据空闲池动态选择

#### FR-E05: 长文档分段式写作 ｜ 已实现(插件)

预估产出超过 300 行或 15KB 的文档任务，首次派发即分段。

**AC:**
- AC1: 流水线评估阶段产出预期大小，超阈值时自动拆分为多段任务
- AC2: 第一段输出目录 + 前半章节，第二段续写剩余章节
- AC3: 后续段的 task prompt 引用前段产出路径，要求 append/edit 而非覆盖
- AC4: 失败后禁止原样重派，必须拆段或升级梯队

#### FR-E06: 并行任务文件名隔离 ｜ 已实现(插件)

多 Agent 并行执行同一任务时，产出文件名必须包含 agentId 标识。

**AC:**
- AC1: 流水线生成的 task prompt 中，产出路径包含 agentId 后缀
- AC2: 禁止多个 Agent 写入相同路径

### V. Verify 阶段（审计 + 验证）

#### FR-V01: 独立代码审计（Review）｜ 已实现(插件)

编码完成后，自动派发独立 Agent 做质量审计。

**AC:**
- AC1: 审计由 audit-01/audit-02 执行，禁止开发者自审
- AC2: 审计引用 spec、arc42、编码产出
- AC3: 审计报告写入 `reports/<project>-review.md`
- AC4: 审计报告按 P0-P3 分级列出问题

#### FR-V02: Post-Completion 自动推进链 ｜ 已实现(插件)

收到开发任务 completion event 后，主会话按链条自动推进。

**AC:**
- AC1: 开发完成 → 自动派 audit-01 做代码审计
- AC2: 审计通过 → 自动派编码 Agent 写 smoke test 并执行
- AC3: smoke test 通过 → 有 Web 页面则派 ux-01 做视觉验证，纯后端跳过
- AC4: 视觉验证通过（或跳过）→ 闭环汇报用户
- AC5: 链条中任何一步失败 → 自动派修复 → 修复完成后从失败步骤重新开始
- AC6: 只有 P0 问题需要用户做方向性决策时才停下来

#### FR-V03: 评审→修复→复验自动闭环 ｜ 已实现(插件)

收到评审 completion 后，自动提取问题并派发修复。

**AC:**
- AC1: 从评审报告中提取 P0/P1 问题
- AC2: P0 问题当场拆分修复任务并派发，不等用户确认
- AC3: P1 问题与 P0 同批派发或排队
- AC4: P2/P3 问题记录待办，不阻断当前批次
- AC5: 修复完成后自动派原评审 Agent 复验
- AC6: 复验通过才算闭环；不通过则继续修复→复验循环

#### FR-V04: 回归测试（Regression）｜ 已实现(插件)

审计通过后，执行回归测试。

**AC:**
- AC1: 执行所有测试用例，报告 pass/fail 及证据
- AC2: 产出 `reports/<project>-regression.md`
- AC3: 回归失败阻断后续阶段

#### FR-V05: 端到端 Smoke Test 门禁 ｜ 已实现(插件)

Implement 完成且代码审计通过后，必须执行端到端 smoke test。

**AC:**
- AC1: smoke test 从用户真实操作视角执行
- AC2: 有 Web 页面的项目通过浏览器实际操作，附带截图证据
- AC3: smoke test 由 UX 角色或独立验证者执行，禁止开发者自测
- AC4: 失败阻断后续流程，修复后重新执行直到通过

#### FR-V06: UX 体验验收 ｜ 已实现(插件)

编码完成 + 代码审计通过后，有 Web 页面的产品必须经过 UX 验收。

**AC:**
- AC1: UX 验收由 ux-01 执行：Playwright 操作真实页面 + 截图 + 逐页审查
- AC2: P0=0 且 P1≤3 为通过
- AC3: 验收产出写入 `reports/ux-review-<product>-<date>.md`
- AC4: 不通过 → 修复 → 复验循环
- AC5: 纯后端/CLI 产品豁免

#### FR-V07: 泛化审查门禁（Publish Generalization Gate）｜ 已实现(插件)

发布前检查实现是否足够通用。

**AC:**
- AC1: 检查是否有硬编码假设
- AC2: 结论三档：通过 / 有条件通过 / 不通过
- AC3: 产出 `reports/<project>-generalization-review.md`

#### FR-V08: 端到端功能验证 ｜ 已实现(插件)

PM/UX 验收前，每个 skill/模块必须先通过端到端功能验证。

**AC:**
- AC1: 用真实输入调用核心函数，检查输出是否符合预期
- AC2: 验证脚本放 `scripts/test-<skill>.js`
- AC3: 验收报告必须附上实际运行结果
- AC4: 触发条件：任何 skill 新建或重大修改后的首次验收

### O. Operate 阶段（部署 + 留痕 + 运营）

#### FR-O01: 部署（Deploy）｜ 已实现(插件)

验证通过后，执行部署。

**AC:**
- AC1: 按架构文档中的部署流程执行
- AC2: 部署完成后触发 post-deploy 验证

#### FR-O02: Post-Deploy 验证（Verify）｜ 已实现(插件)

部署后执行 smoke test 验证。

**AC:**
- AC1: 对已部署系统执行 smoke test
- AC2: 产出 `reports/<project>-verify.md`
- AC3: 验证失败触发回滚流程

#### FR-O03: 交付账本（Ledger）｜ 已实现(插件)

流水线完成后，所有工件和决策记录写入交付账本。

**AC:**
- AC1: 收集所有阶段的产出工件路径
- AC2: 写入结构化的账本记录
- AC3: 账本可查询、可追溯

#### FR-O04: 流水线事件日志 ｜ 已实现(插件)

所有流水线状态变化写入事件日志。

**AC:**
- AC1: 事件类型覆盖：completion_received、advanced、pipeline_completed、hook_error、label_injected、prompt_injected
- AC2: 每条事件包含 timestamp、pipelineId、stageId
- AC3: 事件日志路径可配置（默认 `logs/sevo-pipeline-events.jsonl`）
- AC4: 写入失败不阻断流水线（fail-open）

#### FR-O05: Completion 自动推进 ｜ 已实现(插件+规则)

每个 completion event 到达时，立即检查并派发下一个任务。

**AC:**
- AC1: 收到 subagent_ended 事件后，解析 SEVO label 识别所属流水线和阶段
- AC2: 调用 PipelineEngine.advance() 推进流水线状态
- AC3: 新激活的阶段自动生成 task prompt 并排入待派发队列
- AC4: 通过 before_prompt_build hook 将待派发任务注入主会话
- AC5: 禁止等同批所有任务完成后再统一规划

#### FR-O06: 任务失败重试策略 ｜ 已实现(插件)

阶段失败后的自动重试和升级机制。

**AC:**
- AC1: 同梯队 agent 失败 1 次后，禁止原样重派
- AC2: 必须二选一：拆分（大任务拆小）或升级（派更高梯队 agent）
- AC3: 收到失败 completion 时，若有空闲 agent，立即优化后重派
- AC4: output_tokens 极低（<3k）且未写入文件，视为实质失败
- AC5: 任务描述超过阈值时自动建议拆分

#### FR-O07: 进度透明 ｜ 已实现(插件)

项目进度对用户实时可见。

**AC:**
- AC1: 每个 FR 的完成状态在驾驶舱 Web 页面实时展示
- AC2: 任务完成、阶段推进时通过 IM 主动通知用户
- AC3: 以 spec 中全部 FR 为分母汇报进度，禁止用内部分期偷换口径
- AC4: 每次阶段推进时自动更新 sevo-progress.json

#### FR-O08: 研发流程改进双写 ｜ 已实现(插件)

用户提出的研发流程改进必须同时落地到两个地方。

**AC:**
- AC1: 本地 md（AGENTS.md / SOUL.md）立即写入，L6 层临时兜底
- AC2: SEVO 产品层（spec → arc42 → 代码）走完整 SEVO 流水线永久固化
- AC3: 完整链条：本地 md 写入 → spec 补 FR/AC → arc42 更新 → 代码实现 → 审计验证
- AC4: 检测到审计报告中的流程改进建议时自动注入双写提醒

#### FR-O09: 运行中任务补充 ｜ 已实现(插件)

对已派发的进行中任务有新信息时，必须立即干预。

**AC:**
- AC1: 通过 steer 注入补充信息
- AC2: steer 不适用时，kill 后用更新的任务描述重派
- AC3: 禁止等任务自然完成后再返工
- AC4: pendingSupplements Map 存储待注入的补充信息
- AC5: before_prompt_build hook 中自动将 supplement 注入 task prompt

#### FR-O10: Agent 自动发现与自适应映射 ｜ 已实现(插件)

流水线启动时自动检测当前 OpenClaw 实例的可用 Agent 池，按能力分类映射到各阶段。

**AC:**
- AC1: 插件 init 时读取 openclaw.json agents.list，将每个 agent 分类为 coding / review / architecture / pm / general
- AC2: 每个阶段有推荐 agent 和降级链，推荐不可用时自动降级到下一候选
- AC3: 降级链末端 fallback 为 main（主会话）
- AC4: Agent 池变化时（新增/删除 agent）下次流水线自动适配，无需手动配置

#### FR-O11: 最小运行模式 ｜ 已实现(插件)

只有 1 个 agent（main）时，SEVO 仍能完整运行全部 15 个阶段。

**AC:**
- AC1: 单 agent 模式下所有阶段串行执行
- AC2: 跳过"开发者不能自审"约束，在 prompt 中注入双视角提示
- AC3: 启动时日志明确提示"SEVO 运行在最小模式"
- AC4: 最小模式下流水线功能完整，只是质量保障降级（无独立审计）

#### FR-O12: 安装与初始化 ｜ 已实现(脚本)

提供 `sevo init` 命令或安装脚本，自动完成插件注册。

**AC:**
- AC1: 自动将 sevo-pipeline 注册到 openclaw.json plugins
- AC2: 自动注册 before_prompt_build 和 subagent_ended hooks
- AC3: 检测当前 agent 池并输出适配报告
- AC4: 安装后 `openclaw doctor` Errors: 0

#### FR-O13: 路径配置化 ｜ 未实现

所有产出路径可配置，不硬编码。

**AC:**
- AC1: spec / arc42 / test-case / report 等产出路径通过配置文件或流水线参数指定
- AC2: 默认路径遵循 OpenClaw workspace 约定（docs/design/、docs/architecture/、reports/）
- AC3: 用户可在 sevo:create 时覆盖默认路径

#### FR-O14: 外部用户文档 ｜ 已实现(文档)

提供面向外部用户的完整文档。

**AC:**
- AC1: README.md 包含产品介绍、安装步骤、快速上手（5 分钟跑通第一个流水线）
- AC2: 配置参考文档（所有可配置项、默认值、示例）
- AC3: 阶段说明文档（15 个阶段的职责、输入输出、可跳过条件）
- AC4: 故障排查文档（常见错误、降级行为、日志位置）

#### FR-O15: 阶段内 FR 级完成度追踪与自动补派 ｜ 已实现(插件)

每个阶段启动时，从 spec 提取该阶段涉及的全部 FR 列表，逐条追踪完成状态。阶段内有未完成 FR 时自动派发剩余任务，所有 FR 完成后才允许推进到下一阶段。该逻辑在 L2 插件层硬执行，不依赖主会话 prompt 记忆。

**AC:**
- AC1: implement 阶段启动时，插件从 spec 文件解析全部 FR 列表及其实现状态标记
- AC2: 每个 FR 的完成事件（子任务 completion + spec 标记更新）被插件捕获并更新内部追踪状态
- AC3: 阶段内有未完成 FR 时，插件通过 before_prompt_build 注入 [SEVO Auto-Advance] 指令，指示主会话派发剩余 FR 的开发任务
- AC4: 所有 FR 标记为已实现后，插件才允许阶段推进到 review；未全部完成时阻断推进
- AC5: 追踪状态持久化到流水线状态文件（active-pipelines.json），会话重启后可恢复
- AC6: 适用于所有涉及多 FR 的阶段（implement、review、smoke-test 等），不仅限于 implement

#### FR-O16: 项目产出物隔离 ｜ 已实现(插件)

SEVO 流水线创建的每个项目的产出物（spec、架构文档、代码、测试、报告）隔离到独立目录，不散落在用户 workspace 根目录。

**AC:**
- AC1: `sevo:create <slug>` 时，插件自动创建 `projects/<slug>/` 目录作为项目根
- AC2: 该项目所有阶段的产出物路径基于 `projects/<slug>/` 而非 workspace 根
- AC3: 多个项目并行时产出物互不干扰
- AC4: 项目目录可直接作为独立 Git 仓库初始化

#### FR-O17: 用户体验流方法论注入 ｜ 已实现(插件)

SEVO 的 spec 阶段和 ux-acceptance 阶段必须强制注入“完整用户体验流走查”方法论，确保产出的产品覆盖从获取到日常使用的全链路。

**AC:**
- AC1: methodology.js 新增 `getUserJourneyTemplate()` 函数，返回结构化用户体验流模板（获取→安装→首次使用→核心流程→错误恢复→升级）
- AC2: spec 阶段的 task prompt 中注入用户体验流模板，要求 PM agent 必须在 spec 中画出完整用户旅程
- AC3: spec-review-gate 阶段将“用户体验流完整性”作为硬性审查维度（缺失 = P0 阻断）
- AC4: ux-acceptance 阶段的 task prompt 中注入用户体验流模板，要求 UX agent 按流程逐步验收
- AC5: 方法论内置在插件代码中，不依赖外部 SOUL.md 或用户配置

#### FR-D01: 分发与获取 ｜ 已实现(插件)

SEVO 通过 GitHub 和 ClawHub 双渠道分发，用户可通过一条命令安装。

**AC:**
- AC1: GitHub 仓库（yuchangxu1989-Openclaw/sevo）提供完整插件代码和安装脚本
- AC2: README 包含从 clone 到首次使用的完整步骤
- AC3: 安装命令自动处理依赖检测（OpenClaw 版本兼容性）
- AC4: 安装失败时输出人类可读的错误信息和修复建议

#### FR-D02: 首次使用引导（FTUE）｜ 已实现(插件)

用户安装 SEVO 后，5 分钟内能跑通第一个流水线并看到结果。

**AC:**
- AC1: 安装完成后输出下一步提示，引导用户创建第一个项目
- AC2: 提供内置示例项目（如 hello-sevo），演示完整流水线
- AC3: 示例流水线使用轻量流程（跳过三方会审和 UX 验收），3-5 分钟内完成
- AC4: 流水线运行过程中实时输出阶段进度
- AC5: 完成后输出产出物清单和下一步建议

#### FR-D03: 流水线手动干预 ｜ 已实现(插件)

用户可以暂停、跳过、重启流水线的任意阶段。

**AC:**
- AC1: sevo:pause 暂停流水线
- AC2: sevo:skip 跳过指定阶段
- AC3: sevo:retry 重试失败阶段
- AC4: sevo:resume 恢复暂停的流水线
- AC5: 所有干预操作写入事件日志

#### FR-D04: 流水线状态查询 ｜ 已实现(插件)

用户可在对话中查看流水线状态。

**AC:**
- AC1: sevo:status 列出所有活跃流水线及当前阶段
- AC2: sevo:status <id> 显示单个流水线详细进度
- AC3: sevo:list 列出所有历史流水线
- AC4: 输出格式人类可读

#### FR-D05: 版本管理与升级 ｜ 已实现(插件)

SEVO 遵循语义化版本，提供安全的升级路径。

**AC:**
- AC1: 版本号遵循 semver
- AC2: 升级前自动备份当前配置和活跃流水线状态
- AC3: 状态文件 schema 变更时提供自动迁移
- AC4: major 版本升级需用户确认

#### FR-D06: 错误诊断与用户提示 ｜ 已实现(插件)

流水线失败时，用户看到结构化的诊断信息。

**AC:**
- AC1: 每种已知错误类型有人类可读错误码和修复建议
- AC2: 错误信息包含错误码、描述、可能原因、建议操作
- AC3: sevo:diagnose 对失败流水线做深度诊断

#### FR-D07: 配置验证与自检 ｜ 已实现(插件)

提供 sevo:doctor 命令验证安装和配置完整性。

**AC:**
- AC1: 检查插件注册状态
- AC2: 检查 hook 注册状态
- AC3: 检查 Agent 池可用性
- AC4: 检查依赖版本兼容性
- AC5: 输出 Errors / Warnings / OK 三级结果

---

#### FR-D08: 流水线规模路由 ｜ 已实现(插件)

SEVO Router 在收到需求后先评估规模，自动选择执行档位，避免小任务被拉进完整流水线。

**三档路由：**

- 直接执行（Tier 1）：改配置、查状态、单文件修复等琐碎操作。Agent 直接执行，不创建流水线，不建项目文件夹。
- 轻量流水线（Tier 2）：小功能、脚本、局部改动。在现有目录中工作，走精简阶段（spec → implement → review → verify → ledger），必须包含审计（review）。不创建独立项目文件夹。
- 完整流水线（Tier 3）：新产品、新模块、跨域改动。创建独立 `projects/<slug>/` 文件夹，走完整 15 阶段流水线。

**AC:**
- AC1: Router 评估需求规模时输出档位判定（tier-1/tier-2/tier-3）及判定依据
- AC2: Tier 1 直接执行，不触发 `sevo:create`，不写入流水线状态
- AC3: Tier 2 创建轻量流水线，阶段集为 `['spec', 'implement', 'review', 'verify', 'ledger']`，必须包含 review（审计）
- AC4: Tier 3 行为与当前 `sevo:create` 一致（独立文件夹 + 完整 15 阶段）
- AC5: 用户可通过参数强制指定档位（如 `sevo:create my-tool --tier 2`），覆盖自动判定
- AC6: 档位判定结果记录到事件日志，可通过 `sevo:status` 查看

---

## 二、非功能需求（NFR）

### NFR-S01: Fail-Open 设计 ｜ 已实现(插件)

所有 hook 处理器包裹在 try-catch 中，错误记录日志但不阻断 dispatch。

### NFR-S02: 优雅降级 ｜ 已实现(插件)

SEVO dist/ 目录不存在时，插件自动降级为 no-op，不影响 Gateway 正常运行。

### NFR-S03: Label 协议 ｜ 已实现(插件)

流水线通过结构化 label（`sevo:<pipelineId>:<stageId>:<attempt>`）追踪任务归属。

### NFR-S04: Bridge 模块热加载 ｜ 已实现(插件)

PipelineEngine、LedgerEngine、Router 通过 bridge 模块懒加载，支持文件变更后自动刷新缓存（TTL 30s）。

### NFR-S05: 配置可覆盖 ｜ 已实现(插件)

所有路径（workspaceRoot、sevoRoot、distPath、dataPath、eventsPath）和阶段映射（stageAgentMap）支持通过插件配置、state/config.json 或环境变量覆盖。

### NFR-S06: 宿主无关 ｜ 已实现(插件)

核心流程通用化设计，可在任意宿主环境运行。宿主特有能力通过 Adapter 接入增强，核心流程不因缺少某个宿主而断裂。

**AC:**
- AC1: 所有硬编码路径/API/工具名提取为配置项
- AC2: resolveHostConfig() 从配置读取，提供默认值
- AC3: 默认支持 workspaceRoot、spec 文件路径模式、日志路径

---

## 三、Spec 与实际执行的 Gap 分析

以下表格记录各规则的插件化进度。已标注 ✅ 的条目已在 L2 层插件中实现：

| 规则 | 当前层级 | 状态 |
|------|----------|------|
| SEVO 流水线触发条件评估 | L2 | ✅ FR-S01 插件实现（trigger evaluation） |
| Post-Completion 自动推进链 | L2 | ✅ FR-V02 插件实现（PipelineEngine 驱动全链条自动推进） |
| 评审→修复→复验闭环 | L2 | ✅ FR-V03 插件实现（RFL 机制：提取 P0/P1→派修复→复验→闭环） |
| 长文档分段式写作 | L2 | ✅ FR-E05 插件实现（分段检测+拆分派发） |
| 编码任务 AC 逐条覆盖 | L2 | ✅ FR-S05 插件实现（extractACsFromSpec→注入 prompt→覆盖解析→补全派发→review 注入） |
| 并行任务文件名隔离 | L2 | ✅ FR-E06 插件实现（agentId 后缀注入 task prompt） |
| 任务失败重试策略 | L2 | ✅ FR-O06 插件实现（失败检测+梯队升级+拆段重派） |
| 进度透明（驾驶舱展示） | L2 | ✅ FR-O07 插件实现（进度文件写入+阶段状态追踪） |
| 研发流程改进双写 | L2 | ✅ FR-O08 插件实现（双写检测+事件日志） |
| 运行中任务补充（steer） | L2 | ✅ FR-O09 插件实现（supplement 注入机制） |
| UX 体验验收 | L2 | ✅ FR-V05 插件实现（task-mapper ux-acceptance 阶段） |
| 端到端 Smoke Test | L2 | ✅ FR-V06 插件实现（task-mapper smoke-test 阶段） |
| 端到端功能验证 | L2 | ✅ FR-V08 插件实现（task-mapper e2e-verification 阶段） |
| 阶段方法论注入 | L2 | ✅ FR-S06 插件实现（methodology.js + task-mapper spread 注入） |
| Agent 自动发现与自适应映射 | — | ✅ FR-O10 已实现(插件) |
| 最小运行模式 | — | ✅ FR-O11 已实现(插件) |
| 安装与初始化 | — | ✅ FR-O12 已实现(脚本) |
| 路径配置化 | — | ✅ FR-O13 已实现(插件) |
| 外部用户文档 | — | ✅ FR-O14 已实现(文档) |
| 阶段内 FR 级完成度追踪与自动补派 | L2 | ✅ FR-O15 已实现(插件) |

---

## 四、已实现能力清单（插件层）

基于 `/root/.openclaw/extensions/sevo-pipeline/` 的分析：

### index.js（493 行）— 核心插件
- Hook 1: `subagent_ended`（priority 200）— 检测 SEVO 任务完成，推进流水线
- Hook 2: `before_prompt_build`（priority 850）— 将待派发阶段任务注入主会话 prompt
- Hook 3: `before_tool_call`（priority 800）— 在 sessions_spawn 调用中注入 SEVO label
- 活跃流水线状态管理（active-pipelines.json）
- 事件日志（JSONL append）
- 全局单例 + fail-open 安全包装

### bridge.js（236 行）— 模块桥接
- 懒加载 PipelineEngine / LedgerEngine / Router
- 文件 mtime 感知的缓存刷新
- 单模块失败不影响其他模块
- 可配置路径解析

### task-mapper.js（217 行）— 阶段→任务映射
- 12 个阶段的默认 Agent 映射（spec → pm-01, spec-review-gate → sa-01, implement → T1, review → audit-01 等）
- 自动收集前序阶段产出工件路径
- 为每个阶段生成结构化 task prompt
- 映射可通过配置覆盖

### label-protocol.js（35 行）— 标签协议
- 编码/解码 `sevo:<pipelineId>:<stageId>:<attempt>` 格式
- 标签识别函数

---

## 五、关键架构约束

### AC-01: 阶段绑定设计（Stage-Bound Design）
系统能力绑定「做什么事」（流程阶段/任务类型），不绑定「谁来做」（特定 Agent）。换一个执行者，流程照样跑通。

### AC-02: 可控性分层冗余
同一条规则在多层部署：L6（AGENTS.md prompt）+ L2（插件 hook 拦截）+ L0（文件权限/systemd）。层号越小越可靠。

### AC-03: Fail-Open
所有 hook 处理器 try-catch 包裹，错误记录但不阻断。SEVO 挂了不影响 Gateway 正常 dispatch。

### AC-04: 优雅降级
dist/ 不存在时插件自动 no-op。配置错误时回退默认值。单模块加载失败不影响其他模块。

### AC-05: 核心通用 + 宿主 Adapter
核心流程不绑死单一宿主，但主动复用宿主高价值能力（hooks、guards、skill-inject）。宿主特有能力通过 Adapter 接入。

### AC-06: 编译型流水线状态
流水线状态持久化到文件系统（active-pipelines.json + PipelineEngine data/），不依赖内存。进程重启后状态可恢复。
