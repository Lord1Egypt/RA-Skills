## Description: <br>
QR Generator helps agents generate QR codes with custom colors or logos, batch-create QR codes, work with dynamic QR codes, and decode QR codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to generate QR assets for website links, WiFi credentials, contact details, payment codes, and event registration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented installer uses npx with the latest ClawHub package and the artifact declares a curl prerequisite. <br>
Mitigation: Review the package and command source before installation, and install only in environments where the npx latest-based installer and curl dependency are acceptable. <br>
Risk: QR codes can encode sensitive information such as WiFi passwords, payment details, or private contact data. <br>
Mitigation: Encode sensitive data only when the resulting QR code is intended to share that information with its viewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/xiaoming-qr-generator) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated QR image or document file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce PNG, SVG, and PDF QR outputs when the described QR tooling is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
