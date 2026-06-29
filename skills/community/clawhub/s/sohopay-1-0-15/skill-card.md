## Description: <br>
Initiate payments on the SOHO Pay credit layer using EIP-712 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amitbiswas1992](https://clawhub.ai/user/amitbiswas1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use SohoPay to register an agent wallet, check SOHO Pay credit status, initiate merchant payments, and repay outstanding debt on Base mainnet or Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and submit SOHO Pay transactions that move real funds. <br>
Mitigation: Use a dedicated low-balance wallet, prefer Base Sepolia before mainnet, and verify the network, amount, merchant address, and repayment amount before each run. <br>
Risk: The PRIVATE_KEY controls the configured wallet and could be misused if exposed. <br>
Mitigation: Keep the key local, do not provide a key that controls unrelated funds, and rotate the key if exposure is suspected. <br>
Risk: A mistyped merchant address can send funds to the wrong account. <br>
Mitigation: Require an explicit valid EVM address and confirm the recipient address out of band before payment execution. <br>


## Reference(s): <br>
- [ClawHub SohoPay skill page](https://clawhub.ai/amitbiswas1992/skills/sohopay-1-0-15) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text with transaction hashes, status summaries, setup guidance, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally configured PRIVATE_KEY and explicit EVM addresses for payment execution.] <br>

## Skill Version(s): <br>
1.0.15 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
