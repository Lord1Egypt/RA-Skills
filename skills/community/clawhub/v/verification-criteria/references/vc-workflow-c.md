# Workflow C — Coverage Audit

> Load this file when Workflow C is selected (user wants to audit VC-to-requirement **traceability and coverage**).
> This workflow does NOT score individual VC quality — it checks structural completeness.

## Todo List Template

**IMMEDIATELY after loading this workflow**, call `manage_todo_list` with these items. Mark each `in-progress` before starting and `completed` immediately after finishing.

```
| # | Title | Status |
|---|-------|--------|
| 1 | C.0 确认需求文档 + VC 文件来源 | not-started |
| 2 | C.1 解析需求 ID 和 VC 关联关系 | not-started |
| 3 | C.2 完整性检查（每条需求 ≥ 1 VC） | not-started |
| 4 | C.3 孤儿检测（VC 必须关联到已存在的需求） | not-started |
| 5 | C.4 构建覆盖率矩阵 | not-started |
| 6 | C.5 输出覆盖率审计报告 | not-started |
```

## Accepted Input Sources

- A markdown/Excel/CSV file path in the workspace
- Content pasted directly in chat
- A document already open in the editor

---

### C.0 Identify Sources (MANDATORY)

Use `vscode_askQuestions` to ask for both inputs:

> I need two things for a coverage audit:
> 1. The system requirements (file path or paste)
> 2. The verification criteria (file path or paste)
>
> These can be in the same file or separate files. Which file(s) should I use?

If only one file is provided, check whether it contains both requirements and VCs. If not, ask again for the missing piece.

**If both sources aren't available, do NOT proceed.**

---

### C.1 Parse Requirements and VCs

Extract all requirement IDs from the requirements source. Extract all VCs and their linked requirement IDs from the VC source.

---

### C.2 Completeness Check

- Every requirement must have ≥ 1 VC
- Flag requirements with zero VCs: 🔴 UNCOVERED
- Flag requirements with only partial VC coverage: 🟡 PARTIAL

---

### C.3 Orphan Detection

- Every VC must trace to an existing requirement
- Flag VCs linking to non-existent requirements: 🔴 ORPHAN
- Flag VCs with no linked requirement: 🟠 UNLINKED

---

### C.4 Coverage Matrix

Build a traceability matrix:

| Requirement ID | Linked VC IDs | Status |
|---------------|---------------|--------|
| REQ-001 | VC-REQ-001, VC-REQ-001-2 | ✅ Covered |
| REQ-002 | — | 🔴 Uncovered |
| REQ-003 | VC-REQ-003 | ✅ Covered |
| (orphan) | VC-UNKNOWN-001 | 🔴 Orphan |

---

### C.5 Output: Coverage Audit Report

Load `references/vc-report-templates.md#coverage-audit-report-workflow-c` for the report template. Include:

- Summary stats (total requirements, covered %, uncovered count, orphan count)
- Uncovered requirements list
- Orphan VCs list
- The coverage matrix from C.4
