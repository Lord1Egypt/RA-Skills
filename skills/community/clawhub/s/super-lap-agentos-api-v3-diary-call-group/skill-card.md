## Description:

Helps agents use the agentOS API V3 Diary Call Group endpoints to search guests, inspect allocations, manage appointments, submit feedback, and retrieve branch or recurring appointment details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molexazwo](https://clawhub.ai/user/molexazwo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to answer diary API questions and draft endpoint-specific guidance or calls for scheduling, appointment management, branch lookup, and feedback workflows in agentOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that create, update, cancel, or delete real appointments.

Mitigation: Use a least-privileged API key and require explicit user confirmation before any appointment-changing API call.

Risk: The artifact includes unpinned `npx @lap-platform/lapsh` command examples.

Mitigation: Pin and trust the package version or run the commands in an isolated environment before relying on their output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/molexazwo/skills/super-lap-agentos-api-v3-diary-call-group)
- [LAP](https://lap.sh)
- [agentOS Diary API base URL](https://live-api.letmc.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with endpoint paths and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTOS_API_V3_DIARY_CALL_GROUP_API_KEY for authenticated API use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
