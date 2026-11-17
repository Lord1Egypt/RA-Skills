## Description:

Recognizes images, screenshots, scanned documents, and PDFs using configured OCR and multimodal services, then outputs Markdown results with optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxusong637](https://clawhub.ai/user/zhangxusong637)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to extract OCR text from images and PDFs, preserve document structure as Markdown, and optionally send the result to a Feishu conversation when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents may be sent to configured OCR or multimodal providers.

Mitigation: Install only when those providers are trusted, and keep sensitive workflows on local output or explicitly disabled sending paths.

Risk: Remote attachment input and OpenClaw session recovery can expose documents or credentials in permissive integrations.

Mitigation: Keep remote input and session recovery disabled unless needed, use an allowlist for remote downloads, validate redirects and DNS, and protect configuration secrets with owner-only permissions.

Risk: Local file path handling can process unintended files if exposed in shared or untrusted chat integrations.

Mitigation: Restrict accepted paths to trusted upload directories and review the integration boundary before enabling shared chat use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangxusong637/skills/vision-ocr)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown text and local Markdown result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally send result files to Feishu when explicit session and sending options are provided.]

## Skill Version(s):

1.1.2 (source: server release metadata, package.json, skill.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
