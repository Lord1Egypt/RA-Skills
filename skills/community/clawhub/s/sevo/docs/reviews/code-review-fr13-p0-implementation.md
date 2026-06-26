# FR-13 PipelineEngine P0 代码审计报告

OpenClaw（pm-01 子Agent）｜2026-05-23

---

## 结论：有条件通过

P0 问题 2 个（必须修复后方可合并），P1 问题 5 个（建议修复）。核心模块逻辑正确，类型安全，质量标准加载机制设计良好。主要风险集中在 plugin-adapter 与 advance-on-complete 的集成缺失，以及 adapter/index.ts 的编译错误。

---

## AC 覆盖清单

| AC | 状态 | 代码位置 | 说明 |
|----|------|----------|------|
| AC-13.1 Stage Queue 按 DAG 生成，支持并行分支 | ✅ 覆盖 | `src/engine/stage-gate-guard.ts` L30 `arePrerequisitesMet()` | Guard 调用 `parallel-branch.ts` 的 DAG 校验，active 状态检查 + 前置依赖校验双重保障 |
| AC-13.2 推进判定 30s 内完成 | ✅ 覆盖 | `src/engine/advance-on-complete.ts` L42-49 `withTimeout` | Gate 评估 10s + advance <100ms + triggerStage 15s = 总计 ≤25s。结构性保障 30s SLA |
| AC-13.5 推进决策写入事件日志 | ✅ 覆盖 | `src/engine/advance-decision-log.ts` `appendAdvanceDecision()` | 写入 `events.jsonl`，eventType = `advance_decision`，含完整决策结构 |
| AC-13.6 Gateway 重启后自动恢复 | ✅ 部分覆盖 | `src/init/register-hooks.ts` + 磁盘持久化 | Pipeline 状态持久化到 `state.json`（已有机制），重启后 plugin 重新加载即恢复。`register-hooks.ts` 处理热加载/降级路径 |

---

## P0 问题列表（必须修复）

### P0-1: adapter/index.ts 重复导出导致编译错误

**文件**: `src/adapter/index.ts`

**问题**: 第 2-3 行存在完全重复的导出语句：
```typescript
export { buildStageStandardPrompt, buildTriggerStagePrompt } from './host-adapter.js';
export { buildStageStandardPrompt, buildTriggerStagePrompt } from './host-adapter.js'; // 重复
```

**影响**: TypeScript 编译器会报 duplicate identifier 错误，阻断构建。

**修复**: 删除重复行。

---

### P0-2: plugin-adapter handleSubagentEnded 未接入 advanceOnComplete，outcome 硬编码为 passed

**文件**: `src/plugin-adapter/plugin-adapter.ts` `handleSubagentEnded()` 方法

**问题**:
```typescript
this.bridge.handleStageComplete(tag.pipelineId, tag.stageId, {
  outcome: 'passed', // Default to passed; real implementation would parse output
  artifacts: [],
  failureReason: undefined,
});
```

架构明确要求 `handleSubagentEnded()` 接入 `advance-on-complete` 模块，使用 `resolveOutcome()` 判定阶段结果。当前实现：
1. outcome 永远为 'passed'，失败阶段无法被正确识别
2. 不调用 GateEngine 评估 gate 类型阶段
3. 不记录 advance decision 到 events.jsonl
4. artifacts 永远为空数组，丢失产物信息

**影响**: 
- 失败的阶段会被错误标记为通过，流水线会错误推进
- Gate 阶段（如 spec-review-gate）的结构化评估被跳过
- 推进决策日志在运行时路径中不会被写入（仅 stage-gate-guard 阻断时写入）

**修复**: `handleSubagentEnded` 应调用 `advanceOnComplete()` 或至少使用 `resolveOutcome()` 解析 output 中的 outcome，并传递 artifacts。

---

## P1 问题列表（建议修复）

### P1-1: advance-on-complete 缺少 30s SLA 超时警告日志

**文件**: `src/engine/advance-on-complete.ts`

**问题**: 架构明确要求超过 30s 时写 warning：
```typescript
if (Date.now() - startMs > 30_000)
  logger.warn(`advanceOnComplete exceeded 30s SLA: ${Date.now()-startMs}ms`);
```

实现中记录了 `durationMs` 到决策日志，但没有 console.warn/logger.warn 输出。运维无法从日志中快速发现 SLA 违规。

**建议**: 在 `advanceOnComplete` 返回前增加 30s 阈值检查和 warning 输出。

---

### P1-2: openclaw-adapter.ts 硬编码默认 publishScript 路径

**文件**: `src/adapter/openclaw-adapter.ts`

**问题**:
```typescript
this.publishScript = options.publishScript ?? '/root/.openclaw/workspace/scripts/publish-release.sh';
```

硬编码了 `/root/.openclaw/workspace/` 路径，违反"无硬编码路径"原则。其他用户环境下此路径不存在。

**建议**: 默认值改为基于 `projectRoot` 的相对路径，如 `path.join(options.projectRoot, 'scripts/publish-release.sh')` 或从 package.json scripts 字段推断。

---

### P1-3: 文件路径与架构设计不一致

**问题**: 架构指定的路径 vs 实际路径：

| 架构路径 | 实际路径 |
|----------|----------|
| `src/pipeline/stage-gate-guard.ts` | `src/engine/stage-gate-guard.ts` |
| `src/pipeline/advance-on-complete.ts` | `src/engine/advance-on-complete.ts` |
| `src/pipeline/advance-decision-log.ts` | `src/engine/advance-decision-log.ts` |
| `src/knowledge/default-stage-standards.json` | `src/engine/default-stage-standards.json` |
| `src/knowledge/stage-standards-loader.ts` | `src/engine/stage-standards-loader.ts` |

功能正确，但组织结构偏离架构。`src/engine/` 作为统一目录有其合理性（内聚），但应同步更新架构文档以保持一致。

---

### P1-4: engine 模块未从 src/index.ts 公共 API 导出

**文件**: `src/index.ts`

**问题**: `src/engine/index.ts` 定义了完整的 barrel 导出（`advanceOnComplete`、`evaluateStageGate`、`loadStageStandards` 等），但 `src/index.ts` 未 re-export 这些模块。外部消费者和测试无法通过包入口访问 engine API。

**建议**: 在 `src/index.ts` 增加：
```typescript
export { advanceOnComplete, evaluateStageGate, evaluateStageGateByLoader, ... } from './engine/index.js';
```

---

### P1-5: spec-review-gate 的 SpecReviewGate 类与 checkRequiredSpecSections 功能重叠

**文件**: `src/gates/spec-review-gate.ts`

**问题**: 文件中存在两套检查机制：
1. `checkRequiredSpecSections()` — 基于 heading 提取 + 字符串匹配检查四章节（符合架构要求）
2. `SpecReviewGate` 类 — 基于 `SpecOutput` 结构化数据做 FR/AC 格式校验

两者职责不同但命名容易混淆。`SpecReviewGate.evaluate()` 不调用 `checkRequiredSpecSections()`，意味着通过 `SpecReviewGate` 评估的 spec 可能缺少四章节但仍然通过。

**建议**: 在 `SpecReviewGate.evaluate()` 中集成 `checkRequiredSpecSections` 检查（如果 spec.artifact 路径可用），或在文档中明确两者的使用场景边界。

---

## 代码质量总评

| 维度 | 评价 |
|------|------|
| TypeScript 类型安全 | ✅ 良好。接口定义完整，泛型使用合理，无 any 类型 |
| 错误处理 | ✅ 良好。`withTimeout` 处理 reject，`safeLoadState` 有 try-catch，标准加载器有降级 |
| 无硬编码 agent ID | ✅ 通过。所有 agent 选择通过 `ProjectConfig.stageAgents` 或 `defaultAgentId` 配置 |
| 无硬编码路径 | ⚠️ P1-2 中 openclaw-adapter 有一处硬编码 |
| 导出完整性 | ⚠️ P0-1 重复导出 + P1-4 公共 API 缺失 |
| 架构一致性 | ⚠️ P0-2 核心集成缺失 + P1-3 路径偏离 |

---

## 亮点

1. `withTimeout` 实现简洁优雅，正确处理 resolve 和 reject 两种情况
2. `stage-standards-loader.ts` 的默认 + 用户覆盖合并机制设计良好，支持零代码扩展
3. `evaluateStageGate` 纯函数设计，易于测试，无副作用
4. `spec-review-gate.ts` 的 heading 提取方案比架构建议的正则方案更健壮（先提取 heading 再匹配，避免正文误匹配）
5. `advance-decision-log.ts` 使用 append-only JSONL 格式，符合事件溯源最佳实践
