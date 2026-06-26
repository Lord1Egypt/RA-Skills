## Description: <br>
Generate and read QR codes from text, URLs, image files, and screenshots, with PNG/JPG support and QR generation options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Omar-Khaleel](https://clawhub.ai/user/Omar-Khaleel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to create QR codes from text or URLs and decode QR-code contents from local images or screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decoded QR content can contain malicious or misleading links or text. <br>
Mitigation: Inspect decoded content before opening links, running commands, or acting on the decoded value. <br>
Risk: QR reading requires third-party image and barcode dependencies plus a platform zbar runtime. <br>
Mitigation: Install dependencies from trusted package sources and only deploy where those local dependencies are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Omar-Khaleel/qr-code-pro) <br>
- [Publisher profile](https://clawhub.ai/user/Omar-Khaleel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Code, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples; scripts produce PNG files or decoded text/JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation depends on qrcode and Pillow; reading depends on Pillow, pyzbar, and the platform zbar runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
