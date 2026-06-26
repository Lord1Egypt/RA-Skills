## Description: <br>
将提醒同步到 Windows / Outlook 日历，支持 Microsoft Graph API 设备代码流认证，并可创建、查询、搜索和删除用户 Outlook 日历事件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonsyung-ctrl](https://clawhub.ai/user/jasonsyung-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn reminder or scheduling requests into Microsoft Outlook calendar events, then list, search, or delete those events through command-line scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-lived Microsoft calendar credentials locally in token_store.json. <br>
Mitigation: Protect access to the skill directory, delete token_store.json when it is no longer needed, and reauthenticate only when necessary. <br>
Risk: The skill can read, create, and delete Microsoft Outlook calendar events through Calendars.ReadWrite access. <br>
Mitigation: Install only when this access is acceptable, verify the tenant and client ID setup, and require explicit confirmation before deletes or recurring events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonsyung-ctrl/windows-calendar-sync) <br>
- [Publisher profile](https://clawhub.ai/user/jasonsyung-ctrl) <br>
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0) <br>
- [Microsoft device login](https://microsoft.com/devicelogin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, list, search, and delete Outlook calendar events after Microsoft OAuth authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
