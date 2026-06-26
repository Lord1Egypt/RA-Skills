## Description: <br>
Creates customizable QR codes for URLs, text, WiFi credentials, contact cards, email, phone, SMS, locations, calendar events, and custom data, with batch generation and multiple export formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anisafifi](https://clawhub.ai/user/anisafifi) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
External users and developers use this skill to create QR code files or terminal QR output for links, credentials, contact details, messages, locations, events, and bulk input lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated QR codes and terminal output expose the encoded data, including WiFi passwords, contact details, or private messages. <br>
Mitigation: Encode only information intended for sharing, control distribution of generated files, and avoid long-lived secrets or sensitive personal data unless sharing is deliberate. <br>
Risk: The encoded content may appear in terminal or agent logs during generation. <br>
Mitigation: Avoid entering private content in shared sessions and restrict or clear logs when sensitive data is handled. <br>
Risk: Image-processing dependencies may become outdated. <br>
Mitigation: Install in a virtual environment and keep qrcode, segno, and Pillow updated. <br>


## Reference(s): <br>
- [QR Code Generator Reference](references/readme.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anisafifi/qr-code-generator) <br>
- [OpenClawCLI](https://clawhub.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated QR outputs such as PNG, SVG, PDF, EPS, or terminal ASCII.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local QR code files and batch output directories.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
