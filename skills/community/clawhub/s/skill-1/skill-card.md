## Description: <br>
Generate QR codes from text, URLs, WiFi credentials, vCards, or any data for PNG, SVG, or ASCII output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to generate scannable QR codes for links, text, WiFi access, vCards, and other data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script can create local output files. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or deploying them. <br>
Risk: The script may automatically install the qrcode[pil] Python dependency if it is missing. <br>
Mitigation: In stricter environments, preinstall and pin the dependency before using the skill. <br>
Risk: WiFi QR codes can encode network passwords. <br>
Mitigation: Treat generated WiFi QR codes as secrets and share them only with intended recipients. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated PNG, SVG, or ASCII QR output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local files at user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
