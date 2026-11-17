## Description:

WiseDiag MedOCR converts one PDF or image file into Markdown through the WiseDiag cloud OCR API, including text extraction, table recognition, and multi-column layout support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisediag](https://clawhub.ai/user/wisediag)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract text, tables, and document layout from a single PDF or image. The skill uploads the file to WiseDiag for OCR processing and saves the returned Markdown locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files are sent to WiseDiag's cloud OCR service, which can expose sensitive or confidential document contents to a third-party processor.

Mitigation: Use the skill only for files you are comfortable sending to WiseDiag, and use an offline OCR tool for sensitive personal, financial, medical, credential, or minor-related documents.

Risk: The output-name handling can write Markdown outside the stated output folder when the --name value contains slashes, absolute paths, or '..'.

Mitigation: Use simple filename stems for --name and avoid slashes, absolute paths, and '..' until the filename handling is fixed.

Risk: Weak API-key storage guidance can lead users to keep WiseDiag credentials in shell startup files.

Mitigation: Set the API key only for the current session or use a secret manager instead of storing it directly in shell startup files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wisediag/skills/wisediag-medocr)
- [WiseDiag API key management](https://console.wisediag.com/apiKeyManage)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown file plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one PDF or image at a time; default output path is ~/.openclaw/workspace/WiseOCR/{name}.md.]

## Skill Version(s):

1.0.26 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
