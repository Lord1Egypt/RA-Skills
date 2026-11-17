## Description:

门店营收上报表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Store operations and finance teams use this skill to check Chinese-language store sales report text for arithmetic mismatches, repeated store/date rows, missing fields, and total-row inconsistencies before reporting or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node script over user-provided sales report text.

Mitigation: Review the artifact before installation and run it only in an environment appropriate for the report data being checked.

Risk: The free version omits several checks, including negative amounts, threshold-based differences, zero-channel/nonzero-report cases, and difference-rate checks.

Mitigation: Treat the output as limited to the listed executed checks and review the omitted checks before relying on the result.

Risk: The parser expects Chinese headers and tabular text with recognizable store sales columns.

Mitigation: Provide input with the required Chinese headers or use the included sample to confirm the expected format before checking real reports.

Risk: A clean arithmetic result does not prove the underlying channel data is complete, truthful, or audit-ready.

Mitigation: Use the findings as deterministic report validation, then reconcile against source systems or audit evidence when assurance is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/store-sales-report-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with Node shell commands and optional JSON result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing requirements instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.30 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
