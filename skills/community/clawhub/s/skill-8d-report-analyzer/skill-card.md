## Description:

深度分析8D报告每一步骤质量，重点评价D4根因分析工具应用、D3流/遏制措施、D5/D6纠正预防措施的有效性与逻辑性；当SQE或质量工程师需要对供应商/内部8D报告进行评审、发现不足并提出改进建议时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

SQE, quality engineers, and operations teams use this skill to parse and review supplier or internal 8D reports, identify weaknesses across D1-D8, and generate concrete improvement recommendations. It is especially focused on root-cause depth, containment effectiveness, corrective and preventive action logic, document updates, and closure evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 8D reports may contain confidential supplier, customer, product, or process information.

Mitigation: Process only the report content needed for review and avoid including unnecessary confidential data.

Risk: The document parser depends on local Python packages for DOCX, PDF, and XLSX handling.

Mitigation: Install python-docx, PyPDF2, and openpyxl in a virtual environment from a trusted package source.

Risk: Selecting the wrong local document could expose unrelated report content or produce an incorrect review.

Mitigation: Confirm the exact document file and ask the user to verify parsed content before proceeding to analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-8d-report-analyzer)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-8d-report-analyzer)
- [8D report evaluation criteria](references/8d-criteria.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown analysis with optional JSON parser output for DOCX, PDF, and XLSX inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; requires user confirmation of parsed report content before deep analysis.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
