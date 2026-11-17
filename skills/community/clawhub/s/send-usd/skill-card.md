## Description:

Accepts an agent-to-agent USD transfer request and returns a transfer-style result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeef23](https://clawhub.ai/user/afeef23)

### License/Terms of Use:


## Use Case:

External developers and agent operators can evaluate this skill for agent-to-agent USD transfer request handling. Because the security evidence says it returns successful payment confirmations without authentication or a real payment backend, it should not be installed as a real payment skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-like success confirmations may be mistaken for completed USD transfers.

Mitigation: Do not use for real payments unless authenticated sender identity, explicit user confirmation, provider or ledger integration, settlement status, durable audit records, and stricter amount validation are added and reviewed.

Risk: The skill documentation describes authentication and auditability that the security evidence does not confirm in the implementation.

Mitigation: Review the implementation before deployment and label it as a mock or placeholder unless those controls are actually implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeef23/skills/send-usd)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object with success status, transaction identifier, message, and optional error code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns payment-style status data; evidence does not show authoritative settlement status.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
