## Description: <br>
Automate GUI tests on KylinOS V11 Wayland desktops using wlcctrl for window discovery, scale-aware pointer actions, screenshots, window placement, and result verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyanogenic](https://clawhub.ai/user/cyanogenic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate and verify GUI workflows on KylinOS V11 Desktop, UKUI, and wlcom Wayland environments. It helps agents discover windows and outputs, convert screenshot coordinates into scaled pointer actions, move or resize windows, capture screenshots, and log reproducible wlcctrl commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GUI automation can click, type, move windows, or capture screenshots in the wrong desktop context if the target window or coordinates are not verified. <br>
Mitigation: Use the skill in a controlled test desktop, confirm the target window UUID and coordinates before interaction, and verify results with screenshots or window state. <br>
Risk: Screenshots and logs may contain sensitive information from the desktop under test. <br>
Mitigation: Avoid capturing sensitive screens and store test screenshots and logs only in approved project artifact locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyanogenic/wlcom-gui-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and helper script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshot and log file paths when guiding GUI test workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
