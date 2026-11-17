## Description:

Designs an agent learning loop that captures interaction logs, summarizes patterns with AI, routes candidate lessons through human review, and promotes validated experience into reusable rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mistyhuqwq-art](https://clawhub.ai/user/mistyhuqwq-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product operators, and agent designers use this skill to specify logging, review, and experience-management workflows that help agents improve through observed user corrections and curated rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad always-on logging and long-term reuse of interaction data can capture personal data, credentials, customer data, confidential business configuration, or regulated compliance information.

Mitigation: Define privacy requirements before use: redact secrets and personal data before storage, aggregate or anonymize reports, and set explicit retention and deletion rules.

Risk: AI-generated summaries or candidate rules can promote incorrect patterns into future agent behavior.

Mitigation: Require human approval before any learned rule changes agent behavior, and preserve review decisions and audit records for accepted, rejected, and expired rules.

Risk: Reports and review workflows can expose sensitive operational data to unintended recipients.

Mitigation: Restrict report recipients, use role-based access controls, and limit distribution channels to approved reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mistyhuqwq-art/skills/workflow-dlc-agent-learning)
- [Agent lessons collection](../../lessons/by-role/agent.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured tables and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers phased gate checks, logging schemas, review cadence, experience-layering rules, and lifecycle practices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
