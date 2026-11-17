## Description:

Kannaka Constellation status monitoring -- all apps, services, swarm health, and connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check Kannaka constellation health, inspect connected swarm agents, verify NATS transport status, and diagnose cross-service connectivity issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Joining or listening to a swarm can expose agent identifiers and runtime phase or state information to the configured NATS bus.

Mitigation: Use the default local NATS URL or a NATS server you control, and join shared buses only when that exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/skill-kannaka-constellation)
- [Kannaka radio reference deployment](https://radio.ninja-portal.com)
- [Kannaka observatory reference deployment](https://observatory.ninja-portal.com)
- [Kannaka installer download](https://radio.ninja-portal.com/download)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
