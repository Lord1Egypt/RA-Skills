## Description: <br>
Generate and read QR codes from text, URLs, screenshots, or image files, with support for PNG/JPG inputs and generated image outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Omar-Khaleel](https://clawhub.ai/user/Omar-Khaleel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, automation users, and external ClawHub users can generate QR code image files from text or URLs and decode QR code contents from local image files or screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decoded QR content may contain unsafe or misleading URLs or text. <br>
Mitigation: Treat decoded values as untrusted and inspect them before opening links, executing commands, or sharing the content. <br>
Risk: Dependency installation may introduce supply-chain exposure. <br>
Mitigation: Install qrcode, Pillow, pyzbar, and zbar dependencies from trusted sources, preferably inside a virtual environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Omar-Khaleel/qr-code-intelligence) <br>
- [Publisher profile](https://clawhub.ai/user/Omar-Khaleel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; generated QR image files; decoded text or JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated QR codes are saved to a user-selected output path; decoded QR results may include bounding-box metadata when JSON output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
