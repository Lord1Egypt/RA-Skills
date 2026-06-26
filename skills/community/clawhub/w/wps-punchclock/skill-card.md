## Description: <br>
Automate punching time in/out on WPS Time / NetTime, including clock in/out, break and lunch actions, status checks, screenshot capture, and brief confirmation replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxh141130](https://clawhub.ai/user/dxh141130) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees or agents acting for a WPS Time user use this skill to clock in or out, start or end breaks and lunch, and check current WPS Time / NetTime status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use saved credentials to change payroll-relevant time records. <br>
Mitigation: Use explicit commands, require confirmation before punch actions, and verify status before or after punches to reduce accidental changes. <br>
Risk: Chat-based setup can expose a password in chat or gateway logs. <br>
Mitigation: Prefer the local terminal setup that stores credentials in macOS Keychain and never echo passwords back to the user. <br>
Risk: Screenshots may contain sensitive timekeeping or employee information. <br>
Mitigation: Avoid sharing screenshots in sensitive channels and attach them only where the user expects them. <br>
Risk: The configured WPS Time login flow may not be protected by HTTPS in every environment. <br>
Mitigation: Verify that the WPS login flow is protected by HTTPS before relying on saved credentials. <br>


## Reference(s): <br>
- [Punchclock Runbook](references/PUNCHCLOCK_RUNBOOK.md) <br>
- [WPS Time / NetTime login](http://www.wpstime.com/NetTime/Login.asp) <br>
- [ClawHub skill page](https://clawhub.ai/dxh141130/wps-punchclock) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; punch runs return JSON and screenshot file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status and punch confirmations should be brief and should not include stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
