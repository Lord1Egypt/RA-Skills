## Description:

分析Excel表中的申报失败信息，自动生成Word版本的申报运维报告，用于定位问题、统计趋势、提出整改建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[houyalei](https://clawhub.ai/user/houyalei)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, tax filing, and support teams use this skill to analyze Excel-based filing failure logs, summarize failure trends, identify persistent or burst issues, and generate a Simplified Chinese Word operations report with remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Word reports may preserve operational failure details from the source Excel file, including customer, business, or incident information.

Mitigation: Use approved spreadsheets and output locations, then review the report before sharing it.

Risk: Missing or incorrectly mapped Excel columns may lead to incomplete analysis or misleading trend summaries.

Mitigation: Confirm column mappings when automatic detection fails and review generated summaries before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houyalei/skills/tax-filing-result-analysis)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python-oriented implementation steps for generating a .docx report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report is expected to be in Simplified Chinese and may include tables, charts, summaries, issue lists, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
