## Description:

AI Agent usage tracking and billing verification tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeterwang](https://clawhub.ai/user/jeterwang)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agent operators use this skill to track feature usage, review usage reports and metrics, and connect paid actions to SkillPay.me billing flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact SkillPay.me to create charges, query balances, and generate payment links.

Mitigation: Require explicit user confirmation for charge and recharge actions, constrain allowed amounts, and document what billing data is sent before enabling live use.

Risk: The release evidence reports a shared hardcoded billing key in the published code.

Mitigation: Remove the embedded key, rotate any exposed credential, and require deployments to provide a secret through a secure environment variable.

Risk: The security verdict is suspicious because real payment operations have weak user controls.

Mitigation: Review and test billing flows in a non-production account before installation, and block real billing until controls and data handling are verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeterwang/skills/usage-tracker-clawhub)
- [Publisher Profile](https://clawhub.ai/user/jeterwang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-like text responses with command snippets and billing status details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include usage counts, cost estimates, balances, transaction identifiers, and payment links.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
