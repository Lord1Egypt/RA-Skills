## Description:

X2C Distribution and Wallet API - publish video to the X2C platform and manage assets including balances, X2C claims, USDC swaps, withdrawals, and transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developer agents use this skill to publish video projects to X2C, inspect review status, add episodes, and manage X2C and USDC wallet actions through the X2C Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real wallet operations including claims, swaps, and USDC withdrawals.

Mitigation: Require explicit approval immediately before claim, swap, or withdrawal commands, including the amount, asset, destination address, and API origin.

Risk: The API key may be sent to a configurable API endpoint.

Mitigation: Use a narrowly scoped X2C API key and pin X2C_API_BASE_URL to the official HTTPS API origin before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/x2c-publish)
- [Publisher profile](https://clawhub.ai/user/patches429)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an X2C_API_KEY credential and may use X2C_API_BASE_URL to select the API origin.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
