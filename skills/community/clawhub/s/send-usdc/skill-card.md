## Description: <br>
Send USDC from an authenticated wallet to an Ethereum address or ENS name on Base using the Awal CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to prepare and run USDC transfers to wallet addresses or ENS names after checking authentication and balance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a wallet CLI that sends real USDC without a mandatory final confirmation step. <br>
Mitigation: Require explicit user approval immediately before sending, and manually verify the wallet, amount, recipient, ENS resolution, chain, and balance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRAG/send-usdc) <br>
- [Publisher profile](https://clawhub.ai/user/0xRAG) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; command output may be JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated wallet, sufficient USDC balance, and a valid Ethereum address or ENS recipient.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
