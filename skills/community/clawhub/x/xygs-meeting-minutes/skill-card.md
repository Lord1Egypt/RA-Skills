## Description:

会议纪要融合生成器从钉钉和/或得到 Get笔记的会议纪要 PDF 中提取内容，校准常见 ASR 术语错误，并融合来源内容生成结构化会议纪要 HTML 和 PDF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[caizi333333](https://clawhub.ai/user/caizi333333)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to turn intentionally provided Chinese-language meeting-minutes PDFs into polished, structured meeting notes. It is aimed at business meetings, team discussions, and partnership conversations where dual-source fusion, term correction, action items, and PDF delivery are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting PDFs and generated minutes may contain private or sensitive business information.

Mitigation: Use only PDFs intentionally provided for the task, confirm source files and output destination before processing, and handle generated HTML/PDF files according to the meeting owner's data policy.

Risk: Generated HTML can carry risk if meeting content is untrusted or not properly escaped.

Mitigation: Export only HTML generated from trusted or properly escaped meeting content, as directed by the security guidance.

Risk: ASR term correction can introduce incorrect terminology when the dictionary does not match the meeting context.

Mitigation: Review the corrected terms and allow users to provide additional meeting-specific corrections before final HTML or PDF export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caizi333333/skills/xygs-meeting-minutes)
- [Publisher profile](https://clawhub.ai/user/caizi333333)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML files, optional PDF files, and shell commands for PDF export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on user-provided meeting PDFs, a reusable HTML template, a term-correction dictionary, and an optional PDF export script.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
