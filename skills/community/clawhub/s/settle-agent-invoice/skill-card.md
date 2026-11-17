## Description:

Agent settles an invoice at the end of a multi-step task using CAI transfer after the user confirms the payee and amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through settling an invoice with CAI after checking balance, confirming irreversible transfer details, sending the transfer, and returning proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could approve payment to the wrong payee, destination address, amount, asset, or chain.

Mitigation: Independently verify the invoice details and destination before giving explicit transfer approval.

Risk: Completed transfers may be irreversible.

Mitigation: Treat the confirmation step as final authorization and proceed only after the transfer details are trusted.

Risk: A compromised or untrusted CAI account or API key could expose payment authority.

Mitigation: Use only a trusted CAI account/API key and manage the CAI_API_KEY secret carefully before installing or running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/settle-agent-invoice)
- [CAI skill reference](https://cai.com/skill.md)
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md)
- [CAI developer documentation](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and ordered workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted CAI_API_KEY and explicit user confirmation before transfer.]

## Skill Version(s):

1.0.15 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
