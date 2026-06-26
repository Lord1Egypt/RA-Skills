## Description: <br>
Control Windows mouse clicks and keyboard input through PowerShell scripts for desktop automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottzhouzhou](https://clawhub.ai/user/scottzhouzhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Windows UI automation commands for mouse clicks, text entry, keyboard shortcuts, and DingTalk messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerShell commands can control the active Windows desktop and may click, type, or trigger shortcuts in the wrong application. <br>
Mitigation: Confirm the active window, screen coordinates, and intended action before execution, and test first in a non-production session. <br>
Risk: DingTalk automation may send messages from a logged-in account to an unintended recipient or with unintended content. <br>
Mitigation: Review the recipient and message text immediately before running the command, and avoid sensitive or production accounts without manual approval. <br>
Risk: The security evidence notes unavailable PowerShell scripts, so the exact installed behavior requires review. <br>
Mitigation: Inspect the installed PowerShell scripts from the local skill directory before running any command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottzhouzhou/win-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can affect the active Windows desktop session and logged-in applications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
