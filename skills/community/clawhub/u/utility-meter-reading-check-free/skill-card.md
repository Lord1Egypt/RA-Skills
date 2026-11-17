## Description:

水电抄表与账单核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, property operations, and facilities teams use this skill during monthly close, reconciliation, and inventory checks to verify utility meter reading and billing tables. It recalculates arithmetic relationships, checks totals, detects duplicate rows and missing required fields, and cites the source text for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's conclusions cover only the listed arithmetic checks and are not a full utility-rate audit.

Mitigation: Use the findings as reconciliation support and review rates, tariff rules, on-site readings, and out-of-scope billing adjustments separately.

Risk: Blank base fee cells are treated as zero during recalculation.

Mitigation: Confirm that blank base fees should count as zero for the user's workflow, or replace blanks with explicit amounts before running the check.

Risk: The skill produces Chinese-language output.

Mitigation: Confirm that Chinese-language findings are suitable for the reviewers who will rely on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/utility-meter-reading-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable text or JSON result summaries with cited findings and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided table text; materials are insufficient if required headers or fields are missing.]

## Skill Version(s):

1.0.49 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
