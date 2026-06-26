## Description: <br>
QR code generator for text, URLs, WiFi, vCards, and other data, with support for custom colors, sizes, logos, and PNG or SVG output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate local QR code assets for common payloads such as links, WiFi credentials, contact cards, email, SMS, phone numbers, and geographic coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR codes can expose encoded sensitive data such as WiFi passwords, private URLs, or contact details to anyone who scans them. <br>
Mitigation: Review QR payloads before generation and treat generated QR images as shareable copies of the encoded data. <br>
Risk: Generated files may be written to unintended locations if output paths are chosen carelessly. <br>
Mitigation: Choose output paths intentionally and prefer the current workspace or another trusted local directory. <br>
Risk: The skill depends on Python packages for QR code and image generation. <br>
Mitigation: Install dependencies from a trusted Python package source before executing generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/qr-code-maker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples that generate local QR image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local PNG, SVG, or PDF QR code files when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
