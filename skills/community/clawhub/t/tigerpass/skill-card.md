## Description: <br>
TigerPass is a hardware-secured crypto wallet and trading terminal for AI agents that can trade Hyperliquid, use Polymarket, swap and bridge EVM assets, execute contracts, sign messages, and support x402 and ACE Protocol commerce. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigerpassnet](https://clawhub.ai/user/tigerpassnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, crypto traders, and agent builders use TigerPass to give AI agents a Secure Enclave-backed wallet for mainnet payments, DeFi operations, trading workflows, and agent-to-agent commerce on macOS Apple Silicon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous wallet and trading commands can move or lose real funds. <br>
Mitigation: Start with a fresh low-balance wallet, use testnet or simulation first, and require explicit approval for every trade, payment, bridge, approval, contract write, owner command, and x402 payment. <br>
Risk: Installing or running an unverified CLI grants the agent high financial authority. <br>
Mitigation: Install only if autonomous crypto wallet and trading capability is intended, and verify the TigerPass CLI source and version before use. <br>
Risk: Unlimited token approvals can leave funds exposed beyond a single action. <br>
Mitigation: Avoid unlimited approvals unless you know how to monitor and revoke them; prefer bounded approvals and verify allowances before executing follow-up transactions. <br>


## Reference(s): <br>
- [TigerPass ClawHub listing](https://clawhub.ai/tigerpassnet/tigerpass) <br>
- [TigerPass homepage](https://tigerpass.net) <br>
- [TigerPass CLI source install link](https://github.com/TigerPassNet/tigerpass-cli.git) <br>
- [DeFi Cookbook](references/defi-cookbook.md) <br>
- [ACE Protocol](references/ace-protocol.md) <br>
- [Advanced Commands](references/advanced-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code snippets] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands expect the tigerpass CLI on macOS Apple Silicon and generally produce JSON to stdout.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
