## Description: <br>
Manage Synology Calendar events and todos via API. Supports calendars, events, todos, and contacts. Based on official Calendar API Guide (v5). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fpengziyang](https://clawhub.ai/user/fpengziyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Synology Calendar for listing calendars, creating and deleting calendar events, managing todos, and listing contacts through the Synology Calendar API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Synology account credentials and may expose them through shared shells, logs, or agent context. <br>
Mitigation: Use a least-privilege Synology account, keep credentials out of shared transcripts and logs, and provide them only through protected environment variables. <br>
Risk: The documented default Synology URL uses unencrypted HTTP. <br>
Mitigation: Configure the skill with HTTPS to a trusted Synology NAS before using it with real calendar data. <br>
Risk: Calendar, event, and todo deletion actions can remove user data. <br>
Mitigation: Require explicit user confirmation before delete operations or any agent action that changes calendar data. <br>


## Reference(s): <br>
- [Synology Calendar API Guide](https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Calendar/All/enu/Calendar_API_Guide_enu.pdf) <br>
- [Synology Calendar Office Suite API](https://office-suite-api.synology.com/Synology-Calendar/v1) <br>
- [Synology Calendar API v1](https://office-suite-api.synology.com/Calendar/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Synology Calendar credentials and API calls configured through environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
