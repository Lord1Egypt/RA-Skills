## Description: <br>
Generates and decodes QR codes for URLs, vCards, WiFi credentials, and plain text, with color customization and optional logo embedding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starclimber](https://clawhub.ai/user/starclimber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to create local QR-code image files for common data formats or decode QR-code images when optional decoding dependencies are installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR codes can contain sensitive information such as WiFi credentials. <br>
Mitigation: Treat generated QR images as credentials when they encode secrets, and avoid putting real passwords directly in shell commands where possible. <br>
Risk: Decoded QR content can include untrusted links or instructions. <br>
Mitigation: Inspect decoded text before acting on it, and do not open decoded links blindly. <br>
Risk: Decode mode depends on optional packages beyond the base QR generator dependencies. <br>
Mitigation: Install and review the optional decoding dependencies, including opencv-python and pyzbar, before relying on decode mode. <br>
Risk: Oversized logos can reduce QR-code scan reliability. <br>
Mitigation: Keep logo coverage within the documented size guidance and test generated QR codes with the intended scanners. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/starclimber/skills/qrcodemaker) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, local PNG image outputs, and decoded text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated QR codes are written to local output paths; decode mode prints decoded QR content when its optional dependencies are available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
