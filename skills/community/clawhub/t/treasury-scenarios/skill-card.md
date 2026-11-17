## Description:

Treasury Scenarios provides Chinese-language lookup for Postal Savings Bank treasury system business scenarios, returning process steps, interface combinations, and ASCII flow diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbj-bnu](https://clawhub.ai/user/lbj-bnu)

### License/Terms of Use:

MIT-0

## Use Case:

Treasury operations, finance, and integration teams use this skill to answer scenario-based questions about treasury workflows and the interface sequences used for funds management, payroll, supplier payments, budgeting, SSO, receipts, and account balance inquiries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents payment, payroll, transfer, account, and login-token workflows that may be sensitive in treasury environments.

Mitigation: Install it only where users are authorized to view treasury interface and workflow details.

Risk: Readers could mistake static workflow documentation for authorization to perform real banking actions.

Mitigation: Use separate role checks, approval flows, explicit confirmations, and audit controls for any real banking integration.

## Reference(s):

- [Treasury Scenarios on ClawHub](https://clawhub.ai/lbj-bnu/skills/treasury-scenarios)
- [Skill Instructions](artifact/SKILL.md)
- [Scenario Data](artifact/scenarios.json)
- [Interface Data](artifact/interfaces.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with scenario names, ordered workflow steps, interface combinations, and ASCII flow diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns static reference material from bundled scenario and interface data; it does not execute transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, scenarios.json, SKILL.md version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
