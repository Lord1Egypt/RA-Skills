## Description:

Use this skill when a team, DAO, or builder wants to deploy USDC from a stablecoin treasury into LI.FI Earn vaults under explicit treasury policy limits, prepare a Composer deposit, and produce a receipt-token execution report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, DAOs, builders, and developers use this skill to apply treasury policy limits before selecting a LI.FI Earn vault, preparing a Composer deposit, and producing an execution report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could approve a treasury transaction whose vault, chain, amount, or receipt-token details do not match the treasury policy.

Mitigation: Review the policy checks and Composer quote carefully, and do not approve or sign unless all details match the treasury rules.

Risk: Live LI.FI Earn discovery may be unavailable and the skill may rely on seeded examples.

Mitigation: Confirm whether the output is based on live discovery or seeded examples before using a vault recommendation for execution.

## Reference(s):

- [StableOps Treasury on ClawHub](https://clawhub.ai/richard7463/skills/stableops-lifi-treasury)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown]

**Output Format:** [Markdown with inline shell commands and treasury execution report fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include policy checks, vault details, Composer quote guidance, transaction hash, and receipt-token explanation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
