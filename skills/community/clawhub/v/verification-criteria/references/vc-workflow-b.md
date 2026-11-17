# Workflow B — VC Quality Audit

> Load this file when Workflow B is selected (user provides **existing VCs** and asks to audit/review them).
> This workflow does NOT generate new VCs — it scores SMARTR-OC quality attributes and runs CK-02/CK-03/CK-06 peer review pre-check, then improves below-threshold VCs.

## Todo List Template

**IMMEDIATELY after loading this workflow**, call `manage_todo_list` with these items. Mark each `in-progress` before starting and `completed` immediately after finishing.

```
| # | Title | Status |
|---|-------|--------|
| 1 | B.0 确认 VC 文件来源 | not-started |
| 2 | B.1 解析 VC（提取 ID、关联需求、方法、条件、判据） | not-started |
| 3 | B.2 质量审核：SMARTR-OC 8点评分（含 Source Depth）+ CK-02/CK-03/CK-06 检查 | not-started |
| 4 | B.3 改进建议（修复不达标 VC） | not-started |
| 5 | B.4 输出质量审核报告 | not-started |
```

> **Important**: B.2 → B.3 may loop if revisions fail re-check. Keep `in-progress` until the VC passes both SMARTR-OC ≥ 6/8 and all 🔴 Critical CK items.

## Accepted Input Sources

- A markdown/Excel/CSV file path in the workspace
- Content pasted directly in chat
- A document already open in the editor

---

### B.0 Identify VC Source (MANDATORY)

Use `vscode_askQuestions` to ask:

> Which file contains the verification criteria you'd like me to audit? Please provide the file path or paste the VCs directly.

Read/parse to understand: how many VCs, what format, do they have VC IDs and linked requirement IDs?

**If no source is provided, do NOT proceed.**

---

### B.1 Parse VCs

Extract each VC. For each, capture:
- VC ID (or assign `VC-UNKNOWN-{seq}`)
- Linked requirement ID (flag 🟠 MISSING-LINK if absent)
- Verification method
- Test conditions
- Pass/fail criterion

---

### B.2 Quality Review (SMARTR-OC + CK-02/CK-03/CK-06)

Apply both checks below to **every** VC in a single pass.

**Part 1 — SMARTR-OC:** Load `references/vc-smartr-oc.md` for the 8-point scoring rubric. Score each attribute ✅/❌. Total = number of ✅.

- 8/8: ✅ Excellent
- 6-7/8: ⚠️ Acceptable
- < 6/8: ❌ Needs revision

**Part 2 — CK:** Load `assets/vc-checklist.md` for the 3-item peer review checklist. Flag each item ✅/❌:

| CK | Check Item | Severity |
|----|-----------|----------|
| CK-02 | VC ID naming convention compliance | 🟡 Minor |
| CK-03 | Verification method matches requirement type | 🔴 Critical |
| CK-06 | Sample size reasonable with statistical significance | 🟡 Minor |

**Per-VC disposition:**
- SMARTR-OC < 6/8 **or** CK-03 ❌ → needs revision; proceed to B.3
- SMARTR-OC ≥ 6/8 and only 🟡 Minor CK ❌ → ⚠️ Conditional Pass (list minor issues)
- SMARTR-OC ≥ 6/8 and all CK ✅ → ✅ Ready for Peer Review

---

### B.3 Improvement Suggestions

For each VC flagged for revision in B.2, identify the root cause and fix:

- **SMARTR-OC failures**: Fix per the 'If ✗' column in `references/vc-smartr-oc.md`; the 'Meaning' column explains the root cause.
- **CK-03 failure** (wrong verification method): Select correct method per the decision tree in `../SKILL.md` §Mode A.

Workflow: resolve ALL flagged issues → rewrite VC → re-run B.2. Must clear both SMARTR-OC ≥ 6/8 and CK-03 ✅. If a VC repeatedly fails the same attribute or CK item, escalate — the underlying requirement may need revision.

---

### B.4 Output: Quality Audit Report

Load `references/vc-report-templates.md#quality-audit-report-workflow-b` for the report template. Include:

- Source, total VCs, average SMARTR-OC score, score distribution
- Per-VC SMARTR-OC + CK-02/CK-03/CK-06 results
- Disposition (✅ Pass / ⚠️ Conditional / ❌ Needs Revision)
- Top 3 common issues

---

> **Tip**: Compare the audit result with the author's self-check (if available) to identify systematic self-check blind spots — e.g., sampling bias (only checking ~35% of VCs), missing objective-language violations, or pattern-level C-dimension gaps.
