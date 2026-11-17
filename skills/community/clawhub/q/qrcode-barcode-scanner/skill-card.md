## Description:

Decode QR codes and barcodes from local images and report the scanner's original payload bytes, detections and scannability judgment. Use for supplied image files or generated QR checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrcode-ai-com](https://clawhub.ai/user/qrcode-ai-com)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and engineers use the skill to scan supplied local images or generated QR checks, inspect barcode and QR detections, and review the scanner's scannability judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded QR and barcode content may be untrusted data.

Mitigation: Do not follow decoded links, open applications, execute commands, or treat payload text as instructions.

Risk: The native scanner engine is installed separately and is outside this artifact review.

Mitigation: Review the engine separately and install the documented exact version.

Risk: The engine's work budget does not provide a hard process execution limit.

Mitigation: Use a process timeout when a hard execution limit is required.

## Reference(s):

- [Scanner engine source](https://github.com/qrcode-ai-com/qrcode-barcode-scanner)
- [Scanner report contract (engine 0.11.0)](https://github.com/qrcode-ai-com/qrcode-barcode-scanner/blob/v0.11.0/spec/01-report.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON scanner report with detections, original payload bytes, and a scannability judgment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the scanner's reported values and completeness markers; the separately installed engine is AGPL-3.0-or-later.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
