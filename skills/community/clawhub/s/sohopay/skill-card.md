## Description: <br>
Initiate payments on the SOHO Pay credit layer using EIP-712 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmsteve](https://clawhub.ai/user/nmsteve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent register a SOHO Pay wallet, submit EIP-712 credit payments, check borrower status, and repay outstanding USDC debt on Base mainnet or Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a raw wallet private key to send real on-chain financial transactions. <br>
Mitigation: Use a dedicated low-balance wallet, keep the key local, start on testnet, and avoid using a wallet that controls unrelated funds. <br>
Risk: Mainnet payments or repayments can execute without built-in confirmation or spend limits. <br>
Mitigation: Add confirmation, amount limits, recipient allowlists, and operational review before enabling mainnet payment or repayment workflows. <br>
Risk: An incorrect merchant, contract, or network address can cause irreversible loss of funds. <br>
Mitigation: Verify contract and merchant addresses before use, prefer explicit allowlists, and test the full flow on Base Sepolia before mainnet. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text status reports with setup commands, transaction hashes, balances, and borrower profile fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a sensitive PRIVATE_KEY environment variable and can operate on Base mainnet or Base Sepolia.] <br>

## Skill Version(s): <br>
1.0.17 (source: package.json, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
