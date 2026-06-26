## Description: <br>
Generate QR codes from text, URLs, or data for payments, WiFi sharing, or other scannable PNG outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiaoliuo](https://clawhub.ai/user/shixiaoliuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to turn URLs, text, WiFi details, payment addresses, or other data into a local QR-code PNG file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR codes may encode WiFi passwords, payment addresses, login links, or other private data, and the generated image and console output expose that content. <br>
Mitigation: Review the encoded content before sharing the PNG or logs, and avoid generating QR codes for secrets unless the output location and terminal history are appropriate for sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shixiaoliuo/qrcode-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [PNG image file with console text containing the saved path and encoded content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes qrcode.png by default or a caller-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
