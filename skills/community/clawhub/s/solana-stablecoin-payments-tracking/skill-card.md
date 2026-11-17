## Description:

Streams real-time Solana SPL USDC and USDT transfers from Bitquery over WebSocket, excluding swap transactions and returning amount, USD value, parties, block, transaction, fee, and program-method details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyn](https://clawhub.ai/user/divyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to monitor real-time Solana USDC and USDT payment flow, build treasury alerts, and reconcile transfers with transaction signatures, fees, slots, and block times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bitquery API token is passed in the WebSocket URL and could be exposed through logs, shell history, or proxies.

Mitigation: Provide the token only through BITQUERY_API_KEY, avoid printing or logging the full WebSocket URL, and rotate the key if exposure is suspected.

Risk: The Python dependency is specified as a minimum version, which can change behavior across installs.

Mitigation: Install in a virtual environment or container and consider pinning or hash-locking dependencies before production use.

Risk: Bitquery schema changes can cause subscription validation failures.

Mitigation: Check Bitquery's Solana documentation and adjust only the query where-clause shape while preserving the documented USDC and USDT mint filters and fields.

## Reference(s):

- [Solana stablecoin transfers GraphQL reference](references/graphql-fields.md)
- [Bitquery documentation](https://docs.bitquery.io/)
- [ClawHub skill page](https://clawhub.ai/divyn/skills/solana-stablecoin-payments-tracking)
- [Publisher profile](https://clawhub.ai/user/divyn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets, plus formatted streaming text output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and network access to Bitquery's WebSocket API; the helper script supports an optional timeout.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
