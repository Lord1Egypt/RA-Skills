## Description:

Safe Shrink helps agents guide users through offline document compression, sanitization, OCR, and conversion to the .ssd enhanced Markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwatech](https://clawhub.ai/user/jinwatech)

### License/Terms of Use:

MIT-0 (skill package)

## Use Case:

Developers and end users use Safe Shrink to prepare Office, PDF, image, text, code, and structured files for sharing or AI workflows by shrinking documents, masking sensitive data, extracting OCR text, and producing .ssd or Markdown-style outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release as suspicious because it directs broad file handling into an unverified downloaded Windows executable.

Mitigation: Only run the executable on specific documents after independently verifying the release artifact, and test it in an isolated environment before processing sensitive files.

Risk: The artifact recommends broad antivirus exclusions for the SafeShrink folder.

Mitigation: Do not add broad antivirus exclusions; follow endpoint security policy and investigate any antivirus detection before use.

Risk: The skill processes sensitive documents and claims sanitization, but missed or incorrect masking could expose data.

Mitigation: Review sanitized outputs before sharing externally and avoid processing highly sensitive files unless the release artifact and results have been verified.

## Reference(s):

- [Safe Shrink ClawHub page](https://clawhub.ai/jinwatech/skills/safe-shrink)
- [SafeShrink GitHub repository](https://github.com/JinwaTech/safeshrink)
- [SafeShrink releases](https://github.com/JinwaTech/safeshrink/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI command examples and local document output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .ssd, text, Markdown, compressed document, sanitized document, image, or batch output files through a local Windows executable.]

## Skill Version(s):

1.2.15 (source: evidence.release.version and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
