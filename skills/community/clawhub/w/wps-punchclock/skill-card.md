## Description:

Automate punching time in/out on WPS Time / NetTime (wpstime.com NetTime).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxh141130](https://clawhub.ai/user/dxh141130)

### License/Terms of Use:


## Use Case:

Employees who use WPS Time / NetTime use this skill to set up local credentials, check status, and clock in or out through an agent-assisted browser flow. The skill also supports starting and ending breaks or lunch and returning a concise confirmation with a screenshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs payroll-related punch actions such as clocking in or out and starting or ending breaks or lunch.

Mitigation: Require explicit user confirmation before any punch action and verify the resulting status after execution.

Risk: WPS Time credentials are sensitive and the skill includes a chat-based credential setup path.

Mitigation: Use the local terminal setup so credentials are stored in macOS Keychain and do not enter chat history or gateway logs.

Risk: The login flow currently targets an HTTP URL for credential submission.

Mitigation: Install only after the login flow is changed to HTTPS with origin validation, or restrict use to an environment where that risk has been formally accepted.

Risk: Screenshots of the timeclock page may include employee time or payroll-related information.

Mitigation: Share screenshots only with authorized recipients and store them in an approved local output directory.

Risk: Unattended browser automation can fail if the site adds CAPTCHA, 2FA, layout changes, or if the Mac is asleep or offline.

Mitigation: Treat failed script output as authoritative, do not claim success on errors, and fall back to manual punch-clock use when automation breaks.

## Reference(s):

- [Punchclock Runbook](references/PUNCHCLOCK_RUNBOOK.md)
- [ClawHub Skill Page](https://clawhub.ai/dxh141130/skills/wps-punchclock)
- [WPS Time / NetTime Login](http://www.wpstime.com/NetTime/Login.asp)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions]

**Output Format:** [Brief text confirmation with optional screenshot attachment; setup guidance uses Markdown with shell commands, and the punch script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screenshots under the configured output directory and should not echo stored credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
