## Description: <br>
Manage Todoist tasks, projects, labels, and sections via the `todoist` CLI when users ask to add, complete, list, search, or organize Todoist work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buddyh](https://clawhub.ai/user/buddyh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to manage Todoist tasks, projects, labels, sections, comments, and completed items from an agent through the Todoist CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs a Todoist API token and can change Todoist tasks when requested. <br>
Mitigation: Treat TODOIST_API_TOKEN as a secret, avoid placing it in shared logs or prompts, and revoke it from Todoist settings when it is no longer needed. <br>
Risk: Destructive or state-changing commands such as delete, move, complete, reopen, and update can affect the user's Todoist data. <br>
Mitigation: Verify task IDs, project names, labels, sections, and dates before executing state-changing Todoist CLI commands. <br>
Risk: The Todoist CLI is installed from an external source. <br>
Mitigation: Install only if the external Todoist CLI source is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buddyh/todoist-cli) <br>
- [Publisher profile](https://clawhub.ai/user/buddyh) <br>
- [Todoist API token settings](https://todoist.com/app/settings/integrations/developer) <br>
- [Todoist CLI project homepage](https://github.com/buddyh/todoist-cli) <br>
- [Go install module](https://github.com/buddyh/todoist-cli/tree/main/cmd/todoist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Todoist CLI commands and optional JSON command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call the Todoist CLI and can use TODOIST_API_TOKEN for authentication.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
