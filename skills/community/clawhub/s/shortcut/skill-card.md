## Description:

Manage Shortcut.com project board stories, checklist tasks, and comments from an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catwalksophie](https://clawhub.ai/user/catwalksophie)

### License/Terms of Use:

MIT

## Use Case:

External developers and teams use this skill to let an agent list, create, inspect, update, and delete Shortcut stories, checklist tasks, and comments in a Shortcut workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow-states setup path can write workspace data into shell code that users may source on their machine.

Mitigation: Review the generated workflow-states file before sourcing it, do not add it to shell startup files, and prefer a passive configuration format until the skill is fixed.

Risk: Story, task, and comment delete operations can remove Shortcut workspace content.

Mitigation: Verify story, task, and comment IDs before running delete commands.

Risk: The skill requires a Shortcut API token with access to workspace data.

Mitigation: Use a token with the minimum Shortcut permissions needed and store it with restricted file permissions.

## Reference(s):

- [ClawHub Shortcut skill page](https://clawhub.ai/catwalksophie/skills/shortcut)
- [Shortcut API v3 endpoint](https://api.app.shortcut.com/api/v3)
- [Shortcut workflows API endpoint](https://api.app.shortcut.com/api/v3/workflows)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and text or JSON-capable shell script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Shortcut API token and workspace permissions.]

## Skill Version(s):

1.4.1 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
