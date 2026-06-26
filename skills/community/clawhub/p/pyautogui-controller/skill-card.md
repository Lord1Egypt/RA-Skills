## Description: <br>
Advanced Windows desktop/browser automation via a local Python controller project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzj520lyx](https://clawhub.ai/user/hzj520lyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when direct Windows desktop or screen-based browser control is required for local UI workflows such as screenshots, opening apps, navigation, clicking, typing, and short multi-step automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control the local Windows desktop and browser, including launching programs, clicking, typing, and interacting with live sessions. <br>
Mitigation: Run it only in a trusted test environment or separate browser profile, and avoid using it while sensitive apps, accounts, or documents are open. <br>
Risk: Runtime screenshots, browser state, and failure logs may persist local activity details. <br>
Mitigation: Periodically clear runtime screenshots, failure logs, and browser profile or state directories after use. <br>
Risk: Custom DOM bridge or CDP environment variables can route browser automation through a user-specified command or endpoint. <br>
Mitigation: Do not set custom bridge or CDP environment variables unless the command and endpoint are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzj520lyx/pyautogui-controller) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Controller runs return JSON with success, results, runtime, and warnings fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
