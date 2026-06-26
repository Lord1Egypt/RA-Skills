# Contract Review：SEVO UX/Architecture Design 阶段架构详设

OpenClaw（pm-01 子Agent）｜2026-05-23

---

## 结论：有条件通过

架构详设整体方向正确，模块划分清晰，与现有代码集成路径可行。P0 范围内的核心编排逻辑（路由判定、阶段执行骨架、并行分支依赖）已在代码中实现，架构文档与代码实际状态基本一致。

但存在 2 个 P0 问题（文档与代码不一致导致开发者误导）和 3 个 P1 问题（AC 覆盖缺口），需修复后方可作为编码指导文档使用。

---

## 问题清单

### P0（阻断，必须修复才能进入编码）

| # | 问题 | 说明 |
|---|------|------|
| P0-1 | 文件路径与实际代码不一致 | 架构文档 §2.1 提出新增 `src/stages/ux-interaction-design-stage.ts` 和 `src/stages/architecture-design-stage.ts`，但代码中实际文件名为 `ux-design-stage.ts` 和 `arch-design-stage.ts`（types 文件同理）。开发者按文档创建文件会导致重复实现或导入冲突。必须将文档中的文件路径修正为实际路径。 |
| P0-2 | classifyDesignNeeds 函数签名不一致 | 架构文档 §3.1 将 `classifyDesignNeeds` 定义为同步函数 `function classifyDesignNeeds(input): DesignNeedResult`，但实际代码是 `async function classifyDesignNeeds(input): Promise<DesignNeedResult>`（内部调用 LLM）。接口定义中 `specOutput` 和 `projectConfig` 在代码中是可选的（`specOutput?: SpecOutput`、`projectConfig?: Partial<ProjectConfig>`），文档中标为必填。此外代码中有 `llm` 字段，文档未体现。签名不一致会导致集成代码编译失败。 |

### P1（重要，不阻断编码但必须在 Review 前修复）

| # | 问题 | 说明 |
|---|------|------|
| P1-1 | AC-4.8n/AC-4.8s 传递机制未定义 | Spec 要求 UX 设计文档和架构详设文档是 Implement 阶段的"强制输入"，编码 prompt 必须引用文档路径。架构文档通过 contract-review-gate 依赖链间接保证时序，但未定义 Implement 阶段如何获取这两个 ArtifactRef（是通过 pipeline state 传递？还是 ImplementInput 新增字段？）。缺少此机制，编码阶段无法满足 AC-4.8n/AC-4.8s。 |
| P1-2 | AC-4.8p2 PM 评审循环状态机未详设 | 架构文档定义了 `pmReviewStatus: 'pending' | 'approved' | 'rejected'`，但未描述：谁触发评审？rejected 后如何回到 UX 角色修改？修改后如何重新提交？是否复用 ReviewFixLoop？这是一个独立的子状态机，需要明确转换规则和触发条件。 |
| P1-3 | Spec Review Gate 四维度评审与现有代码的衔接方案不足 | 架构文档 §3.5 定义了 `SpecReviewBundleMultiDim` 类型，但现有 `spec-review-gate.ts` 是单维度评审（只检查结构完整性）。文档说"委托给 SpecReviewGateMultiDim"，但未说明：是替换现有 evaluate() 还是包装？现有 findings 如何映射到 dimension？`requiredDimensions` 由谁决定（projectConfig.hasUI？还是路由结果？）。 |

### P2（建议改进）

| # | 问题 | 说明 |
|---|------|------|
| P2-1 | P0/P1 边界划分与代码现状不匹配 | 架构文档 §6 将 types、constants、router、stages 列为 P0，但这些在代码中已全部实现。实际的 P0 新增工作量为零（除非需要修改）。真正需要新写的是 P1 列表中的 spec-review-dimensions.ts、implementation-review-gate SA 维度、PM 评审流程。建议重新标注优先级，避免开发者误判工作量。 |
| P2-2 | AC-4.8m 结构性保障缺失 | "从小白用户视角出发"依赖 adapter/LLM prompt 质量，架构层面无结构性约束。建议在 UxDesignGenerationRequest 中增加 `targetPersona` 字段或在 stage 执行前注入 persona 约束，使 AC-4.8m 可验证。 |
| P2-3 | AC-4.8u（authorRole=sa 可追溯）未在架构文档中显式提及 | 代码中 `ArchitectureDesignOutput.authorRole: 'sa'` 已实现，但架构文档 §1 概述中列举的 AC 范围未包含 AC-4.8u。建议补充以保持文档完整性。 |

### P3（低优先级建议）

| # | 问题 | 说明 |
|---|------|------|
| P3-1 | stage-graph.ts 边已存在但被列为 P1 | 架构文档 §6 P1 列表第 4 项"router/stage-graph.ts — DAG 边"，但代码中 `DEFAULT_SDD_EDGES` 已包含 `spec-review-gate → ux-interaction-design` 和 `spec-review-gate → architecture-design`。可从 P1 列表移除。 |

---

## AC 覆盖矩阵

| AC 编号 | 覆盖状态 | 架构文档对应位置 | 备注 |
|---------|----------|-----------------|------|
| AC-4.8l | ✅ 完全覆盖 | §3.1 classifyDesignNeeds + §4.3 router调用链 | 路由判定 UX 需求，LLM 语义判断 + 保守 fallback |
| AC-4.8m | ⚠️ 部分覆盖 | §3.3 UxInteractionDesignOutput | 类型定义覆盖产出结构，但"小白用户视角"无结构性保障（P2-2） |
| AC-4.8n | ⚠️ 部分覆盖 | §4.1 依赖链（间接保证时序） | 时序保证有，但传递机制未定义（P1-1） |
| AC-4.8o | ✅ 完全覆盖 | §4.1 并行分支 + §4.2 parallel-branch规则 | 不阻塞其他阶段，CRG 等待完成 |
| AC-4.8p | ✅ 完全覆盖 | §3.3 authorRole: 'ux' | 类型约束 + 工件 metadata 记录 |
| AC-4.8p2 | ⚠️ 部分覆盖 | §3.3 pmReviewStatus 字段 | 字段存在但状态机转换规则未定义（P1-2） |
| AC-4.8q | ✅ 完全覆盖 | §3.1 classifyDesignNeeds + §4.3 router调用链 | 路由判定 Architecture 需求 |
| AC-4.8r | ✅ 完全覆盖 | §3.4 ArchitectureDesignOutput.apiDefinitions | 含 path/method/request/response/errorCodes |
| AC-4.8s | ⚠️ 部分覆盖 | §4.1 依赖链（间接保证时序） | 同 AC-4.8n，传递机制未定义（P1-1） |
| AC-4.8t | ✅ 完全覆盖 | §3.4 ArchitectureDesignInput.uxDesignDocument | 可选引用 UX 设计文档 |
| AC-4.24n4 | ✅ 完全覆盖 | §4.5 implementation-review-gate SA维度 | 逐项核对 API 一致性逻辑已定义 |
| AC-4.24n5 | ✅ 完全覆盖 | §4.5 + §7 关键决策表 | 无文档时自动跳过 |

---

## 开发维度评估

### 模块划分
清晰度：高。新增模块职责单一：
- `design-need-classifier` 只做路由判定
- `ux-design-stage` / `arch-design-stage` 只做阶段执行
- `spec-review-dimensions` 只做多维度评审
- 各模块通过类型接口解耦，adapter 模式支持替换实现

### 与现有代码集成
可行性：高。经逐一验证：
- `types/index.ts` 中 StageId、RoutingResult 已扩展 ✓
- `constants.ts` 中 STAGE_IDS、ALL_STAGES、L0_SKIP_REASONS 已包含 ✓
- `router/router.ts` 已集成 classifyDesignNeeds ✓
- `pipeline/parallel-branch.ts` 已有正确的前置依赖逻辑 ✓
- `router/stage-graph.ts` 已有 DAG 边 ✓
- `stages/index.ts` 已导出两个阶段 ✓

唯一风险：文档中的文件路径名与实际不一致（P0-1），可能导致开发者创建重复文件。

### 状态机分析
无死锁风险。关键路径：
- `ux-interaction-design` 和 `architecture-design` 被 skip 时标记为 skipped，不阻塞 CRG
- CRG 的 `getPrerequisites` 用 `inPipeline()` 检查，skip 的阶段不在 requiredStages 中，不会被等待
- implement 只依赖 CRG，不直接依赖设计阶段，无循环依赖

遗漏路径：PM 评审 rejected 后的回退路径未在状态机中体现（P1-2）。

### P0 范围评估
P0 列表中的 8 项在代码中已全部实现。如果目标是"流水线能跑通"，当前代码已满足——路由能判定、阶段能执行（用默认 adapter 产出骨架文档）、并行分支能正确编排。

真正需要编码的是 P1 列表中的新增工作：
1. `spec-review-dimensions.ts` — 四维度评审（AC-4.5a/AC-4.5b）
2. `implementation-review-gate.ts` SA 维度核对逻辑（AC-4.24n4）
3. PM 评审循环子状态机（AC-4.8p2）
4. Implement 阶段接收设计文档的传递机制（AC-4.8n/AC-4.8s）

---

## 修复要求

1. **P0-1**：将架构文档 §2.1 中的文件路径修正为实际路径（`ux-design-stage.ts`、`arch-design-stage.ts`、`ux-design-types.ts`、`arch-design-types.ts`）
2. **P0-2**：将 §3.1 中 `classifyDesignNeeds` 签名修正为 async，`specOutput` 和 `projectConfig` 标为可选，补充 `llm` 字段
3. **P1-1**：新增一节描述设计文档如何传递到 Implement 阶段（建议方案：pipeline state 中维护 `designArtifacts: Record<StageId, ArtifactRef>`，ImplementInput 新增 `uxDesignDocument?: ArtifactRef` 和 `archDesignDocument?: ArtifactRef`）
4. **P1-2**：新增一节描述 PM 评审循环状态机（触发条件、角色、状态转换、与 ReviewFixLoop 的关系）
5. **P1-3**：补充 spec-review-gate 四维度改造的具体衔接方案（替换 vs 包装、dimension 映射规则、requiredDimensions 决定逻辑）
