## Description:

Uncle Matt lets agents use approved API actions through a hardened local Broker without seeing secrets, calling arbitrary URLs, or becoming an open proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use the skill to let an agent make approved external API calls through a local Broker while keeping API credentials out of the agent's reach. Operators define the allowed actions and their limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan was partial and did not review several referenced documents, configuration paths, and installer scripts. The skill package also does not include the Broker or installers required to use the action tool.

Mitigation: Review the full project documentation, Broker configuration, and installer scripts before setup; verify the allowed actions and keep the Broker bound to loopback.

## Reference(s):

- [Uncle Matt project and operator guides](https://github.com/uncmatteth/UNCLEMATTCLAWBOT)
- [Uncle Matt homepage](https://bobsturtletank.fun)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Action-ID API requests with JSON arguments and returned API data; Markdown guidance for allowed and blocked requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls are limited to operator-approved action IDs; optional voice packs apply only to refusals and warnings.]

## Skill Version(s):

6.420.69 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
