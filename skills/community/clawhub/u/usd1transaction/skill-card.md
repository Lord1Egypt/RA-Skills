## Description: <br>
Allows an agent to transfer USD1, described as USDC on Wormhole, between wallets using Wormhole Liquidity Facility on Testnet by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AsgherAli](https://clawhub.ai/user/AsgherAli) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to check a sender balance when supported and initiate a testnet USD1 transfer to a specified recipient wallet. It is intended for workflows that need a transaction hash, status, and concise transfer result message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accepts a raw wallet private key, which authorizes blockchain transfers. <br>
Mitigation: Use only throwaway testnet wallets and never provide a reused or mainnet private key. <br>
Risk: The skill can broadcast a transfer without a separate confirmation step. <br>
Mitigation: Manually verify the recipient, amount, chain, and actual token before running it, and prefer a signer flow that requires explicit confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AsgherAli/usd1transaction) <br>
- [Publisher profile](https://clawhub.ai/user/AsgherAli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls] <br>
**Output Format:** [JSON object with transaction hash, status, and message fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return failed status and an error message when required parameters are missing or the transfer fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
