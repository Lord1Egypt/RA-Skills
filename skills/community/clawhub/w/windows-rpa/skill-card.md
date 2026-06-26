## Description: <br>
Windows RPA lets an agent control a Windows desktop with mouse, keyboard, screenshot, window management, application launch, clipboard, and shell-command tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qgyz9613](https://clawhub.ai/user/qgyz9613) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to operate Windows desktop applications, manage windows, launch programs, capture screenshots, use the clipboard, and run local commands from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Windows desktop access and local command-line control under the user's account. <br>
Mitigation: Enable approval for shell, application launch, clipboard-read, screenshot, and full-state actions, and review each proposed command before execution. <br>
Risk: Screenshots, clipboard reads, and full desktop state capture may expose passwords, tokens, private documents, or sensitive business applications. <br>
Mitigation: Use the skill only when sensitive windows are closed or hidden, clear sensitive clipboard contents first, and limit screenshot regions when possible. <br>
Risk: Mouse, keyboard, and window actions can affect the wrong application if focus, resolution, or coordinates differ from the expected state. <br>
Mitigation: Verify the active window and screen state before actions, prefer window activation or image matching over fixed coordinates, and test workflows in an isolated environment first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qgyz9613/windows-rpa) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Security policy](artifact/SECURITY.md) <br>
- [Skill configuration](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [JSON status responses, command text, and screenshot image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only; requires Python and pyautogui or pywinauto. Sensitive actions include shell execution, clipboard reads, screenshots, and full desktop state capture.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
