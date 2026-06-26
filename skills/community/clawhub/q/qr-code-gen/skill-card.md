## Description: <br>
Generate QR codes for text, URLs, WiFi connections, and business cards (vCard), with optional custom output paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouyangAbel](https://clawhub.ai/user/ouyangAbel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users use this skill to generate local PNG QR codes for URLs, arbitrary text, WiFi credentials, and vCard contact details without making API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WiFi QR codes can expose network credentials to anyone who can scan or access the generated image. <br>
Mitigation: Generate and share WiFi QR codes only when the network password is intended to be shared with the recipient. <br>
Risk: The utility writes PNG files to user-provided output paths. <br>
Mitigation: Save generated QR codes only in ordinary user-controlled folders and verify the destination path before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ouyangAbel/qr-code-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated QR artifacts are PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local qrcode Python package with Pillow support or the system python3-qrcode package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
