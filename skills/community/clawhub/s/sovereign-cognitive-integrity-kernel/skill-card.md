## Description:

Provides a self-audit workflow for comparing reasoning material against ethical invariants and summarizing drift, divergences, and optional corrective prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can review selected visible outputs or brief decision summaries for possible departures from a chosen set of ethical invariants. The audit is advisory and returns a drift score, divergence summary, and optional corrective prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit receipts may expose private reasoning, prompt history, hidden instructions, secrets, or unrelated context.

Mitigation: Limit audits to user-selected visible outputs and brief decision summaries; exclude private reasoning, hidden instructions, secrets, and unrelated history. Redact receipts and approve any transfer to an optional attestation skill.

## Reference(s):

- [Ethical invariants](references/ETHICAL_INVARIANTS.json)
- [ClawHub skill release](https://clawhub.ai/deepseekoracle/skills/sovereign-cognitive-integrity-kernel)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON audit receipt with a drift score, divergence summary, and optional corrective prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; corrective prompts are not applied automatically.]

## Skill Version(s):

1.2.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
