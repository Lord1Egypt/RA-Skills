## Description:

Manage tasks and projects in Todoist. Use when user asks about tasks, to-dos, reminders, or productivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to inspect, create, search, update, complete, reopen, move, and delete Todoist tasks, projects, labels, and comments through the Todoist CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause account-changing actions such as completing, reopening, moving, updating, or deleting Todoist tasks.

Mitigation: Require explicit user confirmation before running commands that modify or delete Todoist data.

Risk: The skill requires a Todoist API token, and token handling examples can lead to accidental exposure in shell history or logs.

Mitigation: Store the token in a reviewed secret mechanism or environment variable and avoid typing the raw token directly into shell history.

Risk: The installation example allows a semver range for the global Todoist CLI package.

Mitigation: Use an exact reviewed todoist-ts-cli version before enabling the skill in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/todoist-litiao)
- [Todoist homepage](https://todoist.com)
- [Todoist developer integrations settings](https://todoist.com/app/settings/integrations/developer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Todoist CLI commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the todoist binary and TODOIST_API_TOKEN for account access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
