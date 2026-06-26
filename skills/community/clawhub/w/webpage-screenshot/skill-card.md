## Description: <br>
Opens a specified webpage and captures it as a PNG screenshot file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Malenconiaprincep](https://clawhub.ai/user/Malenconiaprincep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when a user needs a URL opened and saved as a visual webpage snapshot. It supports local PNG screenshot output through a project script and browser-based inspection when a file is not required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open and capture user-specified webpages, including sensitive, authenticated, internal, localhost, private-network, or file URL pages if the agent is directed to do so. <br>
Mitigation: Use it only on pages intended for capture, and avoid sensitive or private pages unless screenshotting them is explicitly intended. <br>
Risk: URLs and output paths passed to shell commands may be misinterpreted if they contain special characters or spaces. <br>
Mitigation: Quote or carefully pass URLs and output paths when invoking the screenshot command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Malenconiaprincep/webpage-screenshot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands; PNG file when the screenshot script is executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The screenshot script saves a full-page PNG, defaulting to screenshot.png with a 1280px viewport width.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
