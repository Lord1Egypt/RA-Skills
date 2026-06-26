## Description: <br>
Generate QR codes from URLs or text. Export as PNG with customizable size. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate QR codes for URLs or text with configurable size, margin, and image format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR payload text is sent to api.qrserver.com, which can expose private URLs, credentials, or other sensitive content to a third-party service. <br>
Mitigation: Use the skill only for non-sensitive QR contents, and choose an offline QR generator when encoding passwords, private keys, internal links, recovery URLs, or Wi-Fi credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/qrcode-tool) <br>
- [freedompixels publisher profile](https://clawhub.ai/user/freedompixels) <br>
- [qrserver.com API](https://api.qrserver.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Command-line text or JSON containing a QR image data URL and generation metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses api.qrserver.com to generate QR image data; users should avoid sensitive payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
