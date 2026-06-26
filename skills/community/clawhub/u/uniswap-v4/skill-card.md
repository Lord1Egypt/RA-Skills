## Description: <br>
Swap tokens, quote expected output, manage Permit2 approvals, and read Uniswap V4 pool state on Base, Ethereum mainnet, and Base Sepolia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agents use this skill to inspect Uniswap V4 pool state, obtain quotes, set Permit2 approvals, and execute exact-input swaps with slippage controls on supported EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real wallet transactions. <br>
Mitigation: Use a dedicated low-balance wallet and manually verify chain, router, token addresses, recipient, amount, and slippage before any write action. <br>
Risk: The skill can grant broad ERC20 and Permit2 allowances. <br>
Mitigation: Prefer the documented TypeScript entrypoints, approve only intended tokens, and revoke ERC20 or Permit2 allowances after use. <br>
Risk: Bundled shell paths handle private keys less safely than the TypeScript entrypoints. <br>
Mitigation: Avoid scripts/*.sh for write actions and use PRIVATE_KEY only through an environment variable or secret manager. <br>


## Reference(s): <br>
- [Uniswap V4 deployments](https://docs.uniswap.org/contracts/v4/deployments) <br>
- [Contract addresses](references/addresses.md) <br>
- [V4 architecture](references/v4-architecture.md) <br>
- [V4 encoding reference](references/v4-encoding.md) <br>
- [Clanker token deployments](https://clanker.gitbook.io/clanker-documentation/general/token-deployments) <br>
- [Clanker creator rewards and fees](https://clanker.gitbook.io/clanker-documentation/general/creator-rewards-and-fees) <br>
- [Clanker deployed contracts](https://clanker.gitbook.io/clanker-documentation/references/deployed-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations can return pool or quote data; write operations can return transaction hashes and require wallet credentials.] <br>

## Skill Version(s): <br>
2.0.4 (source: CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
