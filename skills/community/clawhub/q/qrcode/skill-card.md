## Description:

Generate styled QR codes as SVG, PNG, or JPG files from user input with configurable colors, shapes, output formats, and error correction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexavi8](https://clawhub.ai/user/hexavi8)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and external users use QRCode to generate styled QR codes for URLs, contact data, WiFi credentials, print assets, and digital sharing. The skill helps an agent create the QR file, report its path and format, and display the result when possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-output controls are incorrectly scoped and can write outside the intended workspace.

Mitigation: Deploy only after confirming output paths are constrained to a real user-approved workspace or dedicated output directory.

Risk: Large QR image settings can increase resource use.

Mitigation: Use conservative size and scale limits for production deployments and review generated image dimensions before execution.

Risk: Generated QR codes can expose sensitive data such as WiFi passwords, contact details, or payment information.

Mitigation: Warn users to include sensitive content only when they intend that data to be shared through the QR code.

Risk: Dependencies are not pinned by a lockfile in the artifact evidence.

Mitigation: Install with a reviewed lockfile or equivalent dependency pinning before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexavi8/skills/qrcode)
- [Sharp installation guide](https://sharp.pixelplumbing.com/install)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [SVG, PNG, or JPG files with Markdown display guidance and command-line invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated filenames and image properties depend on user-selected text, format, size, styling, error correction, and quality options.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
