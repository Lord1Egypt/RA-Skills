## Description: <br>
Transfer tokens from an OpenAnt wallet on Solana or Base using the OpenAnt CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to prepare and run OpenAnt wallet transfer commands for SOL, ETH, USDC, or token addresses on Solana or Base. It is intended for wallet operation workflows that require checking authentication, balance, chain, token, amount, and recipient before transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token transfers can move real funds and are usually irreversible. <br>
Mitigation: Require explicit user confirmation and independently verify the chain, token, amount, and full recipient address before executing a transfer. <br>
Risk: The skill runs the external OpenAnt CLI at runtime. <br>
Mitigation: Use only the documented OpenAnt wallet commands and check authentication and balance before any transfer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/send-token) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with OpenAnt CLI shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should append --json and require explicit user confirmation before token transfers.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
