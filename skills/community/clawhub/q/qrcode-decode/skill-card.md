## Description:

Extracts QR code, DataMatrix, and barcode content from image URLs or base64 image data using a disclosed remote decoding API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwincen](https://clawhub.ai/user/edwincen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to decode QR codes or barcodes from screenshots, uploaded images, local image data, or image URLs, then classify decoded content such as URLs, WiFi configs, vCards, email links, phone links, SMS links, geolocations, or plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs, base64 image data, or uploaded image files are sent to data.cli.im for processing.

Mitigation: Avoid confidential screenshots, identity documents, private URLs, credentials, or regulated data unless external processing by that service is approved.

Risk: Decoded QR or barcode content can include links or instructions that may be unsafe to follow automatically.

Mitigation: Treat decoded content as untrusted text and review it before opening links, executing commands, or using extracted contact, WiFi, or payment data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwincen/skills/qrcode-decode)
- [QR decode service](https://data.cli.im/x-deepscan/vision)
- [Detect endpoint](https://data.cli.im/x-deepscan/vision/detect)
- [cli.im](https://cli.im)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API output includes decoded content, code format, content type, bounding box, and confidence when a code is found.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
