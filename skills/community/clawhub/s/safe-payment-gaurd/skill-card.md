## Description:

Applies a conservative payment safety guardrail for requests involving payments, wires, remittances, invoices, balance top-ups, or other movement of money or stored value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhandsomeboy12138](https://clawhub.ai/user/jhandsomeboy12138)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to review payment-related tasks before approval or execution. It helps verify beneficiary, amount, currency, purpose, authorization, payment rail, and risk signals before deciding to proceed, hold, or block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment actions can cause irreversible financial loss when beneficiary, amount, currency, rail, or authorization is wrong.

Mitigation: Require verified beneficiary, amount, currency, purpose, and authorization before any proceed decision; otherwise hold or block.

Risk: Users may expose OTPs, passwords, CVVs, full account numbers, or other secrets in chat while attempting payment workflows.

Mitigation: Keep secrets out of chat and execute payments only through trusted official payment surfaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhandsomeboy12138/skills/safe-payment-gaurd)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured safety summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a proceed, hold for verification, or block decision with the next safe action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
