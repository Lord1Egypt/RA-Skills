## Description:

WiseOCR converts a single PDF or image file to Markdown through the WiseDiag cloud OCR API, with support for table recognition and multi-column layout extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisediag](https://clawhub.ai/user/wisediag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use WiseOCR to extract Markdown from one PDF or supported image at a time while preserving structured content such as tables and multi-column layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are uploaded to WiseDiag's cloud service for OCR processing.

Mitigation: Use the skill only for documents approved for cloud processing; do not use it for confidential, financial, identity, credential, minor-related, or regulated documents.

Risk: Persistent plaintext API-key setup can expose the WiseDiag credential.

Mitigation: Set WISEDIAG_API_KEY only for the current session or through a secret manager.

Risk: Unsafe output-name handling can write outside the intended folder when untrusted --name or --output values are used.

Mitigation: Avoid untrusted --name and --output values until output path validation is fixed.

## Reference(s):

- [WiseOCR ClawHub Skill Page](https://clawhub.ai/wisediag/skills/wiseocr)
- [WiseOCR Project Homepage](https://github.com/wisediag/WiseOCR)
- [WiseDiag API Key Management](https://console.wisediag.com/apiKeyManage)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown files and terminal status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one PDF or image per command; default output path is ~/.openclaw/workspace/WiseOCR/{name}.md.]

## Skill Version(s):

1.0.28 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
