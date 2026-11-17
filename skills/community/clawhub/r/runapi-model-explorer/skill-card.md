## Description:

Helps agents discover, compare, price, and recommend RunAPI models by querying RunAPI catalog and pricing tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an assistant what RunAPI models are available, compare model options, check pricing, inspect required fields, search by modality, and get a recommended service/action/model triple.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model and pricing guidance can become stale if catalog or pricing data changes.

Mitigation: Use RunAPI catalog and pricing tools at request time, and avoid quoting prices that were not returned by current tool results.

Risk: The skill intentionally avoids exposing hidden infrastructure provider names, which may limit backend routing transparency.

Mitigation: Treat recommendations as RunAPI service/action/model guidance and consult the publisher when routing transparency is required for review.

## Reference(s):

- [RunAPI Model Explorer on ClawHub](https://clawhub.ai/runapi-ai/skills/runapi-model-explorer)
- [RunAPI Publisher Profile](https://clawhub.ai/user/runapi-ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with compact tables and a recommended service/action/model triple when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current RunAPI tool results for catalog and pricing answers; avoids quoting stale prices.]

## Skill Version(s):

0.1.9 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
