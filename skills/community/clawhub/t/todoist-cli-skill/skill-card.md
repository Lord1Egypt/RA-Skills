## Description: <br>
Manage Todoist tasks, projects, labels, sections, reminders, comments, activity logs, stats, and workspaces through the official Todoist CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leaofelipe](https://clawhub.ai/user/leaofelipe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Todoist accounts use this skill to let an agent inspect and manage tasks, projects, reminders, comments, labels, sections, activity, and stats through the official td CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change, complete, archive, or delete Todoist data without built-in confirmation safeguards. <br>
Mitigation: Before destructive or broad changes, have the agent show the exact matched Todoist item and require explicit confirmation. <br>
Risk: The Todoist API token is an account credential. <br>
Mitigation: Treat TODOIST_API_TOKEN as a secret, avoid exposing it in prompts or logs, and rotate it when the skill is no longer used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leaofelipe/todoist-cli-skill) <br>
- [Official Todoist CLI](https://github.com/Doist/todoist-cli) <br>
- [Todoist API token settings](https://todoist.com/app/settings/integrations/developer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON or NDJSON CLI output when parseable Todoist results are needed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
