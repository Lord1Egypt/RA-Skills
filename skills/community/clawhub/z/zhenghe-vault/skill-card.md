## Description:

Zhenghe Vault helps agents query, deposit, monitor, and withdraw USDC/LOVE positions in an ERC-4626 vault on Base, with explicit operator approval required for fund movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batcatchina](https://clawhub.ai/user/batcatchina)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading-agent operators use this skill to check Zhenghe vault status and request deposit or redemption transaction data for Base. It is intended to guide operator-reviewed wallet actions, not to autonomously sign or submit transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party Zhenghe service receives wallet addresses and requested vault actions and returns transaction data.

Mitigation: Use only with operators who accept that exposure, and independently verify each transaction before signing.

Risk: The skill can facilitate movement of real USDC on Base using server-generated calldata.

Mitigation: Require explicit human approval for every fund movement and do not allow an agent to auto-sign or submit transactions from the API response alone.

Risk: Incorrect transaction fields could move funds unexpectedly or interact with the wrong contract.

Mitigation: Before signing, verify chain ID 8453, contract addresses, function selectors, amounts, receiver and owner fields, and zero native value.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/batcatchina/skills/zhenghe-vault)
- [Publisher profile](https://clawhub.ai/user/batcatchina)
- [Zhenghe system homepage](https://zhenghe-system.vercel.app)
- [Zhenghe A2A endpoint](https://zhenghe-system.vercel.app/api/a2a)
- [Zhenghe agent card](https://zhenghe-system.vercel.app/.well-known/agent.json)
- [LoveVault contract on Basescan](https://basescan.org/address/0x16A7F8CfAD687A87183fCbd1dF7aF09dce05D357)
- [ZhengHeRouter contract on Basescan](https://basescan.org/address/0x2348ec656e395edAbcE2e198DC44647456d81867)
- [USDC contract on Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and optionally ZHENGHE_WALLET_ADDRESS; fund movements require operator approval and external wallet signing.]

## Skill Version(s):

1.0.2 (source: release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
