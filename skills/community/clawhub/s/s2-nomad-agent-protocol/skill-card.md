## Description:

Instructs the OpenClaw agent on how to request geolocation, claim P-SSSU Habitable Slots with user consent, and negotiate boundaries with other agents in the outdoor environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to guide outdoor agents through consent-based geolocation requests, P-SSSU grid claims, and boundary negotiation reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests sensitive geolocation and environmental sensor permissions.

Mitigation: Constrain use to explicit per-action user or system approval and remove unused device permissions before deployment.

Risk: Location-based claim or override actions can run without authorization enforcement in code.

Mitigation: Validate agent identity, priority, and recorded consent before claim or ripple_expand actions, especially before any ownership override.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-nomad-agent-protocol)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Markdown instructions with JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before location or grid-claim actions; tool responses include status and data fields.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, openclaw.plugin.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
