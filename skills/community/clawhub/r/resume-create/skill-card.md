## Description:

创建、优化、修改专业简历。数据驱动生成极简简历 HTML 并导出 PDF。当用户需要创建简历、修改简历、优化简历、生成 PDF 简历时使用。支持从零开始引导收集信息，也支持读取已有简历进行优化改写。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create a new professional resume or improve an existing resume, then generate HTML and PDF resume files for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated resumes can contain sensitive personal data that is retained in local HTML and PDF files.

Mitigation: Review storage location and retention expectations before use, and remove generated resume files when they are no longer needed.

Risk: The resume template can execute unsafe content from resume fields when opened for PDF export.

Mitigation: Use only trusted resume inputs until template escaping, link validation, and unsafe HTML insertion are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linhongbijkm-dot/skills/resume-create)
- [Skill instructions](artifact/SKILL.md)
- [Resume HTML template](artifact/assets/template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, guidance]

**Output Format:** [Structured resume data rendered as HTML and exported to PDF, with conversational guidance and revision notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local HTML and PDF resume files; generated files may contain sensitive personal data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
