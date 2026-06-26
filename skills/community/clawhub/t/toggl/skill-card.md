## Description: <br>
Track time with Toggl via the toggl CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clvrobj](https://clawhub.ai/user/clvrobj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to let an agent start and stop Toggl timers, check current tracking status, view reports, list entries, and manage time entries through the toggl CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Toggl API token and workspace configuration for account access. <br>
Mitigation: Store the Toggl API token securely, keep the config file permission-restricted, and prefer environment or file permissions appropriate to the host. <br>
Risk: The skill can add, edit, stop, and delete Toggl time entries. <br>
Mitigation: Require clear user confirmation before account-mutating actions, especially deleting entries with `toggl rm <id>`. <br>


## Reference(s): <br>
- [ClawHub Toggl skill page](https://clawhub.ai/clvrobj/toggl) <br>
- [Toggl Track profile](https://track.toggl.com/profile) <br>
- [Toggl Track workspace URL pattern](https://track.toggl.com/{workspace_id}/...) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Toggl CLI commands that read or modify time entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
