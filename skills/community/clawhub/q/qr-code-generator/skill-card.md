## Description:

Generates customizable QR codes for URLs, text, WiFi credentials, vCards, email, phone, SMS, location coordinates, calendar events, and custom data, with batch generation and multiple export formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anisafifi](https://clawhub.ai/user/anisafifi)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and operators use this skill to generate individual or batch QR codes for links, credentials, contact cards, events, product information, and similar scannable data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR codes may contain sensitive WiFi passwords or personal data, and this version may print encoded data to stderr.

Mitigation: Avoid using secrets in shared terminals, CI logs, or agent logs, and treat generated QR codes containing credentials or personal data as sensitive artifacts.

Risk: Batch CSV or JSON inputs can write outside the chosen output folder.

Mitigation: Process only trusted batch files and choose an output directory that is acceptable for the skill to write into.

Risk: Installing Python packages into the system environment can affect the local Python installation.

Mitigation: Install dependencies in a virtual environment before running the skill.

## Reference(s):

- [QR Code Generator reference](references/readme.md)
- [ClawHub skill page](https://clawhub.ai/anisafifi/skills/qr-code-generator)
- [qrcode Python package](https://pypi.org/project/qrcode/)
- [segno Python package](https://pypi.org/project/segno/)
- [Pillow documentation](https://python-pillow.org/)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated QR image or document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate PNG, SVG, PDF, EPS, or terminal ASCII output; batch mode can process text, CSV, or JSON inputs.]

## Skill Version(s):

0.1.0 (source: release evidence and reference readme)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
