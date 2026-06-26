## Description: <br>
Automates Windows GUI interactions such as moving the cursor, clicking, typing text, sending keys, and focusing windows with PowerShell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wwb-Daniel](https://clawhub.ai/user/Wwb-Daniel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate Windows desktop applications that require GUI input, including cursor movement, clicks, text entry, special keys, and basic window focus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move the mouse, click, and send keystrokes to the live Windows desktop without being bounded to a verified target window. <br>
Mitigation: Use it only when desktop control is intended; keep sensitive apps closed or unfocused, confirm the active window with screenshots or active-window checks, and require explicit confirmation before clicks or keystrokes that could submit, delete, purchase, send, approve prompts, or change settings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Wwb-Daniel/windows-ui-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against the active Windows desktop session; actions affect whichever window currently has focus.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
