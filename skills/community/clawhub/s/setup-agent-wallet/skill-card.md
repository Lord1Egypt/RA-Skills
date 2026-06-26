## Description: <br>
Set up an agent wallet for Uniswap operations. Use when user needs to provision a wallet for an autonomous agent. Supports Privy (development), Turnkey (production), and Safe (maximum security). Configures spending limits, token allowlists, and funds the wallet for gas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to provision and configure wallets for autonomous Uniswap agents, including provider selection, chain configuration, spending limits, allowlists, funding, and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and fund crypto wallets using broad defaults and unclear confirmation boundaries. <br>
Mitigation: Use dedicated low-funded or testnet wallets first and require explicit confirmation of provider, chain list, funding source, funding amount, spending limits, and configuration file contents before creation or funding. <br>
Risk: Wallet provisioning is delegated to a separate wallet-provisioner subagent. <br>
Mitigation: Inspect and approve the wallet-provisioner subagent separately before relying on this skill for wallet lifecycle actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/setup-agent-wallet) <br>
- [Skill specification](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summary with wallet configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet address, provider, chains, spending limits, token allowlist, gas funding status, and configuration file path.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
