## Description:

Qr Code Toolkit helps agents generate, decode, style, and batch-process QR codes and common barcode formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create QR and barcode images for URLs, WiFi credentials, vCards, and retail or industrial barcode formats, then decode or batch-process QR and barcode images from local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch generation can write files outside the intended output directory when CSV or JSON input supplies unsafe filenames.

Mitigation: Use a dedicated working directory, avoid untrusted batch input files, and review or sanitize filenames before running batch generation.

Risk: Terminal logs may expose encoded QR payload data, including sensitive WiFi credential strings.

Mitigation: Avoid generating secret payloads in shared terminals, redact logs before sharing, and modify logging before sensitive use.

Risk: Dependency versions are lower-bounded rather than pinned exactly.

Mitigation: Pin and review dependencies before using the skill in CI, production, or sensitive environments.

## Reference(s):

- [QR Code Standards](references/qr-standards.md)
- [Barcode Types Reference](references/barcode-types.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python CLI commands; generated artifacts are PNG images or JSON decode results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write PNG image files and JSON batch decode outputs to user-selected paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
