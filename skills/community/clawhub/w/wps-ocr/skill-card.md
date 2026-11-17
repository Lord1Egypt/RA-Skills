## Description:

A lightweight, high-performance file parsing tool that extracts text, handwritten text, formulas, tables, documents, and seals from supported files into Markdown structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[randyliu111](https://clawhub.ai/user/randyliu111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send supported images or PDFs to WPS/Kingsoft OCR and receive extracted text or Markdown for document digitization, translation, or editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads local files or URLs to a third-party WPS/Kingsoft cloud OCR service.

Mitigation: Use it only when disclosure to that service is acceptable, and avoid sensitive IDs, contracts, financial records, or confidential screenshots unless approved.

Risk: Command examples that include user-provided paths or URLs can expose users to shell injection if concatenated into a shell command.

Mitigation: Invoke the Python script with an argument array or carefully quoted arguments rather than building shell commands by string concatenation.

## Reference(s):

- [ClawHub wps-ocr Release Page](https://clawhub.ai/randyliu111/skills/wps-ocr)
- [WPS OCR Access Key Page](https://aiwrite.wps.cn/pdf/parse/accesskey/)
- [WPS OCR Demo Platform](https://aiwrite.wps.cn/pdf/parse/web/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON from the OCR script containing status, message, and markdown_text; Markdown guidance with shell commands for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WPS_OCR_ACCESS_KEY and sends supported local files or public URLs to WPS/Kingsoft cloud OCR.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
