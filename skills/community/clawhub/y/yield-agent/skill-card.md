## Description:

On-chain yield discovery, transaction building, and portfolio management via the Yield.xyz API across 80+ networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apurvmishra](https://clawhub.ai/user/apurvmishra)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill to discover on-chain yield opportunities, inspect yield requirements, build unsigned transactions, check balances, and manage staking, lending, vault, restaking, or liquidity-pool positions through Yield.xyz.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Irreversible DeFi transactions can cause loss of funds if the chain, asset, amount, contract, spender, allowance, or destination is wrong.

Mitigation: Use a wallet that shows decoded transaction details and confirm those values before signing.

Risk: Custom YIELDS_API_URL values can route requests through infrastructure the user does not trust.

Mitigation: Use the default Yield.xyz API endpoint unless a trusted operator explicitly approves another endpoint.

Risk: Position-balance checks may not prove that a wallet has spendable funds or enough gas for a transaction.

Mitigation: Verify spendable wallet balance, network, token amount, and gas in the signing wallet before execution.

Risk: Changing an unsigned transaction returned by the API can produce incorrect execution or permanent fund loss.

Mitigation: Sign freshly returned API transactions exactly as provided; request a new action when transaction details need to change.

## Reference(s):

- [OpenAPI schema](references/openapi.yaml)
- [Safety checks and guardrails](references/safety.md)
- [Unsigned transaction formats](references/chain-formats.md)
- [Wallet integration](references/wallet-integration.md)
- [Agent conversation examples](references/examples.md)
- [Advanced capabilities](references/superskill.md)
- [Yield.xyz API docs](https://docs.yield.xyz)
- [Yield.xyz dashboard](https://dashboard.yield.xyz)
- [Yield.xyz](https://yield.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses, including unsigned transaction payloads for wallet signing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; write operations require wallet review and signing, and may require YIELDS_API_KEY or the included shared API key.]

## Skill Version(s):

0.1.5 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
