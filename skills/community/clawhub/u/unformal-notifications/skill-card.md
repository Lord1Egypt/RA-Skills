## Description:

Get notified when someone completes an Unformal Pulse through an hourly Claude Code routine, a local desktop listener, or on-demand API polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasboury](https://clawhub.ai/user/jonasboury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor Unformal Pulse completions, summarize new responses, and set up local or scheduled alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable remote listener script.

Mitigation: Review the listener before installing it and prefer the bundled artifact script when available.

Risk: The skill handles an Unformal API key and may persist credentials or response data locally.

Mitigation: Use a secret manager or restricted environment file, avoid storing the API key in shell startup files, and set restrictive permissions on ~/.unformal.

Risk: The local listener can trigger desktop notifications from remote response data.

Mitigation: Run the listener only with trusted Unformal sources and avoid granting sensitive macOS automation permissions unless required and reviewed.

## Reference(s):

- [Unformal website](https://unformal.ai)
- [Unformal Studio settings](https://unformal.ai/studio/settings)
- [Listener source](https://unformal.ai/unformal-listen.sh)
- [SSE stream docs](https://unformal.ai/agents)
- [ClawHub skill page](https://clawhub.ai/jonasboury/skills/unformal-notifications)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct agents to call Unformal APIs, create scheduled-task files, run a local listener, and summarize response JSON.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
