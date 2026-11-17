## Description:

X2C Distribution and Wallet API: publish video to the X2C platform and manage assets including balances, claims, swaps, withdrawals, and transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to publish video projects to X2C, upload or reference media assets, check review status, and manage wallet actions such as balances, claims, swaps, withdrawals, and transaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful X2C API credentials.

Mitigation: Use narrowly scoped API keys, keep credential files out of version control, and protect them from other users.

Risk: Wallet actions can move assets through claims, swaps, and withdrawals.

Mitigation: Require explicit confirmation of amount, asset, network, fees, and full destination address before any swap or withdrawal.

Risk: Endpoint control affects where credentialed requests are sent.

Mitigation: Enforce the official HTTPS endpoint before running API calls.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X2C_API_KEY; may use USER_ID and X2C_API_BASE_URL.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
