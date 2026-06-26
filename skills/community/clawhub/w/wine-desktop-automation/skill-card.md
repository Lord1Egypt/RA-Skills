## Description: <br>
Controls desktop applications with mouse and keyboard automation. Invoke when user needs to automate GUI operations, control desktop software, or perform UI testing on Ubuntu+Wine environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaodu](https://clawhub.ai/user/xiaodu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to automate GUI workflows, UI testing, Wine-hosted Windows applications, and repetitive desktop tasks on Ubuntu systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local desktop automation can click controls, type text, switch windows, launch executables, capture screenshots, and manage Wine processes in the active user session. <br>
Mitigation: Use it only for precise user-controlled tasks, keep sensitive windows closed, avoid typing secrets, and require explicit human approval before launching unknown executables, saving screenshots, killing windows or processes, or changing Wine prefixes. <br>
Risk: Window and image matching can target the wrong application or UI element if titles, coordinates, templates, screen resolution, or DPI settings differ. <br>
Mitigation: Prefer exact window titles or process names, constrain image searches to known regions, add UI-response delays, and verify behavior on the target screen configuration before unattended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaodu/wine-desktop-automation) <br>
- [Publisher profile](https://clawhub.ai/user/xiaodu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe or invoke local desktop actions such as mouse and keyboard input, window management, Wine process control, and screenshots when explicitly used by an agent workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
