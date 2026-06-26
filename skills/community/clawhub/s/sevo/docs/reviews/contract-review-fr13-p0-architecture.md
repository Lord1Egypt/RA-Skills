# Contract Review：FR-13 PipelineEngine P0 架构详设

OpenClaw（pm-01 子Agent）｜2026-05-23

---

## 结论：有条件通过

架构整体设计清晰，模块职责单一，实现优先级合理，核心守卫机制（拦截 + 推进 + 审计）的三点闭环逻辑正确。但存在 5 个 P0 问题必须在编码前修复，否则会导致 AC 不满足或陌生用户无法零配置使用。

---

## P0 问题列表（必须修复才能编码）

### P0-1：STAGE_QUALITY_STANDARDS 覆盖不完整

**现状**：`stage-quality-standards.ts` 只定义了 `spec`、`ux-interaction-design`、`contract` 三个阶段的标准。

**问题**：Spec §6.6 明确定义了 Implement、Review/Regression 阶段的执行原则，且 FR-13 spec 说"PipelineEngine 在派发阶段任务时，自动注入该阶段应遵循的专业标准（§6.6）"。缺少这些阶段的标准意味着 `triggerStage()` 对这些阶段不注入任何质量指导，单 Agent 用户在 Implement/Review 阶段得不到专业原则。

**修复要求**：补全 §6.6 中所有已定义阶段的标准：
- `implement`：最小改动、最简实现、目标驱动、主动澄清
- `review`/`regression`：独立性、可验证结论、不放过设计方向问题
- `contract-review-gate`：四方审查维度（产品/开发/质量/体验）

### P0-2：质量标准用 TypeScript 常量硬编码，违反 AC-6.6.3

**现状**：`STAGE_QUALITY_STANDARDS` 是 TypeScript `export const`，修改需要改代码 + 重新构建 + 重新发布。

**问题**：AC-6.6.3 明确要求"原则集可编辑、可扩展，新增阶段或新增原则时不需要改代码"。TypeScript 常量不满足此要求。

**修复要求**：改为运行时可加载的配置文件（JSON/YAML），随 npm 包发布默认版本，用户可通过 `sevo.json` 或项目目录下的配置文件覆盖/扩展。代码中保留 TypeScript 类型定义作为 schema 校验，但实际数据从配置文件读取。

### P0-3：Gateway 重启需求破坏"零配置"承诺

**现状**：§4.2 描述的流程是 `sevo init → 写入 openclaw.json plugins → Gateway 重启 → 加载插件 → hook 生效`。

**问题**：陌生用户执行 `npm install && sevo init` 后，如果需要手动重启 Gateway，就不是"零配置获得阶段推进守卫"。用户可能不知道需要重启，也可能不知道怎么重启。

**修复要求**：架构文档必须明确以下之一：
- 方案 A：`sevo init` 自动触发 Gateway 重启（需说明实现方式和风险）
- 方案 B：`sevo init` 检测 Gateway 运行状态，若在运行则调用 Gateway API 热加载插件（无需重启）
- 方案 C：明确标注"首次 init 后需重启 Gateway"为已知限制，并在 CLI 输出中给出明确提示（降级方案，但必须在文档中说明）

### P0-4：Gate 阶段完成判定逻辑缺失

**现状**：`parseCompletionOutcome()` 通过检查输出中是否包含 `[SEVO:FAILED]` 或 `任务失败` 字符串来判定阶段结果。代码注释说"Gate 阶段由 GateEngine 独立评估"，但没有展示 GateEngine 结果如何流入 `advanceOnComplete`。

**问题**：
1. Gate 阶段（spec-review-gate、contract-review-gate）的完成判定应来自 GateEngine 的结构化结论，不是文本匹配。
2. 普通阶段的文本匹配也不可靠——Agent 可能成功完成但输出中恰好包含"任务失败"这几个字（比如在描述别人的失败），或者失败了但没有输出标记。

**修复要求**：
- Gate 阶段：`advanceOnComplete` 必须从 GateEngine 获取结构化 verdict（passed/rejected），不走 `parseCompletionOutcome`。架构需展示 GateEngine → advanceOnComplete 的数据流。
- 普通阶段：至少说明判定策略的优先级（SevoTag 元数据 > 结构化输出 > 文本匹配 fallback），并标注文本匹配是降级方案。

### P0-5：AC-13.2 的 30 秒 SLA 无保障机制

**现状**：架构描述了 `subagent_ended` → `advanceOnComplete` 的同步调用链，但没有任何关于时间约束的设计。

**问题**：AC-13.2 要求"每个阶段完成后，30 秒内评估门禁并决定推进或阻断"。如果 GateEngine 评估耗时超过 30 秒（比如需要 LLM 调用），或者 `triggerStage` 因为 Adapter 超时而阻塞，整个 SLA 就无法满足。

**修复要求**：
- 明确 `advanceOnComplete` 的时间预算分配（gate 评估上限、trigger 上限）
- 说明 GateEngine 在 P0 中是否涉及 LLM 调用（如果 spec-review-gate 的四章节检查是纯规则，则 30s 可保证；如果需要 LLM，则需要异步机制）
- 若无法在 30s 内完成，需要说明降级策略（先标记 evaluating 状态，异步完成后再推进）

---

## P1 问题列表（建议修复）

### P1-1：advanceOnComplete 缺少错误处理

`advanceOnComplete` 函数没有 try-catch 或错误恢复逻辑。如果 `adapter.triggerStage()` 抛异常（网络超时、Agent 不可用），整个推进链中断，pipeline 卡死在"已 advance 但未 trigger"的中间状态。建议：triggerStage 失败时记录错误事件，标记阶段为 `trigger_failed`，支持重试。

### P1-2：spec-review-gate 四章节检查用正则匹配

`checkRequiredSections` 用正则模式匹配检测章节存在性。这能检测"有没有提到这个词"，但不能检测"是否有独立章节"。一个 spec 在正文中随口提到"用户人群"四个字就能通过检查。建议改为 heading 级别检测（检查 `##` 或 `###` 标题行是否包含对应关键词），至少保证是独立章节而非正文提及。

### P1-3：事件序列化格式不一致

§5.2 中 `AdvanceDecision` 接口定义 `fromStage`/`toStage` 为顶层字段，但 JSON 示例中它们嵌套在 `payload` 内，顶层另有 `stage` 字段。编码时会产生歧义。建议统一：要么全部顶层（简单），要么统一用 `{ timestamp, pipelineId, stage, eventType, payload: {...} }` 的信封格式（与已有 events.jsonl 格式对齐）。

### P1-4：CLI-only 模式下守卫完全失效

§4.3 说无宿主时"Guard 不生效"。这意味着 SEVO 的核心价值（阶段不可跳过）在 CLI-only 模式下不存在。建议：即使无宿主，`sevo advance` CLI 命令本身也应执行 Guard 逻辑（检查前置阶段是否 passed），只是不自动触发而已。

### P1-5：并行阶段 triggerStage 的顺序依赖

`advanceOnComplete` 中用 `for...of` 串行调用 `await adapter.triggerStage()`。如果第一个 triggerStage 耗时较长，第二个并行阶段的触发会被延迟。建议改为 `Promise.allSettled()` 并行触发，失败的单独记录。

### P1-6：AC-6.6.4 降级策略未体现

Spec 要求"原则注入失败时，任务仍可执行（降级而非阻断）"。架构中 `triggerStage()` 的描述没有提到如果质量标准配置文件读取失败或格式错误时的降级行为。建议：标准加载失败时 log warning 并继续派发（不注入标准），不阻断流程。

---

## 对编码 Agent 的建议

1. **先实现 §6 序号 1-2**（decision-log + stage-gate-guard），这两个模块无外部依赖，可以写完整单元测试独立验证。Guard 的测试用例至少覆盖：active 放行、pending 阻断、failed 阻断、无 SevoTag 放行、pipeline 不存在放行。

2. **Gate 阶段判定必须走 GateEngine**：不要用 `parseCompletionOutcome` 处理 gate 阶段。在 `advanceOnComplete` 入口处判断 stageId 是否为 gate 类型，是则调用 GateEngine 获取结构化结论。

3. **质量标准改为 JSON 配置文件**：建议路径 `src/knowledge/default-stage-standards.json`，TypeScript 代码负责加载 + schema 校验 + 合并用户自定义配置。这样满足 AC-6.6.3 的"不改代码"要求。

4. **事件格式对齐已有 events.jsonl**：先 `cat` 一下现有 events.jsonl 的格式，新增的 `advance_decision` 事件必须与已有事件结构一致（信封格式 vs 扁平格式），不要引入第二种序列化风格。

5. **端到端测试是验收关键**：§6 的端到端场景（创建 pipeline → 尝试跳阶段被拦 → 正常推进后放行）必须作为集成测试实现，不能只靠单元测试覆盖。建议用 `vitest` 或项目已有测试框架写一个完整的 pipeline 生命周期测试。

6. **30s SLA 的实现建议**：P0 中 spec-review-gate 如果只做四章节结构检查（纯规则，不调 LLM），则 30s 天然满足。在代码中加一个 `performance.now()` 计时 + warning log（超过 5s 就 warn），为后续 P1 的 LLM gate 评估预留监控基础。
