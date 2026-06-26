## Description: <br>
Use when you need to extract QR code or barcode content from an image, screenshot, photo URL, or local image file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwincen](https://clawhub.ai/user/edwincen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send an image URL or base64 image to the QR/barcode detection service and receive decoded content, content classification, location, and confidence data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, screenshots, or image URLs may contain sensitive QR/barcode content and are sent to an external service for processing. <br>
Mitigation: Avoid passwords, private keys, login QR codes, personal documents, proprietary screenshots, internal URLs, and other sensitive content unless the provider and data handling are acceptable for the use case. <br>
Risk: Decoded content may be a URL, WiFi configuration, contact card, email, phone number, SMS command, geolocation, or other user-provided text. <br>
Mitigation: Review decoded values before opening links, executing commands, importing contacts, joining networks, or using the content in downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwincen/qrcode-decode) <br>
- [Publisher profile](https://clawhub.ai/user/edwincen) <br>
- [QR decode service](https://data.cli.im/x-deepscan/vision) <br>
- [Detection API endpoint](https://data.cli.im/x-deepscan/vision/detect) <br>
- [cli.im](https://cli.im) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decoded QR or barcode content may include content type, bounding box, and confidence values.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
