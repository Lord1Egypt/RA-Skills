## Description:

解析 PowerPoint 演示文稿和 PDF，按页整理可编辑内容与图片说明，并生成含页面截图的 Word 文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can convert slide decks or PDFs into editable, page-by-page Word documents with organized text, image descriptions, and page screenshots for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversion setup may install software or alter persistent command settings without clear approval.

Mitigation: Use a prepared environment and run conversion with --no-install. Require approval before renderer installation, sudo commands, executable-link replacement, or shell configuration edits.

Risk: Conversion output or retained intermediate material may contain errors or sensitive document content.

Mitigation: Keep source documents unchanged, require the text-consistency check to pass, and remove retained screenshots and extracted text when finished.

## Reference(s):

- [Wisely Read PPT on ClawHub](https://clawhub.ai/sedey999/skills/wisely-read-ppt)
- [macOS LibreOffice installation guide](reference/macos-install.md)
- [Subagent workflow guide](reference/subagent-workflow.md)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [DOCX with per-page editable text, image descriptions, and page screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Also creates an image-free DOCX that preserves the text and image descriptions.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
