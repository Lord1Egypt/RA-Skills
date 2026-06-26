## Description: <br>
Read, list, filter, and update Redmine issues through the Redmine REST API using configurable server URL and authentication settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoway](https://clawhub.ai/user/guoway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agents working with Redmine use this skill to inspect issue details, list issues by project or assignment, and make authenticated ticket updates when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live authenticated updates to Redmine tickets. <br>
Mitigation: Use a least-privilege Redmine API key, restrict access to relevant projects where possible, and require explicit user approval before update operations. <br>
Risk: Read-oriented usage can obscure the presence of write-capable update commands. <br>
Mitigation: Treat update commands as state-changing actions and review the target issue ID and fields before execution. <br>
Risk: The skill relies on Redmine credentials supplied through environment variables. <br>
Mitigation: Prefer API-key authentication over username and password, and avoid exposing credentials in logs, shell history, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub Redmine Issue skill page](https://clawhub.ai/guoway/redmine-issue) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDMINE_URL plus either REDMINE_API_KEY or REDMINE_USERNAME and REDMINE_PASSWORD.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
