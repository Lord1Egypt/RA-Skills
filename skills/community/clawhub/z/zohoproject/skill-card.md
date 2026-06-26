## Description: <br>
Manage Zoho Projects by listing portals and projects, creating, updating, completing, and deleting tasks, adding comments, logging time, managing milestones, and querying task lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katprotech](https://clawhub.ai/user/katprotech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Zoho Projects through authenticated API calls for project, task, milestone, comment, and time-log workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live Zoho Projects data, including task creation, updates, time logs, and deletion. <br>
Mitigation: Require explicit user confirmation before any create, update, time-log, or delete action. <br>
Risk: Broad Zoho OAuth scopes and stored refresh credentials can expose more project data or permissions than needed. <br>
Mitigation: Use the narrowest Zoho OAuth scopes that support the workflow and protect refresh tokens, client secrets, and access tokens. <br>
Risk: Remembered portal or project IDs may target the wrong tenant or project. <br>
Mitigation: Verify the current portal and project from fresh Zoho API results before acting on organization-specific project IDs. <br>


## Reference(s): <br>
- [Zoho Projects API documentation](https://projects.zoho.com/api-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zoho OAuth credentials and a Zoho portal ID supplied by environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
