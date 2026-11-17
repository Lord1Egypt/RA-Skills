## Description:

Helps an agent manage WEEEK Task Manager data through the WEEEK Public API, including listing, creating, updating, completing, reopening, and moving tasks across boards and columns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-indi](https://clawhub.ai/user/alex-indi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to let an agent operate on WEEEK tasks, projects, boards, and board columns through command-line calls to the WEEEK Public API. It is useful for task-management workflows where the agent needs to read or update live WEEEK workspace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a WEEEK account token to access task data.

Mitigation: Use the narrowest WEEEK token available and avoid exposing it in logs, prompts, shared shells, or committed files.

Risk: Create, update, complete, reopen, and move commands can change live WEEEK tasks.

Mitigation: Review the intended task operation and target IDs before allowing the agent to run mutating commands.

## Reference(s):

- [WEEEK Public API reference](references/api.md)
- [WEEEK Public API base endpoint](https://api.weeek.net/public/v1)
- [ClawHub skill page](https://clawhub.ai/alex-indi/skills/weeek-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided WEEEK_TOKEN environment variable; optionally uses WEEEK_USER_ID for task assignment.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
