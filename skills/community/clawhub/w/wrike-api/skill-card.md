## Description: <br>
Wrike API integration with managed OAuth for managing tasks, folders, projects, spaces, collaboration, and administrative functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, and agents use this skill to inspect and manage Wrike workspaces, tasks, folders, projects, spaces, time logs, users, invitations, access roles, audit logs, and data exports through an authenticated Wrike connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key that can access a connected Wrike account. <br>
Mitigation: Keep MATON_API_KEY private, install only when Wrike access through Maton is intended, and scope usage to the correct connection. <br>
Risk: Write, administrative, audit-log, invitation, user-management, and data-export operations can expose sensitive data or change account governance. <br>
Mitigation: Review and explicitly approve the target, scope, and intended effect before any sensitive or account-changing operation. <br>


## Reference(s): <br>
- [ClawHub Wrike Skill](https://clawhub.ai/byungkyu/wrike-api) <br>
- [Maton](https://maton.ai) <br>
- [Wrike API Documentation](https://developers.wrike.com/) <br>
- [Wrike OAuth 2.0 Authorization](https://developers.wrike.com/oauth-20-authorization/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; use Maton-Connection when selecting among multiple Wrike connections.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
