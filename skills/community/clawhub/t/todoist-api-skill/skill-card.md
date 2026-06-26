## Description: <br>
Manages Todoist tasks, projects, sections, labels, comments, completed-task reports, activity logs, ID migration, project templates, and sync workflows through Todoist API v1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to automate Todoist task capture, triage, reporting, project setup, and bulk maintenance through a non-interactive CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Todoist account data when provided a token. <br>
Mitigation: Install it only when Todoist account operation is intended, and use a dedicated or revocable Todoist token where possible. <br>
Risk: Bulk, raw, sync, delete, archive, close, reopen, backup, and email-in-address operations can cause broad or sensitive account changes. <br>
Mitigation: Require dry-run review before these operations and use confirmation controls for execution. <br>
Risk: Changing the Todoist API endpoint can redirect requests away from the expected service. <br>
Mitigation: Keep the default Todoist API endpoint unless there is a specific, reviewed reason to override it. <br>


## Reference(s): <br>
- [Todoist API Skill Page](https://clawhub.ai/tristanmanchester/todoist-api-skill) <br>
- [Todoist API endpoint](https://api.todoist.com/api/v1) <br>
- [Reference](references/REFERENCE.md) <br>
- [Recipes](references/RECIPES.md) <br>
- [Gotchas](references/GOTCHAS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or summary command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output can be written to files for large Todoist API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
