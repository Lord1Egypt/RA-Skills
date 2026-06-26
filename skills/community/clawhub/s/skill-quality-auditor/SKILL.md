---
name: skill-reviewer
description: Score and grade AgentSkills across four dimensions: design quality, content quality, security, and usability. Use when asked to score, grade, evaluate, or rate a skill's quality — producing a numeric scorecard with dimension-by-dimension ratings. Triggers on "score this skill", "grade skill", "rate skill quality", "evaluate skill", "skill scorecard", "给技能打分", "技能评分".
---

# Skill Reviewer

Four-dimension quality auditor for AgentSkills.

## Review Process

### Step 1: Inventory & Classify

1. `find /path/to/skill -type f` — list all files. If path doesn't exist or is empty, abort with error.
2. Read `_meta.json` or `.clawhub/origin.json` if present (source, version, author info).
3. Read SKILL.md in full.
4. Classify skill type per `references/weight-adjustment.md` → determine weights.

### Step 2: Scan

1. SKILL.md (full read)
2. scripts/ (full read, do NOT execute)
3. references/ (full read if ≤10 files or ≤50KB total; spot-check otherwise)
4. assets/ (list filenames, flag non-asset file types: .sh/.py/.exe/.bat/.ps1 in assets/ = suspicious)
5. Other files (.json, dotfiles, symlinks) — inspect each

### Step 3: Score Each Dimension

Load reference files: `references/design-quality.md`, `references/content-quality.md`, `references/security.md`, `references/usability.md`.

For each dimension, walk the checklist and score per the rubric. Cite `[file:line]` for each finding.

**Security shortcut:** Run grep sweeps for CRITICAL patterns first (see security.md C1-C11). If any CRITICAL found → D3=1, note it, but **still score remaining dimensions** — don't skip them.

**Orphan file check (security.md):** After reading SKILL.md, cross-reference all mentioned files against the actual file list. Flag orphans.

### Step 4: Calculate & Verdict

Weighted total = Σ(dim_score × adjusted_weight)

| Verdict | Condition |
|---------|-----------|
| ✅ PASS | Total ≥ 8 AND every dimension ≥ 6 AND no CRITICAL findings |
| 🔧 REVISE | Total < 8 OR any dimension < 6 OR any CRITICAL finding |

**CRITICAL auto-revise:** Even if total ≥ 8, any security CRITICAL finding forces REVISE.

## Report Format

Use list format (not tables — compatible with all platforms):

### PASS:
```
【技能审校通过】
技能：{name}
路径：{path}
类型：{type}
综合得分：{score}/10
审校日期：{date}

• 设计质量（{w1}%）：{d1}/10 — {简要说明}
• 内容质量（{w2}%）：{d2}/10 — {简要说明}
• 安全性（{w3}%）：{d3}/10 — {简要说明}
• 实用性（{w4}%）：{d4}/10 — {简要说明}

亮点：
- {亮点1}
- {亮点2}
```

### REVISE:
```
【技能审校打回】
技能：{name}
路径：{path}
类型：{type}
综合得分：{score}/10
审校日期：{date}

⚠️ 判定维度：
• 设计质量（{w1}%）：{d1}/10
• 内容质量（{w2}%）：{d2}/10
• 安全性（{w3}%）：{d3}/10
• 实用性（{w4}%）：{d4}/10

具体问题：
- [D1] {issue} — {file}:{line}
- [D3] 🔴 CRITICAL: {issue} — {file}:{line}

改进方向：
- {方向1}
- {方向2}

达标标准：
- {标准1}
- {标准2}
```

## References

- `references/weight-adjustment.md` — type classification + weight matrix
- `references/design-quality.md` — D1 checklist + rubric + scoring rules
- `references/content-quality.md` — D2 checklist + rubric + scoring rules
- `references/security.md` — D3 pattern table + detection commands
- `references/usability.md` — D4 checklist + rubric + scoring rules
