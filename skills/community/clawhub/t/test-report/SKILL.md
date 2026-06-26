---
name: test-report
description: >
  Generate test summary reports, quality metrics, and test execution analysis.
  Aggregate test results into structured reports with pass/fail rates, coverage,
  trends, and recommendations.
  Use when: (1) summarizing test results, (2) generating quality reports,
  (3) analyzing test trends, (4) calculating test metrics (pass rate, defect density),
  (5) preparing test sign-off reports,
  (6) "测试报告", "质量报告", "测试总结", "通过率", "缺陷分析".
  NOT for: running tests (use api-tester or web-tester), writing test cases
  (use test-case-gen), or bug analysis (use bug-hunter).
metadata:
  openclaw:
    emoji: "📊"
---

# Test Report Generator

Generate professional test summary and quality reports.

## When to Use

✅ **USE this skill when:**
- Summarizing a round of testing results
- Generating quality metrics and dashboards
- Preparing test completion / sign-off reports
- Analyzing defect trends and distribution
- "出个测试报告" / "这轮测试总结一下"

❌ **DON'T use this skill when:**
- Running tests → use `api-tester` or `web-tester`
- Writing test cases → use `test-case-gen`
- Analyzing specific bugs → use `bug-hunter`

## Report Template

### Test Execution Summary Report

```markdown
# 📋 测试报告

**项目**: {project_name}
**版本**: {version}
**测试周期**: YYYY-MM-DD ~ YYYY-MM-DD
**测试负责人**: 虫探 🔍
**报告日期**: YYYY-MM-DD

---

## 1. 概述

本轮测试针对 {version} 版本，覆盖 {module_list} 等核心模块，
共执行 {total} 条用例，通过率 {pass_rate}%。

### 质量结论: ✅ 建议发布 / ⚠️ 有风险 / 🔴 不建议发布

---

## 2. 测试执行统计

| 指标 | 数值 |
|------|------|
| 总用例数 | {total} |
| 已执行 | {executed} |
| 通过 | {passed} ✅ |
| 失败 | {failed} ❌ |
| 阻塞 | {blocked} 🚫 |
| 跳过 | {skipped} ⏭️ |
| 通过率 | {pass_rate}% |
| 执行率 | {exec_rate}% |

### 按模块统计

| 模块 | 总数 | 通过 | 失败 | 通过率 |
|------|------|------|------|--------|
| 登录模块 | 15 | 14 | 1 | 93.3% |
| 用户管理 | 20 | 18 | 2 | 90.0% |
| 订单模块 | 30 | 25 | 5 | 83.3% |

### 按优先级统计

| 优先级 | 总数 | 通过 | 失败 | 通过率 |
|--------|------|------|------|--------|
| P0-核心 | 20 | 20 | 0 | 100% ✅ |
| P1-重要 | 25 | 23 | 2 | 92% |
| P2-一般 | 15 | 12 | 3 | 80% |
| P3-低优 | 5 | 2 | 3 | 40% |

---

## 3. 缺陷统计

| 指标 | 数值 |
|------|------|
| 本轮新增缺陷 | {new_bugs} |
| 已修复 | {fixed} |
| 待修复 | {open} |
| 遗留 | {deferred} |

### 缺陷严重程度分布

| 严重程度 | 数量 | 状态 |
|----------|------|------|
| 🔴 Critical | 0 | - |
| 🟠 Major | 3 | 2 fixed, 1 open |
| 🟡 Minor | 5 | 3 fixed, 2 deferred |
| 🟢 Trivial | 2 | 1 fixed, 1 deferred |

### 缺陷模块分布

| 模块 | 缺陷数 | 缺陷密度 |
|------|--------|----------|
| 订单模块 | 5 | 0.17/用例 |
| 用户管理 | 3 | 0.15/用例 |
| 登录模块 | 2 | 0.13/用例 |

---

## 4. 风险评估

| 风险项 | 影响 | 概率 | 建议 |
|--------|------|------|------|
| {risk_1} | 高/中/低 | 高/中/低 | {mitigation} |

---

## 5. 遗留问题

| ID | 标题 | 严重程度 | 状态 | 备注 |
|----|------|----------|------|------|
| BUG-xxx | {title} | Major | Deferred | {reason} |

---

## 6. 建议

- {recommendation_1}
- {recommendation_2}
```

## Quality Metrics

### Key Metrics to Calculate

```
Pass Rate        = (Passed / Executed) × 100%
Execution Rate   = (Executed / Total) × 100%
Defect Density   = New Bugs / Total Cases
Defect Removal   = Fixed / (Fixed + Open) × 100%
Test Efficiency  = Bugs Found / Test Hours
Reopen Rate      = Reopened / Total Fixed × 100%
```

### Quality Gates

| Metric | 🟢 Good | 🟡 Warning | 🔴 Block |
|--------|---------|-----------|----------|
| P0 Pass Rate | 100% | < 100% | N/A (must be 100%) |
| Overall Pass Rate | ≥ 95% | 90-95% | < 90% |
| Critical Bugs Open | 0 | 1-2 (with workaround) | > 2 |
| Execution Rate | ≥ 95% | 85-95% | < 85% |

### Release Decision

Based on metrics, recommend:

- **✅ Go**: All P0 pass, overall ≥ 95%, 0 critical bugs open
- **⚠️ Conditional Go**: Overall ≥ 90%, ≤ 2 major bugs with workaround
- **🔴 No Go**: P0 failures, or overall < 90%, or critical bugs open

## Trend Analysis Template

When tracking quality across multiple iterations:

```markdown
## 质量趋势（最近 5 轮迭代）

| 迭代 | 用例数 | 通过率 | 新增缺陷 | 遗留缺陷 | 质量评级 |
|------|--------|--------|----------|----------|----------|
| v1.1 | 120 | 92% | 15 | 3 | ⚠️ |
| v1.2 | 135 | 95% | 10 | 2 | ✅ |
| v1.3 | 150 | 93% | 12 | 4 | ⚠️ |
| v1.4 | 160 | 97% | 6 | 1 | ✅ |
| v1.5 | 170 | 98% | 4 | 0 | ✅ |

趋势分析：
- 用例数稳步增长（+42%），测试覆盖在扩大
- 通过率整体上升，v1.3 有回落（原因：新增支付模块）
- 新增缺陷持续下降，代码质量在改善
- 遗留缺陷归零，技术债务控制良好
```

## Defect Root Cause Distribution

缺陷根因分布有助于改进上游环节：

```markdown
### 缺陷根因分布

| 根因分类 | 数量 | 占比 | 改进建议 |
|----------|------|------|----------|
| 需求遗漏/歧义 | 8 | 32% | 加强需求评审，增加测试用例评审环节 |
| 编码逻辑错误 | 7 | 28% | 加强 Code Review，增加单元测试 |
| 接口约定不一致 | 5 | 20% | 统一接口文档，引入契约测试 |
| 环境/配置问题 | 3 | 12% | 环境标准化，配置纳入版本管理 |
| 第三方依赖 | 2 | 8% | 增加 Mock 测试，监控依赖变更 |
```
