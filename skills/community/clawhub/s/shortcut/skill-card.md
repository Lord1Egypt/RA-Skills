## Description: <br>
Manage stories on Shortcut.com kanban boards. Use when creating, updating, or listing tasks/stories on Shortcut project management boards. Supports creating stories with descriptions and types (feature/bug/chore), updating story status, and listing active/completed stories. Includes full checklist task management and comment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catwalksophie](https://clawhub.ai/user/catwalksophie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams using Shortcut can let an agent list, create, update, and inspect project stories, checklist tasks, and comments through Shortcut's API. The skill is useful for routine project-management updates where the agent has an appropriate Shortcut API token and workspace permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete live Shortcut workspace data when supplied with an API token. <br>
Mitigation: Use the least-privileged token available and require explicit confirmation before update or delete requests. <br>
Risk: The workflow initialization script writes a shell configuration file that may later be sourced by the user's shell. <br>
Mitigation: Inspect the generated workflow-states file before sourcing it or adding it to shell startup files. <br>


## Reference(s): <br>
- [Shortcut ClawHub page](https://clawhub.ai/catwalksophie/shortcut) <br>
- [Shortcut API v3](https://api.app.shortcut.com/api/v3) <br>
- [Shortcut workflows API endpoint](https://api.app.shortcut.com/api/v3/workflows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can invoke Shortcut API scripts that read a local API token and may create, update, or delete live workspace data.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter, changelog, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
