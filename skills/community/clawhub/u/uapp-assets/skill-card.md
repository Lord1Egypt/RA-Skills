## Description:

Queries the signed-in Umeng account for App and mini-program inventory using read-only umeng-cli asset APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover Umeng App and mini-program assets for the currently logged-in account, including counts, paginated lists, and platform-filtered summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to send telemetry and may include AppKeys when they appear in task context.

Mitigation: Do not permit telemetry or AppKey reporting unless the user understands what is sent and has consent to disclose those identifiers.

Risk: The installation instructions include a mutable curl-to-shell command.

Mitigation: Prefer a pinned, verified umeng-cli release and avoid running remote installer scripts directly.

Risk: Asset listing can reveal broad account inventory.

Mitigation: Use the skill only with accounts where broad App and mini-program inventory disclosure is acceptable.

## Reference(s):

- [umeng-cli homepage](https://github.com/umeng/umeng-cli)
- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-assets)
- [Publisher profile](https://clawhub.ai/user/squall0925)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only inventory guidance and summaries from umeng-cli call responses; does not write or modify Umeng assets.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
