## Description:

Webex API integration with managed OAuth. Send messages, manage rooms and teams, list memberships, handle webhooks, manage people and team memberships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, developers, and engineers use this skill to work with Webex messaging from an agent, including sending messages, managing rooms and teams, reviewing memberships, and configuring webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and broadly authorize an unpinned external plugin for Webex access.

Mitigation: Review the ClawLink plugin publisher, version, and OAuth scopes before installing, and use a least-privilege OAuth grant or dedicated Webex account where possible.

Risk: Message deletion, membership changes, room or team updates, and webhook creation can affect other Webex users and may be irreversible.

Mitigation: Require explicit user confirmation before write or delete actions and verify target room, team, membership, message, and webhook identifiers before execution.

## Reference(s):

- [Webex API Docs](https://developer.webex.com/docs/api-basics)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=webex)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/webex)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent in selecting and using Webex and ClawLink tools; write and delete operations can affect Webex rooms, messages, memberships, teams, and webhooks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
