# Verification Report Template

> Phase 4 质量阶段结束时，Agent 必须按此格式输出验证报告。禁止用叙述式文字替代。

---

## Report

```
══════════════════════════════════
  VERIFICATION REPORT
  Task [ID]: [task name]
  Branch: [branch]
══════════════════════════════════

Build:     [PASS / FAIL]                  [exit code / error]
Types:     [PASS / FAIL] (X errors)       [npx tsc --noEmit 2>&1 | tail -3]
Lint:      [PASS / FAIL] (X warnings)     [npm run lint 2>&1 | tail -3]
Tests:     [PASS / FAIL] (X/Y passed)     [npm test 2>&1 | tail -10]
Coverage:  [PASS / FAIL] (Z%)             [threshold: 80%]
Security:  [PASS / FAIL] (X issues)       [grep secrets / console.log]
Diff:      [X files changed]              [git diff --stat | tail -1]

──────────────────────────────────
Eval Delta:
  Tests:    +N  | Coverage: +Y%  | Regressions: Z
──────────────────────────────────

Overall:   [✅ READY  /  ⚠️ CONDITIONAL  /  ❌ NOT READY]

Issues to Fix (if NOT READY):
1. [file:line] — [issue description]
2. ...

Resolved Notes (if CONDITIONAL):
1. [file:line] — [minor issue, accepted for now]
```

---

## 各阶段检查详解

### Build
```bash
npm run build 2>&1 | tail -5
```
- PASS: exit 0
- FAIL: exit ≠ 0 → STOP，不继续后续检查

### Types
```bash
npx tsc --noEmit 2>&1 | tail -10
```
- PASS: 0 errors
- FAIL: > 0 errors → 列出前 5 个

### Lint
```bash
npm run lint 2>&1 | tail -10
```
- PASS: 0 errors, 0 warnings（或 warnings < 5 可接受）
- FAIL: errors > 0

### Tests
```bash
npm test 2>&1 | tail -15
```
- PASS: 0 failures
- FAIL: > 0 failures → STOP

### Coverage
```bash
npm run test:coverage 2>&1 | grep -A5 "Coverage"
```
- PASS: ≥ 80% lines
- FAIL: < 80% → 标记为 CONDITIONAL

### Security
```bash
# 无硬编码密钥
grep -rE "API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE" --include="*.ts" --include="*.js" src/ 2>/dev/null | grep -v "node_modules" | grep -v "process.env" || echo "CLEAN"

# 无 console.log
grep -rE "console\.(log|debug)" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | grep -v "logger" || echo "CLEAN"
```
- PASS: 两项都 CLEAN
- FAIL: 任一有输出 → 列出发现

### Diff
```bash
git diff --stat origin/main...HEAD 2>/dev/null || git diff --stat
```
- 列出变更文件数和行数
- 人工检查：有无意外变更、缺失文件、多余文件

---

## 判定规则

| Overall | 条件 |
|---------|------|
| ✅ READY | Build/Types/Lint/Tests/Security 全 PASS |
| ⚠️ CONDITIONAL | Coverage < 80% 或其他小问题，但核心功能不受影响 |
| ❌ NOT READY | Build/Types/Tests 任一 FAIL，或有 Critical 安全问题 |

---

## 使用方式

Phase 4 结束时：

```
1. 按顺序执行 Build → Types → Lint → Tests → Coverage → Security → Diff
2. 填入模板，附实际命令输出
3. 将报告保存到 docs/spm/reviews/YYYY-MM-DD-verification.md
4. 在 WBS 台账 evidence 列引用报告路径
```
