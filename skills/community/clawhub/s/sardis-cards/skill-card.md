## Description:

Virtual card issuance and management for AI agents to make real-world purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let agents issue, monitor, freeze, unfreeze, limit, reveal, and terminate Sardis virtual cards for controlled real-world purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can create or change real payment cards and spending limits.

Mitigation: Use a tightly scoped Sardis API key and require explicit human confirmation before card creation, unfreeze, limit increases, bulk freezes, or termination.

Risk: Full card numbers and CVVs may be revealed through the card details workflow.

Mitigation: Never print, log, store, or return full card numbers or CVVs to the model; use revealed card data only for the immediate approved transaction and discard it.

Risk: Broad card powers can create financial exposure if limits or merchant controls are loose.

Mitigation: Issue cards with minimum required limits, merchant restrictions, transaction monitoring, and fail-closed freezing on suspicious activity.

## Reference(s):

- [Sardis Website](https://sardis.sh)
- [Sardis Virtual Cards Documentation](https://sardis.sh/docs/virtual-cards)
- [Sardis API Reference](https://api.sardis.sh/v2/docs)
- [ClawHub Skill Page](https://clawhub.ai/efedurmaz16/skills/sardis-cards)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request patterns for card creation, card controls, transaction monitoring, and sensitive card reveal workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
