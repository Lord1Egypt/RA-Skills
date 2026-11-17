## Description:

TAPD helps users query and update TAPD project-management records, including requirements, defects, tasks, iterations, comments, and status changes through TAPD MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truesnow](https://clawhub.ai/user/truesnow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, testers, project managers, and engineering leads use this skill to retrieve TAPD work items, summarize iteration progress, inspect defect status, update workflow states, add comments, and request Enterprise WeChat notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change TAPD states, add comments, send Enterprise WeChat messages, or create recurring notifications in a workplace project-management context.

Mitigation: Confirm the target workspace, affected records, message recipients, and schedule before allowing update, comment, messaging, or recurring notification actions.

Risk: TAPD project and personal work data may be sensitive.

Mitigation: Install and use the skill only where TAPD MCP and Enterprise WeChat permissions match the intended workspace and data-handling expectations.

## Reference(s):

- [Usage examples](artifact/references/examples.md)
- [ClawHub TAPD skill page](https://clawhub.ai/truesnow/skills/tapd-skill)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise text with requested TAPD results, summaries, update proposals, and notification guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke TAPD MCP operations and Enterprise WeChat messaging when the configured permissions allow it.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
