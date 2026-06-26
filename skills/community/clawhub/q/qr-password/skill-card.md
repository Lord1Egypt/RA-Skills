## Description: <br>
Transfers credentials between networked and air-gapped devices using QR codes as an optical channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifehackjohn](https://clawhub.ai/user/lifehackjohn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and external users use this skill to generate credential QR codes for air-gapped transfer and decode credential QR codes from images without using a network channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated QR code is equivalent to the credential it encodes and can be copied, photographed, or synced unintentionally. <br>
Mitigation: Use generated QR codes only in private settings, trust the receiving device, avoid screenshots and cloud-synced folders, and delete generated image files immediately after transfer. <br>
Risk: Decoded credentials can be exposed if they are echoed into chat, logs, or files. <br>
Mitigation: Redact passwords in conversation output, avoid storing decoded credentials, and clear browser forms or displayed QR content after use. <br>


## Reference(s): <br>
- [QR Password README](artifact/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lifehackjohn/qr-password) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON credential payloads, and temporary QR image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Credential values should be redacted from conversation output; generated QR images and camera images are intended to be deleted immediately after use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
