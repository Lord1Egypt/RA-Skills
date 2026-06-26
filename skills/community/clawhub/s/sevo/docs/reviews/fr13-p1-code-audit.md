# FR-13 P1 代码实现质量审计

OpenClaw（audit-01 子Agent）| 2026-05-23

---

## 审计范围

| 文件 | 状态 | 行数 |
|------|------|------|
| `src/pipeline/fix-loop.ts` | 新建 | ~170 |
| `src/pipeline/stage-rollback.ts` | 新建 | ~120 |
| `src/scan/scan-mapping.ts` | 新建 | ~130 |
| `src/scan/llm-semantic-verifier.ts` | 新建 | ~70 |
| `src/pipeline/stage-machine.ts` | 修改 | ~60 |
| `src/pipeline/pipeline-engine.ts` | 修改 | +~250 |
| `src/types/index.ts` | 修改 | +~15 |
| `scripts/init.sh` | 修改 | +~40 |

---

## 结论：CONDITIONAL PASS

代码整体质量高，类型安全、状态机设计、接口交互均无阻断性缺陷。发现 0 个 P0、2 个 P1、4 个 P2、4 个 P3。P1 问题不影响核心流程正确性但应在下一迭代修复。

---

## P0（阻断，必须修复才能合并）

无。

---

## P1（应修复，不阻断但影响可维护性/可观测性）

### P1-1: `StageRollback.markBlocked()` 接受 `reason` 参数但未持久化

**文件:** `src/pipeline/stage-rollback.ts` L109-112

```typescript
markBlocked(state: PipelineState, reason: string): void {
  state.pipelineStatus = 'blocked';
  state.updatedAt = new Date().toISOString();
  // reason 参数被丢弃，未写入 state
}
```

**影响:** 当运维人员从 `state.json` 查看 `pipelineStatus: 'blocked'` 时，无法得知阻塞原因，必须去 `events.jsonl` 交叉查询。建议在 `PipelineState` 增加 `blockReason?: string` 字段并在此处赋值。

---

### P1-2: `StageRollback.execute()` 未清理目标阶段的残留元数据

**文件:** `src/pipeline/stage-rollback.ts` L85-93

```typescript
// Transition target stage → active (rollback-guarded)
assertTransition(targetRecord.status, 'active', { reason: 'rollback' });
targetRecord.status = 'active';
targetRecord.startedAt = new Date().toISOString();
targetRecord.completedAt = undefined;
// 缺失：未清理 failureReason / fixAttempts / blockReason
```

**影响:** 如果目标阶段之前经历过 fix_pending 或 failed 状态，其 `failureReason`、`fixAttempts`、`blockReason` 等字段会残留。重新激活后这些字段语义失效，可能误导监控/日志分析。建议在 re-activation 时清理：

```typescript
targetRecord.failureReason = undefined;
targetRecord.fixAttempts = undefined;
targetRecord.blockReason = undefined;
```

---

## P2（建议修复，边界场景或代码卫生）

### P2-1: `pipeline-engine.rollback()` 事件 payload 未反映实际执行结果

**文件:** `src/pipeline/pipeline-engine.ts` L319-327

```typescript
const decision = rollback.execute({ state, failedStage, target, reason });
// 事件始终写 outcome: 'executed'，未检查 decision.executed
this.emitEvent(pipelineId, failedStage, 'stage_rolled_back', {
  outcome: 'executed',  // 应为 decision.executed ? 'executed' : 'failed'
  ...
});
```

**影响:** 理论上此路径不可达（前置校验已排除 execute 失败的条件），但作为防御性编程，事件 payload 应反映真实结果。当前代码在 `execute()` 返回 `{ executed: false }` 时仍记录 `outcome: 'executed'`。

---

### P2-2: `handleFixComplete` 'advance' 路径的递归 `advance()` 异常恢复

**文件:** `src/pipeline/pipeline-engine.ts` L434-452

当 fix 通过后，代码先将状态持久化为 'active'，再调用 `this.advance()`。如果 `advance()` 内部抛出异常（如 clarification coordinator 故障），阶段会停留在 'active' 状态，无外部机制重新驱动。

**影响:** 极端场景下阶段可能卡在 'active' 无人推进。建议在 `advance()` 调用处加 try-catch，失败时回滚到 fix_pending 或记录恢复事件。

---

### P2-3: 并行分支场景下 rollback 目标可能处于 'active' 状态

**文件:** `src/pipeline/stage-rollback.ts` L72-93

`resolveTarget()` 不检查目标阶段当前状态。如果目标阶段正在并行执行（status='active'），`assertTransition('active', 'active')` 会抛出异常（active → active 不在有效转换表中）。

**影响:** 仅在并行分支场景下可能触发。当前 SEVO 的并行分支（test-case-authoring ∥ contract）不太可能成为 rollback 目标，但未来扩展时可能暴露。建议 `resolveTarget()` 增加状态校验或 `execute()` 对 active 目标做特殊处理。

---

### P2-4: `scan-mapping.ts` 中 `ScanMappingGenerator.generate()` 无错误处理

**文件:** `src/scan/scan-mapping.ts` L82-97

```typescript
const response = await opts.adapter.callLlm([...]);
const parsed = safeJsonParse<Partial<ScanMappingConfig>>(response, {});
```

如果 `callLlm` 返回空字符串或非 JSON 内容，`safeJsonParse` 返回 `{}`，`normalizeFrFileMap(undefined)` 返回 `{}`。最终生成一个空的 `frFileMap`，无任何映射。

**影响:** 静默失败——LLM 调用失败时不抛错也不警告，产出空映射文件。调用方无法区分"确实没有映射"和"LLM 调用失败"。建议至少 log 一条 warning 或在 config 中标记 `generatedBy: 'sevo scan --generate-map (empty: llm-failure)'`。

---

## P3（低优先级，代码卫生/文档）

### P3-1: `GateEvaluator` 接口定义但未使用

**文件:** `src/pipeline/fix-loop.ts` L60-62

`GateEvaluator` 接口已定义但在整个 codebase 中未被引用。可能是预留接口或重构残留。建议标注 `@future` 或移除。

---

### P3-2: `FixLoopManager.onFixComplete()` 的副作用未文档化

**文件:** `src/pipeline/fix-loop.ts` L95-117

该方法直接修改传入的 `state` 参数（mutates `currentAttempt.outcome`，pushes to `state.attempts`）。在 `pipeline-engine.ts` 中调用时传入的是合成的临时对象，副作用无害。但方法签名未标注 `@mutates state`，未来维护者可能误用。

---

### P3-3: 合成 `FixLoopState` 中的时间戳不准确

**文件:** `src/pipeline/pipeline-engine.ts` L419-428

`handleFixComplete` 构造合成 `loopState` 时，所有历史 attempt 的 `triggeredAt` 都使用当前时间。这不影响逻辑正确性（`onFixComplete` 不依赖时间戳做决策），但如果未来 `buildFixPrompt()` 被用于展示历史，时间信息会失真。

---

### P3-4: `StageRollback` 每次实例化使用默认配置

**文件:** `src/pipeline/pipeline-engine.ts` L277

```typescript
const rollback = new StageRollback(); // 始终 maxRollbacks=2
```

`maxRollbacks` 无法按项目/流水线配置。当前硬编码为 2，如果未来需要不同项目有不同容忍度，需要重构。作为 P1 实现的首版，可接受。

---

## 审计维度总结

| 维度 | 评级 | 说明 |
|------|------|------|
| 类型安全 | ✅ 优秀 | 零 `any`，类型断言仅在验证后使用，null/undefined 防御完备 |
| 状态机完整性 | ✅ 优秀 | fix_pending/rolled_back 转换无死锁路径，终态正确，guard 机制有效 |
| 接口一致性 | ✅ 良好 | fix-loop 与 rollback 交互正确，数据流清晰，单一写入者模式保持 |
| 边界保护 | ✅ 良好 | maxRetries/maxRollbacks 超限处理正确，null 防御到位，P2-3 为极端边界 |
| 事件记录 | ✅ 良好 | 所有状态变化均写入 events.jsonl，事件类型已注册，P2-1 为防御性缺陷 |
| 代码风格 | ✅ 优秀 | 与现有代码风格完全一致，JSDoc 完整，命名规范，模块职责清晰 |

---

## 附：init.sh 三层降级审计

| 层级 | 条件 | 行为 | 评价 |
|------|------|------|------|
| Tier 1 | 无 OPENCLAW_HOME 且无 CLI | silent exit 0 | ✅ 正确，不干扰非 OpenClaw 环境 |
| Tier 2 | 有 config 无 CLI | warning + exit 0 | ✅ 正确，提示但不阻断 |
| Tier 3 | 完整环境 | 完整注册 | ✅ 正确，含 hook 验证、doctor 检查 |

三层降级逻辑清晰，边界条件处理正确（`~` 路径展开、config 文件不存在等）。`set -u` 确保未定义变量立即报错。主版本升级确认交互合理。
