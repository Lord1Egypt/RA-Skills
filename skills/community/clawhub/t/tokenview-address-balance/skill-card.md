## Description:

Queries supported blockchain wallet balances through the Tokenview API using a configured TOKENVIEW_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdonglobal](https://clawhub.ai/user/bdonglobal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check balances for supported blockchain addresses by providing an address and optional coin. The skill returns Tokenview balance data as JSON and concise user-facing balance or failure text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tokenview API keys may appear in network error output.

Mitigation: Review and update error handling to redact apikey values before installing or using the skill.

Risk: Wallet addresses and selected coin types are sent to Tokenview.

Mitigation: Use the skill only for explicit balance-check requests and avoid querying addresses that should not be shared with Tokenview.

Risk: The trigger can treat detected addresses as balance-query intent too broadly.

Mitigation: Confirm user intent before invoking the balance lookup when a wallet address appears in broader conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bdonglobal/skills/tokenview-address-balance)
- [Tokenview balance API endpoint](https://services.tokenview.io/vipapi/addr/b)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON from the script with concise user-facing balance or failure text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENVIEW_API_KEY and an address; coin is optional and defaults to BTC.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
