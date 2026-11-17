## Description:

Use whenever an agent is about to take an action with side effects (write, send, pay, delete, change configuration) and a Sovereign Agent Logbook MCP server is connected. Teaches when to log, what to put in each field, when to ask a human, and what must never go in the log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domen028](https://clawhub.ai/user/domen028)

### License/Terms of Use:

MIT-0

## Use Case:

Agents connected to a Sovereign Agent Logbook use this guidance to record actions with side effects, capture approvals and outcomes, escalate risky actions, protect sensitive information, and verify the log at the end of a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes MCP server setup and diagnostic commands, and the security scan was partial because a referenced logbook path was not included.

Mitigation: Review the setup and probe commands and confirm the intended server and logbook path before using them.

Risk: Log entries could expose credentials, personal identifiers, or private document and email contents if these are included in arguments or summaries.

Mitigation: Leave secrets and full personal identifiers out of log fields, do not copy document or email contents into entries, and do not rely solely on automatic masking.

## Reference(s):

- [Project homepage](https://github.com/Delfen-com/sovereign-agent-logbook)
- [ClawHub skill release](https://clawhub.ai/domen028/skills/sovereign-agent-logbook)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples and structured logging guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
