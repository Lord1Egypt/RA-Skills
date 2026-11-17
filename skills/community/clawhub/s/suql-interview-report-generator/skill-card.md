## Description:

面试分析报告生成 - 标准化批量生成面试分析报告，按固定11章结构输出DOCX格式

This skill is ready for commercial/non-commercial use.

## Publisher:

[suql82](https://clawhub.ai/user/suql82)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams, hiring managers, and recruiting operations staff use this skill to generate standardized candidate interview analysis reports, hiring decision support, background-check focus areas, compensation suggestions, and probation-period recommendations from required interview materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive candidate and HR records.

Mitigation: Keep processing local where possible and define retention, access, and sharing rules for both source files and generated reports.

Risk: The artifact permits OCR for image and PDF inputs, including unspecified cloud OCR.

Mitigation: Avoid cloud OCR unless the organization has approved the provider and the user explicitly authorizes the upload.

Risk: Generated interview conclusions may affect hiring decisions.

Mitigation: Review report conclusions against the original resume, registration form, job description, and interview record before using them for employment decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance, files]

**Output Format:** [Structured Chinese-language report content and DOCX report generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to become DOCX files named with candidate sequence, candidate name, and interview analysis report title.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
