## Description:

Helps coding agents manage a user's shared Taskhold task list by selecting tasks, recording progress, and requesting decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakemarsh](https://clawhub.ai/user/jakemarsh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and their coding agents use Taskhold to work through a shared task list, add follow-up tasks, record progress, and surface decisions or blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task summaries, progress notes, and file references are sent to Taskhold.

Mitigation: Keep the setup URL and Bearer key private, share only appropriate task information, and review the supplied connection configuration.

## Reference(s):

- [Taskhold MCP endpoint](https://taskhold.com/api/mcp)
- [Taskhold dashboard](https://taskhold.com/dashboard)
- [Taskhold](https://taskhold.com)
- [ClawHub release](https://clawhub.ai/jakemarsh/skills/taskhold)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise task summaries, progress notes, decisions, and status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task information and updates are sent to the connected Taskhold service.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
