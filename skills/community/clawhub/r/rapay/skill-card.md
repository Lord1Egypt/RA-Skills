## Description:

Send and receive compliant B2B payments via the Ra Pay CLI, and onboard a counterparty agent so both sides can transact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greendlt224](https://clawhub.ai/user/greendlt224)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to set up Ra Pay, preview and confirm fiat USD business payments, and coordinate buyer or seller onboarding with counterparties. It is intended only for business-to-business transactions with explicit user approval and a concrete business purpose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to promote and forward Ra Pay onboarding instructions to counterparties.

Mitigation: Require the user to review and approve the exact outreach message, recipient, and delivery channel before any counterparty message is sent.

Risk: The installation flow uses an unpinned global npm package for a payment CLI.

Mitigation: Install only after deciding to trust the Ra Pay npm package, and verify the installed CLI version before using it for business payments.

Risk: The workflow can initiate real business payments if the confirmation step is mishandled.

Mitigation: Always run the preview command first, show the fee breakdown and recipient details to the user, and execute only after explicit user approval.

## Reference(s):

- [Ra Pay Skill Instruction Set](https://rapay.ai/skill.md)
- [ClawHub Skill Page](https://clawhub.ai/greendlt224/skills/rapay)
- [Publisher Profile](https://clawhub.ai/user/greendlt224)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown instructions with inline shell commands, onboarding message text, and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payment execution requires preview output, explicit user confirmation, USD-only amounts, and a stated business purpose.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
