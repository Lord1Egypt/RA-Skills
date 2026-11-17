## Description:

Manage tasks and projects in Todoist using the Official Todoist CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leaofelipe](https://clawhub.ai/user/leaofelipe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent translate Todoist task-management requests into Todoist CLI commands for tasks, projects, labels, sections, reminders, comments, activity logs, stats, and workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad read, write, archive, and delete access to a Todoist account.

Mitigation: Use it only for accounts where direct agent management is intended, and require explicit user confirmation before destructive actions such as deleting tasks, labels, sections, comments, reminders, or projects.

Risk: The Todoist API token is a secret that could be exposed through shared logs, chats, or command history.

Mitigation: Prefer the TODOIST_API_TOKEN environment variable or protected local authentication, and avoid pasting tokens into shared conversations or logs.

Risk: Global installation of the Todoist CLI may pull an unreviewed dependency version.

Mitigation: Pin and review the @doist/todoist-cli version before installing it globally in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leaofelipe/skills/todoist-cli-skill)
- [Todoist CLI](https://github.com/Doist/todoist-cli)
- [Todoist Developer Integrations Settings](https://todoist.com/app/settings/integrations/developer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and Todoist CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Todoist CLI JSON or NDJSON output for parseable command results.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
