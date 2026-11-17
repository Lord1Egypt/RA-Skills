## Description:

将 Word 文档调整为《国家电网公司规范格式》（方正字体、标题层级、28磅行距、-1-页码、表格、中文引号等12条规则）。用户发来 docx 并说"调成规范格式"时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamantanee](https://clawhub.ai/user/diamantanee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing agents use this skill when a user submits a DOCX file and requests State Grid Corporation of China formatting. The skill formats headings, body text, tables, page numbers, table of contents fields, and Chinese quote marks, then produces a new DOCX file for return to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOCX files are processed locally and may contain untrusted content.

Mitigation: Use the skill only with trusted DOCX inputs or add sanitization for document fields and external relationships before formatting.

Risk: Generated documents set Word fields to update automatically, which can refresh existing fields from the source document.

Mitigation: Review field-update behavior before deployment and disable automatic field updates or strip unsafe fields when handling externally supplied DOCX files.

Risk: The artifact describes returning formatted documents through Feishu, which may expose document contents to that delivery channel.

Mitigation: Confirm the document may be shared through Feishu and apply the organization's normal document-handling policy before sending the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamantanee/skills/sgcc-doc-format)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and a generated DOCX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes DOCX input locally and writes a separate formatted DOCX output file; the artifact describes returning the file through Feishu.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
