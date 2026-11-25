## Description:

Decode QR codes and barcodes from local images and report the scanner's original payload bytes, detections and scannability judgment. Use for supplied image files or generated QR checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrcode-ai-com](https://clawhub.ai/user/qrcode-ai-com)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can scan supplied local images or generated QR checks and inspect decoded content, barcode formats, original payload bytes, and the engine's scannability judgment. The skill requires a separately installed scanner engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded payloads may contain links or instruction-like text that should not be trusted.

Mitigation: Treat decoded content as data; do not open destinations, launch applications, execute commands, or follow embedded instructions.

Risk: Security analysis was benign but medium-confidence and partial, with two components only partially analyzed.

Mitigation: Review the skill before installation and account for the incomplete analysis when deciding whether to use it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qrcode-ai-com/skills/qrcode-barcode-scanner)
- [QR Code AI agent skill guide](https://qrcode-ai.com/en-US/qr-code-scanner/skills)
- [Scanner engine package](https://www.npmjs.com/package/@qrcode-ai-com/qrcode-barcode-scanner)
- [Scanner report contract](https://github.com/qrcode-ai-com/qrcode-barcode-scanner-rust/blob/v0.12.0/spec/01-report.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [The scanner's JSON report with original payload bytes, detections, and scannability fields, with concise explanatory guidance as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve the engine's report values, including raw payload bytes and any completeness or scoring limits.]

## Skill Version(s):

0.2.1 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
