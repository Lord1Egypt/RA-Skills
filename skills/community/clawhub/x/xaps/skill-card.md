## Description:

Audit agent value moves before sign or settle; payers attach an X-XAPS-Receipt and counterparties independently clear it as an advisory receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sentvan23](https://clawhub.ai/user/sentvan23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents handling x402 payments, wallet transactions, or paid-work settlement use this skill to request an XAPS audit receipt before execution and to clear receipts independently before accepting value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-audit details are sent to the external XAPS service and may incur the stated audit fee.

Mitigation: Install only when sharing those details and paying the external fee are acceptable for the deployment.

Risk: The XAPS receipt is advisory and does not insure, custody, sign, send, settle, or guarantee the transaction.

Mitigation: Keep the executing agent responsible for final approval, fail closed on missing or rejected receipts, and independently clear receipt details against the exact amount, payee, resource, and value_move use case.

## Reference(s):

- [XAPS SDK](https://github.com/APMC1/xaps-sdk)
- [XAPS API Node](https://api.xaps.network)
- [XAPS Agent Card](https://api.xaps.network/.well-known/xaps-agent-card.json)
- [ClawHub Skill Page](https://clawhub.ai/sentvan23/skills/xaps)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown instructions with bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for shell usage; XAPS_AGENT_KEY is only needed when the agent signs or pays.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
