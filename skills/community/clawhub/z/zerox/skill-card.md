## Description:

Convert documents (PDF, DOCX, PPTX, images, etc.) to Markdown using the zerox library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otacu](https://clawhub.ai/user/otacu)

### License/Terms of Use:


## Use Case:

Developers and document-processing users use this skill to convert PDFs, DOCX, PPTX, and image files into Markdown, including scanned documents that require OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are sent through a third-party API path for conversion.

Mitigation: Use the skill only with documents approved for remote AI processing through the configured API provider and intermediary.

Risk: The converter can fall back to reading a shared credential file.

Mitigation: Prefer an explicitly supplied APIYI_API_KEY environment variable and review local credential storage before installation.

Risk: Background conversion on macOS can trigger unintended commands from crafted filenames.

Mitigation: Avoid background conversion for untrusted filenames and review or sanitize filenames before running the background script.

Risk: The zerox dependency is not pinned to an exact version.

Mitigation: Pin or audit the zerox dependency before using this skill with sensitive documents.

## Reference(s):

- [Zerox project homepage](https://github.com/getomni-ai/zerox)
- [ClawHub Zerox skill page](https://clawhub.ai/otacu/skills/zerox)
- [APIYI API endpoint](https://api.apiyi.com/v1)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown files or Markdown text with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and APIYI_API_KEY; background conversion writes progress logs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
