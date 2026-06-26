## Description: <br>
Native Windows mouse control (move, click, drag) via user32.dll. Use when the user asks you to move the mouse, click, drag, or automate pointer actions on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lurklight](https://clawhub.ai/user/lurklight) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users on Windows use this skill to move the pointer, click mouse buttons, and perform simple drag-style actions through local command execution. It is intended for explicit, supervised desktop automation where coordinates or deltas are provided by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, click, hold, and release mouse buttons on the user's Windows desktop. <br>
Mitigation: Use explicit coordinates or verified targets, start with small reversible actions, and supervise clicks or drags on payment pages, permission prompts, account settings, or other sensitive screens. <br>
Risk: The bundle requires saving text files as executable .cmd and PowerShell scripts before use. <br>
Mitigation: Review the .cmd and .ps1 text before saving them as executable scripts, and install only when local Windows mouse automation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lurklight/win-mouse-native) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with command examples; the local script returns one-line JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only mouse control through local .cmd and PowerShell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
