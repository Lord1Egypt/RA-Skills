# Output Format

Use this structure for concrete R&D problem answers.

All user-facing content must be English. If MCP fields contain non-English raw text, translate or summarize that content into English before presenting it.

## 1. Problem Restatement

Restate the problem as an engineering contradiction:

- Improve:
- Worsening side effect:
- Key constraints:
- Application context:

## 2. TRIZ Frame

List:

- Technical contradiction:
- Candidate inventive principles:
- Search keywords:

Keep this section short. The user wants useful cases, not a TRIZ lecture.

## 3. Similar Solution Cases

Sort cases by `relevance_score` in descending order before presenting them. If a case has no score, place it after scored cases and keep its original MCP order among other unscored cases.

If all returned cases have `relevance_score` missing or null, do not fabricate scores. Add one short note: "The MCP did not provide numeric relevance scores for this query, so cases are presented in the returned order." Do not show a `Relevance score` line or column when scores are missing.

Present every case returned by the MCP service. Do not default to a top-3, top-5, or top-10 subset. If the returned case count is too large for a single response, continue in batches and clearly show:

- total cases returned
- cases shown in the current batch
- remaining cases

Do not show `rank` or `case_id` in the default user-facing answer. These are internal traceability fields and are not useful for most R&D users. Show source identifiers only if the user explicitly asks for them.

Use a compact table only if it remains readable. For many cases or long fields, present each case as a short structured block. Include the six important MCP fields, and include `relevance_score` only when the MCP provides a numeric value.

Recommended fields:

- problem_summary
- effect_summary
- innovation_summary
- triz_technical_contradiction
- triz_svop
- triz_scientific_effects

If numeric `relevance_score` values are present, include `relevance_score` before `problem_summary`.

## 4. Transferable Solution Patterns

Summarize 2 to 4 reusable patterns, such as:

- Segmentation and modularization
- Preliminary action
- Dynamic structure or dynamic control
- Intermediary
- Local quality
- Parameter changes
- Composite materials or functional gradients

Explain how each pattern could transfer to the user's product, process, or system.

## 5. R&D Next Steps

Give 2 to 3 concrete next steps:

- one design direction
- one validation experiment
- one data point or constraint to collect next

## Legal and Confidence Note

When appropriate, add:

"These results are R&D inspiration based on a structured patent-derived case dataset. They are not infringement opinions, freedom-to-operate analysis, or patentability advice."
