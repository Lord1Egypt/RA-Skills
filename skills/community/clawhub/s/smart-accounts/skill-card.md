## Description:

Deploy and manage multi-signature smart accounts on supported EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet operators use this skill to deploy multi-signature smart accounts, manage owners, change signing thresholds, and inspect smart account details through fdx commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ownership or threshold changes can lock or alter control of funds if the address, chain, action, or threshold is wrong.

Mitigation: Confirm every address, chain, action, and threshold with the human before allowing the fdx command to run.

Risk: The skill is scoped to EVM smart accounts through fdx and may fail or mislead if used for unsupported chains.

Mitigation: Verify fdx authentication and supported EVM chain selection before deployment or ownership-management commands.

## Reference(s):

- [Smart Accounts ClawHub Page](https://clawhub.ai/rachidjarray-hk-qa-fdt/skills/smart-accounts)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated fdx wallet and a supported EVM chain.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
