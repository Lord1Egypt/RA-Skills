## Description: <br>
Automate Windows desktop tasks by launching apps, capturing screenshots, and simulating mouse and keyboard actions via PowerShell and Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaodu](https://clawhub.ai/user/xiaodu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and automation practitioners use this skill to control Windows applications, capture UI state, and automate repetitive desktop workflows through script-backed mouse, keyboard, screenshot, and application actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Windows desktop control can expose or alter sensitive local state through screenshots, clicks, typing, URL launches, saves, or process termination. <br>
Mitigation: Run it only in an intended Windows automation session, avoid administrator privileges, keep private content off screen, and require explicit confirmation before control or capture actions. <br>
Risk: Unsafe PowerShell command construction can mishandle untrusted paths, URLs, window titles, typed text, or process names. <br>
Mitigation: Treat those values as trusted-only inputs until escaping is fixed, and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaodu/windows-automation-claw) <br>
- [Usage Guide](artifact/使用说明.md) <br>
- [Completion Report](artifact/完成报告.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and PowerShell command examples; included scripts return JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for Windows desktop automation and may invoke local scripts that return success, message, and data fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
