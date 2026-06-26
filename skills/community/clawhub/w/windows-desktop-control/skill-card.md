## Description: <br>
Windows 桌面控制工具 (仅Windows) - 截屏、窗口管理、鼠标键盘控制、进程管理、系统信息。当用户要求截屏、查看进程、关闭程序、桌面控制时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tr0812](https://clawhub.ai/user/tr0812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they intentionally need an agent to inspect and control a Windows desktop, including screenshots, process lists, mouse and keyboard actions, clipboard access, and system information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local control over a Windows desktop, including screenshots, mouse and keyboard actions, clipboard access, and process termination. <br>
Mitigation: Install only when desktop control is intended, and review click, type, hotkey, clipboard, and kill actions before they run. <br>
Risk: Screenshots and clipboard reads may expose sensitive local information. <br>
Mitigation: Use the skill only in contexts where screen and clipboard contents are approved for agent access. <br>
Risk: The security guidance flags unsafe clipboard and process-kill behavior. <br>
Mitigation: Avoid clipboard set with untrusted text until PowerShell command construction is fixed, and keep process termination limited to reviewed targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tr0812/windows-desktop-control) <br>
- [Publisher profile](https://clawhub.ai/user/tr0812) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the Python tool returns JSON and can write screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only; requires python, powershell, pyautogui, mss, and pillow] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
