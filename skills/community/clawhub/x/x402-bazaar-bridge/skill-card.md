## Description:

Discover, pay, and fetch data from x402-enabled APIs on the Coinbase x402 Bazaar. Supports search, x402 payment signing, caching, and daily budget enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cariohca-ux](https://clawhub.ai/user/cariohca-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover x402 resources, fetch paid API data, sign Base USDC payment authorizations, and monitor local daily spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a wallet private key and can sign Base USDC payment authorizations.

Mitigation: Use a low-balance dedicated wallet, keep the key out of version control, and install only when payment signing from the local environment is acceptable.

Risk: The skill can make paid network requests, and the local budget file should not be treated as the only spending control.

Mitigation: Set a conservative daily budget and enforce wallet-side balance or allowance limits outside the skill.

Risk: The resolve command can choose and fetch an endpoint based on a search result.

Mitigation: Avoid resolve for untrusted queries; review selected endpoints before using payment-enabled fetches.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cariohca-ux/skills/x402-bazaar-bridge)
- [Coinbase x402 Discovery API](https://api.cdp.coinbase.com/platform/v2/x402/discovery)
- [btcnode.uk x402 API example](https://btcnode.uk/api/fees)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may make paid network requests and require wallet configuration for payment-enabled mode.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
