## Description:

Generates QR codes from text or URLs and decodes QR codes from image files, including PNG, JPG, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omar-khaleel](https://clawhub.ai/user/omar-khaleel)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create QR code image files from text or URLs and decode QR code contents from existing images or screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and platform setup can affect QR decoding availability.

Mitigation: Install dependencies in a virtual environment, pin package versions when reproducibility is required, and install the platform zbar dependency before decoding QR codes.

Risk: Documented command paths may not match the packaged file layout.

Mitigation: Adjust script paths to the actual packaged file locations before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omar-khaleel/skills/qr-code-intelligence)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets; generated QR artifacts are PNG files, and decoded QR output can be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python packages qrcode, pillow, and pyzbar; QR decoding also requires the platform zbar dependency.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
