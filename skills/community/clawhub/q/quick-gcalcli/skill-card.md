## Description: <br>
Google Calendar via gcalcli: today-only agenda by default, bounded meaning-first lookup via agenda scans, and fast create/delete with verification--optimized for low tool calls and minimal output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onsra520](https://clawhub.ai/user/onsra520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-assistant agents use this skill to read, search, create, and delete Google Calendar events through a locally configured gcalcli installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Google Calendar events through the user's local gcalcli OAuth access. <br>
Mitigation: Install it only for calendars where agent access is acceptable, and revoke gcalcli OAuth access when the skill is no longer needed. <br>
Risk: Unambiguous delete or edit requests may be executed without an extra confirmation step. <br>
Mitigation: Edit the action policy to require confirmation for all destructive actions when calendars contain sensitive or high-impact events. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onsra520/quick-gcalcli) <br>
- [gcalcli project](https://github.com/insanum/gcalcli) <br>
- [Google Calendar API](https://www.googleapis.com/calendar/) <br>
- [Google OAuth2 token endpoint](https://oauth2.googleapis.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise natural-language responses with optional inline shell commands when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local gcalcli OAuth access and favors bounded agenda scans, confirmation on ambiguous actions, and post-delete verification.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
