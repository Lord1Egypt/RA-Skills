## Description: <br>
Manage tasks and projects in Todoist. Use when user asks about tasks, to-dos, reminders, or productivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect, create, update, complete, search, and delete Todoist tasks, projects, labels, and comments through the Todoist CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may unintentionally create, update, complete, or delete Todoist tasks because the skill exposes task-changing commands. <br>
Mitigation: Require explicit user confirmation before any create, update, complete, reopen, move, or delete command is executed. <br>
Risk: Deleting or modifying the wrong task can occur if a task ID is selected from an ambiguous search result. <br>
Mitigation: Review task details and confirm the exact task ID before destructive or state-changing commands, especially delete. <br>
Risk: The Todoist API token gives access to the user's Todoist account. <br>
Mitigation: Install only for workflows that need Todoist account access and keep TODOIST_API_TOKEN scoped to trusted agent environments. <br>


## Reference(s): <br>
- [Todoist](https://todoist.com) <br>
- [Todoist API Token Settings](https://todoist.com/app/settings/integrations/developer) <br>
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/todoist-litiao) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/litiao1224) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Todoist CLI commands and setup guidance; task-changing actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
