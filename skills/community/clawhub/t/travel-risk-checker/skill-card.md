## Description:

Assesses travel disruption risk for tight flight connections, delayed-arrival hotel needs, and late-night last-mile transport availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlyjqx](https://clawhub.ai/user/mlyjqx)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-service agents use this skill to evaluate connection risk, identify airport hotels for significant delays, and plan backup transport after late arrivals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures unpinned external MCP packages for travel, hotel, and city transport data.

Mitigation: Pin or otherwise vet MCP packages before installation and review package provenance during deployment.

Risk: The skill uses travel-related API keys and may access order, location, flight, hotel, and transport data.

Mitigation: Use scoped, rotatable API keys and clearly disclose what trip and location data may be sent to outside services.

Risk: The security verdict is suspicious due to dependency and data-sharing concerns.

Mitigation: Review the skill before installing and deploy only in environments where external services are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlyjqx/skills/travel-risk-checker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown-style travel risk assessments, recommendations, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on travel order, location, flight status, hotel, and transport data supplied by external MCP services.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter/package.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
