## Description: <br>
QR code generation and reading for text, URLs, WiFi credentials, vCard contacts, image decoding, and batch generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yushimohuang](https://clawhub.ai/user/yushimohuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to ask an agent to create QR code images, decode QR codes from image files, or prepare QR codes for WiFi and contact sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR images and decoded terminal output can expose sensitive content such as WiFi passwords, contact details, tokens, or private URLs. <br>
Mitigation: Use guest or temporary credentials when sharing WiFi QR codes, avoid encoding secrets unless necessary, and delete or protect generated QR images that contain private data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Markdown with bash commands and generated PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local qrencode and zbar-tools utilities when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
