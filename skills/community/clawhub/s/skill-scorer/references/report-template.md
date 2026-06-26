# Report Template — skill-scorer

> **Bilingual output rule:** Always generate the FULL report in Chinese first, then a clear separator, then the FULL report in English. No interleaving. Both versions must have identical scores, issues, and suggestions.

---

## Report Language Structure

The report is a single document with two complete halves:

```
┌──────────────────────────────────┐
│  Part 1: 中文完整报告              │
│  (Header → Score Card → Strengths │
│   → Issues → Quick Wins → Roadmap │
│   → Follow-Up)                    │
├──────────────────────────────────┤
│  --- (separator)                  │
├──────────────────────────────────┤
│  Part 2: English Full Report      │
│  (Header → Score Card → Strengths │
│   → Issues → Quick Wins → Roadmap │
│   → Follow-Up)                    │
└──────────────────────────────────┘
```

Use the delivery format that matches the user's context:
- **In Claude.ai / Cowork**: Output as formatted markdown directly in conversation
- **In Claude Code**: Output as markdown AND optionally save to file if user requests

---

### Section 1: Header & Summary

**Chinese version:**
```markdown
# 🎯 Skill 质检报告

**Skill 名称:** {skill_name}
**版本:** {version or "N/A"}
**评估日期:** {date}
**总分:** {score}/100（{grade}）

> {一句话总评}
```

**English version:**
```markdown
# 🎯 Skill Quality Report

**Skill:** {skill_name}
**Version:** {version or "N/A"}
**Evaluated:** {date}
**Overall Score:** {score}/100 ({grade})

> {one_sentence_verdict}
```

### Section 2: Score Card

Present as a visual table with bar indicators.

**Chinese version — use Chinese dimension names:**

```markdown
## 📊 评分卡

| # | 维度 | 得分 | 评级 |
|---|------|------|------|
| 1 | 元数据与触发 | {score}/100 | {bar} |
| 2 | 结构与架构 | {score}/100 | {bar} |
| 3 | 指令清晰度 | {score}/100 | {bar} |
| 4 | 工作流与逻辑 | {score}/100 | {bar} |
| 5 | 错误处理 | {score}/100 | {bar} |
| 6 | 上下文效率 | {score}/100 | {bar} |
| 7 | 可移植性与兼容性 | {score}/100 | {bar} |
| 8 | 安全性与鲁棒性 | {score}/100 | {bar} |

**加权总分: {final_score}/100 — 等级: {grade}**
```

**English version — use English dimension names:**

```markdown
## 📊 Score Card

| # | Dimension | Score | Rating |
|---|-----------|-------|--------|
| 1 | Metadata & Triggering | {score}/100 | {bar} |
| 2 | Structure & Architecture | {score}/100 | {bar} |
| 3 | Instruction Clarity | {score}/100 | {bar} |
| 4 | Workflow & Logic | {score}/100 | {bar} |
| 5 | Error Handling | {score}/100 | {bar} |
| 6 | Context Efficiency | {score}/100 | {bar} |
| 7 | Portability & Compatibility | {score}/100 | {bar} |
| 8 | Safety & Robustness | {score}/100 | {bar} |

**Weighted Total: {final_score}/100 — Grade: {grade}**
```

Rating bar format:
- 90-100: `████████████ Excellent`
- 80-89:  `█████████░░ Very Good`
- 70-79:  `████████░░░ Good`
- 60-69:  `██████░░░░░ Acceptable`
- 50-59:  `█████░░░░░░ Needs Work`
- 40-49:  `████░░░░░░░ Poor`
- 0-39:   `██░░░░░░░░░ Critical`

### Section 3: Strengths

List 2-4 things the skill does well. Lead with positives.

**Chinese version:**
```markdown
## ✅ 亮点

- **{亮点标题}**: {说明}
- **{亮点标题}**: {说明}
```

**English version:**
```markdown
## ✅ Strengths

- **{strength_title}**: {explanation}
- **{strength_title}**: {explanation}
```

### Section 4: Issue List

Group by severity. Each issue must have: location, description, impact, and fix suggestion.

**Chinese version:**
```markdown
## 🔍 发现的问题

### 🔴 严重 ({count})

**问题 C1: {标题}**
- **位置:** {file}:{section or line range}
- **问题:** {具体问题描述}
- **影响:** {为什么重要}
- **修复:** {具体可执行的建议}

### 🟡 警告 ({count})

**问题 W1: {标题}**
- **位置:** {file}:{section}
- **问题:** {具体问题描述}
- **影响:** {为什么重要}
- **修复:** {具体可执行的建议}

### 🟢 建议 ({count})

**问题 S1: {标题}**
- **位置:** {file}:{section}
- **建议:** {改进思路}
```

**English version:**
```markdown
## 🔍 Issues Found

### 🔴 Critical ({count})

**Issue C1: {title}**
- **Location:** {file}:{section or line range}
- **Problem:** {what's wrong}
- **Impact:** {why it matters}
- **Fix:** {specific actionable suggestion}

### 🟡 Warning ({count})

**Issue W1: {title}**
- **Location:** {file}:{section}
- **Problem:** {what's wrong}
- **Impact:** {why it matters}
- **Fix:** {specific actionable suggestion}

### 🟢 Suggestion ({count})

**Issue S1: {title}**
- **Location:** {file}:{section}
- **Suggestion:** {improvement idea}
```

### Section 5: Top 3 Quick Wins

The 3 highest-impact fixes. Each must include a before/after example.

**Chinese version:**
```markdown
## 🚀 Top 3 快速优化

### 优化 1: {标题}
**收益:** {哪方面提升} | **工作量:** {低/中/高}

修改前:
\`\`\`markdown
{当前内容}
\`\`\`

修改后:
\`\`\`markdown
{优化后内容}
\`\`\`

**原因:** {为什么这样改更好}
```

**English version:**
```markdown
## 🚀 Top 3 Quick Wins

### Quick Win 1: {title}
**Impact:** {what improves} | **Effort:** {low/medium/high}

Before:
\`\`\`markdown
{current content}
\`\`\`

After:
\`\`\`markdown
{improved content}
\`\`\`

**Why:** {explanation of the improvement}
```

### Section 6: Optimization Roadmap

Prioritized improvement plan in phases.

**Chinese version:**
```markdown
## 📋 优化路线图

### 阶段 1: 紧急修复（立即处理）
- [ ] {修复_1}
- [ ] {修复_2}

### 阶段 2: 质量提升（下次迭代）
- [ ] {改进_1}
- [ ] {改进_2}

### 阶段 3: 打磨细节（有空再做）
- [ ] {打磨_1}
- [ ] {打磨_2}
```

**English version:**
```markdown
## 📋 Optimization Roadmap

### Phase 1: Critical Fixes (do immediately)
- [ ] {fix_1}
- [ ] {fix_2}

### Phase 2: Quality Improvements (next iteration)
- [ ] {improvement_1}
- [ ] {improvement_2}

### Phase 3: Polish (when time permits)
- [ ] {polish_1}
- [ ] {polish_2}
```

### Section 7: Follow-Up Prompt

**Chinese version:**
```markdown
---

💡 **下一步:**
- 输入 `fix` → 自动修复 Critical 和 Warning 级别问题，生成优化后的 SKILL.md
- 输入 `deep [维度编号]` → 对某个维度做深度分析
- 输入 `rewrite` → 生成该 skill 的完整优化版本
```

**English version:**
```markdown
---

💡 **Next Steps:**
- Type `fix` → Auto-fix critical and warning issues, generate an improved SKILL.md
- Type `deep [dimension_number]` → Deep dive into a specific dimension
- Type `rewrite` → Generate a fully optimized version of this skill
```

---

## Formatting Rules

1. **Bilingual structure is mandatory** — complete Chinese report first, `---` separator, then complete English report. Never interleave languages within a section. Code snippets in before/after examples stay in their original language (usually English) in both versions.
2. Use emoji sparingly — only for section headers and severity indicators
3. Keep the report scannable — busy PMs should understand the score in 10 seconds
4. Code blocks use markdown syntax highlighting
5. Before/after examples must be real content from the evaluated skill, not generic
6. If the skill is short (<50 lines), keep the report proportionally short — don't pad
7. The overall tone should be that of a **constructive senior code reviewer**: honest, specific, and helpful
8. Both language versions must contain **identical** scores, issue counts, and severity levels — no discrepancies allowed
