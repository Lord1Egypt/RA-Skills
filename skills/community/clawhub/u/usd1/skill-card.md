## Description: <br>
Transfers USD1 (USDC on Wormhole) between wallets using Wormhole Liquidity Facility on testnet and returns the transaction hash and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AsgherAli](https://clawhub.ai/user/AsgherAli) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to initiate testnet USD1/USDC wallet-to-wallet transfers, optionally check sender balance, and receive transaction status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to handle a raw wallet private key and can submit a token transfer directly. <br>
Mitigation: Use only a disposable testnet wallet or a signer flow with explicit approval, and do not provide any mainnet or reused private key. <br>
Risk: Incorrect token, amount, chain, or recipient inputs could lead to failed or unintended transfers. <br>
Mitigation: Verify the exact token, amount, chain, and recipient address outside the skill before invoking it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AsgherAli/usd1) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [JSON object with transactionHash, status, and message fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success or failed status; runs on Testnet by default and requires amount, recipient address, and private key input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, changelog, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
