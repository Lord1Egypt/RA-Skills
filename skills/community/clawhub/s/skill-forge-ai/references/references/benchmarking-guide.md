# Quality Self-Assessment & Differentiation Guide

Complete methodology for Phase 2 quality self-assessment in skill-forge v5.1.

> **v5.1 架构变更**：同类搜索已前移到 Step 0.4（创建前）。Phase 2 现在聚焦于创建后的质量自评和差异化验证。

**When to read**: When entering Phase 2 (after Phase 1 creation + self-validation completes), or when triggered by "技能评估" entry. Read this file in full before starting assessment.

---

## Step 5a: 腾讯9维度自评

Evaluate the created Skill on these **9 Tencent Skills Manual dimensions**:

| # | Tencent Principle | What to check |
|---|-------------------|---------------|
| 1 | **Description: trigger precision** | Does description clearly state WHEN to invoke? |
| 2 | **Description: keyword frontloading** | Are core trigger keywords in first 200 chars? |
| 3 | **Description: Do NOT scope** | Does description explicitly state what it's NOT for? |
| 4 | **One Skill = One Job** | Does it focus on a single scenario with one deliverable? |
| 5 | **4-module structure** | 任务/输出格式/规则/示例 all present? |
| 6 | **Output format: concrete** | Every field has fixed format, no vague instructions? |
| 7 | **Rules: Intern Test** | Every rule is directly actionable, no useless defaults? |
| 8 | **Example: edge case coverage** | Example covers boundary situations? |
| 9 | **Size: under 200 lines** | Lean and focused, no bloat? Progressive disclosure (references/scripts/assets)? |

### Self-Assessment Table

Fill in self-evaluation scores (1-10) and mark weak dimensions:

| # | Tencent Principle | Score (1-10) | Weak? | Notes |
|---|-------------------|--------------|-------|-------|
| 1 | Trigger precision | | | |
| 2 | Keyword frontloading | | | |
| 3 | Do NOT scope | | | |
| 4 | One Job | | | |
| 5 | 4-module structure | | | |
| 6 | Output concreteness | | | |
| 7 | Intern Test rules | | | |
| 8 | Edge case coverage | | | |
| 9 | Size control (≤200 lines + progressive disclosure) | | | |

**Any score <7 → mark as weak dimension, must propose fix in Step 5c.**

---

## Step 5b: 差异化验证

### If Step 0.4 found peers (分支b)

Verify that the differentiation advantages identified in Step 0.4 are actually reflected in the created Skill:

```
Step 0.4 差异点: [具体差异]
  → Skill中的体现: [在哪个模块/规则/示例中落地]
  → 验证结果: ✅已落地 / ❌未落地

Step 0.4 差异点: [具体差异]
  → Skill中的体现: [在哪个模块/规则/示例中落地]
  → 验证结果: ✅已落地 / ❌未落地
```

**未落地的差异点 → 补充到Step 5c修复方案。**

### If Step 0.4 found no peers (分支c)

Skip differentiation verification. Proceed directly to Step 5c blind spot check.

---

## Step 5c: 盲区修复

### For weak dimensions (Step 5a score <7)

List specific improvements with Tencent Manual justification:

```
弱项1: [维度#N - 具体问题]（评分: X/10）
  → 腾讯手册依据: [相关原则]
  → 修复方案: [具体修复动作]
  → 预期提升: 修复后评分可达 X/10

弱项2: [维度#N - 具体问题]（评分: X/10）
  → 腾讯手册依据: [相关原则]
  → 修复方案: [具体修复动作]
  → 预期提升: 修复后评分可达 X/10
```

### For unlanded differentiation (Step 5b ❌)

```
未落地差异: [差异点]
  → 补充位置: [哪个模块需要补充]
  → 补充内容: [具体内容]
```

---

## Step 5d: 用户决策

Present assessment results with options:

1. **采纳修复** — Apply all fixes, re-run Step 4 validation
2. **保持原样** — Ship as-is, acknowledge weak dimensions

**User's decision is final.** AI recommends but never forces.

---

## 独立评估入口（技能评估触发词）

When triggered by "技能评估 / skill评估 / 评估技能" (not part of full workflow):

1. Ask user for the Skill to evaluate (file path or content)
2. Run Step 5a self-assessment (9 dimensions)
3. Run Step 5c blind spot analysis
4. Present results + improvement suggestions
5. User decides whether to apply fixes

**Note**: This path does NOT include Step 5b (differentiation verification), because there's no Step 0.4 peer search context.
