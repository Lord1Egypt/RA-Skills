## Description:

Extracts text from one or more uploaded images and organizes the results by image in a structured Markdown document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asiangiantduck](https://clawhub.ai/user/asiangiantduck)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert batches of screenshots, document images, or presentation images into editable Markdown while preserving image order and text structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images may contain sensitive text that will be inspected and extracted in the current session.

Mitigation: Avoid uploading sensitive images unless the user is comfortable having their text extracted in-session.

Risk: OCR output can be incomplete or incorrect when images are blurry, poorly lit, or otherwise hard to read.

Mitigation: Review extracted text before reuse and flag low-quality images or uncertain recognition results in the Markdown output.

## Reference(s):

- [Output Document Format Specification](references/output-format.md)
- [ClawHub Skill Page](https://clawhub.ai/asiangiantduck/skills/test20260402)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown document segmented by image, with optional .md file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves upload order and marks images with no text or OCR failures when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
