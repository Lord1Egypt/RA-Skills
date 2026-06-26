## Description: <br>
Access to blockchain asset and transaction signature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernel1983](https://clawhub.ai/user/kernel1983) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use W3connect to retrieve an ETH-compatible wallet address and initiate ETH or USDC transfers through a local wallet service with authenticator-code verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real ETH or USDC transfers through a local wallet service. <br>
Mitigation: Confirm chain, token, amount, and recipient address or email outside the agent before authorizing any transaction. <br>
Risk: The local web3b0x service at 127.0.0.1:5333 is not verified by the artifact files. <br>
Mitigation: Install and use the skill only after separately verifying and trusting the local service. <br>
Risk: An authenticator code functions as authorization to move funds. <br>
Mitigation: Treat each code as sensitive and one-time use, and keep only limited funds in the connected wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kernel1983/w3connect) <br>
- [Publisher profile](https://clawhub.ai/user/kernel1983) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a local web3b0x service at 127.0.0.1:5333 and may initiate real ETH or USDC transfers when supplied with valid parameters.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
