## Description:

供应商信息结构化整理与Markdown质量管理档案生成；根据用户提供的资料(WORD/PDF/Excel)提取关键信息，按模板汇总生成供应商档案，支持SVG组织架构图

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Supplier management and quality teams use this skill to turn authorized Word, PDF, Excel, text, or Markdown supplier materials into structured supplier quality management profiles. It helps extract supplier details, quality certifications, inspection-system information, quality data, cooperation records, and improvement plans, then generates Markdown and optional document outputs with an SVG organization chart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier documents may contain contact details, business-sensitive information, certifications, quality data, audit records, or other confidential material.

Mitigation: Process only documents the user is authorized to handle, store generated profiles in an access-controlled location, and redact unnecessary sensitive fields before sharing outputs.

Risk: The skill includes a shell-command workflow for chart generation, which could become unsafe if extracted supplier data is interpolated into commands.

Mitigation: Do not construct shell commands directly from extracted supplier data; validate inputs, quote arguments safely, and prefer passing data through structured files or APIs.

Risk: Generated supplier profiles may be incomplete or misleading when source documents are scanned PDFs, missing required fields, or use nonstandard Excel columns.

Mitigation: Flag missing values for user review, request OCR or manual entry for scanned PDFs, and ask the user to confirm column mappings before relying on extracted Excel data.

Risk: The declared Python dependency may resolve differently across environments.

Mitigation: Pin dependencies in a virtual environment before use and review generated document outputs before distribution.

## Reference(s):

- [Server-resolved GitHub source: duding-engicool/skill-supplier-profile-organizer](https://github.com/duding-engicool/skill-supplier-profile-organizer)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-supplier-profile-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown supplier profile by default, with optional Word/PDF document output and SVG organization chart assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated files such as a supplier quality management profile and an SVG organization chart; incomplete source information is marked for follow-up.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata; artifact frontmatter declares 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
