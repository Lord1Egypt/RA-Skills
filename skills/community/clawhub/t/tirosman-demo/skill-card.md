## Description:

Drive the TirOSMAN autonomous multi-agent demo (5 projects x 150 tasks, Jira-like lifecycle, QA approval) from any MCP-aware client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mturac](https://clawhub.ai/user/mturac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill from MCP-aware clients to estimate, start, monitor, reset, and QA-approve or reject a TirOSMAN autonomous multi-agent demo run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the demo may spend NVIDIA tokens and create or reset demo task data.

Mitigation: Confirm trust in the local TirOSMAN MCP server and review the cost estimate before starting or resetting a run.

Risk: If TIROSMAN_DEMO_WEBHOOK_URL is configured, task transition events may be sent to an external automation or messaging service.

Mitigation: Leave the webhook unset unless external event sharing is intended, and avoid sensitive project names or metadata when it is enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mturac/skills/tirosman-demo)
- [Publisher profile](https://clawhub.ai/user/mturac)

## Skill Output:

**Output Type(s):** [guidance, API calls, text, configuration]

**Output Format:** [Markdown or plain text with MCP tool calls and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cost estimates, board/status views, QA decisions, task lifecycle changes, and reset actions through the local MCP integration.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
