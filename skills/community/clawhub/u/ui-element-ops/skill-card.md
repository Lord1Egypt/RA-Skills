## Description: <br>
Parse UI screenshots into structured element JSON (type, OCR text, bbox) and operate desktop UI from parsed elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murongg](https://clawhub.ai/user/murongg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to parse screenshots into UI element data, find or wait for elements, and perform desktop actions such as clicks, typing, key presses, screenshots, and coordinate calibration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect screenshots and control the desktop, so unintended clicks, typed text, hotkeys, or screenshots could affect sensitive workflows. <br>
Mitigation: Install and use it only when desktop inspection and control are intended; avoid sensitive screens and workflows where accidental UI actions or screenshots would be harmful. <br>
Risk: The security summary flags an overbroad shell-command hook around wait refresh behavior. <br>
Mitigation: Avoid wait refresh commands unless the exact command is fully controlled and reviewed. <br>
Risk: The skill installs and uses external PyPI, GitHub, and Hugging Face dependencies. <br>
Mitigation: Review external dependencies and keep PyAutoGUI failsafe enabled before allowing UI operation. <br>
Risk: Parsing and capture-and-parse commands are compute-heavy and can be slow, especially on CPU-only machines. <br>
Mitigation: Avoid tight parsing loops and reuse recent elements JSON outputs when they are still valid. <br>


## Reference(s): <br>
- [UI Element Ops ClawHub Release](https://clawhub.ai/murongg/ui-element-ops) <br>
- [Microsoft OmniParser](https://github.com/microsoft/OmniParser) <br>
- [Type Rules Example](references/type_rules.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON element files, overlay PNG files, and optional desktop action results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create elements JSON, overlay images, screenshots, and coordinate calibration profiles.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
