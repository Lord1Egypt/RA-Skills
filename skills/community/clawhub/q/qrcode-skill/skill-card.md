## Description: <br>
Generates QR code PNG images from text or URLs and decodes QR code images through a remote MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marc-chen](https://clawhub.ai/user/marc-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create scannable QR codes or extract text from QR images without implementing QR parsing directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR text and QR images are sent to a remote MCP service. <br>
Mitigation: Avoid using the skill with secrets, private tickets, internal URLs, or real Wi-Fi credentials unless the service's data handling is trusted. <br>


## Reference(s): <br>
- [MCP API Reference](artifact/references/mcp-api.md) <br>
- [Qrcode Skill on ClawHub](https://clawhub.ai/marc-chen/qrcode-skill) <br>
- [QR Code MCP Server](https://qrcode.api4claw.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown responses with base64 PNG image embeds, optional PNG files, and decoded text strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [QR generation limits text to 1000 characters and image size to 128-1024 pixels; QR text and images are processed by a remote MCP service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
