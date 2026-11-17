## Description:

客诉质量复盘分析；当用户需要客诉台账分析、售后质量问题复盘、投诉统计报告生成或客诉异常清单分析时使用；覆盖数据清洗、统计分析与改善建议

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality teams and agents use this skill to analyze customer complaint ledgers, after-sales issue records, and complaint exception lists. It helps confirm field mappings, summarize complaint patterns, identify repeated issues, and produce internal quality review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complaint spreadsheets and generated reports may contain customer names, contact details, IDs, or sensitive free-text details.

Mitigation: Redact unnecessary personal or confidential data before analysis and treat generated JSON, Markdown, and HTML reports as internal confidential documents.

Risk: The skill can produce misleading analysis if the input fields are ambiguous, incomplete, or incorrectly mapped.

Mitigation: Confirm key field mappings, analysis goals, preliminary findings, and the report outline with the user before generating final conclusions.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-complaint-quality-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-complaint-quality-analysis)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Field mapping reference](references/field-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; JSON analysis results and Markdown/HTML report files when scripts are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill works from user-provided complaint spreadsheets and asks for field mapping, analysis target, and report outline confirmation before final report generation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
