## Description: <br>
Helps agents check USDC balances, send transfers, approve EVM spending, and verify transactions across EVM-compatible chains and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform single-chain USDC operations, including balance checks, transfers, EVM approvals, and transaction verification on EVM networks and Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write operations require wallet key handling and irreversible blockchain transaction signing. <br>
Mitigation: Prefer wallet-mediated or hardware signing, use test wallets and small amounts, and never expose private keys in chat, logs, source control, or shared environments. <br>
Risk: Wrong chain, token address, recipient, amount, spender, or decimal handling can move the wrong asset or value. <br>
Mitigation: Verify the chain, native Circle-issued USDC contract or mint, recipient, amount, spender, and transaction receipt before reporting success; use 6 decimals for USDC. <br>


## Reference(s): <br>
- [EVM Operations Guide](references/evm.md) <br>
- [Solana Operations Guide](references/solana.md) <br>
- [Circle USDC Contract Addresses](https://developers.circle.com/stablecoins/usdc-contract-addresses) <br>
- [Circle Developer Documentation](https://developers.circle.com) <br>
- [viem Documentation](https://viem.sh) <br>
- [Circle Stablecoin EVM Contracts](https://github.com/circlefin/stablecoin-evm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes chain-specific addresses, transaction checks, and confirmation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
