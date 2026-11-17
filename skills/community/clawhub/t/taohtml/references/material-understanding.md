# Material Understanding

Use this reference for an explicitly bound Word, PDF, PPT, or HTML input before designing or migrating the report.

For an existing project, first apply `project-handoff.md`. A `review_only` request
uses its read-only state map and does not create a Material Understanding Summary.
For a `meaning_preserving_local` continuation, do not use this reference or rebuild
the summary. For a `meaning_changing` continuation, use it only for the affected
source delta; do not restart full material intake when the inherited interpretation
remains supported.

## Goal

Build a source-grounded understanding that the user can correct. Do not propose page layouts, visual styles, or animation during this stage.

## Inspection

Before opening a PDF, run the `pdf` profile in `environment-preflight.md`. Inspect
only materials already eligible under the intake workflow's source-binding rules.
Do not open a workspace candidate to decide whether it should be bound.

Inspect the complete available source, not only the first pages. Extract:

- Topic and intended purpose stated by the material
- Original section structure
- Core viewpoints that must not be lost
- Data, examples, screenshots, cases, quotations, and other evidence
- Source labels, links, footnotes, and attachment references
- Repeated, weak, or contradictory claims
- Missing units, inconsistent definitions, or data that cannot be interpreted safely

For each bound item, record its `source_role`, `availability_status`, inspection
coverage, evidence-verification status, what it supports, and what it cannot
establish. Use the exact role and status vocabulary in `project-handoff.md`.
`workspace_readable` and `external_retrieved_inspected` describe current access, not
provenance or truth; record whether inspection was complete or partial.

If the file cannot be read completely, say exactly which part is unavailable and request a usable copy. Do not pretend the source was fully inspected.

## Handoff Source Semantics

Keep these distinctions visible:

- Original customer material may support source facts within the coverage actually
  inspected.
- External public evidence may support a source fact only when the exact locator,
  retrieved content, relevant claim, and verification result are recorded. It is
  neither original customer material nor Agent-generated material.
- A secondary handoff summary supports only what the earlier account says. It does
  not prove the original data, quotation, citation, evidence link, or conclusion.
- A current artifact supports what is visibly present in that artifact. It does not
  prove the origin or accuracy of rendered claims.
- A visual reference supports observed visual facts within its confirmed mode and
  never becomes report evidence by itself.
- Agent-generated material stays separate from source facts and enters the delivery
  verification ledger when used.
- Described-but-unavailable material remains record-only or unverified until it is
  retrieved or its loss is authoritatively confirmed.

Do not write “the sources were cleaned” or “the originals are gone” because a shell
lookup failed. Record the exact checked scope and retain `not_yet_verified` or
`handoff_record_only` unless the user or an authoritative platform/source state
confirms loss.

## Complexity

Judge complexity from the combination of:

- Amount and variety of source material
- Length and likely page count
- Number of claims and evidence relationships
- Logical or data conflicts
- Importance of the intended use

For simple material, keep the summary short. For complex material, include evidence gaps and conflicts.

## Material Understanding Summary

Use this adaptive structure:

```markdown
# 材料理解摘要

## 主题与目的
...

## 原始结构
1. ...

## 必须保留的核心观点
- ...

## 已有证据与数据
- 观点：...
  - 支撑材料：...

## 材料来源绑定
- 材料：路径、上传标识或精确外部定位
  - source_binding：current_upload_or_user_explicit / task_instruction_explicit / candidate_confirmed / agent_retrieved_external
  - 来源理由：用户当前上传或明确指定 / 当前任务说明明确声明 / Agent 展示候选路径后获用户确认 / 当前任务授权下从外部来源取回并记录精确定位
  - source_role：original_customer_material / external_public_evidence / secondary_handoff_summary / current_artifact / visual_reference / agent_generated_material / described_unavailable_material
  - availability_status：workspace_readable / external_retrieved_inspected / platform_visible_not_retrieved / handoff_record_only / confirmed_missing / not_yet_verified
  - evidence_verification：verified / unverified / conflicting / not_applicable
  - 检查覆盖：完整 / 部分 / 未取回，并写明检查依据
  - 可支撑：...
  - 不能支撑：...

## 发现的问题
- 重复、缺口、冲突或数据口径问题

## 当前理解
- TaoHtml 对材料整体逻辑的简要复述

请确认以上理解是否准确，或直接指出需要修正的部分。
```

Remove empty sections rather than filling them with placeholders.

Keep `材料来源绑定` for every material actually used. This is provenance, not a
creative-supplement disclosure. Do not describe an explicitly bound material as
TaoHtml-generated content.

For a meaning-changing continuation, keep the summary compact and delta-oriented:
identify which prior interpretation remains supported, what the requested change
affects, and which source roles or availability gaps constrain that change. Do not
imply that a detailed secondary summary is sufficient for every later edit. A
meaning-preserving local continuation does not create or reconfirm this summary.

## Evidence And Data

Determine required evidence from the report type and claim. Data, cases, outcomes, comparisons, risk claims, and conclusion-level judgments normally require support.

Use this order:

1. Search the customer's material.
2. If a required gap remains and browsing is available, find public evidence.
3. Show the public source and the conclusion it would support for customer confirmation.
4. If public evidence conflicts with customer material, show both sides and the impact; do not choose silently when it changes the conclusion.

Classify a public or third-party source retrieved during the current task as
`agent_retrieved_external | external_public_evidence |
external_retrieved_inspected`. Record the exact locator, retrieval time, inspection
coverage, supported claim, and `verified | unverified | conflicting` result. Do not
classify it as `original_customer_material` or `agent_generated_material`, and do not
use `workspace_readable` unless the exact evidence artifact is actually present and
readable in the task workspace.

Customer data visualized by the agent remains customer evidence. Never alter it, relabel it as generated, or invent values and present them as customer evidence. When a useful report needs an illustrative chart, use separately tracked simulated values, label the chart `示意 / 模拟 / 待核实` next to the visual, and include the values in the delivery verification list.

During a meaning-preserving local continuation, layout, technical, portability, and
local-expression changes proceed without rebuilding or reconfirming this summary.
Before changing real data, source attribution, evidence relationships, real
identities, achieved outcomes, core conclusions, structure, scope, or responsibility,
restore the original source or obtain the user's explicit confirmation of the exact
change and enter the meaning-changing branch in `project-handoff.md`. High-risk
factual verification remains mandatory.

When units or definitions are inconsistent, correct only what can be determined safely. Put every correction, reason, and consequence in the design brief's confirmation section.

Keep a source record even when the customer does not want citations displayed in the final pages. The design brief should identify the source, supported viewpoint, and intended use.

## Summary Confirmation

Wait for explicit confirmation or correction. A confirmed summary freezes the source interpretation, not the final report structure. Structure and visual decisions follow in the intake workflow.
