# Verification Before Completion

## Overview

**Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying

## Eval Delta — 执行前后对比 🆕

每个 Phase 3 任务完成后、标记 WBS `done` 之前，必须做执行前后差异对比：

### 步骤

```
1. BASELINE (任务执行前):
   npm test 2>&1 | tee /tmp/baseline-<task-id>.log
   # 记录: 总测试数、通过数、覆盖率

2. CURRENT (任务执行后):
   npm test 2>&1 | tee /tmp/current-<task-id>.log

3. DELTA (对比):
   - 新增测试数: grep -c "✓" current.log - grep -c "✓" baseline.log
   - 覆盖率变化: diff <coverage-before> <coverage-after>
   - 回归检查: 任何之前通过的测试现在失败？
```

### 输出格式

```
📊 Eval Delta — Task [ID]

Baseline:  47 tests | 100% pass | 72% coverage
Current:   54 tests | 100% pass | 78% coverage
──────────────────────────────────
Delta:     +7 tests | 0 regressions | +6% coverage

✅ 正向变化：无回归，覆盖率和测试数均有提升
```

### 异常情况

| 情况 | 处理 |
|------|------|
| 覆盖率为 0 | baseline 时项目还没有测试——标记为 ⚠️ 高风险（无基线），而非 N/A。在 evidence 中注明 |
| 回归 > 0 | **STOP**。标记 `blocked`，进入系统调试流程 |
| 测试数减少 | 确认是否是移除了冗余测试（合理）还是删除了有效测试（违规） |
| 覆盖率下降 | 标记为 `DONE_WITH_CONCERNS`，在 evidence 中注明 |

**铁律：没有 Eval Delta 对比，不能标记任务 `done`。**

## Standardized Verification Report 🆕

Phase 4 结束时，**必须使用标准化模板**输出验证报告，禁止叙述式文字。

模板：`templates/verification-report.md`

7 阶段顺序执行：Build → Types → Lint → Tests → Coverage → Security → Diff

判定：
- 全 PASS → ✅ READY
- Coverage < 80% 或其他小问题 → ⚠️ CONDITIONAL
- Build/Types/Tests 任一 FAIL → ❌ NOT READY

报告保存到 `docs/spm/reviews/YYYY-MM-DD-verification.md`，在 WBS 台账 evidence 列引用。
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom: passes | Code changed |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- Trusting agent success reports blindly
- ANY wording implying success without running verification

## Evidence for WBS

When marking a WBS task `done`, the evidence IS the verification output.

```
WBS Update:
Task 2 completed.
Evidence: `npm test` → 47/47 pass, exit 0
```
