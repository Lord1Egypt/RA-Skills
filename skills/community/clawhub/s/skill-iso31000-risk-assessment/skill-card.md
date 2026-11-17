## Description:

帮助零基础用户通过交互式问答完成ISO31000合规风险评估与应对；当用户需要风险识别、风险分析、风险应对或生成风险管理报告时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, quality, and operations users use this skill to run a guided ISO31000 risk assessment, analyze risks, select response strategies, and generate Markdown risk reports or action plans. It also helps agents parse uploaded Excel risk lists and fold the extracted items into the assessment workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is primarily Chinese-language and depends on users sharing operational details for risk assessment.

Mitigation: Install only when a Chinese-language workflow is appropriate and share only the operational details needed for the assessment.

Risk: The Excel parser can read and print arbitrary local workbook paths without size or scope limits.

Mitigation: Provide only intended uploaded workbooks, prefer a specific sheet, avoid very large files, and review parser output before using it.

Risk: Generated reports and action plans may contain confidential business information.

Mitigation: Review generated Markdown before saving or sharing it and remove sensitive details that should not be retained.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-iso31000-risk-assessment)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-iso31000-risk-assessment)
- [Report templates](references/report-templates.md)
- [Risk response strategies](references/response-strategies.md)
- [Risk numbering rules](references/risk-numbering.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language conversational guidance, Markdown tables and reports, and occasional shell commands for Excel parsing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process user-provided Excel workbooks with pandas/openpyxl and print parsed workbook data as JSON.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
