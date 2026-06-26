# SkillHub Peer Benchmarking Guide

Complete methodology for Phase 2 peer benchmarking in skill-forge.

**When to read**: When entering Phase 2 (after Phase 1 creation + self-validation completes). Read this file in full before starting benchmarking.

---

## Step 5a: Search & Rank

### Primary: SkillHub API

```
URL: https://api.skillhub.cn/api/v1/search?q=<keywords>
Keywords: extract from the created Skill's name + core function
Example: for "interview-insight-miner", search "interview insight analysis"
```

API returns quality metrics: `downloads`, `installs`, `stars`, `score`.

### Quality Ranking Formula

```
综合评分 = downloads × 0.4 + installs × 0.3 + stars × 0.3
```

| Metric | Weight | Rationale |
|--------|--------|-----------|
| downloads | 0.4 | Most objective — people downloaded because it has real value |
| installs | 0.3 | More precise — actually installed after downloading |
| stars | 0.3 | Community endorsement — but biased by age (older Skills get more stars) |

Sort by score descending, take **Top 3**.

### CLI Fallback (when API unavailable)

```bash
skillhub search <keywords>
```

CLI does not return downloads/stars. Use proxy ranking:
1. Higher version → more iterations → likely better quality
2. Longer description (>200 chars) → author was more thorough
3. Description contains specific trigger scenarios → more practical

Take Top 3.

---

## Step 5b: Tencent Manual Compliance Comparison

Compare our Skill against Top 3 peers on these **9 Tencent Skills Manual dimensions**:

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

Fill in the comparison table:

| Tencent Principle | Our Skill | #1 Peer | #2 Peer | #3 Peer | Gap? |
|-------------------|-----------|---------|---------|---------|------|
| 1. Trigger precision | | | | | |
| 2. Keyword frontloading | | | | | |
| 3. Do NOT scope | | | | | |
| 4. One Job | | | | | |
| 5. 4-module structure | | | | | |
| 6. Output concreteness | | | | | |
| 7. Intern Test rules | | | | | |
| 8. Edge case coverage | | | | | |
| 9. Size control (≤200 lines + progressive disclosure) | | | | | |

---

## Step 5c: Differentiation & Gap Analysis

### If our Skill duplicates an existing high-quality Skill

→ Recommend user install the existing Skill: `skillhub install <slug>`

### If our Skill has meaningful differences

→ Document differentiation:
```
vs [Peer #1 name]: 我们做X不做Y，对方做Y不做X
vs [Peer #2 name]: 我们的输出格式更[具体/专业/简洁]
vs [Peer #3 name]: 我们的规则覆盖了[对方遗漏的边界情况]
```

### If peers reveal blind spots in our Skill

→ List specific improvements with Tencent Manual justification:
```
盲区1: [具体问题]（违反腾讯手册原则：[哪条原则]）
  → 修复方案：[具体修复]
盲区2: [具体问题]（违反腾讯手册原则：[哪条原则]）
  → 修复方案：[具体修复]
```

---

## Step 5d: User Decision

Present benchmarking results with 3 options:

1. **采纳补充** — Apply all gap fixes, re-run Step 4 validation
2. **保持原样** — Ship as-is, acknowledge gaps
3. **直接安装已有** — If a peer Skill already does the job well, install it instead

**User's decision is final.** AI recommends but never forces.
