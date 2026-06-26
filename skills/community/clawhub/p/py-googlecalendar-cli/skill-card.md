## Description: <br>
Tiny Python CLI tool to manage Google Calendar events from the command line, including listing, adding, updating, and deleting events through the Calendar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwings](https://clawhub.ai/user/xwings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Google Calendar events from a local command-line workflow. It supports reading upcoming events and making calendar changes when valid Google OAuth credentials are provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change real Google Calendar data when OAuth credentials are available. <br>
Mitigation: Install only for intended calendar-management workflows, scope access to the intended calendar when possible, and review add, update, and delete commands before execution. <br>
Risk: Google OAuth client secrets and refresh tokens are sensitive credentials. <br>
Mitigation: Store credentials securely and avoid passing secrets through shared shells, logs, or command histories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwings/py-googlecalendar-cli) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls] <br>
**Output Format:** [Plain text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth credentials and network access to the Google Calendar API; mutating commands can create, update, or delete calendar events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
