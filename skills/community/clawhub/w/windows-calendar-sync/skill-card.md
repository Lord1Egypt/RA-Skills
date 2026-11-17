## Description:

将提醒同步到 Windows / Outlook 日历，支持通过 Microsoft Graph API 设备代码流认证并写入用户 Outlook 日历。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonsyung-ctrl](https://clawhub.ai/user/jasonsyung-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, list, search, and delete reminders or schedule items in a Microsoft Outlook calendar from natural-language calendar requests. It is intended for Windows/Outlook calendar synchronization after the user completes Microsoft OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived Microsoft calendar tokens are stored in plaintext in token_store.json.

Mitigation: Use the skill only on trusted, non-shared machines; remove token_store.json and revoke the Microsoft app grant when the skill is no longer needed.

Risk: The skill requests Calendars.ReadWrite and offline_access permissions for a Microsoft app.

Mitigation: Verify the Azure tenant and client ID before authenticating, and grant access only if calendar read/write and refresh-token access are acceptable.

Risk: Calendar events can be deleted without an additional confirmation step.

Mitigation: List or search events first, confirm the event ID, and avoid automated deletion flows unless the target event is unambiguous.

Risk: Calendar times may be wrong if the assumed timezone does not match the user expectation.

Mitigation: Confirm the intended timezone and ISO 8601 start time before creating or modifying events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonsyung-ctrl/skills/windows-calendar-sync)
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0)
- [Microsoft device login](https://microsoft.com/devicelogin)
- [Azure app registrations](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown with PowerShell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, list, search, or delete Microsoft Outlook calendar events through Microsoft Graph after OAuth authorization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
