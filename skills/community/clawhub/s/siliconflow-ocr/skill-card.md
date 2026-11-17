## Description:

Helps agents extract text from local images or image URLs through SiliconFlow, with additional PDF and batch workflows described in the skill documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonrard](https://clawhub.ai/user/leonrard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe text from images for document processing. Its documentation also describes workflows for multi-page PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or image URLs are sent to an external OCR service, which may expose private or regulated content.

Mitigation: Review data-handling requirements and avoid submitting sensitive documents without approval.

Risk: The documentation and shipped script disagree on the default model, PDF and batch support, and proxy handling.

Mitigation: Test the shipped script with nonsensitive inputs and verify the required capabilities and connectivity before relying on it.

## Reference(s):

- [SiliconFlow OCR on ClawHub](https://clawhub.ai/leonrard/skills/siliconflow-ocr)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Plain text or JSON for OCR results; Markdown for usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR text can be printed or saved to a file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
