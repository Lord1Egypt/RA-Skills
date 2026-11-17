## Description:

QR code generation and decoding skill for creating scannable QR codes from text or URLs and extracting text from QR code images via a remote MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marc-chen](https://clawhub.ai/user/marc-chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate PNG QR codes from text or URLs and decode QR code images into their embedded text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR text or QR images are sent to the listed remote MCP service.

Mitigation: Do not use this skill for passwords, OTP setup codes, private tickets, payment data, access tokens, or confidential business data unless that transfer is acceptable.

## Reference(s):

- [MCP API Reference](references/mcp-api.md)
- [QR Code MCP Server](https://qrcode.api4claw.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown responses with base64 PNG image embeds, decoded text, optional PNG files, and MCP configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated QR input is limited to 1000 characters; QR image size is 128 to 1024 pixels with a 512 pixel default.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
