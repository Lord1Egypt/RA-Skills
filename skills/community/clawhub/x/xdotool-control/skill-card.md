## Description: <br>
Mouse and keyboard automation using xdotool for clicking Chrome extension icons, typing into GUI apps, switching browser tabs, automating desktop UI, and running screenshot-verify-click loops without a browser relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremysommerfeld8910-cpu](https://clawhub.ai/user/jeremysommerfeld8910-cpu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to control Linux desktop windows, Chrome, mouse clicks, keyboard input, screenshots, and coordinate-based GUI workflows when browser relay access is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live-desktop and browser control. <br>
Mitigation: Use it only when that control is intended, preferably in a disposable desktop or dedicated browser profile. <br>
Risk: Coordinate-based clicks or typing may target the wrong window or sensitive page. <br>
Mitigation: Close sensitive windows and verify target windows, screenshots, and coordinates before allowing clicks or typed input. <br>
Risk: Screenshots written to /tmp may contain sensitive desktop or browser content. <br>
Mitigation: Delete temporary screenshots from /tmp after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeremysommerfeld8910-cpu/xdotool-control) <br>
- [Publisher profile](https://clawhub.ai/user/jeremysommerfeld8910-cpu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference temporary screenshot file paths created under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
