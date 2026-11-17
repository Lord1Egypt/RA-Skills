## Description:

基于过程和风险思维生成符合ISO9001标准的质量管理体系文件，支持四级文件结构和乌龟图；覆盖质量手册、程序文件、作业文件、记录表单等全套体系文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

External quality managers, consultants, and enterprise teams use this skill to collect company and process information, then draft ISO9001:2015 quality management system documents. It supports quality manuals, procedures, work instructions, record forms, and turtle-diagram process analysis for review and customization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores enterprise profile details in enterprise-info.json and generated documents may contain confidential business records.

Mitigation: Install only in a private workspace, treat the profile and generated documents as confidential, and delete enterprise-info.json when the project is finished or before switching companies.

Risk: Generated ISO9001 materials may be incomplete or inaccurate if company, process, responsibility, or risk details are missing.

Mitigation: Review manuals, procedures, work instructions, forms, and any marked placeholders with qualified quality personnel before operational use or certification activities.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-iso9001-qms-generator)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-iso9001-qms-generator)
- [ISO9001 file selection template](references/file-selection-template.md)
- [ISO9001:2015 standard clauses reference](references/iso9001-standards.md)
- [Process analysis guide](references/process-analysis-guide.md)
- [Quality manual template](references/quality-manual-template.md)
- [Turtle diagram guide](references/turtle-diagram-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Conversational guidance, Markdown source, JSON company profile data, and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python-docx 1.1.2 for Word document generation when the conversion script is run.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
