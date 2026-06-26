## Description: <br>
Generate QR code for Wi-Fi credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate a QR code for Wi-Fi credentials so a phone can join a network without manually typing the password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated QR code and any command-line password reveal Wi-Fi credentials to anyone who can see them. <br>
Mitigation: Treat the QR code and password as sensitive, share them only with intended users, and avoid exposing them in logs, screenshots, or public terminals. <br>
Risk: The skill depends on the local qrencode command. <br>
Mitigation: Install qrencode from a trusted package manager and confirm the wifi-qr command behavior on the target system before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local qrencode binary; generated QR content encodes supplied Wi-Fi credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
